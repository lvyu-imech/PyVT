# wrapper for some useful vtk components
import math
import vtk

def create_featureedge_actor(inputdata):

    geometryFilter = vtk.vtkGeometryFilter()
    geometryFilter.SetInputData(inputdata)
    featureEdges = vtk.vtkFeatureEdges()
    featureEdges.SetInputConnection(geometryFilter.GetOutputPort())
    featureEdges.BoundaryEdgesOn()
    #featureEdges.FeatureEdgesOff()
    featureEdges.ManifoldEdgesOff()
    featureEdges.NonManifoldEdgesOff()
    featureEdges.SetColoring(False)
    featureEdges.Update()

    edgeMapper = vtk.vtkPolyDataMapper()
    edgeMapper.SetInputConnection(featureEdges.GetOutputPort())
    edgeMapper.ScalarVisibilityOff()

    FeatureActor = vtk.vtkActor()
    FeatureActor.SetMapper(edgeMapper)

    colors = vtk.vtkNamedColors()
    FeatureActor.GetProperty().SetColor(colors.GetColor3d("FireBrick"))

    return FeatureActor

def create_boundbox_actor(inputdata):

    outline = vtk.vtkOutlineFilter()
    ##outline = vtk.vtkStructuredGridOutlineFilter()
    outline.SetInputData(inputdata)

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    OutlineActor = vtk.vtkActor()
    OutlineActor.SetMapper(outlineMapper)
    OutlineActor.GetProperty().SetColor(0, 0, 0)

    return OutlineActor

def create_mesh_actor(inputdata):
 
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(inputdata)
    mapper.ScalarVisibilityOff()
                
    WireframeActor = vtk.vtkActor()
    WireframeActor.SetMapper(mapper)
    WireframeActor.GetProperty().SetRepresentationToWireframe()
    bgcolor = (0, 0, 0)
    WireframeActor.GetProperty().SetColor(bgcolor)
    #WireframeActor.GetProperty().SetColor(0, 0, 0)
    #WireframeActor.GetProperty().SetLineWidth(1.5)

    return WireframeActor

def create_orientaxes_actor():
                
    axes = vtk.vtkAxesActor()
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().ItalicOff()
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().BoldOff()
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().ShadowOff()
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(16)

    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().ItalicOff()
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().BoldOff()
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShadowOff()
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(16)

    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().ItalicOff()
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().BoldOff()
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0, 0, 0)
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShadowOff()
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(16)

    return axes

def create_colorbar_actor(colormap):

    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(colormap)

    scalar_bar.GetTitleTextProperty().ItalicOff()
    scalar_bar.GetTitleTextProperty().BoldOff()
    scalar_bar.GetTitleTextProperty().ShadowOff()
    scalar_bar.GetTitleTextProperty().SetColor(0, 0, 0)
    scalar_bar.GetTitleTextProperty().SetFontSize(16)
    scalar_bar.GetLabelTextProperty().ItalicOff()
    scalar_bar.GetLabelTextProperty().BoldOff()
    scalar_bar.GetLabelTextProperty().ShadowOff()
    scalar_bar.GetLabelTextProperty().SetColor(0, 0, 0)
    scalar_bar.GetLabelTextProperty().SetFontSize(16)
    scalar_bar.UnconstrainedFontSizeOn()
    scalar_bar.SetBarRatio(0.2)
    scalar_bar.SetTextPad(4)

    return scalar_bar

# iso-surface filter
def algo4isosurf(inputdata, scalarname, value):
        
    # create isosurf with given parameters
    iso = vtk.vtkContourFilter()
    iso.SetInputData(inputdata)
    iso.SetComputeScalars(True)
    iso.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS_THEN_CELLS, scalarname) 
    iso.SetNumberOfContours(len(value))
    for i in range(len(value)):
        iso.SetValue(i, value[i])

    iso.Update()

    return iso

# cutplane filter
def algo4cutplane(inputdata, og, nm, num_slices, offset):
    
    mag = math.sqrt(nm[0]*nm[0] + nm[1]*nm[1] + nm[2]*nm[2])

    cuttercombo = vtk.vtkAppendPolyData()
    for j in range(num_slices):
        normal = tuple([nm[i]/mag for i in range(3)])
        origin = tuple([og[i] + nm[i]*offset*float(j) for i in range(3)])
        
        # initialize plane
        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        
        # create cutter
        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        cutter.SetInputData(inputdata)
        cutter.Update()
        
        cuttercombo.AddInputConnection(cutter.GetOutputPort())

    return cuttercombo 
 
# streamline filter
def algo4streamline(inputdata, params):
    
    # set up seed source
    if params[0] == 'point':
        seedsource = vtk.vtkPointSource()
        seedsource.SetCenter(params[1])
        seedsource.SetRadius(params[2])
        seedsource.SetNumberOfPoints(params[3])
    elif params[0] == 'line':
        seedsource = vtk.vtkLineSource()
        seedsource.SetPoint1(params[4])
        seedsource.SetPoint2(params[5])
        seedsource.SetResolution(params[6])
    elif params[0] == 'plane':
        seedsource = vtk.vtkPlaneSource()
        seedsource.SetOrigin(params[7])
        seedsource.SetPoint1(params[8])
        seedsource.SetPoint2(params[9])
        seedsource.SetXResolution(params[10])
        seedsource.SetYResolution(params[11])
    else:
        print('something wrong in the setting parameterms')
        return
        
    # set up streamtracer
    integ = vtk.vtkRungeKutta4()
    stracer = vtk.vtkStreamTracer()
    stracer.SetInputData(inputdata)
    stracer.SetSourceConnection(seedsource.GetOutputPort())
    stracer.SetIntegrator(integ)
    if params[12] == 'forward':
        stracer.SetIntegrationDirectionToForward()
    elif params[12] == 'backward':
        stracer.SetIntegrationDirectionToBackward()
    elif params[12] == 'both':
        stracer.SetIntegrationDirectionToBoth()
    stracer.SetMaximumPropagation(params[13])
    stracer.SetInitialIntegrationStep(params[14])
    stracer.Update()
    
    return stracer

