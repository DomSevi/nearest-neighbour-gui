import sys
import random
import csv
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
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

        self.sliderLabel = QtWidgets.QLabel("Liczba sąsiadów")
        self.slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setRange(1, 20)
        self.slider.setValue(self.neighbourCount)
        self.slider.valueChanged.connect(self.update_slider)

        self.metricLabel = QtWidgets.QLabel("Rodzaj metryki")
        self.metricButton = QtWidgets.QPushButton(("Euklidesowa", "Miejska")[self.metricType])
        self.metricButton.clicked.connect(self.update_metric)

        self.voteLabel = QtWidgets.QLabel("Rodzaj głosowania")
        self.voteButton = QtWidgets.QPushButton(("Prosty", "Ważony")[self.voteType])
        self.voteButton.clicked.connect(self.update_type)

        self.innerLayout = QtWidgets.QVBoxLayout()
        self.innerLayout.addWidget(self.sliderLabel)
        self.innerLayout.addWidget(self.slider)
        self.innerLayout.addWidget(self.metricLabel)
        self.innerLayout.addWidget(self.metricButton)
        self.innerLayout.addWidget(self.voteLabel)
        self.innerLayout.addWidget(self.voteButton)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.pixmap = QtGui.QPixmap(600, 600)
        self.pixmap.fill(QColor(0, 0, 0))
        self.pixmapLabel = QtWidgets.QLabel()
        self.pixmapLabel.setPixmap(self.pixmap)
        self.layout.addWidget(self.pixmapLabel)
        self.layout.addLayout(self.innerLayout)

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

    @QtCore.Slot()
    def update_metric(self):
        self.metricType = not self.metricType
        self.metricButton.setText(("Euklidesowa", "Miejska")[self.metricType])

    @QtCore.Slot()
    def update_type(self):
        self.voteType = not self.voteType
        self.voteButton.setText(("Prosty", "Ważony")[self.voteType])

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            print(event.pos())
