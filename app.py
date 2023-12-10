
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSlider
from image import Image


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
        self.innerLayout.setContentsMargins(10, 10, 10, 10)
        self.innerLayout.addWidget(self.sliderLabel)
        self.innerLayout.addWidget(self.slider)
        self.innerLayout.addWidget(self.metricLabel)
        self.innerLayout.addWidget(self.metricButton)
        self.innerLayout.addWidget(self.voteLabel)
        self.innerLayout.addWidget(self.voteButton)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(Image())
        self.layout.addLayout(self.innerLayout)

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


