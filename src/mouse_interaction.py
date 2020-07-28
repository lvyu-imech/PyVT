from __future__ import print_function
import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, renWin, ren, communicator, parent=None):
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent",self.leftButtonReleaseEvent)
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)
        self.AddObserver("MouseMoveEvent", self.mymousemoveEvent)
        self.AddObserver('KeyPressEvent', self.OnKeyPress)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()
        #self.iren = iren
        self.comm = communicator
        self.ren = ren
        self.renWin = renWin
        self.chosenpiece = None
        self.proppicker = vtk.vtkPropPicker()
        self.pointpicker = vtk.vtkPointPicker()

        self.leftbuttondown = False
        #self.camera = self.ren.GetActiveCamera()
        #self.iren.SetInteractorStyle(None)
        #self.lastX, self.lastY = self.iren.GetLastEventPosition()
        #self.x, self.y = self.iren.GetEventPosition()

    def mymousemoveEvent(self, obj, event):
        
        if self.leftbuttondown:
            if self.comm.frame_axes != None and self.comm.frame_axes.actor2D != None:
             
                winsize = self.GetInteractor().GetRenderWindow().GetSize()
                self.comm.frame_axes.pos_update(winsize)
        
        self.OnMouseMove()

        return 

    def OnKeyPress(self, obj, event):
        key = self.GetInteractor().GetKeySym()

        if key == 'd':
            if self.chosenpiece is not None:

                self.ren.RemoveActor2D(self.chosenpiece)
                self.renWin.Render()

        vtk.vtkInteractorStyleTrackballCamera.OnKeyPress(self)

    def leftButtonPressEvent(self,obj,event):   # rotate
        
        self.leftbuttondown = True
        clickPos = self.GetInteractor().GetEventPosition()
        self.proppicker.Pick(clickPos[0], clickPos[1], 0, self.ren)
        
        self.chosenpiece = self.proppicker.GetActor2D()
    
        if self.comm.switch == True:
            winsize = self.GetInteractor().GetRenderWindow().GetSize()
            self.comm.pickedpoint.append([clickPos[0]/winsize[0], clickPos[1]/winsize[1]])

            if len(self.comm.pickedpoint) == 2:
                if self.comm.leaderactor in self.ren.GetActors2D():
                    self.ren.RemoveActor2D(self.comm.leaderactor)

                self.comm.leaderactor = vtk.vtkLeaderActor2D()
                self.comm.leaderactor.SetPosition(self.comm.pickedpoint[0])
                self.comm.leaderactor.SetPosition2(self.comm.pickedpoint[1])
                self.comm.leaderactor.SetArrowPlacementToPoint2()
                self.comm.leaderactor.SetMinimumArrowSize(25)
                self.comm.leaderactor.SetMaximumArrowSize(25)
                self.comm.leaderactor.GetProperty().SetColor(0, 0, 0)
                 
                self.comm.pickedpoint = []
                self.ren.AddActor2D(self.comm.leaderactor)
                self.renWin.Render()
        
        self.OnLeftButtonDown()
        return

    def leftButtonReleaseEvent(self,obj,event):
        
        self.chosenpiece = None
        self.leftbuttondown = False 
        
        self.OnLeftButtonUp()
        return

    def rightButtonPressEvent(self,obj,event):
        self.OnMiddleButtonDown()
        return

    def rightButtonReleaseEvent(self, obj, event):
        self.OnMiddleButtonUp()
        return

    def middleButtonPressEvent(self,obj,event):
        self.OnRightButtonDown()
        return

    def middleButtonReleaseEvent(self,obj,event):
        self.OnRightButtonUp()
        return
