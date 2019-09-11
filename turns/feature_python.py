import FreeCADGui as Gui
import FreeCAD as App


class FeaturePython:
    ''' basic defs'''

    def __init__(self, obj):

        obj.Proxy = self
        self.Object = obj

    def attach(self, vobj):
        self.Object = vobj.Object

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class ViewProvider:
    ''' basic defs '''

    def __init__(self, obj):

        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def setupContextMenu(self, obj, menu):

        menu.clear()

        action = menu.addAction("simulate track")
        action.triggered.connect(lambda:self.methodA(obj.Object))
        action = menu.addAction("MyMethod #2")

        menu.addSeparator()

        action.triggered.connect(lambda:self.methodB(obj.Object))
        action = menu.addAction("Edit Sketch")
        action.triggered.connect(lambda:self.myedit(obj.Object))

    def myedit(self,obj):

        self.methodB(None)

        Gui.activeDocument().setEdit(obj.Name)

        self.methodA(None)

    def methodA(self,obj):

        print ("Method A",obj.Label)

        _step_size = 2

        if not obj.trailerOn:

            for s in range(obj.beginSegment, obj.endSegment + 1):

                obj.step = s
                a = App.ActiveDocument.recompute()

                if s % _step_size == 0:
                    Gui.updateGui()

            App.activeDocument().recompute()

        else:

            obj.truck.step = obj.truck.beginSegment

            for _s in range(obj.truck.beginSegment, obj.truck.endSegment + 1):

                obj.truck.step = _s + 1
                obj.step = _s
                a = App.ActiveDocument.recompute()

                if obj.error:

                    print ("fbs error -- break")
                    break

                if _s % _step_size == 0:
                    Gui.updateGui()

            App.activeDocument().recompute()

        Gui.updateGui()
        App.activeDocument().recompute()

    def methodB(self,obj):

        print ("my method B Starter")
        App.activeDocument().recompute()

    def methodC(self,obj):

        print ("my method C After Edit finished")
        #Gui.activateWorkbench("NurbsWorkbench")
        App.activeDocument().recompute()

    def unsetEdit(self,vobj,mode=0):
        self.methodC(None)

    def doubleClicked(self,vobj):

        print ("double clicked")
        self.myedit(vobj.Object)