# vector field filter
def algo4vectorfield_wgfilter(inputdata, gfilter, flag, scalefactor, skipfactor):

    # arrow style 
    arrow = vtk.vtkArrowSource()
    arrow.SetTipResolution(24)
    #arrow.SetTipRadius(0.1)
    #arrow.SetTipLength(3.5)
    arrow.SetShaftResolution(24)
    #arrow.SetShaftRadius(0.03)

    glyph = vtk.vtkGlyph3D()
    skippointF = vtk.vtkMaskPoints()
    skippointF.SetOnRatio(skipfactor)
    if flag:
        skippointF.SetInputConnection(gfilter.GetOutputPort())
    else:
        skippointF.SetInputData(inputdata)
    skippointF.Update()

    glyph.SetInputConnection(skippointF.GetOutputPort())
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByVector()
    glyph.SetVectorModeToUseVector()
    glyph.SetColorModeToColorByScalar()
    glyph.SetScaleFactor(scalefactor)
    
    return glyph 

# vector field filter
def algo4vectorfield(inputdata, inputparams):

    geom_unit_params = inputparams[0]
    vectorname       = inputparams[1]
    scalefactor      = inputparams[2]
    skipfactor       = inputparams[3]

    # arrow style 
    arrow = vtk.vtkArrowSource()
    arrow.SetTipResolution(24)
    #arrow.SetTipRadius(0.1)
    #arrow.SetTipLength(3.5)
    arrow.SetShaftResolution(24)
    #arrow.SetShaftRadius(0.03)

    appendF = vtk.vtkAppendPolyData()
    have_listed_item = False
    if geom_unit_params[0] != None:
        og, nm, num_slices, offset = geom_unit_params[0]
        cutter = algo4cutplane(inputdata, og, nm, num_slices, offset)
        appendF.AddInputConnection(cutter.GetOutputPort())
        have_listed_item = True

    if geom_unit_params[1] != None:
        scalarname = geom_unit_params[1][0]
        values     = geom_unit_params[1][1]
        isosurf = algo4isosurf(inputdata, scalarname, values)
        appendF.AddInputConnection(isosurf.GetOutputPort())
        have_listed_item = True

    if geom_unit_params[2] != None:
        params = geom_unit_params[2]
        stracer = algo4streamline(inputdata, params)
        stracer.Update()
        stracer.GetOutput().GetPointData().SetActiveVectors(vectorname)
        appendF.AddInputConnection(stracer.GetOutputPort())
        have_listed_item = True

    glyph = vtk.vtkGlyph3D()
    skippointF = vtk.vtkMaskPoints()
    skippointF.SetOnRatio(skipfactor)
    if have_listed_item:
        skippointF.SetInputConnection(appendF.GetOutputPort())
    else:
        skippointF.SetInputData(inputdata)
    skippointF.Update()
    
    glyph.SetInputConnection(skippointF.GetOutputPort())
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByVector()
    glyph.SetVectorModeToUseVector()
    glyph.SetColorModeToColorByScalar()
    glyph.SetScaleFactor(scalefactor)

    return glyph

# define a colormap with given name
def define_colormap(colormapname, scalarbounds):

    # build a vtk lookup table
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    if colormapname == 'Set3':
        tableSize = 12
    elif colormapname == 'tab20':
        tableSize = 20
    else:
        tableSize = 256
                           
    from .src.colormap import color_map
                                      
    for i in range(tableSize):
        cv = color_map(i, colormapname)
        ctf.AddRGBPoint(float(i)/tableSize, cv[0], cv[1], cv[2])
                                              
    clut = vtk.vtkLookupTable()
    clut.SetTableRange(scalarbounds)
    clut.SetNumberOfTableValues(tableSize)
    clut.Build()
    
    for i in range(0, tableSize):
        rgb = list(ctf.GetColor(float(i) / tableSize)) + [1]
        clut.SetTableValue(i, rgb)

    return clut

# define an stand-alone mapper 
def define_standalone_mapper(opt, colormapname, scalar_range, relative_range):
    
    bounds = relative_range
    adj_bounds = (scalar_range[0] + float(bounds[0])/99.0 * (scalar_range[1] - scalar_range[0]), \
                  scalar_range[0] + float(bounds[1])/99.0 * (scalar_range[1] - scalar_range[0]), )
            
    if opt==0:
        mapper = vtk.vtkDataSetMapper()
    else:
        mapper = vtk.vtkPolyDataMapper()
                              
    # build a vtk lookup table
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    if colormapname == 'Set3':
        tableSize = 12
    elif colormapname == 'tab20':
        tableSize = 20
    else:
        tableSize = 256
                                  
    from .src.colormap import color_map
                                      
    for i in range(tableSize):
        cv = color_map(i, colormapname)
        ctf.AddRGBPoint(float(i)/tableSize, cv[0], cv[1], cv[2])
                                              
    clut = vtk.vtkLookupTable()
    clut.SetTableRange(adj_bounds)
    clut.SetNumberOfTableValues(tableSize)
    clut.Build()
                                              
    for i in range(0, tableSize):
        rgb = list(ctf.GetColor(float(i) / tableSize)) + [1]
        clut.SetTableValue(i, rgb)
    
    mapper.InterpolateScalarsBeforeMappingOn()
    mapper.SetLookupTable(clut)
    mapper.SetScalarRange(adj_bounds)

    return mapper

