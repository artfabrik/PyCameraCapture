import sys  
import os
import multicameracapture
from PySide import QtCore, QtGui
import subprocess

class Model(object):
	def __init__(self):
		self.cameras = []
	
	def updateCameras(self):
		cameras = []
		if os.name!="posix":
			os.chdir("C:\\gphoto2")
		#my_env = os.environ
		#my_env["CAMLIBS"] = "camlibs"
		#my_env["IOLIBS"] = "iolibs"
		#p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,env=env)
		p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		print out
		cam_string = False
		for line in out.splitlines():
 			print "test:", line.rstrip()
			if cam_string:
				print "THIS IS A CAM"
				cameras.append(line.rstrip())
			if line.rstrip() == '----------------------------------------------------------':
				cam_string = True
				print "NOW IT STARTS"
		return cameras
		
	def getCameras(self):
		self.cameras = self.updateCameras()
		return self.cameras

class ControlMainWindow(QtGui.QMainWindow):
	def __init__(self, model, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.model = model
		self.ui =  multicameracapture.Ui_MainWindow()
		self.ui.setupUi(self)
		self.setupEvents()
        
	def updateActiveCamTable(self):
		cameras = self.model.getCameras()
		tableModel = QtGui.QStandardItemModel(1, len(cameras), self.ui.tableView)
		for row, camera in enumerate(cameras):
			item = QtGui.QStandardItem(camera)
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			tableModel.setItem(row, 0, item)
		self.ui.tableView.setModel(tableModel)
	
	def setupEvents(self):
		self.ui.previewButton.clicked.connect(self.updateActiveCamTable)
		

if __name__ == '__main__':  
	print("Running in " + os.getcwd() + " .\n")
	app = QtGui.QApplication(sys.argv)  
	controller = ControlMainWindow(Model())
	controller.show()
	app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
			app, QtCore.SLOT("quit()"))
	app.exec_()
