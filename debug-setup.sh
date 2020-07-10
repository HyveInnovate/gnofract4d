#!/bin/bash

# https://docs.python.org/3/tutorial/venv.html
python3 -m venv xcode-env
source xcode-env/bin/activate

nm $(which python)

pip install --upgrade pip
pip install pygobject

python whoami.py
# 1 - create new Xcode project "macos - library"
# 1.1 - framework = "plain C/C++"
# 1.2 - type dynamic
# 2 - in "build phases" of the target -> add the cpp files of fract4dc
# 3 - in "build settings" of the project
# 3.1 - include the python header path in "header search path"
# 3.2 - set the "user header search" to point to this project folders containing header files
# 4 - edit the "run scheme"
# 4.1 - set the output of whoami.py as the "executable"
# 4.2 - set the argument of the executable equal to the path of gnofract4d script

# lldb python

# references
# https://jonasdevlieghere.com/sanitizing-python-modules/
# https://stackoverflow.com/questions/13324336/compiling-and-linking-c-extension-for-python-in-xcode-for-mac