# scene module class
class Scene_Module():
    
    scalar_name = ''
    scalar_range = None
    relative_range = None
    opacity = 1
    colormap = ''
    cutplane = None
    cutplane_param = None
    isosurf = None
    isosurf_param = None
    streamline = None
    streamline_param = None
    vectorfield = None
    vectorfield_param = None
    geomcombine = None
    mapper     = None
    actor      = None
    
    def __init__(self):
        pass

    def write(self, fp):
        
        import json
        
        json.dump(self.scalar_name, fp);      fp.write('\n')
        json.dump(self.scalar_range, fp);     fp.write('\n')
        json.dump(self.relative_range, fp);   fp.write('\n')
        json.dump(self.opacity, fp);          fp.write('\n')
        json.dump(self.colormap, fp);         fp.write('\n')
        json.dump(self.cutplane_param, fp);   fp.write('\n')
        json.dump(self.isosurf_param, fp);    fp.write('\n')
        json.dump(self.streamline_param, fp); fp.write('\n')
        json.dump(self.vectorfield_param, fp);fp.write('\n')

    def render(self, input_data):
        
        appendF = vtk.vtkAppendPolyData()
        
        have_subset = False
        if self.cutplane_param != None: 
            have_subset = True 
            og, nm, numcut, offset = self.cutplane_param
            self.cutplane = algo4cutplane(input_data, og, nm, numcut, offset)
            appendF.AddInputConnection(self.cutplane.GetOutputPort())

        if self.isosurf_param != None:
            have_subset = True
            scalarname, values = self.isosurf_param
            self.isosurf = algo4isosurf(input_data, scalarname, values)
            appendF.AddInputConnection(self.isosurf.GetOutputPort())

        if self.streamline_param != None: 
            have_subset = True
            self.streamline = algo4streamline(input_data, self.streamline_param)
            appendF.AddInputConnection(self.streamline.GetOutputPort())

        if self.vectorfield_param != None:
            have_subset = True
            self.vectorfield = algo4vectorfield(input_data, self.vectorfield_param)
            appendF.AddInputConnection(self.vectorfield.GetOutputPort())

        if have_subset:
            self.mapper = define_standalone_mapper(2, self.colormap, self.scalar_range, self.relative_range)
            self.geomcombine = appendF
            self.geomcombine.Update()
            self.geomcombine.GetOutput().GetPointData().SetActiveScalars(self.scalar_name)
            self.mapper.SetInputConnection(self.geomcombine.GetOutputPort())
            self.mapper.StaticOn()
        else:
            self.mapper = define_standalone_mapper(0, self.colormap, self.scalar_range, self.relative_range)
            self.geomcombine = vtk.vtkPassThroughFilter()
            self.geomcombine.SetInputData(input_data)
            self.geomcombine.Update()
            self.geomcombine.GetOutput().GetPointData().SetActiveScalars(self.scalar_name)
            self.mapper.SetInputConnection(self.geomcombine.GetOutputPort())
            self.mapper.StaticOn()
        
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetOpacity(self.opacity)

    def load(self, fp):

        import json
        
        self.scalar_name = json.loads(fp.readline())
        self.scalar_range = json.loads(fp.readline())
        self.relative_range = json.loads(fp.readline())
        self.opacity = json.loads(fp.readline())
        self.colormap = json.loads(fp.readline())
        self.cutplane_param = json.loads(fp.readline())
        self.isosurf_param = json.loads(fp.readline())
        self.streamline_param = json.loads(fp.readline())
        self.vectorfield_param = json.loads(fp.readline())


# colormap legend
class Scene_Module_Legend():
   
    scalar_name = ' '
    scalar_range = None
    relative_range = None
    colormapname = ''

    title = ''
    orient = 0 
    numoflabels = 2
    position = []
    height = 0 
    width = 0

    actor = None

    def __init__(self):
        pass

    def write(self, fp):
        
        import json
        json.dump(self.scalar_name, fp); fp.write('\n')
        json.dump(self.scalar_range, fp); fp.write('\n')
        json.dump(self.relative_range, fp); fp.write('\n')
        json.dump(self.colormapname, fp); fp.write('\n')
        
        json.dump(self.title, fp); fp.write('\n')
        json.dump(self.orient, fp); fp.write('\n')
        json.dump(self.numoflabels, fp); fp.write('\n')
        json.dump(self.position, fp); fp.write('\n')
        json.dump(self.height, fp); fp.write('\n')
        json.dump(self.width, fp); fp.write('\n')
        

    def render(self):
        
        bounds = (self.scalar_range[0] + float(self.relative_range[0])/99.0 \
                                       * (self.scalar_range[1] - self.scalar_range[0]), \
                  self.scalar_range[0] + float(self.relative_range[1])/99.0 \
                                       * (self.scalar_range[1] - self.scalar_range[0]), )
        
        colormap   = define_colormap(self.colormapname, bounds)
        scalar_bar = create_colorbar_actor(colormap)
        scalar_bar.SetTitle(self.title)
        scalar_bar.SetOrientation(self.orient)
        scalar_bar.SetNumberOfLabels(self.numoflabels)
        scalar_bar.SetPosition(self.position)
        scalar_bar.SetWidth(self.width)
        scalar_bar.SetHeight(self.height)

        self.actor = scalar_bar

    def load(self, fp):
        
        import json
       
        self.scalar_name = json.loads(fp.readline())
        self.scalar_range = json.loads(fp.readline())
        self.relative_range = json.loads(fp.readline())
        self.colormapname = json.loads(fp.readline())
        
        self.title = json.loads(fp.readline())
        self.orient = json.loads(fp.readline())
        self.numoflabels = json.loads(fp.readline())
        self.position = json.loads(fp.readline())
        self.height = json.loads(fp.readline())
        self.width = json.loads(fp.readline())

# arrow for annotation 
class Scene_Module_Arrow(): 

    pointA = None 
    pointB = None
    actor  = None

    def __init__(self):
        pass

    def write(self, fp):
        
        import json
        
        json.dump(self.pointA, fp); fp.write('\n')
        json.dump(self.pointB, fp); fp.write('\n')
   
    def render(self):
     
        self.actor = vtk.vtkLeaderActor2D()
        self.actor.SetPosition(self.pointA)
        self.actor.SetPosition2(self.pointB)
        self.actor.SetArrowPlacementToPoint2()
        self.actor.SetMinimumArrowSize(25)
        self.actor.SetMaximumArrowSize(25)
        self.actor.GetProperty().SetColor(0, 0, 0)

    def load(self, fp):
        
        import json
        self.pointA = json.loads(fp.readline())
        self.pointB = json.loads(fp.readline())

# annotation text
class Scene_Module_Text(): 
    
    text = ''
    fontsize = 16
    position = [] 
    position2 = []
    actor = None

    def __init__(self):
        pass

    def write(self, fp):
        
        import json
        
        json.dump(self.text, fp);      fp.write('\n')
        json.dump(self.fontsize, fp);  fp.write('\n')
        json.dump(self.position, fp);  fp.write('\n')
        json.dump(self.position2, fp); fp.write('\n')
       
    def render(self):
        
        self.actor = vtk.vtkTextActor()
        self.actor.SetInput(self.text)
        self.actor.GetTextProperty().SetColor((0, 0, 0))
        self.actor.GetTextProperty().SetFontSize(self.fontsize)
        self.actor.SetPosition(self.position)
        self.actor.SetPosition2(self.position2)

    def load(self, fp):

        import json
        
        self.text      = json.loads(fp.readline())
        self.fontsize  = json.loads(fp.readline())
        self.position  = json.loads(fp.readline())
        self.position2 = json.loads(fp.readline())


    
