
## Introduction
PyVT is a open-source light-weight python-based visualization tool built upon VTK. 
It is designated for visualization and graphic analysis of CFD/fluid-dynamic datasets. 
It is capable of generating cutplane/streamline/vector/isosurface in a interactive GUI.

## Dependencies:
0. python3
1. numpy
2. vtk
3. PyQt5
4. matplotlib 

## Installation on Mac OS (tested on high sierra or newer) and linux (tested on Ubuntu)  
naive approach:
1. Download the tarball package and uncompress it
2. Make sure Python3 installed
3. Run: python3 setup.py install 

if conda is used:
1. create a new environment: conda create --name myenv python3/python
2. step 1 should install pip already, just run: pip install ./pyvt-1.0


## Issues with cgns io interface:

Once installation of cgns is complete, navigate to the folder of cgns_to_vtk, and check 
the path of runtime library to be loaded. On Mac, do:
"
otool -L ./cgns_to_vtk
"
to check the search path; and use the command:
"
install_name_tool -add_rpath "@loader_path/../../lib" cgns_to_vtk
"
to add additional search path so that the dyn library can be loaded when cgns_to_vtk is
executed


