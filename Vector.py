import sys
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.animation as pa

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#create application (sys.args could be passed in to facilitate command line arguments)

def vectorField():
    x, y = np.meshgrid(np.linspace(-25, 25, 10), np.linspace(-25, 25, 10))
    u = 1
    v = 0
    pl.quiver(x, y, u, v)
    pl.show()


#create window
def main():

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("This is a test")
    window.resize(1920,1080)
    window.move(100, 100)
    vf = QLabel(vectorField(), parent=window)
    vf.move(int(1920/2), int(1080/2))

#show window
    window.show()

#run apps main loop
    sys.exit(app.exec())

if __name__=="__main__":
    main()