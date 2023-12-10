import csv

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont
from PySide6.QtWidgets import QSlider


def column(matrix, i):
    return [row[i] for row in matrix]


def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier


def getColor(color) -> QColor:
    if color == '1':
        return QColor(255, 0, 0)
    elif color == '2':
        return QColor(0, 255, 0)
    elif color == '3':
        return QColor(0, 0, 255)
    elif color == '4':
        return QColor(255, 255, 0)
    elif color == '5':
        return QColor(0, 255, 255)


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Metric type
        # False - Euklidesowa, True - Miejska
        self.metricType = False

        # Classification type
        # False - simple, True - weighting inversed squared distance
        self.voteType = False

        self.neighbourCount = 5

        self.rows = []

        # Canvas and painter
        self.pixmap = QtGui.QPixmap(600, 600)
        self.pixmap.fill(QColor(255, 255, 255))
        self.pixmapLabel = QtWidgets.QLabel()
        self.pixmapLabel.setPixmap(self.pixmap)

        self.pixmapLayout = QtWidgets.QVBoxLayout()
        self.pixmapLayout.addWidget(self.pixmapLabel)
        self.pixmapLayout.setSpacing(0)
        self.pixmapLayout.setContentsMargins(0, 0, 0, 0)

        self.painter = QPainter(self.pixmap)
        self.painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        self.painter.setRenderHints(QPainter.RenderHint.TextAntialiasing, True)
        self.font = QFont()
        self.font.setPixelSize(15)
        self.painter.setFont(self.font)

        # UI - right side
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
        self.layout.addLayout(self.pixmapLayout)
        self.layout.addLayout(self.innerLayout)

        # Read from a file, paint points and keep copy of the points only
        self.drawPoints()
        self.pixmapCopy = QtGui.QPixmap(600, 600)
        self.pixmapCopy = self.pixmap.copy()

    def drawPoints(self):
        # Read the input file and store rows in rows var
        file = open("input.txt")
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()

        # Normalizacja
        new_rows = []
        min_x = float(rows[0][0])
        max_x = float(rows[0][0])
        min_y = float(rows[0][1])
        max_y = float(rows[0][1])
        for row in rows:
            if float(row[0]) < min_x:
                min_x = float(row[0])
            elif float(row[0]) > max_x:
                max_x = float(row[0])
            if float(row[1]) < min_y:
                min_y = float(row[1])
            elif float(row[1]) > max_y:
                max_y = float(row[1])
        # Normalizacja
        for row in rows:
            x = 2 * ((float(row[0]) - min_x)/(max_x - min_x)) - 1
            y = 2 * ((float(row[1]) - min_y)/(max_y - min_y)) - 1
            new_rows.append([x, y, row[2]])

        self.rows = new_rows
        for point in self.rows:
            self.painter.setBrush(QBrush(getColor(point[2])))
            x = (float(point[0])*224)+300
            y = (float(point[1])*224)+300
            self.painter.drawEllipse(int(x), int(y), 8, 8)
        self.pixmapLabel.setPixmap(self.pixmap)

    def getKNN(self, point: QtGui.QMouseEvent):
        x = (point.x() - 300) / 224
        y = (point.y() - 300) / 224
        dist = []

        # Euklidesowa
        if not self.metricType:
            for row in self.rows:
                result = (pow(x - row[0], 2) + pow(y - row[1], 2))**0.5
                dist.append([row[0], row[1], row[2], truncate_float(result, 2)])

        # Miejska
        if self.metricType:
            for row in self.rows:
                xdiff = x - row[0]
                if xdiff < 0:
                    xdiff = xdiff * -1
                ydiff = y - row[1]
                if ydiff < 0:
                    ydiff = ydiff * -1

                result = xdiff + ydiff
                dist.append([row[0], row[1], row[2], truncate_float(result, 2)])

        print(self.neighbourCount)
        kdist = []
        curr_largest = dist[0]
        for row in dist:
            if len(kdist) < self.neighbourCount:
                if curr_largest[3] < row[3]:
                    curr_largest = row
                kdist.append(row)
            elif curr_largest[3] > row[3]:
                kdist.pop(kdist.index(curr_largest))
                kdist.append(row)
                curr_largest = kdist[0]
                for j in kdist:
                    if curr_largest[3] < j[3]:
                        curr_largest = j

        self.painter.setPen(QPen(QColor(0, 0, 0), 15, Qt.PenStyle.SolidLine))

        for i in kdist:
            self.painter.drawText(i[0] * 224 + 300, i[1] * 224 + 300, str(i[3]))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:

            self.painter.drawPixmap(0, 0, 600, 600, self.pixmapCopy)
            brush = QBrush(QColor(255, 0, 0))
            self.painter.setPen(QPen(QColor(255, 0, 0), 4, Qt.PenStyle.SolidLine))
            self.painter.setBrush(brush)
            self.painter.drawRect(event.x() - 8, event.y() - 8, 16, 16)
            self.getKNN(event)
            self.pixmapLabel.setPixmap(self.pixmap)

    @QtCore.Slot()
    def update_slider(self, value):
        self.neighbourCount = value
        print(self.neighbourCount)

    @QtCore.Slot()
    def update_metric(self):
        self.metricType = not self.metricType
        self.metricButton.setText(("Euklidesowa", "Miejska")[self.metricType])

    @QtCore.Slot()
    def update_type(self):
        self.voteType = not self.voteType
        self.voteButton.setText(("Prosty", "Ważony")[self.voteType])
