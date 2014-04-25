import sys  
import gui
import model
from PySide import QtCore, QtGui

class ControlMainWindow(QtGui.QMainWindow):
	def __init__(self, model, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.model = model
		self.ui = gui.Ui_MainWindow()
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
	
	def download(self):
		self.model.captureAllCameraImages()
	
	def setupEvents(self):
		self.ui.previewButton.clicked.connect(self.updateActiveCamTable)
		self.ui.downloadButton.clicked.connect(self.download)

if __name__ == '__main__':  
	app = QtGui.QApplication(sys.argv)  
	controller = ControlMainWindow(model.Model())
	controller.show()
	app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
			app, QtCore.SLOT("quit()"))
	app.exec_()
