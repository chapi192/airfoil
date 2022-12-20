import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#create application (sys.args could be passed in to facilitate command line arguments)
app = QApplication([])


#create window
window = QWidget()
window.setWindowTitle("This is a test")
window.resize(1920,1080)
window.move(100, 100)
helloMsg = QLabel("<h1>Hello World!</h1>", parent=window)
helloMsg.move(int(1920/2), int(1080/2))

#show window
window.show()

#run apps main loop
sys.exit(app.exec())