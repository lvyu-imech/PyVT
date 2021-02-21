# read input data
import vtk
import numpy as np
from vtk.util import numpy_support as VN

def read_input_file(file_name):

    filename = file_name.lower()
        
    # Read the data file.
    if filename.endswith(".vtk"):  # read all legacy vtk types

        # PolyData, StructuredGrid, StructuredPoints, UnstructuredGrid, RectilinearGrid
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(file_name)
        reader.ReadAllScalarsOn()
        reader.ReadAllVectorsOn()
        #reader.ReadAllTensorsOn()
        #reader.ReadAllFieldsOn()
        #reader.ReadAllNormalsOn()
        #reader.ReadAllColorScalarsOn()
    elif filename.endswith(".stl"):

        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_name)
        
    elif filename.endswith(".vtu"):  # read XML unstructuredGrid type
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_name)

    elif filename.endswith(".vts"):  # read XML structuredGrid type
        reader = vtk.vtkXMLStructuredGridReader()
        reader.SetFileName(file_name)

    elif filename.endswith(".plt"):  # read Tecplot data file (binary)
        # built-in reader is not very reliable
        #reader = vtk.vtkTecplotReader()
        #reader.SetFileName(file_name)
        
        # external helper to load binary tecplot data
        #import myio.binarytecplot as bt
        from .binarytecplot import LoadTecplotFile

        output = None
        tecline = LoadTecplotFile(file_name, info = True)
        x_arr = np.array(tecline.zone[0].data[0])
        y_arr = np.array(tecline.zone[0].data[1])
        z_arr = np.array(tecline.zone[0].data[2])
        nxyz  = 3
        xyz_arr = np.column_stack((x_arr, y_arr, z_arr))
        tecpoints = vtk.vtkPoints()
        tecpoints.SetData(VN.numpy_to_vtk(xyz_arr))
        if tecline.zone[0].type == 0: 
            # ordered data format
            output = vtk.vtkStructuredGrid()
            dims = (tecline.zone[0].imax, tecline.zone[0].jmax, tecline.zone[0].kmax)
            output.SetDimensions(dims)
            output.SetPoints(tecpoints)
            varlist = tecline.zone[0].variable
            for i in range(len(varlist)-nxyz):
                tecarray = VN.numpy_to_vtk(np.array(tecline.zone[0].data[nxyz+i]))
                tecarray.SetName(varlist[nxyz+i])
                output.GetPointData().AddArray(tecarray)
            
            return output
        
        if tecline.zone[0].type == 1:
            celltype = vtk.VTK_LINE
        if tecline.zone[0].type == 2:
            celltype = vtk.VTK_TRIANGLE
        if tecline.zone[0].type == 3:
            celltype = vtk.VTK_QUAD
        if tecline.zone[0].type == 4:
            celltype = vtk.VTK_TETRA
        if tecline.zone[0].type == 5:
            celltype = vtk.VTK_HEXAHEDRON
        if tecline.zone[0].type == 6:
            celltype = vtk.VTK_POLYGON
        if tecline.zone[0].type == 7:
            celltype = vtk.VTK_POLYHEDRON

        cellConn = np.array(tecline.zone[0].connectivity, dtype=np.uint)
        connectdata = np.concatenate((np.ones((cellConn.shape[0], 1), dtype=int)*cellConn.shape[1], cellConn), axis=1).ravel()

        teccells = vtk.vtkCellArray()
        teccells.SetNumberOfCells(cellConn.shape[0])
        teccells.SetCells(cellConn.shape[0], VN.numpy_to_vtk(connectdata, deep=True, array_type=vtk.VTK_ID_TYPE))
        output = vtk.vtkUnstructuredGrid()
        output.SetPoints(tecpoints)
        output.SetCells(celltype, teccells)
        varlist = tecline.zone[0].variable
        for i in range(len(varlist)-nxyz):
            tecarray = VN.numpy_to_vtk(np.array(tecline.zone[0].data[nxyz+i]))
            tecarray.SetName(varlist[nxyz+i])
            output.GetPointData().AddArray(tecarray)

    elif filename.endswith(".dat"):  # read Tecplot data file (ASCII)
        if True:
            #import myio.asciitecplot as at
            from .asciitecplot import tecdata

            plt = tecdata() 
            plt.read_tecplot(file_name)
            #only load the first zone
            tecpoints = vtk.vtkPoints()
            tecpoints.SetData(VN.numpy_to_vtk(plt.xyz))
            
            if plt.elementtype == None:
                output = vtk.vtkStructuredGrid()
                output.SetDimensions(plt.dims)
                output.SetPoints(tecpoints)
                for i in range(len(plt.variables)-3):
                    tecarray = VN.numpy_to_vtk(plt.results[:,i])
                    tecarray.SetName(plt.variables[i+3])
                    output.GetPointData().AddArray(tecarray)
                    
                return output 

            if plt.elementtype == 'FEBRICK':
                celltype = vtk.VTK_HEXAHEDRON
            if plt.elementtype == 'FETETRAHEDRON':
                celltype = vtk.VTK_TETRA
            if plt.elementtype == 'FEQUADILATERAL':
                celltype = vtk.VTK_QUAD
            if plt.elementtype == 'FETRIANGLE':
                celltype = vtk.VTK_TRIANGLE
            cellConn = plt.elements
 
            connectdata = np.concatenate((np.ones((cellConn.shape[0], 1), dtype=int)*cellConn.shape[1], cellConn), axis=1).ravel()
            teccells = vtk.vtkCellArray()
            teccells.SetNumberOfCells(cellConn.shape[0])
            teccells.SetCells(cellConn.shape[0], VN.numpy_to_vtk(connectdata, deep=True, array_type=vtk.VTK_ID_TYPE))
            output = vtk.vtkUnstructuredGrid()
            output.SetPoints(tecpoints)
            output.SetCells(celltype, teccells)
            for i in range(len(plt.variables)-3):
                tecarray = VN.numpy_to_vtk(plt.results[:,i])
                tecarray.SetName(plt.variables[i+3])
                output.GetPointData().AddArray(tecarray)
                 
        # tried for unstructured tecplot data; not working
        #reader = vtk.vtkTecplotReader()
        #reader.SetFileName(file_name)

    elif filename.endswith(".p3d"):  # read Plot3D data file
            
        reader = vtk.vtkPlot3DMetaReader()
        reader.SetFileName(file_name)
        
    elif filename.endswith(".cgns"): # read cgns data file
        import sys
        import os
        #searchfolder = os.path.join(os.path.abspath(os.curdir), 'cgns')
        here, s = os.path.split(__file__)
        searchfolder = here + '/cgns'
        print(searchfolder)
        
        for dirpath, dirnames, files in os.walk(searchfolder):
            ifile = ''
            for ifile in files:
                if ifile == 'cgns_to_vtk':
                    break
            if ifile == 'cgns_to_vtk':
                break
            
        converter = dirpath + '/' + ifile + ' -a ' + file_name 
        os.system(converter)
        
        vtkfilename = os.path.abspath(os.curdir) + '/' + 'Zone1.vtk'
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(vtkfilename)
        reader.ReadAllScalarsOn()
        reader.ReadAllVectorsOn()

    #reader.Update()  # Needed because of GetScalarRange
 
    if filename.endswith(".p3d"):
        reader.Update()  # Needed because of GetScalarRange
        output = reader.GetOutput().GetBlock(0)
    elif filename.endswith(".dat") or filename.endswith(".plt"):
        pass
    else:
        reader.Update()  # Needed because of GetScalarRange
        output = reader.GetOutput()

        if filename.endswith(".cgns"):
            #delete the temp .vtk file
            os.system('rm' + ' ' + vtkfilename)


    return output
