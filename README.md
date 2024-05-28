# PyMan

Simple CLI utility script for browsing inbuilt python manuals and documentation directly from the shell, built for my own learning purposes. Looking to expand into a full
application soon with many more features and ability to install into a virtual environment and use the same way while it is activated.

Place in Linux script directory, make executable and run as below.

Functionality implemented:
$ pyman <inspect> => man page in console
$ pyman <module> -docs => Open official Python documentation page

Working on:
$ pyman pathlib Path => Go to specific function definition
$ pyman -dir => Generate list of all available members of module/function
$ pyman -def => Find file path of module/function code and open in editor
