# PyMan

Simple CLI utility script for browsing inbuilt python manuals and documentation directly from the shell, built for my own learning purposes. Looking to expand into a full
application soon with many more features and ability to install into a virtual environment and use the same way while it is activated.

Place in Linux script directory, make executable, change shebang python path if needed and run as below.

Functionality implemented: <br />
Usage: module_name [OPTIONS] <br />
$ pyman pathlib => man page in console <br />
$ pyman pathlib.Path => Definition of this class or function of the module <br />
    -m    Open manual page for this module, or member definition. Defaults to if no option supplied. <br />
    -d    Generate list of all available members of module/function <br />
    -doc  Open official Python documentation page <br />
    -sc   Generate list of all available members of module/function <br />
