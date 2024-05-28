#!/bin/python3

"""
PyMan
Bring up help, functions, doumentation and definition files conveniently in the command line.
"""

import sys
import argparse
import pkgutil
import importlib
import subprocess
import webbrowser

def import_module(module_name: str):  # Return type for module?
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")

def get_module_functions(module):  # -> list[Callable]:
    attributes = dir(module)
    # TODO: Need function objects below instead of string parameter
    # in order to run dir(function), otherwise just does dir(str) every time
    functions = [attr for attr in attributes if not attr.startswith("_")]
    return functions

def get_modules() -> list:
    module_list = [x.name for x in list(pkgutil.iter_modules()) if not x.name.startswith("_")]
    return module_list

def get_builtins() -> list:
    return [x for x in dir(__builtins__) if not x.startswith("_")]

def print_man(func_obj):
    eval("print(help(func_obj))")

def open_definition(func_obj, editor="vim"):
    # Locate file path where function is
    # May not work for builtins
    subprocess.run(["echo", f"TODO: find file where the definition for {func_obj} is and open in {editor}"])
    exit(0)

def create_eval_string(module: str, function: str | None = None):
    if not function:
        eval_string = f"help({module})"
    else:
        eval_string = f"help({module}.{function})"
    return eval_string

def partial_search(search_term: str) -> list[str]:
    """
    TODO: Give suggestions for module functions too
    e.g. thread.Thread will match for search term 'Thr'
    """
    mods = get_modules()
    builtin = get_builtins()
    all_members = mods + builtin
    matches = [m for m in all_members if m.startswith(search_term)]
    return matches

def search_all(search_term: str) -> str | None:
    mods = get_modules()
    builtin = get_builtins()
    if search_term in mods:
        print(f"'{search_term}' found in module list.")
        return "module"
    elif search_term in builtin:
        print(f"'{search_term}' found in builtin function list.")
        return "builtin"
    if len(partial_search(search_term)) > 0:
        print("Possible suggestions:")
        results = partial_search(search_term)
        for m in results:
            print(m)
        return "partial"

def open_docs_page(module_name: str) -> None:
    """
    TODO: 
    Check if 404 not found, then if this response, don't open in browser
    Also run suggestions here like with man function
    """
    url = f"https://docs.python.org/3/library/{module_name}.html"
    # If invalid URL, print no page found
    # Idea: Jump to a function definition on the page
    try:
        webbrowser.open(url)
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(
        prog="PyMan",
    )

    # One arg required
    parser.add_argument(
        "module", 
        help="Name of the module or inbuilt function"
    )
    
    # This needs to be option for first argument so pyman -i also allowed
    parser.add_argument(
        "-i", "--interactive", 
        help="TODO: interactive menu",
        action="store_true"
    )
    
    parser.add_argument(
        "-m", "--man", 
        help="Open module's man page in the console.",
        action="store_true"
    )
    
    parser.add_argument(
        "-d", "--dir", 
        help="List available functions and classes for this module",
        action="store_true"
    )
    
    parser.add_argument(
        "-def", "--definition", 
        help="TODO: Open file definition in vim or custom editor choice",
        action="store_true"
    )
    
    parser.add_argument(
        "-doc", "--documentation", 
        help="Open official docs page in browser",
        action="store_true"
    )
    
    args = parser.parse_args()
    if args.documentation is True:
        open_docs_page(args.module)
        sys.exit()
    if args.dir is True:
        # Not working! Needs a function object, just processes string right now
        print(f"--- Inbuilt Functions for <{args.module}> ---")
        for module in get_module_functions(args.module):
            print(f"* {module}")
        sys.exit()

    if args.definition is True:
        open_definition(args.module)
    
    # No other arguments, default to --man
    results = search_all(args.module)
    if not results:
        print("No matches found.")
        sys.exit() 
    elif results == "module":
        mod = import_module(args.module)
        if args.dir is True:
            funcs = get_module_functions(mod)
            for f in funcs:
                print(f)
            sys.exit(0)
        print_man(mod)
    
    elif results == "builtin":
        # str is not caught here it should be treated as a module
        print_man(args.module)
    elif results == "partial":
        # Prints any close matches in above function
        pass

if __name__ == "__main__":
    main()

