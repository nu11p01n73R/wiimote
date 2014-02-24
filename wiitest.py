
from linuxWiimoteLib import Wiimote
import time
import sys
from PyQt4 import QtGui,QtCore
import threading
points=[]
flag=True
corner={}
robotRunning=False
clear=False
wiimote=Wiimote()
setting=True

class wiiThread(threading.Thread):
    def run(self):
      global wiimote,points
      wii(points)
      return
      
class guiThread(threading.Thread):
    def run(self):
	global wiimote,points
	gui(points)
	
class trial(QtGui.QWidget):
    def __init__(self,points):
        super(trial , self).__init__()
        global wiimote,corner
        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 30
        self.myPenColor = QtCore.Qt.red
        imageSize = QtCore.QSize(corner['Threex'],corner['Threey'])
		imageSize = QtCore.QSize(1300,768)
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_ARGB32)    
        self.points=points
        self.start=1
        self.window()
        
	
    def window(self):	    
		self.setWindowTitle('Trial')
	
        self.setGeometry(600 , 600 , 600 , 600)
        self.show()
   
    def draw(self):
		global wiimote,points,start,corner
		painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, 10,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        for i in range(self.start,len(points)):
	    try:
		  #painter.drawLine(points[i][0],768-points[i][1],points[i+1][0],768-points[i+1][1])
		  painter.drawLine(points[i][0],corner['Threey']-points[i][1],points[i+1][0],corner['Threey']-points[i+1][1])
		  self.update()
	    except IndexError:
		  break
	    self.start=i-1
	    
    
    def clearAll(self):
		for i in range(1300):
			for j in range(768):
				self.image.setPixel(i,j,QtGui.qRgba(255, 255, 255, 4))
		self.start=1
		self.update()
	     
    def paintEvent(self, event):
		global wiimote,clear
		painter = QtGui.QPainter(self)
		painter.drawImage(event.rect(), self.image)
		
		if clear:
		  self.clearAll()
		  clear=False
		else:  
		  self.draw()
        

def connectWii(wiimote):
	print "Press 1 & 2 "
	wiimote.Connect()
	
def getCorners(wiimote):
	global corner
	print "first corner"
	temp=readValue(wiimote)
	corner['basex']=temp[0]
	corner['basey']=temp[1]
	corner['Onex']=0
	corner['Oney']=0
	time.sleep(3)
	print "opposite corner"
	temp = readValue(wiimote)
	corner['Threex'] = temp[0]-corner['basex']
	corner['Threey'] = temp[1]-corner['basey']
	
	corner['Twox'] = corner['Threex']
	corner['Twoy'] = 0
	
	corner['Fourx'] = 0
	corner['Foury'] = corner['Threey']
	print corner['Onex'],corner['Oney']
	print "==========,corner['Threey'========================"
	print corner['Twox'],corner['Twoy']
	print "=================================="
	print corner['Threex'],corner['Threey']
	print "=================================="
	print corner['Fourx'],corner['Foury']
	print "=================================="
	return corner
  
	
def readValue(wiimote):
	wiimote.activate_IR()
	x=y=i=0
	while i<50:
		time.sleep(.01)
		if wiimote.IRState.RawX1 != 1023 or wiimote.IRState.RawY1 != 1023:
			x+=wiimote.IRState.RawX1
			y+=wiimote.IRState.RawY1
			print i
			i += 1	
	return ([x/50,y/50])
      
def IRdraw(wiimote,corner):
	global points,robotRunning
	wiimote.activate_IR()
	reading = False
	i = 0
	while True:
	  if reading and (wiimote.IRState.RawX1 == 1023 or wiimote.IRState.RawY1 == 1023):
	      break
	  elif  wiimote.IRState.RawX1 != 1023 and wiimote.IRState.RawY1 != 1023:
	    reading = True
	    points.append([wiimote.IRState.RawX1-corner['basex'],wiimote.IRState.RawY1-corner['basey']])
	    print i,wiimote.IRState.RawX1-corner['basex'],wiimote.IRState.RawY1-corner['basey']
	time.sleep(3)
	robotRunning=True


def wii(points):
  global wiimote,robotRunnig
  while True:
    print "Please wait three seconds"
    time.sleep(3)
    print "start drawing"
    IRdraw(wiimote,corner)
    robotControl()
    while robotRunning:
      pass
    points=[]

def gui(points):  
  app = QtGui.QApplication(sys.argv)
  t = trial(points)
  sys.exit(app.exec_())
  
def calibration(wiimote):
  global flag,corner
  base={}
  connectWii(wiimote)
  corner=getCorners(wiimote)
  flag=False
  
  
def main():
  global wiimote,flag
  wiiObj=wiiThread()
  guiObj=guiThread()
  calibration(wiimote)
  wiiObj.start()
  while flag:
     pass
  guiObj.run()
  
  
if __name__=='__main__':
  main()



