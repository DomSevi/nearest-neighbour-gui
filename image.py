import csv
from math import trunc

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush, QPen


class Image(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.rows = []

        self.pixmap = QtGui.QPixmap(600, 600)
        self.pixmap.fill(QColor(255, 255, 255))
        self.pixmapLabel = QtWidgets.QLabel()
        self.pixmapLabel.setPixmap(self.pixmap)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pixmapLabel)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.painter = QPainter(self.pixmap)
        self.painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        self.painter.setRenderHints(QPainter.RenderHint.TextAntialiasing, True)

        self.drawPoints()
        self.pixmapCopy = QtGui.QPixmap(600, 600)
        self.pixmapCopy = self.pixmap.copy()

    @staticmethod
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
        for row in rows:
            x = 2 * ((float(row[0]) - min_x)/(max_x - min_x)) - 1
            y = 2 * ((float(row[1]) - min_y)/(max_y - min_y)) - 1
            new_rows.append([x, y, row[2]])

        self.rows = new_rows

        for point in self.rows:
            self.painter.setBrush(QBrush(self.getColor(point[2])))
            x = (float(point[0])*224)+300
            y = (float(point[1])*224)+300
            self.painter.drawEllipse(int(x), int(y), 8, 8)

        self.pixmapLabel.setPixmap(self.pixmap)

    def getKNN(self, point: QtGui.QMouseEvent):
        x = (point.x()-300)/224
        y = (point.y()-300)/224
        dist = []
        #for row in self.rows:

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.getKNN(event)
            self.painter.drawPixmap(0, 0, 600, 600, self.pixmapCopy)
            brush = QBrush(QColor(255, 0, 0))
            self.painter.setPen(QPen(QColor(255, 0, 0), 4, Qt.PenStyle.SolidLine))
            self.painter.setBrush(brush)
            self.painter.drawRect(event.x() - 8, event.y() - 8, 16, 16)
            self.pixmapLabel.setPixmap(self.pixmap)