class Scene_Module_FrameAxes():

    title_x = 'X'
    title_y = 'Y'
    title_z = 'Z'
    
    show_x  = True
    show_y  = True
    show_z  = True

    bounds_x = None
    bounds_y = None
    bounds_z = None
    
    noflabel_x = 4
    noflabel_y = 4
    noflabel_z = 4
    
    grid_on      = False
    font_factor  = 1.5
    label_factor = 0.6 
    offset       = 20 
    
    actor   = None 
    actor2D = None
    
    actor2D_x = vtk.vtkAxisActor2D() 
    actor2D_y = vtk.vtkAxisActor2D()
    actor2D_z = vtk.vtkAxisActor2D()
    
    exponent_x = 0 
    exponent_y = 0 
    exponent_z = 0 

    def __init__(self):
        pass
    
    def write(self, fp):
        import json
        
        json.dump(self.show_x, fp);      fp.write('\n')
        json.dump(self.show_y, fp);      fp.write('\n')
        json.dump(self.show_z, fp);      fp.write('\n')
        
        json.dump(self.title_x, fp);      fp.write('\n')
        json.dump(self.title_y, fp);      fp.write('\n')
        json.dump(self.title_z, fp);      fp.write('\n')
        
        json.dump(self.bounds_x, fp);     fp.write('\n')
        json.dump(self.bounds_y, fp);     fp.write('\n')
        json.dump(self.bounds_z, fp);     fp.write('\n')
         
        json.dump(self.noflabel_x, fp);   fp.write('\n')
        json.dump(self.noflabel_y, fp);   fp.write('\n')
        json.dump(self.noflabel_z, fp);   fp.write('\n')

        json.dump(self.exponent_x, fp);   fp.write('\n')
        json.dump(self.exponent_y, fp);   fp.write('\n')
        json.dump(self.exponent_z, fp);   fp.write('\n')
        
        json.dump(self.font_factor, fp);  fp.write('\n')
        json.dump(self.label_factor, fp); fp.write('\n')
        json.dump(self.offset, fp);       fp.write('\n')
        json.dump(self.grid_on, fp);      fp.write('\n')
    
    def load(self, fp):
        import json

        self.show_x = json.loads(fp.readline())
        self.show_y = json.loads(fp.readline())
        self.show_z = json.loads(fp.readline())
        
        self.title_x = json.loads(fp.readline())
        self.title_y = json.loads(fp.readline())
        self.title_z = json.loads(fp.readline())
        
        self.bounds_x = json.loads(fp.readline())
        self.bounds_y = json.loads(fp.readline())
        self.bounds_z = json.loads(fp.readline())
        
        self.noflabel_x = json.loads(fp.readline())
        self.noflabel_y = json.loads(fp.readline())
        self.noflabel_z = json.loads(fp.readline())
        
        self.exponent_x = json.loads(fp.readline())
        self.exponent_y = json.loads(fp.readline())
        self.exponent_z = json.loads(fp.readline())
        
        self.font_factor  = json.loads(fp.readline())
        self.label_factor = json.loads(fp.readline())
        self.offset   = json.loads(fp.readline())
        self.grid_on  = json.loads(fp.readline())
  
    def remove_grid(self, renderer): 
        if self.actor != None:
            renderer.RemoveActor(self.actor)

    def show_grid(self, renderer):
        if self.actor != None:
            bounds = (self.bounds_x[0], self.bounds_x[1], \
                      self.bounds_y[0], self.bounds_y[1], \
                      self.bounds_z[0], self.bounds_z[1] )
            self.actor.SetBounds(bounds)
            renderer.AddActor(self.actor) 
            return

        self.actor = vtk.vtkCubeAxesActor()
        self.actor.SetCamera(renderer.GetActiveCamera())
        bounds = (self.bounds_x[0], self.bounds_x[1], \
                  self.bounds_y[0], self.bounds_y[1], \
                  self.bounds_z[0], self.bounds_z[1] )
        self.actor.SetBounds(bounds)

        self.actor.SetFlyMode(0)
        self.actor.DrawXGridlinesOn()
        self.actor.DrawYGridlinesOn()
        self.actor.DrawZGridlinesOn()
        self.actor.GetXAxesGridlinesProperty().SetColor(0,0,0)
        self.actor.GetYAxesGridlinesProperty().SetColor(0,0,0)
        self.actor.GetZAxesGridlinesProperty().SetColor(0,0,0)

        self.actor.SetGridLineLocation(2)
        
        self.actor.XAxisVisibilityOff()
        self.actor.YAxisVisibilityOff() 
        self.actor.ZAxisVisibilityOff()
        self.actor.XAxisLabelVisibilityOff()
        self.actor.YAxisLabelVisibilityOff()
        self.actor.ZAxisLabelVisibilityOff()
        self.actor.XAxisTickVisibilityOff()
        self.actor.YAxisTickVisibilityOff()
        self.actor.ZAxisTickVisibilityOff()

        self.actor.SetXTitle('')
        self.actor.SetYTitle('')
        self.actor.SetZTitle('')

        renderer.AddActor(self.actor)

    def render2D(self, renderer, bounds): 
        
        self.actor2D = vtk.vtkCubeAxesActor2D()
        self.actor2D.SetCamera(renderer.GetActiveCamera())
        if bounds == None:
            bounds = (self.bounds_x[0], self.bounds_x[1], \
                      self.bounds_y[0], self.bounds_y[1], \
                      self.bounds_z[0], self.bounds_z[1] )
        self.actor2D.SetBounds(bounds)
        
        self.actor2D.SetXAxisVisibility(False)
        self.actor2D.SetYAxisVisibility(False)
        self.actor2D.SetZAxisVisibility(False)
        
        self.actor2D.SetFlyMode(0)
        #self.actor.GetXAxisActor2D().SetUseFontSizeFromProperty(True)
        #self.actor.GetXAxisActor2D().SetSizeFontRelativeToAxis(False)
        #self.actor.GetXAxisActor2D().UseFontSizeFromPropertyOn() 
        
        #self.actor.GetXAxisActor2D().SizeFontRelativeToAxisOff()
        #self.actor.SetSizeFontRelativeToAxis(False)

        self.actor2D.GetXAxisActor2D().SetLabelFactor(self.label_factor)
        self.actor2D.GetYAxisActor2D().SetLabelFactor(self.label_factor)
        self.actor2D.GetZAxisActor2D().SetLabelFactor(self.label_factor)
        self.actor2D.SetFontFactor(self.font_factor)        

        self.actor2D.GetXAxisActor2D().SetTickOffset(self.offset)
        self.actor2D.GetYAxisActor2D().SetTickOffset(self.offset)
        self.actor2D.GetZAxisActor2D().SetTickOffset(self.offset)
        
        self.actor2D.SetNumberOfLabels(4)
       
        self.actor2D.GetAxisTitleTextProperty().ItalicOff()
        self.actor2D.GetAxisTitleTextProperty().SetColor(0, 0, 0)
        self.actor2D.GetAxisTitleTextProperty().ShadowOff()
        self.actor2D.GetAxisTitleTextProperty().BoldOff()
        self.actor2D.GetAxisTitleTextProperty().SetFontFamilyToTimes()
       
        self.actor2D.GetAxisLabelTextProperty().ItalicOff()
        self.actor2D.GetAxisLabelTextProperty().SetColor(0, 0, 0)
        self.actor2D.GetAxisLabelTextProperty().ShadowOff()
        self.actor2D.GetAxisLabelTextProperty().BoldOff()
        self.actor2D.GetAxisLabelTextProperty().SetFontFamilyToArial()
        
        self.actor2D.GetProperty().SetColor(0, 0, 0) 

        self.actor2D.SetCornerOffset(0.0)
    
        renderer.AddActor2D(self.actor2D)
 
    def update(self, winsize):

        # update titles
        self.actor2D_x.SetTitle(self.title_x)
        self.actor2D_y.SetTitle(self.title_y)
        self.actor2D_z.SetTitle(self.title_z)
        
        # update bounds
        bounds = (self.bounds_x[0], self.bounds_x[1], \
                  self.bounds_y[0], self.bounds_y[1], \
                  self.bounds_z[0], self.bounds_z[1] )
        self.actor2D.SetBounds(bounds)
        
        # update positions of componental axes
        self.pos_update(winsize)

        # update no. of labels
        self.actor2D_x.SetNumberOfLabels(self.noflabel_x) 
        self.actor2D_y.SetNumberOfLabels(self.noflabel_y) 
        self.actor2D_z.SetNumberOfLabels(self.noflabel_z)
        
        # update offset
        self.actor2D_x.SetTickOffset(self.offset)
        self.actor2D_y.SetTickOffset(self.offset)
        self.actor2D_z.SetTickOffset(self.offset)
        
        # update font scaling factor
        self.actor2D_x.SetFontFactor(self.font_factor) 
        self.actor2D_y.SetFontFactor(self.font_factor) 
        self.actor2D_z.SetFontFactor(self.font_factor) 
        
        # update label scaling factor
        self.actor2D_x.SetLabelFactor(self.label_factor)
        self.actor2D_y.SetLabelFactor(self.label_factor)
        self.actor2D_z.SetLabelFactor(self.label_factor)
        
        self.pos_update(winsize) 
       
        self.actor2D_x.SetVisibility(self.show_x)
        self.actor2D_y.SetVisibility(self.show_y)
        self.actor2D_z.SetVisibility(self.show_z)
 
   #     self.actor2D_x.GetLabelTextProperty().SetFontSize(10)
   #     self.actor2D_y.GetLabelTextProperty().SetFontSize(10)
   #     self.actor2D_z.GetLabelTextProperty().SetFontSize(10)
   #     self.actor2D_x.GetTitleTextProperty().SetFontSize(20)
   #     self.actor2D_y.GetTitleTextProperty().SetFontSize(20)
   #     self.actor2D_z.GetTitleTextProperty().SetFontSize(20)
        
    def mock(self, renderer, winsize):

        if self.actor2D.GetXAxisActor2D().GetTitle() == 'X':
            self.actor2D_x.ShallowCopy(self.actor2D.GetXAxisActor2D())
        elif self.actor2D.GetYAxisActor2D().GetTitle() == 'X':
            self.actor2D_x.ShallowCopy(self.actor2D.GetYAxisActor2D())
        else: 
            self.actor2D_x.ShallowCopy(self.actor2D.GetZAxisActor2D())
        
        if self.actor2D.GetXAxisActor2D().GetTitle() == 'Y':
            self.actor2D_y.ShallowCopy(self.actor2D.GetXAxisActor2D())
        elif self.actor2D.GetYAxisActor2D().GetTitle() == 'Y':
            self.actor2D_y.ShallowCopy(self.actor2D.GetYAxisActor2D())
        else: 
            self.actor2D_y.ShallowCopy(self.actor2D.GetZAxisActor2D())
        
        if self.actor2D.GetXAxisActor2D().GetTitle() == 'Z':
            self.actor2D_z.ShallowCopy(self.actor2D.GetXAxisActor2D())
        elif self.actor2D.GetYAxisActor2D().GetTitle() == 'Z':
            self.actor2D_z.ShallowCopy(self.actor2D.GetYAxisActor2D())
        else: 
            self.actor2D_z.ShallowCopy(self.actor2D.GetZAxisActor2D())
    
        # update factor 
        #self.font_factor  = self.actor2D_z.GetFontFactor()
        #self.label_factor = self.actor2D_z.GetLabelFactor() 
        
        # update font scaling factor
        self.actor2D_x.SetFontFactor(self.font_factor) 
        self.actor2D_y.SetFontFactor(self.font_factor) 
        self.actor2D_z.SetFontFactor(self.font_factor) 
        
        # update label scaling factor
        self.actor2D_x.SetLabelFactor(self.label_factor)
        self.actor2D_y.SetLabelFactor(self.label_factor)
        self.actor2D_z.SetLabelFactor(self.label_factor)
        
        self.pos_update(winsize) 

        self.actor2D_x.SetAxisVisibility(True)
        self.actor2D_y.SetAxisVisibility(True)
        self.actor2D_z.SetAxisVisibility(True)
        
        # make axes actor unpickable
        self.actor2D.PickableOff()
        self.actor2D_x.PickableOff()
        self.actor2D_y.PickableOff()
        self.actor2D_z.PickableOff()
        
        renderer.AddActor2D(self.actor2D_x)
        renderer.AddActor2D(self.actor2D_y)
        renderer.AddActor2D(self.actor2D_z)

    def pos_update(self, winsize):
          
        pos1 = self.actor2D.GetXAxisActor2D().GetPosition() 
        pos2 = self.actor2D.GetXAxisActor2D().GetPosition2()
        rang = self.actor2D.GetXAxisActor2D().GetRange()

        if self.actor2D.GetXAxisActor2D().GetTitle() == 'X':
            self.actor2D_x.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_x.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_x.SetRange(rang) 
        elif self.actor2D.GetXAxisActor2D().GetTitle() == 'Y':
            self.actor2D_y.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_y.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_y.SetRange(rang) 
        else:
            self.actor2D_z.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_z.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_z.SetRange(rang) 

        pos1 = self.actor2D.GetYAxisActor2D().GetPosition()
        pos2 = self.actor2D.GetYAxisActor2D().GetPosition2()
        rang = self.actor2D.GetYAxisActor2D().GetRange()
        
        if self.actor2D.GetYAxisActor2D().GetTitle() == 'X':
            self.actor2D_x.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_x.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_x.SetRange(rang) 
        elif self.actor2D.GetYAxisActor2D().GetTitle() == 'Y':
            self.actor2D_y.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_y.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_y.SetRange(rang) 
        else:
            self.actor2D_z.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_z.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_z.SetRange(rang) 
        
        pos1 = self.actor2D.GetZAxisActor2D().GetPosition()
        pos2 = self.actor2D.GetZAxisActor2D().GetPosition2()
        rang = self.actor2D.GetZAxisActor2D().GetRange()
        
        if self.actor2D.GetZAxisActor2D().GetTitle() == 'X':
            self.actor2D_x.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_x.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_x.SetRange(rang) 
        elif self.actor2D.GetZAxisActor2D().GetTitle() == 'Y':
            self.actor2D_y.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_y.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_y.SetRange(rang) 
        else:
            self.actor2D_z.SetPosition( float(pos1[0])/float(winsize[0]), float(pos1[1])/float(winsize[1]))
            self.actor2D_z.SetPosition2(float(pos2[0])/float(winsize[0]), float(pos2[1])/float(winsize[1]))
            self.actor2D_z.SetRange(rang) 
        
