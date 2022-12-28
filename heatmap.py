import sys

import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavToolbar

class HeatmapCanvas(FigureCanvas):
	def __init__(self, figure: Figure, array):
		super().__init__(figure)
		self._array = array

		self._axes = self.figure.subplots()
		self.plot()

	def plot(self):
		self._axes.imshow(self._array, origin='lower', cmap='cool')

class HeatmapWindow(QDialog):
	def __init__(self, array):
		super().__init__()
		self._main = QWidget()
		self.canvas = HeatmapCanvas(Figure(), array)

		layout = QVBoxLayout(self._main)
		layout.addWidget(NavToolbar(self.canvas, self))
		layout.addWidget(self.canvas)
		self.setLayout(layout)

def main():
	# Check whether there is already a running QApplication
	qapp = QApplication.instance()
	if not qapp:
		qapp = QApplication(sys.argv)

	length, height = 100, 100
	array = np.zeros((length, height))

	for (idx, _) in np.ndenumerate(array):
		y = (2 * (idx[0]+0.5) / array.shape[0] - 1) * 2
		x = (2 * (idx[1]+0.5) / array.shape[1] - 1) * 2

		array[idx] = x * (x**2 + y**2) * np.exp(-(x**2 + y**2))

	window = HeatmapWindow(array)
	window.setWindowTitle("Heatmap Test")
	window.show()
	window.activateWindow()
	window.raise_()
	sys.exit(qapp.exec())

if __name__ == "__main__":
	main()
