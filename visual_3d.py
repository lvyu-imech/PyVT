import math
import vtk

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
from matplotlib.figure import Figure
import matplotlib.cm as cm

# import plot


class AppForm(QMainWindow):
	elementChanged = pyqtSignal(int, int)
	def __init__(self, parent=None):
		super(AppForm, self).__init__()
		# QMainWindow.__init__(self, parent)
		self.setWindowTitle('3D View')
		self.create_main_frame()
		self.create_menu()
		# self.create_status_bar()
		self.Qe = 0


	def save_plot(self):
		file_choices = "PNG (*.png)|*.png"

		path, ext = QFileDialog.getSaveFileName(self,
												'Save file', '',
												file_choices)
		path = path.encode('utf-8')
		if not path[-4:] == file_choices[-4:].encode('utf-8'):
			path += file_choices[-4:].encode('utf-8')
		# print(path)
		w2if = vtk.vtkWindowToImageFilter()
		w2if.SetInput(self.vtkWidget)
		w2if.Update()
		if path:
			# self.canvas.print_figure(path.decode())
			writer = vtk.vtkPNGWriter
			writer.SetFileName(path.decode())
			writer.SetInputData(w2if.Getself.output())
			writer.Write()
			self.statusBar().showMessage('Saved to %s' % path, 2000)

	def load_file(self):
		file_name = filename.lower()
		global reader
		# Read the source file.
		if file_name.endswith(".vtk"):  # read all legacy vtk types

			# self.output can be:
			# PolyData, StructuredGrid, StructuredPoints, UnstructuredGrid, RectilinearGrid
			reader = vtk.vtkDataSetReader()
			reader.ReadAllScalarsOn()
			reader.ReadAllVectorsOn()
			reader.ReadAllTensorsOn()
			reader.ReadAllFieldsOn()
			reader.ReadAllNormalsOn()
			reader.ReadAllColorScalarsOn()

		elif file_name.endswith(".vtu"):  # read XML unstructuredGrid type
			reader = vtk.vtkXMLUnstructuredGridReader()

		elif file_name.endswith(".vts"):  # read XML structuerdGrid type
			reader = vtk.vtkXMLStructuredGridReader()

		reader.SetFileName(file_name)
		reader.Update()  # Needed because of GetScalarRange
		self.output = reader.GetOutput()
		self.setup()

		return reader,

	def setup(self):
		self.volume = vtkObject()
		self.volume.output = reader.GetOutput()
		self.volume.pointData = self.volume.output.GetPoint
		# print(self.volume.output)
		self.points = []
		self.volume.scalar_range = self.volume.output.GetScalarRange()
		self.volume.xmin, self.volume.xmax, self.volume.ymin, self.volume.ymax, self.volume.zmin, self.volume.zmax = self.output.GetBounds()
		for i in range(self.volume.output.GetNumberOfPoints()):
			self.points.append(self.volume.output.GetPoint(i))
			self.volume.x.append(self.volume.output.GetPoint(i)[0])
			self.volume.y.append(self.volume.output.GetPoint(i)[1])
			self.volume.z.append(self.volume.output.GetPoint(i)[2])

	def create_main_frame(self):
		self.main_frame = QFrame()
		self.main_frame.setFrameShape(QFrame.StyledPanel)
		self.left_frame = QFrame()
		self.left_frame.setFrameShape(QFrame.StyledPanel)
		self.canvas = myCanvas()
		self.canvas.background()

		# Create the navigation toolbar, tied to the canvas
		#
		self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

		# Other GUI controls
		#
		AddFile = QAction(QIcon('icons/images.png'), 'A', self)  #
		AddFile.setShortcut('Ctrl+N')
		AddFile.triggered.connect(self.browse_folder)

		self.plot3d = QAction(QIcon('icons/cupe_plan.PNG'), 'UnstructuredGrid', self)
		self.plot3d.setEnabled(1)
		self.plot3d.triggered.connect(self.plot)

		# self.sturctured = QAction(QIcon('icons/cupe.PNG'), 'StructuredGrid', self)
		# self.unstructured.setEnabled(1)
		# self.unstructured.triggered.connect(self.plot_structured)

		self.view_xy = QAction(QIcon('icons/x.png'), 'view XY plane', self)
		self.view_xy.setEnabled(1)
		self.view_xy.triggered.connect(self.xy_grid)

		self.view_yz = QAction(QIcon('icons/y.png'), 'view YZ plane', self)
		self.view_yz.setEnabled(1)
		self.view_yz.triggered.connect(self.yz_grid)

		self.view_xz = QAction(QIcon('icons/z.png'), 'view XZ plane', self)
		self.view_xz.setEnabled(1)
		self.view_xz.triggered.connect(self.xz_grid)

		self.toolbar = self.addToolBar('Add data file')
		self.toolbar.addAction(AddFile)

		self.slice = QAction(QIcon('icons/slice.png'), 'slice', self)
		self.slice.setEnabled(1)
		self.slice.triggered.connect(self.slicer)

		self.show_streamline = QAction(QIcon('icons/stremline.png'), 'show streamline', self)
		self.show_streamline.setEnabled(1)
		self.show_streamline.triggered.connect(self.stream_line)

		self.show_vector = QAction(QIcon('icons/vector_field.png'), 'show vector field', self)
		self.show_vector.setEnabled(1)
		self.show_vector.triggered.connect(self.vector_field)

		self.show_isoContour = QAction(QIcon('icons/isoContour.png'), 'show iso contour', self)
		self.show_isoContour.setEnabled(1)
		self.show_isoContour.triggered.connect(self.isoContour)

		# self.toolbar.addAction(self.unstructured)
		# self.toolbar.addAction(self.sturctured)
		self.toolbar.addAction(self.plot3d)
		self.toolbar.addAction(self.view_xy)
		self.toolbar.addAction(self.view_yz)
		self.toolbar.addAction(self.view_xz)
		# self.toolbar.addAction(self.slice)
		self.toolbar.addAction(self.show_streamline)
		self.toolbar.addAction(self.show_vector)
		self.toolbar.addAction(self.show_isoContour)

		# Layout
		#
		main_layout = QHBoxLayout()
		right_split = QVBoxLayout()
		left_split = QVBoxLayout()


		# left side widget
		self.styleChoice = QLabel("Choose color map")
		self.color_schem = QComboBox(self)
		self.color_schem.addItem("1")
		self.color_schem.addItem("2")
		self.color_schem.move(50, 250) # move to a specific position
		self.styleChoice.move(10, 150)
		# color_schem.activated[str].connect(self.style_choice)
		left_split.addWidget(self.color_schem)


		self.le = QLineEdit()
		self.btn = QPushButton("OK")
		self.btn.clicked.connect(self.getItem)
		self.values = ''
		self.leLabel = QLabel("Enter value from: " + self.values)
		left_split.addWidget(self.leLabel)
		left_split.addWidget(self.le)
		left_split.addWidget(self.btn)


		self.slider1 = QSlider(Qt.Horizontal)
		self.slider1.setObjectName("x_slider")
		self.slider1.sliderMoved.connect(self.sliders)
		self.lb1 = QLabel('x')
		self.lb1.setAlignment(Qt.AlignCenter)
		self.slider2 = QSlider(Qt.Horizontal)
		self.slider2.setObjectName("y_slider")
		self.slider2.sliderMoved.connect(self.sliders)
		self.lb2 = QLabel('y')
		self.lb2.setAlignment(Qt.AlignCenter)
		self.slider3 = QSlider(Qt.Horizontal)
		self.slider3.setObjectName("z_slider")
		self.slider3.sliderMoved.connect(self.sliders)
		self.lb3 = QLabel('z')
		self.lb3.setAlignment(Qt.AlignCenter)
		self.value_x, self.value_y, self.value_z = 0, 0, 0

		# left_split.addWidget(self.axes_to_slice)
		left_split.addStretch()
		left_split.addWidget(self.slider1)
		left_split.addWidget(self.lb1)
		left_split.addWidget(self.slider2)
		left_split.addWidget(self.lb2)
		left_split.addWidget(self.slider3)
		left_split.addWidget(self.lb3)
		# left_split.setStretch(0,1)
		# left_split.setStretch()
		main_layout.addLayout(left_split,1)


		self.vtkWidget = QVTKRenderWindowInteractor(self.main_frame)
		right_split.addWidget(self.vtkWidget)
		right_split.addWidget(self.mpl_toolbar)
		main_layout.addLayout(right_split,2)

		self.widget = QWidget()
		self.widget.setLayout(main_layout)
		self.widget.setFixedSize(720,560)
		self.setCentralWidget(self.widget)

	def getItem(self):
		self.item = float(self.le.text())

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
		# 	  shortcut='F1', slot=self.on_about,
		# 	  tip='About the demo')
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

	def browse_folder(self):
		global filename

		if self.Qe == 1:
			self.MessageSave()
		else:
			# options = QFileDialog.Options()
			# options |= QFileDialog.DontUseNativeDialog
			filename, _ = QFileDialog.getOpenFileName(self, "Open", "", "VTK Files (*.vtu *.vts *.vtk);;All Files (*)")
			# if filename:
			# 	self.listWidget.clear()
			# 	self.listWidget.addItem(filename)

	def plot(self):
		# colors = vtk.vtkNamedColors()
		self.load_file()
		print(self.output)
		scalar_range = self.output.GetScalarRange()

		# Create the color map
		self.colorLookupTable = vtk.vtkLookupTable()
		self.colorLookupTable.SetTableRange(min(scalar_range), max(scalar_range))
		self.colorLookupTable.Build()

		# Generate the colors for each point based on the color map
		colors = vtk.vtkUnsignedCharArray()
		colors.SetNumberOfComponents(3)
		colors.SetName("Colors")

		for i in range(0, self.output.GetNumberOfPoints()):
			p = 3 * [0.0]
			self.output.GetPoint(i, p)
			# print(p)

			dcolor = 3 * [0.0]
			self.colorLookupTable.GetColor(p[2], dcolor);
			# print("dcolor: "
			# 	  + str(dcolor[0]) + " "
			# 	  + str(dcolor[1]) + " "
			# 	  + str(dcolor[2]))
			color = 3 * [0.0]
			for j in range(0, 3):
				color[j] = int(255.0 * dcolor[j])

			# print("color: "
			# 	  + str(color[0]) + " "
			# 	  + str(color[1]) + " "
			# 	  + str(color[2]))
			try:
				colors.InsertNextTupleValue(color)
			except AttributeError:
				# For compatibility with new VTK generic data arrays.
				colors.InsertNextTypedTuple(color)

		# fileName = reader.GetFileName()
		# if fileName.endswith(".vtu") or fileName.endswith(".vts"):
		self.output.GetPointData().SetScalars(colors)

		# Create the mapper that corresponds the objects of the vtk.vtk file
		# into graphics elements
		volume_mapper = vtk.vtkDataSetMapper()
		volume_mapper.SetInputData(self.output)
		volume_mapper.SetScalarRange(scalar_range)
		# mapper.ScalarVisibilityOff()



		# Create the Actor
		self.volume_actor = vtk.vtkActor()
		self.volume_actor.SetMapper(volume_mapper)
		# actor.GetProperty().EdgeVisibilityOn()
		self.volume_actor.GetProperty().SetLineWidth(1.0)
		# actor.GetProperty().SetOpacity(0.3)

		# Create the Renderer
		self.renderer = vtk.vtkRenderer()
		self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
		self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

		# add cubeAxes to plot
		cubeAxesActor = vtk.vtkCubeAxesActor()
		cubeAxesActor.SetBounds(reader.GetOutput().GetBounds())
		cubeAxesActor.SetCamera(self.renderer.GetActiveCamera())
		cubeAxesActor.GetTitleTextProperty(0).SetColor(0.0, 0.0, 0.0)
		cubeAxesActor.GetLabelTextProperty(0).SetColor(0.0, 0.0, 0.0)

		cubeAxesActor.GetTitleTextProperty(1).SetColor(0.0, 0.0, 0.0)
		cubeAxesActor.GetLabelTextProperty(1).SetColor(0.0, 0.0, 0.0)

		cubeAxesActor.GetTitleTextProperty(2).SetColor(0.0, 0.0, 0.0)
		cubeAxesActor.GetLabelTextProperty(2).SetColor(0.0, 0.0, 0.0)

		cubeAxesActor.DrawXGridlinesOn()
		cubeAxesActor.GetXAxesLinesProperty().SetColor(1,0,0)
		cubeAxesActor.DrawYGridlinesOn()
		cubeAxesActor.GetYAxesLinesProperty().SetColor(0, 1, 0)
		cubeAxesActor.DrawZGridlinesOn()
		cubeAxesActor.GetZAxesLinesProperty().SetColor(0, 0, 1)
		if vtk.VTK_MAJOR_VERSION > 5:
			cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)

		cubeAxesActor.XAxisMinorTickVisibilityOff()
		cubeAxesActor.YAxisMinorTickVisibilityOff()
		cubeAxesActor.ZAxisMinorTickVisibilityOff()


		self.camera = vtk.vtkCamera()
		self.renderer.AddActor(self.volume_actor)
		self.renderer.ResetCamera()
		self.renderer.SetBackground(1, 1, 1)  # Set background to white
		self.renderer.AddActor(cubeAxesActor)

		self.slider1.setValue(0)
		self.slider2.setValue(0)
		self.slider3.setValue(0)
		self.iren.Initialize()
		self.iren.Start()

	# def color_map(self):


	def xy_grid(self):
		self.camera.SetPosition(1, 1, 1)
		self.camera.SetFocalPoint(1, 1, 0)
		self.renderer.SetActiveCamera(self.camera)
		self.renderer.ResetCamera()
		self.iren.Initialize()
		self.iren.Start()

	def yz_grid(self):
		self.camera.SetPosition(1, 1, 1)
		self.camera.SetFocalPoint(0, 1, 1)
		self.renderer.SetActiveCamera(self.camera)
		self.renderer.ResetCamera()
		self.iren.Initialize()
		self.iren.Start()

	def xz_grid(self):
		self.camera.SetPosition(1, 1, 1)
		self.camera.SetFocalPoint(1, 0, 1)
		self.renderer.SetActiveCamera(self.camera)
		self.renderer.ResetCamera()
		self.iren.Initialize()
		self.iren.Start()


	def value_change_slot(self, index):
		if self.sender() == self.slider1:
			self.value_x = self.volume.x[index]
			# print("list_slider x {} {}".format(index, self.value_x))
		elif self.sender() == self.slider2:
			self.value_y = self.volume.y[index]
			# print("list_slider y {} {}".format(index, self.value_y))
		elif self.sender() == self.slider3:
			self.value_z = self.volume.z[index]
			# print("list_slider z {} {}".format(index, self.value_z))
		self.iren.Render()

	def sliders(self):
		# print("yes here")
		self.slider1.setRange(0,len(self.volume.x)-1)
		self.slider1.setTracking(True)
		self.slider1.valueChanged.connect(self.value_change_slot)

		self.slider2.setRange(0,len(self.volume.y)-1)
		self.slider2.setTracking(True)
		self.slider2.valueChanged.connect(self.value_change_slot)

		self.slider3.setRange(0,len(self.volume.z)-1)
		self.slider3.setTracking(True)
		self.slider3.valueChanged.connect(self.value_change_slot)

		origin = (self.value_x, self.value_y, self.value_z)
		print("origin: ", origin)
		normal = (1,1,1)

		self.slicer(origin, normal)


	def slicer(self, origin, normal):		# try vtk.vtkImageReslice()
		# create a plane to cut,here it cuts in the XZ direction (xz normal=(1,0,0);XY =(0,0,1),YZ =(0,1,0)
		self.plane = vtk.vtkPlane()
		# if xz:
		# 	for i in range(int(self.xmin), int(self.xmax)):
		self.plane.SetOrigin(origin)
		# planes.append(plane)
		self.plane.SetNormal(normal)

		# create cutter
		self.cutter = vtk.vtkCutter()
		# for x in planes:
		self.cutter.SetCutFunction(self.plane)
		self.cutter.SetInputConnection(reader.GetOutputPort())
		self.cutter.Update()

		cutterMapper = vtk.vtkDataSetMapper()
		# cutterMapper.SetInputConnection(cutStrips.GetOutputPort())
		cutterMapper.SetInputConnection(self.cutter.GetOutputPort())

		min, max = self.cutter.GetOutput().GetScalarRange()
		min= "%6.2f" % min
		max = "%6.2f" % max
		print(self.cutter.GetOutput())
		# print(self.range)
		self.leLabel.setText("Enter value from: (" + str(min) + ', ' + str(max) + ')')

		# create plane actor
		self.planeActor = vtk.vtkActor()
		# planeActor.GetProperty().SetColor(1.0, 1, 0)
		self.planeActor.GetProperty().SetLineWidth(2)
		self.planeActor.SetMapper(cutterMapper)
		self.volume_actor.GetProperty().SetOpacity(0)

		self.renderer.AddActor(self.planeActor)
		self.iren.Render()
		self.iren.Initialize()
		self.cutter.Update()
		#print("sliced")

	def slicer2(self, origin, normal):
		reslice = vtk.vtkImageReslice()
		reslice.SetInputData(reader.GetOutput())
		reslice.SetOutputDimensionality(2)
		if isinstance(normal[0], np.ndarray):
			newaxis = np.divide(normal, self.mag(normal)[:, None])
		else:
			newaxis =  normal / self.mag(normal)
		pos = np.array(origin)
		initaxis = (0, 0, 1)
		crossvec = np.cross(initaxis, newaxis)
		angle = np.arccos(np.dot(initaxis, newaxis))
		T = vtk.vtkTransform()
		T.PostMultiply()
		T.RotateWXYZ(np.rad2deg(angle), crossvec)
		T.Translate(pos)
		M = T.GetMatrix()
		reslice.SetResliceAxes(M)
		reslice.SetInterpolationModeToLinear()
		reslice.Update()
		vslice = vtk.vtkImageDataGeometryFilter()
		vslice.SetInputData(reslice.GetOutput())
		vslice.Update()
		sliceMapper = vtk.vtkPolyDataMapper()
		sliceMapper.SetInputConnection(vslice.GetOutputPort())

		min, max = vslice.GetOutput().GetScalarRange()
		min = "%6.2f" % min
		max = "%6.2f" % max
		print(vslice.GetOutput())
		# print(self.range)
		self.leLabel.setText("Enter value from: (" + str(min) + str(max) + ')')

		self.sliceActor = vtk.vtkActor()
		self.sliceActor.SetMapper(sliceMapper)
		self.volume_actor.GetProperty().SetOpacity(0)

		self.renderer.AddActor(self.sliceActor)
		self.iren.Render()
		self.iren.Initialize()

	def mag(self, z):
		"""Get the magnitude of a vector."""
		if isinstance(z[0], np.ndarray):
			return np.array(list(map(np.linalg.norm, z)))
		else:
			return np.linalg.norm(z)

	def stream_line(self):
		scalarRange = [0.0, 0.0]
		maxTime = 0
		if reader.GetOutput().GetPointData().GetScalars():
			reader.GetOutput().GetPointData().GetScalars().GetRange(scalarRange)

		if reader.GetOutput().GetPointData().GetVectors():
			maxVelocity = reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
			maxTime = 4.0 * reader.GetOutput().GetLength() / maxVelocity

		line = vtk.vtkLineSource()
		line.SetResolution(39)
		rakeMapper = vtk.vtkPolyDataMapper()
		rakeMapper.SetInputConnection(line.GetOutputPort())
		rake = vtk.vtkActor()
		rake.SetMapper(rakeMapper)

		streamer = vtk.vtkStreamTracer()
		streamer.SetInputConnection(reader.GetOutputPort())
		streamer.SetSourceConnection(line.GetOutputPort())
		streamer.SetMaximumPropagation(maxTime)
		streamer.SetInitialIntegrationStep(.5)
		streamer.SetMinimumIntegrationStep(.1)
		streamer.SetIntegratorType(2)
		streamer.Update()

		mapStreamLines = vtk.vtkPolyDataMapper()
		mapStreamLines.SetInputConnection(streamer.GetOutputPort())
		mapStreamLines.SetScalarRange(scalarRange)

		streamActor = vtk.vtkActor()
		streamActor.SetMapper(mapStreamLines)

		self.renderer.AddActor(streamActor)
		self.renderer.AddActor(rake)
		self.iren.Initialize()
		self.iren.Start()
		print("showing vector field")

		'''
		vtkHedgeHog hhog
		   hhog SetInput [reader GetOutput]
		   hhog SetScaleFactor 0.001

		vtkPolyDataMapper hhogMapper
		   hhogMapper SetInput [hhog GetOutput]
		   hhogMapper SetLookupTable lut
		   hhogMapper ScalarVisibilityOn
		   eval hhogMapper SetScalarRange [[reader GetOutput] GetScalarRange]

		vtkActor hhogActor
		   hhogActor SetMapper hhogMapper
		'''

	def isoContour(self):
		'''
		vtkStructuredGridReader reader
		   reader SetFileName “Data/density.vtk”
		   reader Update

		vtkContourFilter iso
		   iso SetInputConnection [reader GetOutputPort]
		   iso SetValue 0 0.26

		vtkPolyDataMapper isoMapper
		   isoMapper SetInputConnection [iso GetOutputPort]
		   eval isoMapper SetScalarRange [[reader GetOutput] GetScalarRange]

		vtkActor isoActor
		   isoActor SetMapper isoMapper
		'''

		print(self.volume.scalar_range)

		iso = vtk.vtkContourFilter()
		iso.SetInputConnection(self.cutter.GetOutputPort())
		iso.SetValue(0, self.item)

		self.isoMapper = vtk.vtkPolyDataMapper()
		self.isoMapper.SetInputConnection(iso.GetOutputPort())

		isoActor = vtk.vtkActor()
		isoActor.SetMapper(self.isoMapper)
		isoActor.GetProperty().SetColor(1.0,1,0)

		self.renderer.AddActor(isoActor)
		self.iren.ReInitialize()
		self.iren.Start()


	def vector_field(self):
		'''
		vtkArrowSource arrow
		   arrow SetTipResolution 6
		   arrow SetTipRadius 0.1
		   arrow SetTipLength 0.35
		   arrow SetShaftResolution 6
		   arrow SetShaftRadius 0.03

		vtkGlyph3D glyph
		   glyph SetInput [reader GetOutputPort]
		   glyph SetSource [arrow GetOutputPort]
		   glyph SetVectorModeToUseVector
		   glyph SetColorModeToColorByScalar
		   glyph SetScaleModeToDataScalingOff
		   glyph OrientOn
		   glyph SetScaleFactor 0.2

		vtkPolyDataMapper glyphMapper
		   glyphMapper SetInput [glyph GetOutput]
		   glyphMapper SetLookupTable lut
		   glyphMapper ScalarVisibilityOn
		   eval glyphMapper SetScalarRange [[reader GetOutput] GetScalarRange]

		vtkActor glyphActor
		   glyphActor SetMapper contourMapper
		:return:
		'''
		arrow = vtk.vtkArrowSource()
		arrow.SetTipResolution(6)
		arrow.SetTipRadius(0.1)
		arrow.SetTipLength(0.35)
		arrow.SetShaftResolution(6)
		arrow.SetShaftRadius(0.03)

		glyph = vtk.vtkGlyph2D()
		glyph.SetInputConnection(self.cutter.GetOutputPort())
		glyph.SetSourceConnection(arrow.GetOutputPort())
		glyph.SetVectorModeToUseVector()
		glyph.SetColorModeToColorByScalar()
		glyph.SetScaleModeToDataScalingOff()
		glyph.OrientOn()
		glyph.SetScaleFactor(self.item)

		glyphMapper = vtk.vtkPolyDataMapper()
		glyphMapper.SetInputConnection(glyph.GetOutputPort())
		glyphMapper.SetLookupTable(self.colorLookupTable)
		glyphMapper.ScalarVisibilityOn()

		glyphActor = vtk.vtkActor()
		glyphActor.SetMapper(self.isoMapper)
		# glyphActor.GetProperty().SetColor(0.0,1,0)

		# hhog = vtk.vtkHedgeHog()
		# hhog.SetInputConnection(self.cutter.GetOutputPort())
		# hhog.SetScaleFactor(0.1)
		#
		# hhogMapper = vtk.vtkPolyDataMapper()
		# hhogMapper.SetInputConnection(hhog.GetOutputPort())
		# hhogMapper.ScalarVisibilityOn()
		#
		# hhogAector = vtk.vtkActor()
		# hhogAector.SetMapper(hhogMapper)

		self.renderer.AddActor(glyphActor)
		self.iren.ReInitialize()
		self.iren.Start()



class vtkObject():
	def __init__(self):
		self.output = None
		self.pointData = None
		self.scalar_range = None
		self.xmin = None
		self.xmax = None
		self.ymin = None
		self.ymax = None
		self.zmin = None
		self.zmax = None
		self.x, self.y, self.z = [], [], []


class myCanvas(FigureCanvas):

	def __init__(self):
		# Create the mpl Figure and FigCanvas objects.
		# 5x4 inches, 100 dots-per-inch
		#
		self.dpi = 100
		self.fig = Figure((5.0, 4.0), dpi=self.dpi)
		FigureCanvas.__init__(self, self.fig)

	def background(self):
		self.fig.clear()
		self.ax = self.fig.add_subplot(111, projection='3d')
		self.ax.mouse_init(rotate_btn=1, zoom_btn=3)
		# self.ax.plot(xarray, yarray, zarray, 'ok')
		self.ax.set_xlabel('X ')
		self.ax.set_ylabel('Y ')
		self.ax.set_zlabel('Z ')
		self.draw()


def main():
	app = QApplication(sys.argv)
	print('true')
	window = AppForm()
	window.show()
	app.exec_()

if __name__ =='__main__':
	main()


