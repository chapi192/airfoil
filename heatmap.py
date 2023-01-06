import sys

import numpy as np

from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #changed both of these to _qt5agg for figureCanvas and Navtoolbar. Dunno why it didnt work but it does now
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar

class HeatmapCanvas(FigureCanvas):
	def __init__(self, figure: Figure, array):
		super().__init__(figure)
		self._axes = self.figure.subplots()

		self._image = self._axes.imshow(array, origin='lower', cmap='cool')
		self._cbar = self.figure.colorbar(self._image)

	def plot(self, array):
		self._image.set_data(array)
		self._image.set_clim(array.min(), array.max())
		self.draw()

class HeatmapWindow(QDialog):
	def __init__(self, array):
		super().__init__()
		self.setWindowTitle("Heatmap Test")
		self._main = QWidget()
		self._canvas = HeatmapCanvas(Figure(), array)

		layout = QVBoxLayout(self._main)
		layout.addWidget(NavToolbar(self._canvas, self))
		layout.addWidget(self._canvas)
		self.setLayout(layout)

	def updateCanvas(self, array):
		self._canvas.plot(array)
