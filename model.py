import subprocess
import os

class Model(object):
	def __init__(self):
		self.cameras = []
		if os.name!="posix":
			os.chdir("C:\\gphoto2")
			win_env = os.environ
			win_env["CAMLIBS"] = "camlibs"
			win_env["IOLIBS"] = "iolibs"
	
	def captureAllCameraImages(self):
		print("captureall")
		for camera in self.cameras:
			print(camera)
			self.captureCameraImage(camera[1])
		
	def captureCameraImage(self, port):
		p = subprocess.Popen(['gphoto2', '--capture-image-and-download', '--port', port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print p.communicate()
	
	def getCameras(self):
		self.cameras = updateCameras()
		return self.cameras

def updateCameras():
	cameras = []
	p = subprocess.Popen(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	print out
	cam_string = False
	for line in out.splitlines():
		if cam_string:
			camParams = line.split("usb:")
			camera = (camParams[0].rstrip(),"usb:"+camParams[1].rstrip())
			cameras.append(camera)
		if line.rstrip() == '----------------------------------------------------------':
			cam_string = True
	return cameras
