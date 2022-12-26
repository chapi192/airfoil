import sys

import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavToolbar

class HeatmapWindow(QDialog):
	def __init__(self):
		super().__init__()
		self._main = QWidget()
		self.canvas = FigureCanvas(Figure())

		layout = QVBoxLayout(self._main)
		layout.addWidget(NavToolbar(self.canvas, self))
		layout.addWidget(self.canvas)
		self.setLayout(layout)

		self._axes = self.canvas.figure.subplots()
		self.plot()

	def plot(self):
		x, y = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-2, 2, 100))
		c = x * (x**2 + y**2) * np.exp(-(x**2 + y**2))

		c_bounds = self._axes.pcolormesh(x, y, c, cmap="cool")
		self.canvas.figure.colorbar(c_bounds)

def main():
	# Check whether there is already a running QApplication
	qapp = QApplication.instance()
	if not qapp:
		qapp = QApplication(sys.argv)

	window = HeatmapWindow()
	window.setWindowTitle("Heatmap Test")
	window.show()
	window.activateWindow()
	window.raise_()
	sys.exit(qapp.exec())

if __name__ == "__main__":
	main()
