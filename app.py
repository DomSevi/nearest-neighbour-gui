import sys
import random
import csv
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.neighbourCount = 5

        # Metric type
        # False - Euklidesowa, True - Miejska
        self.metricType = False

        # Classification type
        # False - simple, True - weighting inversed squared distance
        self.voteType = False

        self.slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setRange(1, 20)
        self.slider.setValue(self.neighbourCount)
        self.slider.valueChanged.connect(self.update_slider)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.slider)

        # Read the input file and store rows in rows var
        file = open("input.txt")
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)

        file.close()

    @QtCore.Slot()
    def update_slider(self, value):
        print(value)

