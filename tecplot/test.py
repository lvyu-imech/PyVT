import tecIO as tec
import vtk
from vtk.util import numpy_support as VN
import numpy as np


plt = tec.Tecplot()
plt.read_tecplot('OneraM6_SU2_RANS.dat')
#plt.read_tecplot('wing_surf.dat')
tecpoints = vtk.vtkPoints()
tecpoints.SetData(VN.numpy_to_vtk(plt.zones[0].xyz))

if plt.zones[0].tet_elements.any(): 
    
    print('tetrahedra')

if plt.zones[0].hexa_elements.any():
        
    print('hexahedra')
    tecpoints = vtk.vtkPoints()
    tecpoints.SetData(VN.numpy_to_vtk(plt.zones[0].xyz))
    cellConn = plt.zones[0].hexa_elements
    connectdata = np.concatenate((np.ones((cellConn.shape[0], 1), dtype=int)*cellConn.shape[1], cellConn), axis=1).ravel() 
    teccells = vtk.vtkCellArray()
    teccells.SetNumberOfCells(plt.zones[0].hexa_elements.shape[0])
    teccells.SetCells(plt.zones[0].hexa_elements.shape[0], VN.numpy_to_vtk(connectdata, deep=True, array_type=vtk.VTK_ID_TYPE)) 
    output = vtk.vtkUnstructuredGrid()
    output.SetPoints(tecpoints)
    output.SetCells(vtk.VTK_HEXAHEDRON, teccells)

    for i in range(len(plt.zones[0].variables)-3):
        tecarray = VN.numpy_to_vtk(plt.zones[0].nodal_results[:,i])
        tecarray.SetName(plt.zones[0].variables[i+3])
        output.GetPointData().AddArray(tecarray) 
        

    print(plt.zones[0].xyz.shape)
    print(plt.zones[0].nodal_results.shape)
    print(output.GetPointData())

if plt.zones[0].quad_elements.any():
    
    print('quad')
    tecpoints = vtk.vtkPoints()
    tecpoints.SetData(VN.numpy_to_vtk(plt.zones[0].xyz))
    cellConn = plt.zones[0].quad_elements
    connectdata = np.concatenate((np.ones((cellConn.shape[0], 1), dtype=int)*cellConn.shape[1], cellConn), axis=1).ravel() 
    teccells = vtk.vtkCellArray()
    teccells.SetNumberOfCells(plt.zones[0].quad_elements.shape[0])
    teccells.SetCells(plt.zones[0].quad_elements.shape[0], VN.numpy_to_vtk(connectdata, deep=True, array_type=vtk.VTK_ID_TYPE)) 
    output = vtk.vtkUnstructuredGrid()
    output.SetPoints(tecpoints)
    output.SetCells(vtk.VTK_QUAD, teccells)
    
    for i in range(len(plt.zones[0].variables)-3):
        tecarray = VN.numpy_to_vtk(plt.zones[0].nodal_results[:,i])
        tecarray.SetName(plt.zones[0].variables[i+3])
        output.GetPointData().AddArray(tecarray) 

    print(plt.zones[0].xyz.shape)
    print(plt.zones[0].nodal_results.shape)
    print(output.GetPointData())
if plt.zones[0].tri_elements.any():
    
    print('trianle')


