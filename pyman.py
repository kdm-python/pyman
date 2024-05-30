#!/bin/python3

"""
PyMan
Bring up help, functions, or definition file conveniently in the command line

--- TODO ---

* pyman threading.Thread is not bringing up the module function help
* Give suggestions for module functions too: e.g. thread.Thread will match search term 'Thr'
* Find out how to find file path of module that is inbuilt (May only work when installed in venv)
* Interative menu -i to loop over search, open man page then come back to program

* Must be a way to do autocomplete on command line input: expand into full application

"""


import sys
import argparse
import pkgutil
import importlib
import subprocess
import webbrowser

# This is a new line
def foo():
    print("Look")

def import_module(module_name: str):  # Return type for module?
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")

def get_module_functions(module):  # -> list[Callable]:
    attributes = dir(module)
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
        help="TODO: Open official docs page in browser",
        action="store_true"
    )
    
    args = parser.parse_args()

    results = search_all(args.module)
    if not results:
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
        # str is not caught here it should be treated as a module
        pass

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
    
    # TODO: List of function dicts [{index, func_name, func_obj}]
    # Then access the function object or name based on index, run man function
    # assert choice in list of dicts index keys
    
    test_indexes = [1, 2, 3]
    test_func_names = [ "importlib", "argparse", "sys"]
    test_func_objs = [importlib, argparse, sys]
    # Iterate above with keys and values somehow
    test_func_dicts = [{}, {}, {}]

    while True:
        print(f"--- Functions and Classes for {module_name} ---")
        # Loop over list of dicts func_name
        for i, func in enumerate(dir(mod)):
            print(f"{i}: {func}")
        choice = input("Enter number or q to exit -> ")
        if choice == ("q" or "Q"):
            sys.exit(0)
        else:
            # Loop over list of dicts func_obj I think
            for i, func in enumerate(dir(mod)):
                if i == "t":
                    # Access func obj based on the displayed numbers
                    test_func_obj = sys.modules
                    print_man(test_func_obj)
                    # man_process = subprocess.Popen(['man', function_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    continue
                elif choice == i:
                    print("TODO: Match choice to index of function")
                    continue
                print(f"{choice} is invalid.")
                    # Now to wait until man processed funished in shell, return to loop
                    # Perhaps something in subprocess module. Or maybe does automatically?

if __name__ == "__main__":
    main()
    # m = partial_search("th")
    # print(m)