# render an image for output with give actors/widgets
#def render_with_actor(actor_list, actor2D_list, text_list,  \
#                      arrow_list, legend_list,  frame_axes, orient_axes, \
#                      camera_params, file_name, winsize, scale=1): 
def render_with_actor(actor_list, actor2D_list, text_list,  \
                      arrow_list, legend_list,  frame_axes, orient_axes, \
                      mycamera, file_name, winsize, scale=1): 

    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    #camera = vtk.vtkCamera()
    #camera.SetPosition(camera_params[0])
    #camera.SetFocalPoint(camera_params[1])
    #camera.SetViewUp(camera_params[2])
    #camera.SetViewAngle(camera_params[3])
    
    #ren.SetActiveCamera(camera)
    ren.SetActiveCamera(mycamera)
     
    renWin = vtk.vtkRenderWindow()
    #renWin.SetOffScreenRendering(True)
    renWin.AddRenderer(ren)
    renWin.SetSize(winsize[0]*scale, winsize[1]*scale)

    # create a renderwindowinteractor
    #iren = vtk.vtkRenderWindowInteractor()
    #iren.SetRenderWindow(renWin)
 
    for item in actor_list:
        ren.AddActor(item)

    for item in actor2D_list:
        ren.AddActor2D(item)

    for item in text_list:
        item.actor.GetTextProperty().SetFontSize(item.actor.GetTextProperty().GetFontSize() * scale) 
        pos = item.actor.GetPosition()
        item.actor.SetPosition(pos[0]*scale, pos[1]*scale)
        pos = item.actor.GetPosition2()
        item.actor.SetPosition2(pos[0]*scale, pos[1]*scale)
        ren.AddActor2D(item.actor)
    
    for arrow in arrow_list:
        arrow.actor.SetMinimumArrowSize(25*scale)
        arrow.actor.SetMaximumArrowSize(25*scale)
        linewidth  = arrow.actor.GetProperty().GetLineWidth()
        arrow.actor.GetProperty().SetLineWidth(linewidth*scale)
        ren.AddActor2D(arrow.actor)
    
    legend_fontsize_list = []
    for legend in legend_list:
        fontsize = legend.actor.GetTitleTextProperty().GetFontSize()
        legend.actor.GetTitleTextProperty().SetFontSize(fontsize * scale) 
        fontsiz  = legend.actor.GetLabelTextProperty().GetFontSize()
        legend.actor.GetLabelTextProperty().SetFontSize(fontsiz  * scale) 
        ren.AddActor2D(legend.actor)

        legend_fontsize_list.append((fontsize, fontsiz))
    
    if frame_axes.actor2D != None:
    #    cubeAxesActor = vtk.vtkCubeAxesActor()
    #    bounds = (frame_axes.bounds_x[0], frame_axes.bounds_x[1], \
    #              frame_axes.bounds_y[0], frame_axes.bounds_y[1], \
    #              frame_axes.bounds_z[0], frame_axes.bounds_z[1] )

    #    cubeAxesActor.SetBounds(bounds)
    #    cubeAxesActor.SetCamera(camera)
    #    cubeAxesActor.SetFlyMode(0)

    #    cubeAxesActor.GetTitleTextProperty(0).SetColor(0, 0, 0)
    #    cubeAxesActor.GetTitleTextProperty(0).SetFontFamilyToTimes()
    #    cubeAxesActor.GetLabelTextProperty(0).SetColor(0, 0, 0 )
    #    cubeAxesActor.GetLabelTextProperty(0).SetFontFamilyToTimes()
    #    cubeAxesActor.GetTitleTextProperty(0).SetFontSize(20)
    #    cubeAxesActor.GetLabelTextProperty(0).SetFontSize(20)
    #    
    #    cubeAxesActor.GetTitleTextProperty(1).SetColor(0, 0, 0)
    #    cubeAxesActor.GetTitleTextProperty(1).SetFontFamilyToTimes()
    #    cubeAxesActor.GetLabelTextProperty(1).SetColor(0, 0, 0 )
    #    cubeAxesActor.GetLabelTextProperty(1).SetFontFamilyToTimes()
    #    cubeAxesActor.GetTitleTextProperty(1).SetFontSize(20)
    #    cubeAxesActor.GetLabelTextProperty(1).SetFontSize(20)
    #    
    #    cubeAxesActor.GetTitleTextProperty(2).SetColor(0, 0, 0)
    #    cubeAxesActor.GetTitleTextProperty(2).SetFontFamilyToTimes()
    #    cubeAxesActor.GetLabelTextProperty(2).SetColor(0, 0, 0 )
    #    cubeAxesActor.GetLabelTextProperty(2).SetFontFamilyToTimes()
    #    cubeAxesActor.GetTitleTextProperty(2).SetFontSize(20)
    #    cubeAxesActor.GetLabelTextProperty(2).SetFontSize(20)

    #    cubeAxesActor.GetXAxesLinesProperty().SetColor(0, 0, 0)
    #    cubeAxesActor.GetYAxesLinesProperty().SetColor(0, 0, 0)
    #    cubeAxesActor.GetZAxesLinesProperty().SetColor(0, 0, 0)
    #    cubeAxesActor.GetXAxesGridlinesProperty().SetColor(0, 0, 0 )
    #    cubeAxesActor.GetYAxesGridlinesProperty().SetColor(0, 0, 0 )
    #    cubeAxesActor.GetZAxesGridlinesProperty().SetColor(0, 0, 0 )
    #    cubeAxesActor.XAxisMinorTickVisibilityOff()
    #    cubeAxesActor.YAxisMinorTickVisibilityOff()
    #    cubeAxesActor.ZAxisMinorTickVisibilityOff()
    #    
    #    cubeAxesActor.SetScreenSize(20) 
    #    cubeAxesActor.SetLabelOffset(18)
    #    cubeAxesActor.SetTitleOffset(18)

    #    ren.AddActor(cubeAxesActor)
     
        offset = frame_axes.actor2D_x.GetTickOffset()
        if frame_axes.show_x:
            frame_axes.actor2D_x.SetTickOffset(offset*scale)
            ren.AddActor2D(frame_axes.actor2D_x)
        if frame_axes.show_y:
            frame_axes.actor2D_y.SetTickOffset(offset*scale)
            ren.AddActor2D(frame_axes.actor2D_y)
        if frame_axes.show_z:
            frame_axes.actor2D_z.SetTickOffset(offset*scale)
            ren.AddActor2D(frame_axes.actor2D_z)
        if frame_axes.grid_on:
            ren.AddActor(frame_axes.actor)
    
    if orient_axes.GetEnabled():
        rgba = [0] * 4
        colors = vtk.vtkNamedColors()
        colors.GetColor("Carrot", rgba)
        orient_axes_widget = vtk.vtkOrientationMarkerWidget()
        orient_axes_widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        orient_axes_widget.SetOrientationMarker(orient_axes.GetOrientationMarker())
        orient_axes_widget.SetViewport(orient_axes.GetViewport())
        orient_axes_widget.SetInteractor(iren)
        orient_axes_widget.On()

    renWin.Render()
    
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.Update()

    # Read the data file.
    if file_name.lower().endswith(".png"):
        writer = vtk.vtkPNGWriter()
    elif file_name.lower().endswith(".jpg"):
        writer = vtk.vtkJPEGWriter()
    elif file_name.endswith(".eps"):
        writer = vtk.vtkPostScriptWriter()
    elif file_name.endswith(".bmp"):
        writer = vtk.vtkBMPWriter()
    elif file_name.endswith(".tiff"):
        writer = vtk.vtkTIFFWriter()
    else:
        print('image file not support~')
        return
    
    writer.SetFileName(file_name)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()

    # revert the settings for some actors
    for item in text_list:
        item.actor.GetTextProperty().SetFontSize(int(item.actor.GetTextProperty().GetFontSize()/scale))
        pos = item.actor.GetPosition()
        item.actor.SetPosition(pos[0]/scale, pos[1]/scale)
        pos = item.actor.GetPosition2()
        item.actor.SetPosition2(pos[0]/scale, pos[1]/scale)

    for arrow in arrow_list:
        arrow.actor.SetMinimumArrowSize(25)
        arrow.actor.SetMaximumArrowSize(25)
        linewidth  = arrow.actor.GetProperty().GetLineWidth()
        arrow.actor.GetProperty().SetLineWidth(linewidth/scale)

    for i in range(len(legend_list)): 
        legend = legend_list[i] 
        fontsize, fontsiz = legend_fontsize_list[i]
        
        legend.actor.GetTitleTextProperty().SetFontSize(fontsize)
        legend.actor.GetLabelTextProperty().SetFontSize(fontsiz )
    
    if frame_axes.actor2D != None:
        offset = frame_axes.actor2D_x.GetTickOffset()
        if frame_axes.show_x:
            frame_axes.actor2D_x.SetTickOffset(int(offset/scale))
            ren.AddActor2D(frame_axes.actor2D_x)
        if frame_axes.show_y:
            frame_axes.actor2D_y.SetTickOffset(int(offset/scale))
            ren.AddActor2D(frame_axes.actor2D_y)
        if frame_axes.show_z:
            frame_axes.actor2D_z.SetTickOffset(int(offset/scale))
            ren.AddActor2D(frame_axes.actor2D_z)


