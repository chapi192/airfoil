from PyQt5 import QtCore, QtGui, QtWidgets

import LBImplement
import heatmap
import Vector

#  Created as a way to pass data between the LB class and Window/Canvas classes using a set timer
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
		self._hm_window.updateCanvas(self._lb_impl.rho)

def run(MainWindow, windowX: int, windowY: int):
	lb_impl = LBImplement.LatticeBolztman(windowX, windowY)
	hm_window = heatmap.HeatmapWindow(lb_impl.rho)
	hm_window.setParent(MainWindow)  # TODO: change to match the GUI structure
	hm_window.move(10, 10)

	dm = DataManager(lb_impl, hm_window)

	hm_window.show()
	hm_window.raise_()

	return dm

def connect(timer: QtCore.QTimer, dm: DataManager):
	timer.timeout.connect(dm.update)
