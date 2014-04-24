# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Sewa\Desktop\untitled.ui'
#
# Created: Mon Apr 21 18:01:08 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import subprocess
from PySide import QtCore, QtGui
import os

print os.name

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(80, 70, 641, 401))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 480, 151, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        
        
        
        ################################################################################
        # create table
        self.tableModel = QtGui.QStandardItemModel(3, 3, self.tableView)
        
        #item = QtGui.QStandardItem('(%d, %d)' % (1, 1))
        #item.setTextAlignment(QtCore.Qt.AlignCenter)
        #model.setItem(1, 1, item)
        #self.tableView.setModel(model)
        
        
        
        #p = subprocess.Popen(['D:\\ARTFABRIK\\140213 - DSLR capturing\\gphoto-2.4.14-win32-build2\\win32\\gphoto2.exe', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.Popen(['D:\\ARTFABRIK\\140213 - DSLR capturing\\gphoto-2.4.14-win32-build2\\win32\\gphoto2.exe', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.Popen(['dir C:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.call(['dir C:'])
        #p = subprocess.Popen(["start", "cmd", "/k", "C:", "/k", "cd gphoto2", "/k", "set CAMLIBS=camlibs", "set IOLIBS=iolibs"], shell = True, cwd="C://gphoto2")
        #p = subprocess.Popen(["start", "cmd", "/k", "gphoto2.exe --auto-detect"], shell = True, cwd="C://gphoto2")
        #p = subprocess.Popen(["start", "cmd", "/k", "C: & cd C:\\gphoto2 & gphoto2.exe --auto-detect"], shell = True)
        #subprocess.call(["gphoto2.exe", "--help"]);
        
        
        
        ################################################################################
        # update on click
        self.pushButton.clicked.connect(self.updateActiveCamTable)
        
        
        
    def updateActiveCamTable(self):
        ################################################################################
        # init gphoto
	if os.name!="posix":
	    os.chdir("C:\\gphoto2")

        my_env = os.environ
        my_env["CAMLIBS"] = "camlibs"
        my_env["IOLIBS"] = "iolibs"
        
        # get camera list
        p = subprocess.Popen([('gphoto2.exe','gphoto2')[not os.name=="posix"], '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
        
        out, err = p.communicate()
        print out
        
        ################################################################################
        # print camera list to table
        cam_string = False
        row = 0
        for line in out.splitlines():
            #the real code does filtering here
            print "test:", line.rstrip()
            if cam_string:
                print "THIS IS A CAM"
                item = QtGui.QStandardItem(line.rstrip())
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableModel.setItem(row, 0, item)
                self.tableView.setModel(self.tableModel)
                row += 1
                
            if line.rstrip() == '----------------------------------------------------------':
                cam_string = True
                print "NOW IT STARTS"
        
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        
class ControlMainWindow(QtGui.QMainWindow):
  def __init__(self, parent=None):
    super(ControlMainWindow, self).__init__(parent)
    self.ui =  Ui_MainWindow()
    self.ui.setupUi(self)
   
if __name__ == "__main__":
    # QtGui.QApplication.setStyle(new QPlastiqueStyle);
    QtGui.QApplication.setStyle("plastique")
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