# load data and directly write out image file 
def render_script_mode(journal_file):
   
    import numpy as np
    from vtk.util import numpy_support as VN

    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    camera = vtk.vtkCamera()
    ren.SetActiveCamera(camera)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetOffScreenRendering(True)

    # create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
 
    fp = open(journal_file, 'r') 

    import json
    
    filename = json.loads(fp.readline())


    # load data
    from .myio.data_reader import read_input_file

    output = read_input_file(filename)

    # basic data processing
    num_array = output.GetPointData().GetNumberOfArrays()
    scalarnamelist = []
    vectornamelist = []

    name_append = ['x', 'y', 'z']
    for i in range(num_array):
        varname = output.GetPointData().GetArrayName(i)
        darray = VN.vtk_to_numpy(output.GetPointData().GetArray(varname))

        if darray.ndim == 2:
            if darray.shape[1] == 3:
                vectornamelist.append(varname)
                for i in range(3):
                    comps = VN.numpy_to_vtk(darray[:, i])
                    comps.SetName(varname + '_' + name_append[i])

                    output.GetPointData().AddArray(comps)
                    scalarnamelist.append(comps.GetName())
        else:
            scalarnamelist.append(varname)

    output.GetPointData().SetActiveScalars(None)
    
    # process defined scalars
    scalar_formula_list = json.loads(fp.readline())
    defined_scalar_list = json.loads(fp.readline())

    from .src.eqn_parser import DataTabular, interpret

    dt = DataTabular()
    nscalar = len(scalarnamelist)
    for index in range(nscalar):
        name = 'scalar_' + str(index+1)
        dt.add_name(name)
        dt.add_array(VN.vtk_to_numpy(output.GetPointData().GetArray(scalarnamelist[index])))

    for index in range(len(scalar_formula_list)):
        formula = scalar_formula_list[index]
        tecarray = VN.numpy_to_vtk(interpret(formula, dt)) 
        tecarray.SetName(defined_scalar_list[index])
        output.GetPointData().AddArray(tecarray)
     
        name ='scalar_' + str(nscalar+1+index)
        dt.add_name(name)
        dt.add_array(VN.vtk_to_numpy(output.GetPointData().GetArray(defined_scalar_list[index])))

        scalarnamelist.append(defined_scalar_list[index])

    # process defined vectors
    vector_component_list = json.loads(fp.readline())
    defined_vector_list   = json.loads(fp.readline())

    for index in range(len(defined_vector_list)):

        vector_name = defined_vector_list[index]
        uvel = VN.vtk_to_numpy(output.GetPointData().GetArray(vector_component_list[index][0]))
        vvel = VN.vtk_to_numpy(output.GetPointData().GetArray(vector_component_list[index][1]))
        wvel = VN.vtk_to_numpy(output.GetPointData().GetArray(vector_component_list[index][2]))

        udf_vector = np.stack((uvel, vvel, wvel), axis=1)
        varray = VN.numpy_to_vtk(udf_vector)
        varray.SetName(vector_name)
        output.GetPointData().AddArray(varray)
        output.GetPointData().SetActiveVectors(vector_name)
   
    module_list = []
    numofmodule = json.loads(fp.readline())
    for i in range(numofmodule):
        item = Scene_Module()
        item.load(fp)
        item.render(output)
        ren.AddActor(item.actor)
        module_list.append(item)

        size = len(module_list)
        name = 'module_' + str(size)
   
    text_list = []
    numofannota = json.loads(fp.readline())
    for i in range(numofannota):
        item = Scene_Module_Text()
        item.load(fp)
        item.render()
        ren.AddActor2D(item.actor)
        text_list.append(item)

    arrow_list = [] 
    numofarrow  = json.loads(fp.readline())
    for i in range(numofarrow):
        item = Scene_Module_Arrow()
        item.load(fp)
        item.render()
        ren.AddActor2D(item.actor)
        arrow_list.append(item)
   
    legend_list = []
    numoflegend = json.loads(fp.readline())
    for i in range(numoflegend):
        item = Scene_Module_Legend()
        item.load(fp)
        item.render()
        ren.AddActor2D(item.actor)
        legend_list.append(item)

    mainframe_width = json.loads(fp.readline())
    mainframe_height = json.loads(fp.readline())
   
    canvas_width = json.loads(fp.readline())
    canvas_height = json.loads(fp.readline())
    renWin.SetSize(canvas_width, canvas_height)
   
    camera.SetPosition(json.loads(fp.readline()))
    camera.SetFocalPoint(json.loads(fp.readline()))
    camera.SetViewUp(json.loads(fp.readline()))
    camera.SetViewAngle(json.loads(fp.readline()))
    ren.ResetCamera()

    renWin.Render()
   
    # check if orientation axis is on
    flag = json.loads(fp.readline())
    if flag == True:
        AxesActor = create_orientaxes_actor()
        rgba = [0] * 4
        colors = vtk.vtkNamedColors()
        colors.GetColor("Carrot", rgba)
        orient_axes_widget = vtk.vtkOrientationMarkerWidget()
        orient_axes_widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        orient_axes_widget.SetOrientationMarker(AxesActor)
        orient_axes_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
        orient_axes_widget.SetInteractor(iren)
        orient_axes_widget.On()
    
    # check if domain outline is on
    flag = json.loads(fp.readline())
    if flag == True:
        FeatureActor = create_featureedge_actor(output)
        ren.AddActor(FeatureActor)

    # check if bounding box is on
    flag = json.loads(fp.readline())
    if flag == True:
        OutlineActor = create_boundbox_actor(output)
        ren.AddActor(OutlineActor)

    # check if mesh is on
    flag = json.loads(fp.readline())
    if flag == True:
        WireframeActor = create_mesh_actor(output)
        ren.AddActor(WireframeActor)

    # check if background color is changed
    flag = json.loads(fp.readline())
    if flag == True:
        colors = vtk.vtkNamedColors()
        ren.SetBackground(colors.GetColor3d("SlateGray"))
    else:
        ren.SetBackground(1, 1, 1)

    # write out image file
    
    # pre-processing to ensure fontsize/position consistency
    amply_factor = 3 
    
    for item in text_list:
        item.actor.GetTextProperty().SetFontSize(item.actor.GetTextProperty().GetFontSize() * amply_factor)
        pos = item.actor.GetPosition()
        item.actor.SetPosition(pos[0]*amply_factor, pos[1]*amply_factor)
        pos = item.actor.GetPosition2()
        item.actor.SetPosition2(pos[0]*amply_factor, pos[1]*amply_factor)

    for arrow in arrow_list:
        arrow.actor.SetMinimumArrowSize(75)
        arrow.actor.SetMaximumArrowSize(75)
        linewidth  = arrow.actor.GetProperty().GetLineWidth()
        arrow.actor.GetProperty().SetLineWidth(linewidth*amply_factor)

    for legend in legend_list:
        fontsize = legend.actor.GetTitleTextProperty().GetFontSize()
        legend.actor.GetTitleTextProperty().SetFontSize(fontsize * amply_factor)
        fontsize = legend.actor.GetLabelTextProperty().GetFontSize()
        legend.actor.GetLabelTextProperty().SetFontSize(fontsize * amply_factor)

    renWin.Render()

    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    #w2if.SetScale(amply_factor) 
    w2if.Update()

    #writer = vtk.vtkPostScriptWriter()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName('test_figg.png')
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()
    
    #iren.Initialize()
    #iren.Start()

    # check if background color is changed
    #flag = json.loads(fp.readline())
    #if flag == True:
    #    colors = vtk.vtkNamedColors()
    #    renderer.SetBackground(colors.GetColor3d("SlateGray"))
    #else:
    #    renderer.SetBackground(1, 1, 1)
 

    fp.close()

