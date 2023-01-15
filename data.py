from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import LBImplement
import heatmap
import Vector

#  Created as a way to pass data between the LB class and Canvas classes using a timer
class DataManager():
	def __init__(
	    self, lb_impl: LBImplement.LatticeBolztman,
	    hm_window: heatmap.HeatmapWindow
	):
		self._lb_impl = lb_impl
		self._lb_impl.calculateInitial()
		self._hm_window = hm_window

	def update(self):
		self._lb_impl.calcNext()

		pressure = self._lb_impl.rho
		# Removes the pressure data where an obstacle exists
		pressure_masked = np.ma.masked_where(self._lb_impl.obstacle, pressure)
		self._hm_window.updateCanvas(pressure_masked)

def run(MainWindow, windowX: int, windowY: int):
	lb_impl = LBImplement.LatticeBolztman(windowX, windowY)
	hm_window = heatmap.HeatmapWindow(lb_impl.rho)
	hm_window.setParent(MainWindow)  # TODO: change to match the GUI structure
	hm_window.move(10, 10)

	dm = DataManager(lb_impl, hm_window)

	hm_window.show()

	return dm

# Ties the updating of the sim to a set interval of time
def connect(timer: QtCore.QTimer, dm: DataManager):
	timer.timeout.connect(dm.update)
