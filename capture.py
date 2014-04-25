import sys  
import os
import multicameracapture
from PySide import QtCore, QtGui
import subprocess

class Model(object):
	def __init__(self):
		self.cameras = []
		if os.name!="posix":
			os.chdir("C:\\gphoto2")
			win_env = os.environ
			win_env["CAMLIBS"] = "camlibs"
			win_env["IOLIBS"] = "iolibs"
	
	def updateCameras(self):
		cameras = []
		
		#p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,env=env)
		if os.name!="posix":
			p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			p = subprocess.Popen(['gphoto2.exe', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		out, err = p.communicate()
		print out
		cam_string = False
		for line in out.splitlines():
 			print "test:", line.rstrip()
			if cam_string:
				print "THIS IS A CAM"
				
				camera = (
					line.split("usb:")[0].rstrip(),
					"usb:"+line.split("usb:")[1].rstrip()
				)
				
				#print(camera);
				
				cameras.append(camera)
			if line.rstrip() == '----------------------------------------------------------':
				cam_string = True
				print "NOW IT STARTS"
		return cameras
	
	def captureAllCameraImages(self):
		for camera in self.cameras:
			print(camera)
			self.captureCameraImage(camera[1])
		
	def captureCameraImage(self, port):
		if os.name=="posix":
			print("IS POSIX")
			p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			p = subprocess.Popen(['gphoto2.exe', '--capture-image-and-download', '--port', port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print p.communicate()
	
	def getCameras(self):
		self.cameras = self.updateCameras()
		self.captureAllCameraImages()
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
		tableModel = QtGui.QStandardItemModel(2, len(cameras), self.ui.tableView)
		for row, camera in enumerate(cameras):
			itemName = QtGui.QStandardItem(camera[0])
			itemName.setTextAlignment(QtCore.Qt.AlignCenter)
			tableModel.setItem(row, 0, itemName)
			
			itemPort = QtGui.QStandardItem(camera[1])
			itemPort.setTextAlignment(QtCore.Qt.AlignCenter)
			tableModel.setItem(row, 1, itemPort)
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
