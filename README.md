# PyMan

Simple CLI utility script for browsing inbuilt python manuals and documentation directly from the shell, built for my own learning purposes. Looking to expand into a full
application soon with many more features and ability to install into a virtual environment and use the same way while it is activated.

Place in Linux script directory, make executable and run as below.

Functionality implemented: <br />
$ pyman <inspect> => man page in console <br />
$ pyman <module> -docs => Open official Python documentation page <br />

Working on: <br />
$ pyman pathlib Path => Go to specific function definition <br />
$ pyman -dir => Generate list of all available members of module/function <br />
$ pyman -def => Find file path of module/function code and open in editor <br />
