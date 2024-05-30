#!/bin/python3

"""
PyMan
Bring up help, functions, or definition file conveniently in the command line
"""

import sys
import argparse
import pkgutil
import importlib
import subprocess
import inspect
from typing import Any, Callable
import webbrowser

def import_module(module_name: str):  # Return type for module?
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")

def get_module_functions(module_name: str, include_dunder: bool = False) -> list[Callable]:  # -> list[Callable]:
    # Import should be done first and object passed to here or the man page function
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as err:
        print(err)
        sys.exit()
    else:
        attributes = dir(module)
        functions = [
            getattr(module, attr).__name__ for attr in attributes 
            if callable(getattr(module, attr))
            
        ]
        if not include_dunder:
            functions = [func for func in functions if not func.startswith("_")]
            
        return functions

def get_modules() -> list:
    module_list = [x.name for x in list(pkgutil.iter_modules()) if not x.name.startswith("_")]
    return module_list

def get_builtins() -> list:
    return [x for x in dir(__builtins__) if not x.startswith("_")]

def open_module_man(module):
    help(module)

def open_module_func(func_obj):
    help(func_obj)

def open_man_page(module: Any, function: Callable | None = None) -> None:
    # Required parameter: first command line arg => man of module
    # Optional second arg after module ot trigger running 
    # Type for module import object?
    if not function:
        help(module)
    else:
        module_function_string = f"help({module}.{function})"
        print(f"{module_function_string=}")
        print("TODO: Access module function definition")

def get_source_path():
    # Only open ones with a .py file located
    # Builtin ones written in C can be ignored for the moment
    # Display message if a file not found: inform the builtin is in the interpreter in C
    ...

def open_file_source(func_obj: Callable, editor="vim"):
    # Run get_source_path to find file, if one found, do this:
    subprocess.run(["echo", f"TODO: find file where the definition for {func_obj} is and open in {editor}"])
    # if get_source_path(func_obj( is None: echo a message
    exit(0)

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
        return "module"
    elif search_term in builtin:
        return "builtin"
    if len(partial_search(search_term)) > 0:
        print("Possible suggestions:")
        results = partial_search(search_term)
        for m in results:
            print(m)
        return "partial"

def open_docs_page(module_name: str) -> None:
    """
    --- TODO ---
    * Run same check suggestions here like with man function
    * Check if 404 not found, then if this response, don't open in browser:
    Will have to check the http status code somehow?
    * Jump to highlighted definition of a single function within the docs: 
    Run ctrl-f in the browser somehow?
    """
    url = f"https://docs.python.org/3/library/{module_name}.html"
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
        print(f"--- Inbuilt Functions for <{args.module}> ---")
        for module in get_module_functions(args.module):
            print(f"* {module}")
        sys.exit()

    if args.definition is True:
        open_file_source(args.module)
    
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
        open_module_man(mod)
    
    elif results == "builtin":
        # str is not caught here it should be treated as a module
        open_module_man(args.module)
    elif results == "partial":
        # Prints any close matches in above function
        pass

if __name__ == "__main__":
    main()

def run_menu_loop(module_name: str, search_filter: str | None = None):
    """
    Display module functions enumerated in alphabetical order.
    Optionally display only those starting with or matching the search filter string.
    Conversion between function names and objects maybe required.
    Select function by number or q to exit.

    TODO: Run the man page function, then once user quits the shell man page, back to
    the menu loop to choose another or exit.
    """
    # Import module
    # Derive function list from modules 
    mod = import_module(module_name)
    assert module_name in locals(), f"Error: '{module_name}' not in locals() after importing."
    # This returns function objects, we want them named
    # Check is alphabetised
    
    func_objects = get_module_functions(mod)
    print(f"{func_objects[:10]=}")
    
    while True:
        print(f"--- Functions and Classes for {module_name} ---")
        # Loop over list of dicts func_name
        for i, func in enumerate(dir(mod)):
            print(f"{i}: {func}")
        choice = input("Enter number or q to exit -> ")
        if choice == ("q" or "Q"):
            sys.exit()
        else:
            # Loop over list of dicts func_obj I think
            for i, func in enumerate(dir(mod)):
                if i == "t":
                    # Access func obj based on the displayed numbers
                    test_func_obj = sys.modules
                    open_module_man(test_func_obj)
                    # man_process = subprocess.Popen(['man', function_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    continue
                elif choice == "i":
                    print("TODO: Match choice to index of function")
                    continue
                print(f"{choice} is invalid.")
                    # Now to wait until man processed funished in shell, return to loop
                    # Perhaps something in subprocess module. Or maybe does automatically?
