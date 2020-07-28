import math
import vtk
from vtk_wrapper import *
from src.qrangeslider import QRangeSlider
import sys, os, random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support as VN
import numpy as np

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib.cm as cm

from src.text_form        import popup_widget_4TX
from src.scalar_form      import popup_widget_4SC
from src.streamline_form  import popup_widget_4SL
from src.cutplane_form    import popup_widget_4CP
from src.isosurf_form     import popup_widget_4IS
from src.vectorfield_form import popup_widget_4VF
from src.axes_form        import popup_widget_4AX



class AppForm(QMainWindow):
   
    scalar_signal     = pyqtSignal()
    cutplane_signal   = pyqtSignal(int)
    isosurf_signal    = pyqtSignal(int)
    streamline_signal = pyqtSignal(int)
    vectorfield_signal= pyqtSignal(int)
    text_signal       = pyqtSignal(int)
    axes_signal       = pyqtSignal()

    filename = ''
    outfilename = ''
    colormaplist = []
    camera = vtk.vtkCamera()
    camera_params = []
    
    # chlid widget
    popup_4TX = None
    popup_4SC = None
    popup_4VC = None
    popup_4CP = None
    popup_4IS = None
    popup_4SL = None
    popup_4VF = None
    frame_axis_dialog = None

    # editing-active Actors
    volume_actor = None 
    planeActor   = None 
    isoActor     = None 
    streamActor  = None 
    glyphActor   = None 
        
    listed_cutplane   = [None] 
    listed_isosurf    = [None]
    listed_streamline = [None]
    listed_vectorfield= [None]  
    
    listed_cutplane_model   = [None] 
    listed_isosurf_model    = [None]
    listed_streamline_model = [None]
    listed_vectorfield_model= [None]  
  
    currlut = vtk.vtkLookupTable() 
  
    # Data related variables
    scalarnamelist = []
    vectornamelist = []
  
    activescalarname = ''
    activevectorname = ''

    scalar_formula_list = []
    defined_scalar_list = []
    vector_component_list = []
    defined_vector_list = []

    # scene module list
    module_list = []
    legend_list = []
    arrow_list  = []
    text_list   = []
    
    def __init__(self):
        super(AppForm, self).__init__()
        self.setWindowTitle('PyVT' + "\u00a9" + 'Lv&Liu')
        self.create_main_frame()
        self.create_menu()
     
        # Global actor 
        self.cubeAxesActor  = None     # actor of axes
        self.OutlineActor   = None     # actor of outline 
        self.WireframeActor = None     # actor of wireframe(mesh) 
        self.FeatureActor   = None     # actor of feature edges

        # self.create_status_bar()
        self.output = None  #load from input data file 
        self.volume = None
        self.cutter = None

        self.sliceActor = None
        self.item = 0

        self.converter = None
        self.interpolated_data = None
    
    def save_plot(self):
        file_choices = "PNG (*.png);; \
                        EPS (*.eps);; \
                        JPG (*.jpg);; \
                        TIFF (*.tiff);; \
                        BMP (*.bmp)"

        path, ext = QFileDialog.getSaveFileName(self,
                                                'Save file', '',
                                                file_choices)
        path = path.encode('utf-8')
        self.outfilename = path.decode()
        self.write_plot()
        
    def write_plot(self):

        # write plot
        actor_list = []
        if self.FeatureActor != None: 
            actor_list.append(self.FeatureActor)
        if self.OutlineActor != None:
            actor_list.append(self.OutlineActor)
        if self.WireframeActor != None:
            actor_list.append(self.WireframeActor)
         
        for item in self.module_list:
            actor_list.append(item.actor)

        actor2d_list = [] 

        winsize = self.vtkWidget.GetRenderWindow().GetSize() 
        camera_params = [self.camera.GetPosition(), self.camera.GetFocalPoint(), \
                         self.camera.GetViewUp(),   self.camera.GetViewAngle() ]
        render_with_actor(actor_list, actor2d_list, self.text_list, self.arrow_list, self.legend_list, \
                          self.frame_axes, self.orient_axes_widget, camera_params, self.outfilename, winsize, 2)

    def load_colormaps(self):

        from src.colormap import _selected_cmaps
        
        self.colormaplist = [] 
        
        for i in range(len(_selected_cmaps)):
            self.colormaplist.append(_selected_cmaps[i])
            #self.color_select.addItem(_selected_cmaps[i])
            self.color_select.addItem('') 
            cmname = 'icons/cm_' + _selected_cmaps[i] + '.png' 
            icon = QIcon()
            icon.addPixmap(QPixmap(cmname), QIcon.Normal, QIcon.Off)
            self.color_select.setItemIcon(i, icon) 
        
        size = QSize(150, 25)
        self.color_select.setIconSize(size)

        self.select_colorbar() 

    def open_file(self):
        
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open", "", "VTK Files (*.vtu *.vts *.vtk);; \
                                                                          Tecplot Bin File(*.plt);;       \
                                                                          Tecplot ASCII File(*.dat);;   \
                                                                          Plot3D File(*.p3d);;            \
                                                                          PYGG State File(*.stat);;       \
                                                                          All Files (*)")
        if len(self.filename)==0:
            return 
        
        if self.filename.endswith('.stat'):
            journal_file = self.filename 
            self.parse_journal(journal_file)
        else:
            self.load_data()


    def parse_journal(self, journal_file):
        
        fp = open(journal_file, 'r') 

        import json
        
        self.filename = json.loads(fp.readline())
        self.load_data()
 
        # process defined scalar
        self.scalar_formula_list = json.loads(fp.readline())
        self.defined_scalar_list = json.loads(fp.readline())
        from src.eqn_parser import DataTabular, interpret

        # preview data tabular
        dt = DataTabular()
        nscalar = len(self.scalarnamelist)
        for index in range(nscalar):
            name = 'scalar_' + str(index+1)
            dt.add_name(name)
            dt.add_array(VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.scalarnamelist[index])))

        for index in range(len(self.scalar_formula_list)):
            formula = self.scalar_formula_list[index]
            tecarray = VN.numpy_to_vtk(interpret(formula, dt))
            tecarray.SetName(self.defined_scalar_list[index])
            self.output.GetPointData().AddArray(tecarray)
            
            name ='scalar_' + str(nscalar+1+index)
            dt.add_name(name)
            dt.add_array(VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.defined_scalar_list[index])))

            self.scalarnamelist.append(self.defined_scalar_list[index])
            self.variable_select.addItem(self.defined_scalar_list[index])
           
        # process defined vector
        self.vector_component_list = json.loads(fp.readline())
        self.defined_vector_list   = json.loads(fp.readline())

        for index in range(len(self.defined_vector_list)):

            vector_name = self.defined_vector_list[index]
            uvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.vector_component_list[index][0]))
            vvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.vector_component_list[index][1]))
            wvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.vector_component_list[index][2]))
            
            udf_vector = np.stack((uvel, vvel, wvel), axis=1)
            varray = VN.numpy_to_vtk(udf_vector)
            varray.SetName(vector_name)
            self.output.GetPointData().AddArray(varray)
            self.output.GetPointData().SetActiveVectors(vector_name)

        numofmodule = json.loads(fp.readline())
        for i in range(numofmodule):
            item = Scene_Module()
            item.load(fp)
            item.render(self.output)
            self.renderer.AddActor(item.actor)
            self.module_list.append(item)
        
            size = len(self.module_list)
            name = 'module_' + str(size)
            qtitem = QListWidgetItem(name)
            qtitem.setFlags(qtitem.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            qtitem.setCheckState(Qt.Unchecked)
            self.mcontainer.addItem(qtitem)

        numofannota = json.loads(fp.readline())
        for i in range(numofannota):
            item = Scene_Module_Text()
            item.load(fp)
            item.render()
            self.renderer.AddActor2D(item.actor)
            self.text_list.append(item)
    
        numofarrow  = json.loads(fp.readline())
        for i in range(numofarrow):
            item = Scene_Module_Arrow()
            item.load(fp)
            item.render()
            self.renderer.AddActor2D(item.actor)
            self.arrow_list.append(item)

        numoflegend = json.loads(fp.readline())
        for i in range(numoflegend):
            item = Scene_Module_Legend()
            item.load(fp)
            item.render()
            self.renderer.AddActor2D(item.actor)
            self.legend_list.append(item)

        mainframe_width = json.loads(fp.readline())
        mainframe_height = json.loads(fp.readline())
        
        self.resize(mainframe_width, mainframe_height)
       
        canvas_width = json.loads(fp.readline())
        canvas_height = json.loads(fp.readline())
        
        self.camera.SetPosition(json.loads(fp.readline()))
        self.camera.SetFocalPoint(json.loads(fp.readline()))
        self.camera.SetViewUp(json.loads(fp.readline()))
        self.camera.SetViewAngle(json.loads(fp.readline()))

        # check if orientation axis is on
        flag = json.loads(fp.readline())
        if flag == True: 
            AxesActor = create_orientaxes_actor()
            rgba = [0] * 4
            colors = vtk.vtkNamedColors()
            colors.GetColor("Carrot", rgba)
            self.orient_axes_widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
            self.orient_axes_widget.SetOrientationMarker(AxesActor)
            self.orient_axes_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
            self.orient_axes_widget.SetInteractor(self.iren)
            self.orient_axes_widget.On()

        # check if domain outline is on 
        flag = json.loads(fp.readline())
        if flag == True:
            self.FeatureActor = create_featureedge_actor(self.output)
            self.renderer.AddActor(self.FeatureActor)

        # check if bounding box is on
        flag = json.loads(fp.readline())
        if flag == True:
            self.OutlineActor = create_boundbox_actor(self.output)
            self.renderer.AddActor(self.OutlineActor)

        # check if mesh is on
        flag = json.loads(fp.readline())
        if flag == True:
            self.WireframeActor = create_mesh_actor(self.output)
            self.renderer.AddActor(self.WireframeActor)

        # check if background color is changed
        flag = json.loads(fp.readline())
        if flag == True:
            colors = vtk.vtkNamedColors()
            self.renderer.SetBackground(colors.GetColor3d("SlateGray"))
        else:
            self.renderer.SetBackground(1, 1, 1)

        # check if frame axis is on
        flag = json.loads(fp.readline())
        if flag == True:
            self.frame_axes.load(fp)
            self.frame_axes.render2D(self.renderer, None)
            self.vtkWidget.GetRenderWindow().Render()
                
            winsize = self.vtkWidget.GetRenderWindow().GetSize()
            self.frame_axes.mock(self.renderer, winsize) 
            self.frame_axes.update(winsize)
            
            if self.frame_axes.grid_on:
                self.frame_axes.show_grid(self.renderer)

            self.vtkWidget.GetRenderWindow().Render()
            
            
            self.init_frame_axes_dialog()
            self.communicator.frame_axes = self.frame_axes
        
        fp.close()
        
#        self.renderer.ResetCamera()
        
        self.vtkWidget.GetRenderWindow().Render()
    
    def write_journal(self):
       
        fp = open('journal.stat', 'w')

        import json
      
        json.dump(self.filename, fp); fp.write('\n') 

        json.dump(self.scalar_formula_list, fp); fp.write('\n')
        json.dump(self.defined_scalar_list, fp); fp.write('\n')

        json.dump(self.vector_component_list, fp); fp.write('\n')
        json.dump(self.defined_vector_list, fp); fp.write('\n')

        json.dump(len(self.module_list), fp); fp.write('\n')
        for item in self.module_list:
            item.write(fp)
       
        json.dump(len(self.text_list), fp); fp.write('\n')
        for item in self.text_list:
            item.write(fp)
       
        json.dump(len(self.arrow_list), fp); fp.write('\n')
        for item in self.arrow_list:
            item.write(fp)

        json.dump(len(self.legend_list), fp); fp.write('\n')
        for item in self.legend_list:
            item.write(fp)

        # main window dimensions
        json.dump(self.width(), fp); fp.write('\n')
        json.dump(self.height(), fp); fp.write('\n')
        
        # canvas dimensions
        winsize = self.vtkWidget.GetRenderWindow().GetSize()
        json.dump(winsize[0], fp); fp.write('\n')
        json.dump(winsize[1], fp); fp.write('\n')
       
        json.dump(self.camera.GetPosition(), fp); fp.write('\n')
        json.dump(self.camera.GetFocalPoint(), fp); fp.write('\n')
        json.dump(self.camera.GetViewUp(), fp); fp.write('\n')
        json.dump(self.camera.GetViewAngle(), fp); fp.write('\n')

        # if orientation axis is on
        flag = self.orient_axes_widget.GetEnabled()
        json.dump(flag, fp); fp.write('\n')
        
        # if domain outline is on 
        flag = (self.FeatureActor != None)
        json.dump(flag, fp); fp.write('\n')

        # if bounding box is on 
        flag = (self.OutlineActor != None)  
        json.dump(flag, fp); fp.write('\n')
        
        # if mesh is on
        flag = (self.WireframeActor != None)
        json.dump(flag, fp); fp.write('\n')
       
        # if background color is changed
        if (1.0, 1.0, 1.0) == self.renderer.GetBackground(): 
            flag = False
        else:
            flag = True
        json.dump(flag, fp); fp.write('\n')
      
        # if frame axis is no
        flag = (self.frame_axes.actor2D != None)
        json.dump(flag, fp); fp.write('\n')
        self.frame_axes.write(fp)

        fp.close() 

    def load_data(self):
    
        from myio.data_reader import read_input_file
        
        self.output = read_input_file(self.filename)

        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = self.output.GetBounds()

        # set scalars with given array data 
        num_array = self.output.GetPointData().GetNumberOfArrays()

        # find and list variable array names 
        self.scalarnamelist = []
        self.vectornamelist = [] 
        name_append = ['x', 'y', 'z']
        for i in range(num_array):
            varname = self.output.GetPointData().GetArrayName(i)
            darray = VN.vtk_to_numpy(self.output.GetPointData().GetArray(varname))
            
            if darray.ndim == 2:
                # check if it's a vector
                if darray.shape[1] == 3:
                    self.vectornamelist.append(varname)
                    # break vector to componental scalars
                    for i in range(3):
                        comps = VN.numpy_to_vtk(darray[:, i])
                        comps.SetName(varname + '_' + name_append[i])
                        self.output.GetPointData().AddArray(comps)
                        self.scalarnamelist.append(comps.GetName())
                        self.variable_select.addItem(comps.GetName())
            else: 
                self.scalarnamelist.append(varname)
                self.variable_select.addItem(varname)

        self.output.GetPointData().SetActiveScalars(None)
        
    def select_scalar_variable(self): 
        # change array scalar based on the variable_select QComboBox output
        index = self.variable_select.currentIndex()

        if index != 0:
            self.output.GetPointData().SetActiveScalars(self.scalarnamelist[index-1])
        else:
            # no scalar array selected
            if self.output == None: return 
            self.output.GetPointData().SetActiveScalars(None)
        
        self.render_module() 
       

    def select_colorbar(self):
        # change colorbar based on the color_select QComboBox output
        index = self.color_select.currentIndex()
        colormapname = self.colormaplist[index]

        # build a vtk lookup table 
        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToDiverging()
        if colormapname == 'Set3':
            tableSize = 12
        elif colormapname == 'tab20':
            tableSize = 20
        else:
            tableSize = 256

        import src.colormap as myCM
        
        for i in range(tableSize):
            cv = myCM.color_map(i, colormapname) 
            ctf.AddRGBPoint(float(i)/tableSize, cv[0], cv[1], cv[2])

        #self.currlut = vtk.vtkLookupTable()
        self.currlut.SetNumberOfTableValues(tableSize)
        self.currlut.Build()

        for i in range(0, tableSize):
            rgb = list(ctf.GetColor(float(i) / tableSize)) + [1]
            self.currlut.SetTableValue(i, rgb)

    def define_mapper(self, opt): 
        
        #find the adjusted bounds of the scalar range
        bounds = self.range_slider.getRange() 
        
        scalar_range = self.output.GetScalarRange()    
      
        adj_bounds = (scalar_range[0] + float(bounds[0])/99.0 * (scalar_range[1] - scalar_range[0]), \
                      scalar_range[0] + float(bounds[1])/99.0 * (scalar_range[1] - scalar_range[0]), )
        
        scalar_range = adj_bounds 

        self.currlut.SetTableRange(scalar_range) 
        
        # Create the mapper that corresponds the objects into graphics elements
        if opt==0:
            mapper = vtk.vtkDataSetMapper()
        else:
            mapper = vtk.vtkPolyDataMapper()

        #mapper.SetInputData(self.output)
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetLookupTable(self.currlut)
        mapper.SetScalarRange(scalar_range)

        return mapper

    def define_vector_variable(self):
        if self.output == None:
            pass 
        else:
            import vector_form as VC

            self.popup_4VC = VC.popup_widget_4VC(self.scalarnamelist)
            self.popup_4VC.exec_()
   
            uvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.popup_4VC.x_comp_var_name))
            vvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.popup_4VC.y_comp_var_name))
            wvel = VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.popup_4VC.z_comp_var_name))
            
            udf_vector = np.stack((uvel, vvel, wvel), axis=1)
            varray = VN.numpy_to_vtk(udf_vector)
            varray.SetName(self.popup_4VC.vector_name)
            self.output.GetPointData().AddArray(varray)
            self.output.GetPointData().SetActiveVectors(self.popup_4VC.vector_name)
   
        self.vector_component_list.append((self.popup_4VC.x_comp_var_name,\
                                           self.popup_4VC.y_comp_var_name,\
                                           self.popup_4VC.z_comp_var_name   ))
        self.defined_vector_list.append(self.popup_4VC.vector_name)

    def control_scalar_variable_vis(self):
        if self.output == None:
            pass
        else:
            if self.popup_4SC.isVisible():
                self.popup_4SC.close()
            
            self.popup_4SC.varlist = []
            for item in self.scalarnamelist:
                self.popup_4SC.varlist.append(item)

            self.popup_4SC.reinitialize()
            self.popup_4SC.show()
    
    def define_scalar_variable(self):
        
        from src.eqn_parser import DataTabular, interpret

        # preview data tabular
        dt = DataTabular()
        for index in range(len(self.scalarnamelist)):
            name = 'scalar_' + str(index+1)
            dt.add_name(name)
            dt.add_array(VN.vtk_to_numpy(self.output.GetPointData().GetArray(self.scalarnamelist[index])))

        formula = self.popup_4SC.formula.replace(" ", "")
        tecarray = VN.numpy_to_vtk(interpret(formula, dt)) 
        tecarray.SetName(self.popup_4SC.new_var_name)
        self.output.GetPointData().AddArray(tecarray)
         
        self.scalarnamelist.append(self.popup_4SC.new_var_name)
        self.variable_select.addItem(self.popup_4SC.new_var_name)
    
        self.scalar_formula_list.append(formula) 
        self.defined_scalar_list.append(self.popup_4SC.new_var_name)

    def adjust_opacity(self, value):
        self.volume_actor.GetProperty().SetOpacity(1-float(value)/99.0)
        self.volume_actor.GetProperty().ShadingOff()

    def control_cutplane_vis(self):
        if self.cutplane_see.isChecked():
            self.cutplane_see.setIcon(QIcon('./icons/visible.png'))
            self.planeActor.SetVisibility(False) 
        else:
            self.cutplane_see.setIcon(QIcon('./icons/invisible.png'))
            self.planeActor.SetVisibility(True)
            
        self.vtkWidget.GetRenderWindow().Render()

    def define_cutplane(self):
        if self.output == None:
            pass
        else:
            if self.popup_4CP.isVisible():
                self.popup_4CP.close()
            
            self.popup_4CP.show()
            
    def preview_cutplane(self, data):
      
        if self.popup_4CP.def_type == 'x':
            value  = self.popup_4CP.x_factor 
            normal = (1.0, 0.0, 0.0)
            origin = (float(value)/99.0*(self.xmax-self.xmin)+self.xmin, 0.0, 0.0)
            
        elif self.popup_4CP.def_type == 'y':
            value  = self.popup_4CP.y_factor 
            normal = (0.0, 1.0, 0.0)
            origin = (0.0, float(value)/99.0*(self.ymax-self.ymin)+self.ymin, 0.0)
            
        elif self.popup_4CP.def_type == 'z':
            value  = self.popup_4CP.z_factor 
            normal = (0.0, 0.0, 1.0)
            origin = (0.0, 0.0, float(value)/99.0*(self.zmax-self.zmin)+self.zmin)
        
        elif self.popup_4CP.def_type == 'other':
            
            normal = self.popup_4CP.udf_nml
            origin = self.popup_4CP.udf_org
        
        nm  = list(normal); og = list(origin)
        
        cutter = algo4cutplane(self.output, og, nm, self.popup_4CP.numcut, self.popup_4CP.offset)
   
        cutterMapper = self.define_mapper(2)
        cutterMapper.SetInputConnection(cutter.GetOutputPort())
        self.planeActor.SetMapper(cutterMapper)
        self.planeActor.GetProperty().SetOpacity(1-float(self.setopacity.value())/99.0)
        self.volume_actor.SetVisibility(False)

        self.vtkWidget.GetRenderWindow().Render()
      
        if data == 1: 
            # add to cutplane list for further use
            size = len(self.listed_cutplane)
            name = 'cutplane_' + str(size)
            self.listed_cutplane.append([og, nm, self.popup_4CP.numcut, self.popup_4CP.offset])
            self.cutplane_select.addItem(name) 
            self.listed_cutplane_model.append(cutter)  


    def control_isosurf_vis(self):
        if self.isosurf_see.isChecked():
            self.isosurf_see.setIcon(QIcon('./icons/visible.png'))
            self.isoActor.SetVisibility(False)
        else:
            self.isosurf_see.setIcon(QIcon('./icons/invisible.png'))
            self.isoActor.SetVisibility(True)
        
        self.vtkWidget.GetRenderWindow().Render()
    
    def define_isosurf(self):
        if self.output == None or self.output.GetPointData().GetScalars() == None:
            pass
        else:
            if self.popup_4IS.isVisible():
                self.popup_4IS.close()
       
            scalar_range = self.output.GetScalarRange()
            self.popup_4IS.upperbound = scalar_range[1]
            self.popup_4IS.lowerbound = scalar_range[0]
            self.popup_4IS.set_range();
            self.popup_4IS.show()
  
    def preview_isosurf(self, data):
        
        values = self.popup_4IS.iso_value
        scalarname = self.output.GetPointData().GetScalars().GetName()
        
        isosurf = algo4isosurf(self.output, scalarname, values)
        
        isoMapper = self.define_mapper(2)
        isoMapper.SetInputConnection(isosurf.GetOutputPort())
        
        self.isoActor.SetMapper(isoMapper)
        self.isoActor.GetProperty().SetOpacity(1-float(self.setopacity.value())/99.0)

        self.volume_actor.SetVisibility(False) 
       
        self.vtkWidget.GetRenderWindow().Render()

        if data == 1:
            size = len(self.listed_isosurf)
            
            self.listed_isosurf.append([scalarname, values])
            name = 'isosurf_' + str(size)
            self.isosurf_select.addItem(name) 
            self.listed_isosurf_model.append(isosurf)

    def control_streamline_vis(self):
        if self.streamline_see.isChecked():
            self.streamline_see.setIcon(QIcon('./icons/visible.png'))
            self.streamActor.SetVisibility(False) 
        else:
            self.streamline_see.setIcon(QIcon('./icons/invisible.png'))
            self.streamActor.SetVisibility(True)
        
        self.vtkWidget.GetRenderWindow().Render()
    
    def define_streamline(self): 
        
        if self.output == None or self.output.GetPointData().GetVectors() == None:
            pass
        else:
            if self.popup_4SL.isVisible():
                self.popup_4SL.close()
            
            self.popup_4SL.show()
            
    def preview_streamline(self, data):
       
        # collecting streamline parameter
        paramlist = []
        paramlist.append(self.popup_4SL.SL_seed_type)
        paramlist.append(self.popup_4SL.SL_point_center)
        paramlist.append(self.popup_4SL.SL_point_radius)
        paramlist.append(self.popup_4SL.SL_point_numseed)
        paramlist.append(self.popup_4SL.SL_line_pointA)
        paramlist.append(self.popup_4SL.SL_line_pointB)
        paramlist.append(self.popup_4SL.SL_line_reso)
        paramlist.append(self.popup_4SL.SL_plane_origin)
        paramlist.append(self.popup_4SL.SL_plane_pointA)
        paramlist.append(self.popup_4SL.SL_plane_pointB)
        paramlist.append(self.popup_4SL.SL_plane_resoX)
        paramlist.append(self.popup_4SL.SL_plane_resoY)

        paramlist.append(self.popup_4SL.SL_integ_direct) 
        paramlist.append(self.popup_4SL.SL_integ_max_step)
        paramlist.append(self.popup_4SL.SL_integ_init_step)

        stracer = algo4streamline(self.output, paramlist)

        mapStreamLines = self.define_mapper(2) 
        mapStreamLines.SetInputConnection(stracer.GetOutputPort())
        
        self.streamActor.SetMapper(mapStreamLines)
        self.streamActor.GetProperty().SetOpacity(1-float(self.setopacity.value())/99.0)
        self.volume_actor.SetVisibility(False)
 
        self.vtkWidget.GetRenderWindow().Render()

        if data == 1:
            size = len(self.listed_streamline)
            
            self.listed_streamline.append(paramlist)
            name = 'streamline_' + str(size)
            self.streamline_select.addItem(name) 
            self.listed_streamline_model.append(stracer)

    def control_vectorfield_vis(self):
        if self.vectorfield_see.isChecked():
            self.vectorfield_see.setIcon(QIcon('./icons/visible.png'))
            self.glyphActor.SetVisibility(False)
        else:
            self.vectorfield_see.setIcon(QIcon('./icons/invisible.png'))
            self.glyphActor.SetVisibility(True)
        
        self.vtkWidget.GetRenderWindow().Render()
    
    def define_vectorfield(self): 
        
        if self.output == None or self.output.GetPointData().GetVectors() == None:
            pass
        else:
            if self.popup_4VF.isVisible():
                self.popup_4VF.close()
            
            self.popup_4VF.show()
            
    def preview_vectorfield(self, data): 

        appendF = vtk.vtkAppendPolyData()
        have_listed_item = False  
        if self.cutplane_select.currentIndex() != 0:
            index = self.cutplane_select.currentIndex()
            cutter = self.listed_cutplane_model[index]
            appendF.AddInputConnection(cutter.GetOutputPort())
            have_listed_item = True 

        if self.isosurf_select.currentIndex() != 0:
            
            index = self.isosurf_select.currentIndex()
            isosurf = self.listed_isosurf_model[index]
            appendF.AddInputConnection(isosurf.GetOutputPort())
            have_listed_item = True

        if self.streamline_select.currentIndex() != 0:
            
            index = self.streamline_select.currentIndex() 
            streamline = self.listed_streamline_model[index]
            streamline.GetOutput().GetPointData().SetActiveVectors(self.popup_4VC.vector_name)
            appendF.AddInputConnection(streamline.GetOutputPort())
            have_listed_item = True
 
        glyph = algo4vectorfield_wgfilter(self.output, appendF, have_listed_item, self.popup_4VF.scaling_factor, self.popup_4VF.skip_factor) 

        glyphMapper = self.define_mapper(2)
        glyphMapper.SetInputConnection(glyph.GetOutputPort())
        
        self.glyphActor.SetMapper(glyphMapper)
        self.glyphActor.GetProperty().SetOpacity(1-float(self.setopacity.value())/99.0)
        self.volume_actor.SetVisibility(False)
        
        self.vtkWidget.GetRenderWindow().Render()

        if data==1:
            size = len(self.listed_vectorfield)
            geom_unit_params = [None,  None,  None ]
            geom_unit_model  = [None,  None,  None ]
            
            if self.cutplane_select.currentIndex() != 0:
                geom_unit_params[0] = self.listed_cutplane[self.cutplane_select.currentIndex()]
                geom_unit_model[0] = cutter

            if self.isosurf_select.currentIndex() != 0:
                geom_unit_params[1] = self.listed_isosurf[self.isosurf_select.currentIndex()]
                geom_unit_model[1] = isosurf

            if self.streamline_select.currentIndex() != 0:
                geom_unit_params[2] = self.listed_streamline[self.streamline_select.currentIndex()]
                geom_unit_model[2] = streamline

            self.listed_vectorfield.append([geom_unit_params, self.popup_4VC.vector_name, self.popup_4VF.scaling_factor, self.popup_4VF.skip_factor])
            name = 'vectorfield_' + str(size)
            self.vectorfield_select.addItem(name) 
            self.listed_vectorfield_model.append(geom_unit_model)


    def create_main_frame(self):
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.canvas = myCanvas()
        #self.canvas.background()

        # Create the navigation toolbar, tied to the canvas
        self.popup_4TX = popup_widget_4TX(self)
        self.popup_4SC = popup_widget_4SC(self)        
        self.popup_4IS = popup_widget_4IS(self, [])#
        self.popup_4SL = popup_widget_4SL(self)
        self.popup_4CP = popup_widget_4CP(self)
        self.popup_4VF = popup_widget_4VF(self)
        self.frame_axis_dialog = popup_widget_4AX(self) 
       
        # Other GUI controls
        #
        AddFile = QAction(QIcon('icons/open.png'), 'open file', self)  #
        AddFile.setShortcut('Ctrl+N')
        #AddFile.triggered.connect(self.browse_folder)
        AddFile.triggered.connect(self.open_file) 

        self.save_figure = QAction(QIcon('icons/save_figure.png'), 'save figure', self)
        self.save_figure.triggered.connect(self.save_plot)
        
        self.save_journal = QAction(QIcon('icons/save.png'), 'save journal', self)
        self.save_journal.triggered.connect(self.write_journal)
        
        self.orient_axes = QAction(QIcon('icons/orient_axes.png'), 'show orientation axes', self)
        self.orient_axes.triggered.connect(self.show_orient_axes)
       
        self.frame_axis = QAction(QIcon('icons/frame_axes.png'), 'show frame axes', self)
        self.frame_axis.triggered.connect(self.show_frame_axes)
        self.axes_signal.connect(self.adjust_frame_axes)

        self.view_x = QAction(QIcon('icons/x.png'), 'view YZ plane', self)
        self.view_x.setCheckable(True)
        self.view_x.triggered.connect(self.view_yz)

        self.view_y = QAction(QIcon('icons/y.png'), 'view YZ plane', self)
        self.view_y.setCheckable(True)
        self.view_y.triggered.connect(self.view_xz)

        self.view_z = QAction(QIcon('icons/z.png'), 'view XZ plane', self)
        self.view_z.setCheckable(True)
        self.view_z.triggered.connect(self.view_xy)
     
        self.outline = QAction(QIcon('icons/outline.png'), 'show outline', self)
        self.outline.triggered.connect(self.show_featureedge)
        
        self.boundbox = QAction(QIcon('icons/boundbox.png'), 'show bounding box', self)
        self.boundbox.triggered.connect(self.show_boundbox)

        self.mesh = QAction(QIcon('icons/mesh.png'), 'show mesh', self)
        self.mesh.triggered.connect(self.show_mesh)
        
        self.colorbar = QAction(QIcon('icons/colorbar.png'), 'show colorbar', self)
        self.colorbar.setCheckable(True)
        self.colorbar.triggered.connect(self.control_colorbar)

        self.background = QAction(QIcon('icons/background.png'), 'change background color', self)
        self.background.triggered.connect(self.change_bgcolor)

        self.reset = QAction(QIcon('icons/reset.png'), 'reset view', self)
        self.reset.triggered.connect(self.reset_camera)
     
        self.rot90 = QAction(QIcon('icons/rotate90deg.png'), 'rotate by 90deg', self)
        self.rot90.triggered.connect(self.reset_camera)
     
        self.vector_define = QAction(QIcon('icons/define_vector.png'), 'define vector', self)
        self.vector_define.triggered.connect(self.define_vector_variable)

        self.scalar_define = QAction(QIcon('icons/define_scalar.png'), 'define scalar', self)
        self.scalar_define.triggered.connect(self.control_scalar_variable_vis)
        self.scalar_signal.connect(self.define_scalar_variable)
        
        self.text_add = QAction(QIcon('icons/text.png'), 'add text', self)
        self.text_add.setCheckable(True)
        self.text_add.triggered.connect(self.control_text)
        self.text_signal.connect(self.show_text)

        self.arrow_add = QAction(QIcon('icons/arrow.png'), 'add arrow', self)
        self.arrow_add.setCheckable(True)
        self.arrow_add.triggered.connect(self.control_arrow)
        
        self.toolbar = self.addToolBar('Add data file')
        self.toolbar.addAction(AddFile)
        self.toolbar.addAction(self.save_journal)
        self.toolbar.addAction(self.save_figure)
        self.toolbar.addAction(self.scalar_define)
        self.toolbar.addAction(self.vector_define)
        self.toolbar.addAction(self.frame_axis)
        self.toolbar.addAction(self.colorbar)
        self.toolbar.addAction(self.text_add)
        self.toolbar.addAction(self.arrow_add)
        self.toolbar.addAction(self.orient_axes)
        self.toolbar.addAction(self.outline)
        self.toolbar.addAction(self.boundbox)
        self.toolbar.addAction(self.mesh)
        self.toolbar.addAction(self.background)
        self.toolbar.addAction(self.reset)
        self.toolbar.addAction(self.rot90)
        self.toolbar.addAction(self.view_x)
        self.toolbar.addAction(self.view_y)
        self.toolbar.addAction(self.view_z)
        
        # Layout
        #
        main_layout = QHBoxLayout()
        right_split = QVBoxLayout()
        # left part of the main window 
        left_split  = QGridLayout() 

        # left side widget
        self.styleChoice = QLabel("Choose color map")
        
        self.color_select = QComboBox(self)
        self.color_select.move(50, 250) # move to a specific position
        self.styleChoice.move(10, 150)
        self.load_colormaps()
        self.color_select.activated[str].connect(self.select_colorbar)
        
        self.variable_select = QComboBox(self)
        self.variable_select.addItem("# shade")
        self.variable_select.activated[str].connect(self.select_scalar_variable)

        ## cutplane items 
        self.cutplane_select    = QComboBox(self);   self.cutplane_select.addItem('unspecified')
        self.cutplane           = QToolButton(self); self.cutplane.setToolTip('Define cutplane') 
        self.cutplane.clicked.connect(self.define_cutplane) 
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/cutplane.png'), QIcon.Normal, QIcon.Off)
        self.cutplane.setIcon(icon)
        self.cutplane.setIconSize(QSize(42, 24))
        self.cutplane_signal.connect(self.preview_cutplane) 
        self.cutplane_see       = QToolButton(self); self.cutplane_see.setIcon(QIcon('./icons/invisible.png')) 
        self.cutplane_see.setCheckable(True)
        self.cutplane_see.clicked.connect(self.control_cutplane_vis)
        
        ## isosurface items 
        self.isosurf_select     = QComboBox(self);   self.isosurf_select.addItem('unspecified')
        self.isosurf            = QToolButton(self); self.isosurf.setToolTip('Define isosurface')
        self.isosurf.clicked.connect(self.define_isosurf) 
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/isosurf.png'), QIcon.Normal, QIcon.Off)
        self.isosurf.setIcon(icon)
        self.isosurf.setIconSize(QSize(42, 24))
        self.isosurf_signal.connect(self.preview_isosurf) 
        self.isosurf_see       = QToolButton(self); self.isosurf_see.setIcon(QIcon('./icons/invisible.png')) 
        self.isosurf_see.setCheckable(True)
        self.isosurf_see.clicked.connect(self.control_isosurf_vis)
        
        ## streamline items 
        self.streamline_select  = QComboBox(self);   self.streamline_select.addItem('unspecified')
        self.streamline         = QToolButton(self); self.streamline.setToolTip("Define streamline")
        self.streamline.clicked.connect(self.define_streamline)
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/streamline.png'), QIcon.Normal, QIcon.Off)
        self.streamline.setIcon(icon)
        self.streamline.setIconSize(QSize(42, 24))
        self.streamline_signal.connect(self.preview_streamline)
        self.streamline_see     = QToolButton(self); self.streamline_see.setIcon(QIcon('./icons/invisible.png')) 
        self.streamline_see.setCheckable(True)
        self.streamline_see.clicked.connect(self.control_streamline_vis)
        

        ## vectorfield items 
        self.vectorfield_select = QComboBox(self);   self.vectorfield_select.addItem('unspecified')
        self.vectorfield        = QToolButton(self); self.vectorfield.setToolTip("Define vector field")
        self.vectorfield.clicked.connect(self.define_vectorfield)
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/vectorfield.png'), QIcon.Normal, QIcon.Off)
        self.vectorfield.setIcon(icon)
        self.vectorfield.setIconSize(QSize(42, 24))
        self.vectorfield_signal.connect(self.preview_vectorfield) 
        self.vectorfield_see    = QToolButton(self); self.vectorfield_see.setIcon(QIcon('./icons/invisible.png')) 
        self.vectorfield_see.setCheckable(True)
        self.vectorfield_see.clicked.connect(self.control_vectorfield_vis)
       

        self.setopacity = QSlider(Qt.Horizontal)
        self.setopacity.setObjectName("opacity_slider")
        self.setopacity.setTracking(True)
        self.setopacity.valueChanged.connect(lambda val: self.adjust_opacity(val))

        ## preview button
        self.preview_button = QToolButton(self); self.preview_button.setToolTip("Preview")  
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/preview.png'), QIcon.Normal, QIcon.Off)
        self.preview_button.setIcon(icon)
        self.preview_button.setIconSize(QSize(52, 24))
        self.preview_button.clicked.connect(self.plot_preview)
        
        ## clean preview
        self.clean_button = QToolButton(self); self.clean_button.setToolTip("Clean")  
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/clean.png'), QIcon.Normal, QIcon.Off)
        self.clean_button.setIcon(icon)
        self.clean_button.setIconSize(QSize(52, 24))
        self.clean_button.clicked.connect(self.clean_preview)
     
        ## add to basket button
        self.add2basket_button = QToolButton(self); self.add2basket_button.setToolTip("Add to container")  
        icon = QIcon() 
        icon.addPixmap(QPixmap('icons/add2basket.png'), QIcon.Normal, QIcon.Off)
        self.add2basket_button.setIcon(icon)
        self.add2basket_button.setIconSize(QSize(52, 24))
        self.add2basket_button.clicked.connect(self.add_module)
        
        self.varname_label  = QLabel("variable"); self.varname_label.resize(30, 18)
        self.range_label    = QLabel("range");    self.range_label.resize(30, 18)
        self.colormap_label = QLabel("colormap"); self.colormap_label.resize(30, 18)
        self.opacity_label  = QLabel("opacity");  self.opacity_label.resize(30, 18)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setObjectName("line2")

        self.range_slider = QRangeSlider()
        self.range_slider.setBackgroundStyle("background-color:white;")
        self.range_slider.handle.setStyleSheet("background-color:white;")

        # hints for QGridLayout: addWidget(*Widget, row, column, rowspan, colspan)
        left_split.addWidget(self.varname_label,     0, 0, 1, 1); left_split.addWidget(self.variable_select,   0, 1, 1, 5) 
        left_split.addWidget(self.range_label,       1, 0, 1, 1); left_split.addWidget(self.range_slider,      1, 1, 1, 5)
        left_split.addWidget(self.colormap_label,    2, 0, 1, 1); left_split.addWidget(self.color_select,      2, 1, 1, 5)
        left_split.addWidget(self.opacity_label,     3, 0, 1, 1); left_split.addWidget(self.setopacity,        3, 1, 1, 5)
        left_split.addWidget(self.line,              4, 0, 1, 6) 
        
        left_split.addWidget(self.cutplane,          5, 0, 1, 2); left_split.addWidget(self.cutplane_select,   5, 1, 1, 4); left_split.addWidget(self.cutplane_see,   5, 5, 1, 1)
        left_split.addWidget(self.isosurf,           6, 0, 1, 2); left_split.addWidget(self.isosurf_select,    6, 1, 1, 4); left_split.addWidget(self.isosurf_see,    6, 5, 1, 1)
        left_split.addWidget(self.streamline,        7, 0, 1, 2); left_split.addWidget(self.streamline_select, 7, 1, 1, 4); left_split.addWidget(self.streamline_see, 7, 5, 1, 1) 
        left_split.addWidget(self.vectorfield,       8, 0, 1, 2); left_split.addWidget(self.vectorfield_select,8, 1, 1, 4); left_split.addWidget(self.vectorfield_see,8, 5, 1, 1)
        left_split.addWidget(self.line1,             9, 0, 1, 6) 
        left_split.addWidget(self.clean_button,     10, 0, 1, 2); left_split.addWidget(self.add2basket_button,10, 1, 1, 2); left_split.addWidget(self.preview_button, 10, 3, 1, 2) 

        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_split.addWidget(dummy, 11, 0, 1,  6)

        # add a list for module item
        self.mcontainer_label = QLabel("Scene Module Container:");
        self.mcontainer = QListWidget(); #QListView(); 
        self.mcontainer.setObjectName("listView")
        self.module_render = QPushButton(self); self.module_render.setText('render'); self.module_render.clicked.connect(self.render_module)
        self.module_clear  = QPushButton(self); self.module_clear.setText('clear');   self.module_clear.clicked.connect(self.clear_module)
        self.module_delete = QPushButton(self); self.module_delete.setText('delete'); self.module_delete.clicked.connect(self.delete_module)
        left_split.addWidget(self.line2,            12, 0, 1, 6) 
        left_split.addWidget(self.mcontainer_label, 13, 0, 1, 5)
        left_split.addWidget(self.mcontainer,       14, 0, 4, 4); left_split.addWidget(self.module_render,   14, 4, 1, 2) 
        left_split.addWidget(self.module_delete,    15, 4, 1, 2)
        left_split.addWidget(self.module_clear,     16, 4, 1, 2)

        main_layout.addLayout(left_split,1)

        self.vtkWidget = QVTKRenderWindowInteractor(self.main_frame)
        self.renderer = vtk.vtkRenderer()
        #self.renderer.UseDepthPeelingOn()   # whether success depends on hardware; slow rendering speed with poor GPU 

        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren     = self.vtkWidget.GetRenderWindow().GetInteractor()
        
        from src.mouse_interaction import MyInteractorStyle
        self.communicator = Info_Exchanger()
        instyle = MyInteractorStyle(self.vtkWidget.GetRenderWindow(), self.renderer, self.communicator)
        self.iren.SetInteractorStyle(instyle)

        self.scalar_bar_widget = vtk.vtkScalarBarWidget()
        self.scalar_bar_widget.SetInteractor(self.iren) 
        
        self.text_widget = vtk.vtkTextWidget()
        self.text_widget.SetInteractor(self.iren)
        
        self.orient_axes_widget = vtk.vtkOrientationMarkerWidget()
        #self.orient_axes_widget.SetInteractor(self.iren)

        self.frame_axes = Scene_Module_FrameAxes()

        self.volume_actor = vtk.vtkActor()
        self.planeActor   = vtk.vtkActor()
        self.isoActor     = vtk.vtkActor()
        self.streamActor  = vtk.vtkActor()
        self.glyphActor   = vtk.vtkActor() 

        self.renderer.AddActor(self.volume_actor)
        self.renderer.AddActor(self.planeActor  )
        self.renderer.AddActor(self.isoActor    )
        self.renderer.AddActor(self.streamActor )
        self.renderer.AddActor(self.glyphActor  )

        right_split.addWidget(self.vtkWidget)
        
        main_layout.addLayout(right_split,2)

        self.widget = QWidget()
        self.widget.setLayout(main_layout)
        self.widget.setMinimumSize(900,600)
        self.setCentralWidget(self.widget)
       
        # initialize render window
        self.renderer.SetBackground(1, 1, 1)  # Set background to white
        self.renderer.SetActiveCamera(self.camera)
        self.iren.Initialize()
        self.vtkWidget.GetRenderWindow().Render()
        self.iren.Start()
            
        # camera parameter 
        #Position 
        #FocalPoint 
        #ViewUp 
        #ViewAngle 
        self.camera_params.append(self.camera.GetPosition()) 
        self.camera_params.append(self.camera.GetFocalPoint()) 
        self.camera_params.append(self.camera.GetViewUp()) 
        self.camera_params.append(self.camera.GetViewAngle())

    def show_frame_axes(self):
        if self.frame_axes.actor2D != None:
            self.frame_axis_dialog.show()
            #self.renderer.RemoveActor2D(self.frame_axes.actor2D)
            #self.frame_axes.actor2D = None
            #self.vtkWidget.GetRenderWindow().Render()
        else:
            if self.output == None: 
                print('there is no input data')
            else:
                self.frame_axes.render2D(self.renderer, self.output.GetBounds())
                self.vtkWidget.GetRenderWindow().Render()
                
                winsize = self.vtkWidget.GetRenderWindow().GetSize()
                self.frame_axes.mock(self.renderer, winsize) 

                self.vtkWidget.GetRenderWindow().Render()
                
                self.init_frame_axes_dialog()
                self.frame_axis_dialog.show()

                self.communicator.frame_axes = self.frame_axes
  
    def init_frame_axes_dialog(self):
                
        # setup dialog initial conditions
        self.frame_axis_dialog.title_x = self.frame_axes.title_x
        self.frame_axis_dialog.title_y = self.frame_axes.title_y
        self.frame_axis_dialog.title_z = self.frame_axes.title_z
                
        bounds = self.output.GetBounds()
        bounds_x = (bounds[0], bounds[1])
        self.frame_axis_dialog.bounds_x = self.frame_axes.bounds_x = bounds_x
        bounds_y = (bounds[2], bounds[3])
        self.frame_axis_dialog.bounds_y = self.frame_axes.bounds_y = bounds_y
        bounds_z = (bounds[4], bounds[5])
        self.frame_axis_dialog.bounds_z = self.frame_axes.bounds_z = bounds_z

        self.frame_axis_dialog.noflabel_x = self.frame_axes.noflabel_x
        self.frame_axis_dialog.noflabel_y = self.frame_axes.noflabel_y
        self.frame_axis_dialog.noflabel_z = self.frame_axes.noflabel_z

        self.frame_axis_dialog.exponent_x = self.frame_axes.exponent_x
        self.frame_axis_dialog.exponent_y = self.frame_axes.exponent_y
        self.frame_axis_dialog.exponent_z = self.frame_axes.exponent_z
                
        self.frame_axis_dialog.font_factor  = self.frame_axes.font_factor
        self.frame_axis_dialog.label_factor = self.frame_axes.label_factor
        self.frame_axis_dialog.offset       = self.frame_axes.offset
        self.frame_axis_dialog.grid_on      = self.frame_axes.grid_on

        self.frame_axis_dialog.set_initial_status()

    def adjust_frame_axes(self):
       
        # pass new axes configure to axes instance
        self.frame_axes.show_x = self.frame_axis_dialog.show_x
        self.frame_axes.show_y = self.frame_axis_dialog.show_y
        self.frame_axes.show_z = self.frame_axis_dialog.show_z
        
        self.frame_axes.title_x = self.frame_axis_dialog.title_x
        self.frame_axes.title_y = self.frame_axis_dialog.title_y
        self.frame_axes.title_z = self.frame_axis_dialog.title_z
        
        self.frame_axes.bounds_x = self.frame_axis_dialog.bounds_x
        self.frame_axes.bounds_y = self.frame_axis_dialog.bounds_y
        self.frame_axes.bounds_z = self.frame_axis_dialog.bounds_z

        self.frame_axes.noflabel_x = self.frame_axis_dialog.noflabel_x
        self.frame_axes.noflabel_y = self.frame_axis_dialog.noflabel_y
        self.frame_axes.noflabel_z = self.frame_axis_dialog.noflabel_z

        self.frame_axes.exponent_x = self.frame_axis_dialog.exponent_x
        self.frame_axes.exponent_y = self.frame_axis_dialog.exponent_y
        self.frame_axes.exponent_z = self.frame_axis_dialog.exponent_z

        self.frame_axes.label_factor = self.frame_axis_dialog.label_factor
        self.frame_axes.font_factor  = self.frame_axis_dialog.font_factor
        self.frame_axes.offset       = self.frame_axis_dialog.offset
        self.frame_axes.grid_on      = self.frame_axis_dialog.grid_on
        
        if self.frame_axes.grid_on:
            self.frame_axes.show_grid(self.renderer)
        else:
            self.frame_axes.remove_grid(self.renderer)

        # update
        winsize = self.vtkWidget.GetRenderWindow().GetSize()
        self.frame_axes.update(winsize)
        self.vtkWidget.GetRenderWindow().Render()

    def show_featureedge(self):
        if self.FeatureActor != None:
            self.renderer.RemoveActor(self.FeatureActor)
            self.FeatureActor = None
            self.vtkWidget.GetRenderWindow().Render()
        else:
            if self.output == None:
                pass
                #print('there is no input data')
            else:
                
                self.FeatureActor = create_featureedge_actor(self.output)

                self.renderer.AddActor(self.FeatureActor)
                self.vtkWidget.GetRenderWindow().Render()
                 

    def show_boundbox(self):
        if self.OutlineActor != None:
            self.renderer.RemoveActor(self.OutlineActor)
            self.OutlineActor = None
            self.vtkWidget.GetRenderWindow().Render()
        else:
            if self.output == None: 
                pass
                print('there is no input data')
            else:
                self.OutlineActor = create_boundbox_actor(self.output)
                
                self.renderer.AddActor(self.OutlineActor)
                self.vtkWidget.GetRenderWindow().Render()
                #print('bounding box:')
                #print(self.OutlineActor.GetPosition())

    def show_mesh(self):
        if self.WireframeActor != None:
            self.renderer.RemoveActor(self.WireframeActor)
            self.WireframeActor = None
            self.vtkWidget.GetRenderWindow().Render()
        else:
            if self.output == None:
                print('there is no input data')
            else:
                self.WireframeActor = create_mesh_actor(self.output)
                self.renderer.AddActor(self.WireframeActor)
                self.vtkWidget.GetRenderWindow().Render()

    def change_bgcolor(self):
      
        if self.renderer.GetBackground() == (1.0, 1.0, 1.0):    # if background is white
            colors = vtk.vtkNamedColors()
            self.renderer.SetBackground(colors.GetColor3d("SlateGray"))
        else:
            self.renderer.SetBackground(1, 1, 1)                # Set background to white

        self.vtkWidget.GetRenderWindow().Render()

    def control_colorbar(self):
        if self.colorbar.isChecked():
            self.show_colorbar()
        else:
            self.hide_colorbar()

    def show_colorbar(self):

        # create the scalar_bar
        scalar_bar = create_colorbar_actor(self.currlut) 
        scalar_bar.SetTitle(self.variable_select.currentText() + '\n')
        self.scalar_bar_widget.SetScalarBarActor(scalar_bar)
        self.scalar_bar_widget.On()
        
        self.vtkWidget.GetRenderWindow().Render()
    
    def hide_colorbar(self):

        # turn off the widget and make a copy of the linked actor 
        legend = Scene_Module_Legend()
        
        legend.scalar_range   = self.output.GetScalarRange()
        legend.relative_range = self.range_slider.getRange()
        
        index = self.color_select.currentIndex()
        legend.colormapname   = self.colormaplist[index]

        legend.title  = self.scalar_bar_widget.GetScalarBarActor().GetTitle()
        legend.orient = self.scalar_bar_widget.GetScalarBarActor().GetOrientation()
        legend.numoflabels = self.scalar_bar_widget.GetScalarBarActor().GetNumberOfLabels()
        legend.width  = self.scalar_bar_widget.GetScalarBarActor().GetWidth()
        legend.height = self.scalar_bar_widget.GetScalarBarActor().GetHeight()
        legend.position = self.scalar_bar_widget.GetScalarBarActor().GetPosition()
        legend.render()

        self.legend_list.append(legend) 
        self.renderer.AddActor2D(legend.actor)
        
        self.scalar_bar_widget.Off()
        self.vtkWidget.GetRenderWindow().Render()

    def control_text(self):
        if self.text_add.isChecked():
            if self.popup_4TX.isVisible():
                self.popup_4TX.close()
            
            self.popup_4TX.show()
        else:
            self.hide_text()
        
    def show_text(self, val):
        
        if val == 0:
            self.text_add.setChecked(False)
        else: 
            text_actor = vtk.vtkTextActor()
            text_actor.SetInput(self.popup_4TX.text_input)
            text_actor.GetTextProperty().SetColor((0, 0, 0))
            #text_actor.GetTextProperty().SetOrientation(90)

            text_representation = vtk.vtkTextRepresentation()
            text_representation.GetPositionCoordinate().SetValue(0.1, 0.5)
            text_representation.GetPosition2Coordinate().SetValue(0.2, 0.1)
            text_representation.SetShowBorderToOn()

            #self.text_widget = vtk.vtkTextWidget()
            self.text_widget.SetRepresentation(text_representation)
            #self.text_widget.SetInteractor(self.iren)
            self.text_widget.SetTextActor(text_actor)
            self.text_widget.SelectableOff()
             
            self.text_widget.GetTextActor().GetTextProperty().SetJustificationToLeft()
            self.text_widget.GetTextActor().GetTextProperty().SetVerticalJustificationToBottom()
            self.text_widget.On()

            self.vtkWidget.GetRenderWindow().Render()

    def hide_text(self):
 
        # hide text_widget and make a copy of the linked actor
        annota = Scene_Module_Text() 
        annota.text = self.text_widget.GetTextActor().GetInput()
        annota.fontsize = self.text_widget.GetTextActor().GetScaledTextProperty().GetFontSize()
        annota.position = self.text_widget.GetTextActor().GetPosition()
        annota.position2 = self.text_widget.GetTextActor().GetPosition2()
        annota.render()  
        
        self.text_list.append(annota)

        self.renderer.AddActor2D(annota.actor)
       
        self.text_widget.Off()
        self.vtkWidget.GetRenderWindow().Render()

    def control_arrow(self):

        if self.arrow_add.isChecked():
            self.communicator.switch = True
        else:
            # pass over the picked parameters
            arrow = Scene_Module_Arrow()
            arrow.pointA = self.communicator.leaderactor.GetPosition()
            arrow.pointB = self.communicator.leaderactor.GetPosition2()
            arrow.actor  = self.communicator.leaderactor
            self.arrow_list.append(arrow) 
            
            # reset the actor instance
            self.communicator.leaderactor = None
            self.communicator.switch = False 

    def show_orient_axes(self):

        if self.orient_axes_widget.GetEnabled():
            self.orient_axes_widget.Off()
            self.vtkWidget.GetRenderWindow().Render()
            self.iren.Start()
        else: 
            AxesActor = create_orientaxes_actor()
            rgba = [0] * 4
            colors = vtk.vtkNamedColors()
            colors.GetColor("Carrot", rgba)
            self.orient_axes_widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
            self.orient_axes_widget.SetOrientationMarker(AxesActor)
            self.orient_axes_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
            self.orient_axes_widget.SetInteractor(self.iren)
            self.orient_axes_widget.SetInteractive(False)
            self.orient_axes_widget.On()

            self.vtkWidget.GetRenderWindow().Render()

    def reset_camera(self):
        self.camera.SetPosition(self.camera_params[0])
        self.camera.SetFocalPoint(self.camera_params[1])
        self.camera.SetViewUp(self.camera_params[2])
        self.camera.SetViewAngle(self.camera_params[3])
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.iren.Initialize()
        self.iren.Start()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QApplication.setStyle(QStyleFactory.create(text))

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
              shortcut="Ctrl+S", slot=self.save_plot,
              tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close,
                 shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
                         (load_file_action, None, quit_action))

        # self.help_menu = self.menuBar().addMenu("&Help")
        # about_action = self.create_action("&About",
        #       shortcut='F1', slot=self.on_about,
        #       tip='About the demo')
        #
        # self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def clean_preview(self):
        
        self.cutplane_select.setCurrentIndex(0)
        self.planeActor.GetProperty().SetOpacity(0)
        
        self.isosurf_select.setCurrentIndex(0)
        self.isoActor.GetProperty().SetOpacity(0)

        self.streamline_select.setCurrentIndex(0)
        self.streamActor.GetProperty().SetOpacity(0)

        self.vectorfield_select.setCurrentIndex(0)
        self.glyphActor.GetProperty().SetOpacity(0)
        self.volume_actor.SetVisibility(False)
        
        self.vtkWidget.GetRenderWindow().Render()
 
    def plot_preview(self):
        
        have_listed_elem = False
        alpha = 1.0 - float(self.setopacity.value())/99.0

        # check if any element is specified
        if self.cutplane_select.currentIndex() != 0: 
            have_listed_elem = True
            self.volume_actor.SetVisibility(False)
           
            index = self.cutplane_select.currentIndex()
            model = self.listed_cutplane_model[index]
             
            elem_mapper = self.define_mapper(2)
            elem_mapper.SetInputConnection(model.GetOutputPort())

            self.planeActor.SetMapper(elem_mapper)
            self.planeActor.GetProperty().SetOpacity(alpha)
        else:
            self.planeActor.GetProperty().SetOpacity(0)

        if self.isosurf_select.currentIndex() != 0:
            have_listed_elem = True
            self.volume_actor.SetVisibility(False)
            
            index = self.isosurf_select.currentIndex()
            model = self.listed_isosurf_model[index]
            scalar_name = self.output.GetPointData().GetScalars().GetName()
            model.GetOutput().GetPointData().SetActiveScalars(scalar_name)
            elem_mapper = self.define_mapper(2)
            elem_mapper.SetInputConnection(model.GetOutputPort())
            
            self.isoActor.SetMapper(elem_mapper)
            self.isoActor.GetProperty().SetOpacity(alpha)
        else: 
            self.isoActor.GetProperty().SetOpacity(0)
            
        if self.streamline_select.currentIndex() != 0:
            have_listed_elem = True
            self.volume_actor.SetVisibility(False)
            
            index = self.streamline_select.currentIndex()
            model = self.listed_streamline_model[index]
            
            elem_mapper = self.define_mapper(2)
            elem_mapper.SetInputConnection(model.GetOutputPort())
            
            self.streamActor.SetMapper(elem_mapper)
            self.streamActor.GetProperty().SetOpacity(alpha)
        else:
            self.streamActor.GetProperty().SetOpacity(0)
            
        if self.vectorfield_select.currentIndex() != 0:
            have_listed_elem = True
            self.volume_actor.SetVisibility(False)
            
            index = self.vectorfield_select.currentIndex()
            models = self.listed_vectorfield_model[index]
            vector_name = self.listed_vectorfield[index][1]
            scaling_factor = self.listed_vectorfield[index][2]
            skip_factor    = self.listed_vectorfield[index][3]

            appendF = vtk.vtkAppendPolyData()
            flag = False
            if models[0] != None:
                appendF.AddInputConnection(models[0].GetOutputPort())
                flag = True

            if models[1] != None:
                appendF.AddInputConnection(models[1].GetOutputPort())
                flag = True

            if models[2] != None:
                models[2].GetOutput().GetPointData().SetActiveVectors(vector_name)
                appendF.AddInputConnection(models[2].GetOutputPort())
                flag = True

            glyph = algo4vectorfield_wgfilter(self.output, appendF, flag, scaling_factor, skip_factor)
            
            elem_mapper = self.define_mapper(2)
            elem_mapper.SetInputConnection(glyph.GetOutputPort())
           
            self.glyphActor.SetMapper(elem_mapper)
            self.glyphActor.GetProperty().SetOpacity(alpha)
        else:
            self.glyphActor.GetProperty().SetOpacity(0)

        if not have_listed_elem: 
          
            # Create the mapper that corresponds the objects of the vtk.vtk file
            # into graphics elements
            volume_mapper = self.define_mapper(0) 
            volume_mapper.SetInputData(self.output)

            # update the Actor
            self.volume_actor.SetVisibility(True)
            self.volume_actor.SetMapper(volume_mapper)
            self.volume_actor.GetProperty().SetOpacity(alpha)
            
        self.vtkWidget.GetRenderWindow().Render()
   
    def add_module(self):
        
        new_module = Scene_Module()
        
        new_module.scalar_name  = self.variable_select.currentText() 
        new_module.scalar_range = self.output.GetPointData().GetArray(new_module.scalar_name).GetRange() 
        new_module.relative_range = self.range_slider.getRange()
        index = self.color_select.currentIndex()
        new_module.colormap = self.colormaplist[index]
        new_module.opacity = 1.0-float(self.setopacity.value())/99.0

        have_listed_elem = False
        # check if any element is specified
        if self.cutplane_select.currentIndex() != 0: 
            have_listed_elem = True
            index = self.cutplane_select.currentIndex()
            new_module.cutplane_param = self.listed_cutplane[index]

        if self.isosurf_select.currentIndex() != 0:
            have_listed_elem = True
            index      = self.isosurf_select.currentIndex()
            new_module.isosurf_param = self.listed_isosurf[index]

        if self.streamline_select.currentIndex() != 0:
            have_listed_elem = True
            index = self.streamline_select.currentIndex()
            new_module.streamline_param = self.listed_streamline[index]

        if self.vectorfield_select.currentIndex() != 0:
            have_listed_elem = True
            index = self.vectorfield_select.currentIndex()
            new_module.vectorfield_param = self.listed_vectorfield[index]

        new_module.render(self.output)
        self.module_list.append(new_module)
        size = len(self.module_list)
        name = 'module_' + str(size)
        item = QListWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        item.setCheckState(Qt.Unchecked)
        self.mcontainer.addItem(item)

    # render modules
    def render_module(self):
       
        if self.mcontainer.count() == 0:
            return 
        
        for row in range(self.mcontainer.count()):
            module = self.module_list[row]
            if self.mcontainer.item(row).checkState() == Qt.Checked:
                #module.geomcombine.Update()
                #module.geomcombine.GetOutput().GetPointData().SetActiveScalars(module.scalar_name)
            
                self.renderer.AddActor(module.actor)
            else: 
                self.renderer.RemoveActor(module.actor)
                
        self.vtkWidget.GetRenderWindow().Render()

    def clear_module(self):
        
        if self.mcontainer.count() == 0:
            return 
        
        for row in range(self.mcontainer.count()):
            module = self.module_list[row]
            self.renderer.RemoveActor(module.actor)
            self.mcontainer.item(row).setCheckState(Qt.Unchecked)

        self.vtkWidget.GetRenderWindow().Render()

    # delete moduels
    def delete_module(self):
        
        if self.mcontainer.count() == 0: 
            return 

    # set view direction 
    def view_yz(self):
        self.camera.SetPosition(1, 1, 1)
        self.camera.SetFocalPoint(0, 1, 1)
        self.camera.SetViewUp(0, 0, 1)
        if self.view_x.isChecked():
            self.camera.Elevation(180)
        else:
            pass
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def view_xz(self):
        self.camera.SetPosition(1, 1, 1)
        self.camera.SetFocalPoint(1, 0, 1)
        self.camera.SetViewUp(0, 0, 1)
        if self.view_y.isChecked():
            self.camera.Elevation(180)
        else:
            pass
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def view_xy(self):
        self.camera.SetPosition(1, 1, 1)
        self.camera.SetFocalPoint(1, 1, 0)
        self.camera.SetViewUp(0, 1, 0)
        if self.view_z.isChecked():
            self.camera.Elevation(180)
        else:
            pass
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def mag(self, z):
        """Get the magnitude of a vector."""
        if isinstance(z[0], np.ndarray):
            return np.array(list(map(np.linalg.norm, z)))
        else:
            return np.linalg.norm(z)


class myCanvas(FigureCanvas):

    def __init__(self, height=5.0, width=5.0):
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.fig = plt.gcf()
        self.dpi = 400
        #self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.fig.set_size_inches(height, width, forward=True)
        FigureCanvas.__init__(self, self.fig)

    def reSize(self,height,width):
        self.fig.set_size_inches(height, width, forward=True)

    def background(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.mouse_init(rotate_btn=1, zoom_btn=3)
        # self.ax.plot(xarray, yarray, zarray, 'ok')
        self.ax.set_xlabel('X ')
        self.ax.set_ylabel('Y ')
        self.ax.set_zlabel('Z ')
        self.draw()

class Info_Exchanger(QObject):

    def __init__(self):
        super().__init__()
    
    leaderactor = None
    pickedpoint = []
    switch = False

    # frame_axes 
    frame_axes = None

def main():
    
    script_mode = False 
    
    if script_mode == False:
        app = QApplication(sys.argv)
        window = AppForm()
        window.show()
        app.exec_()
    
    if script_mode == True: 
        render_script_mode('journal.stat') 

if __name__ =='__main__':
    main()


