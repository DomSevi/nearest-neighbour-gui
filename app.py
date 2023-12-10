import csv
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont
from PySide6.QtWidgets import QSlider

# Aplikacja do znajdowania k najblizszych sąsiadów
# Po kliknięciu w planszę z punktami pojawi się nowy punkt i w zależności
# od tego do których sąsiadów jest najbardziej podobny przyjmie ich kolor.
#
# Umożliwia wybór ilości znajdowanych najbliższych sąsiadów, od 1 do 20
# Pozwala również na twa tryby obliczania odleglosci jak i ważenia głosów na to do kogo jest najpodobniejszy
#
# Aplikacja wczyta punkty z pliku input.txt w folderze z tym plikiem
# Punkty muszą być w formacie x,y,z, gdzie z to typ/kolor/rodzina punktu
#
# Dominik Sobieraj


# Zwaraca kolumne listy wielowymiarowej
def column(matrix, i):
    return [row[i] for row in matrix]


# Zwraca float z k miejscami po przecinku
def truncate_float(float_number, k):
    multiplier = 10 ** k
    return int(float_number * multiplier) / multiplier


# Zwraca kolor na podstawie int, 1 - 5
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


# Główna klasa aplikacji
class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Metryka
        # False - Euklidesowa, True - Miejska
        self.metricType = False

        # Klasyfikacja
        # False - prosta, True - ważona odwrotnością kwadratu odległości
        self.voteType = False

        self.neighbourCount = 5
        self.rows = []
        self.lastClick = [0, 0]

        # Canvas and painter - left side
        self.pixmap = QtGui.QPixmap(600, 600)
        self.pixmap.fill(QColor(255, 255, 255))
        self.pixmapLabel = QtWidgets.QLabel()
        self.pixmapLabel.setPixmap(self.pixmap)

        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.addWidget(self.pixmapLabel)
        self.leftLayout.setSpacing(0)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)

        self.painter = QPainter(self.pixmap)
        self.painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        self.painter.setRenderHints(QPainter.RenderHint.TextAntialiasing, True)
        self.font = QFont()
        self.font.setPixelSize(12)
        self.painter.setFont(self.font)

        # UI - right side
        self.sliderLabel = QtWidgets.QLabel("Liczba sąsiadów " + str(self.neighbourCount))
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

        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setContentsMargins(10, 10, 10, 10)
        self.rightLayout.addWidget(self.sliderLabel)
        self.rightLayout.addWidget(self.slider)
        self.rightLayout.addWidget(self.metricLabel)
        self.rightLayout.addWidget(self.metricButton)
        self.rightLayout.addWidget(self.voteLabel)
        self.rightLayout.addWidget(self.voteButton)

        # Main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)

        # Read from a file, paint points and keep copy of the points only
        self.drawPoints()
        self.pixmapCopy = QtGui.QPixmap(600, 600)
        self.pixmapCopy = self.pixmap.copy()

    # Uruchamiana po zainicjalizowaniu UI, wczytuje plik input.txt i rysuje punkty
    def drawPoints(self):
        # Read the input file and store rows in rows var
        file = open("input.txt")
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()

        # Znalezienie najwiekszych i najmniejszych wartosci
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

        # Rysowanie punktów
        for point in self.rows:
            self.painter.setBrush(QBrush(getColor(point[2])))
            x = (float(point[0])*224)+300
            y = (float(point[1])*224)+300
            self.painter.drawEllipse(int(x), int(y), 8, 8)
        self.pixmapLabel.setPixmap(self.pixmap)

    # Funkcja licząca odległosci od ostatniego kliknięcia, ustala również podobność do danej klasy
    def getKNN(self):
        if self.lastClick[0] == 0 or self.lastClick[1] == 0 or self.lastClick[0] > 600 or self.lastClick[1] > 600:
            return

        self.painter.drawPixmap(0, 0, 600, 600, self.pixmapCopy)
        x = (self.lastClick[0] - 300) / 224
        y = (self.lastClick[1] - 300) / 224
        dist = []

        # Liczenie odległosci na dwa sposoby
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

        # Znalezienie k-najblizszych sąsiadów
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

        # Narysowanie odleglosci obok poszczególnych punktów
        self.painter.setPen(QPen(QColor(0, 0, 0), 15, Qt.PenStyle.SolidLine))
        for i in kdist:
            self.painter.drawText(i[0] * 224 + 300, i[1] * 224 + 300, str(i[3]))

        # Przynależność do klasy
        # Simple
        colorCount = []
        index = 0
        if not self.voteType:
            colorCount = [column(kdist, 2).count('1'), column(kdist, 2).count('2'), column(kdist, 2).count('3'),
                          column(kdist, 2).count('4'), column(kdist, 2).count('5')]
            index = colorCount.index(max(colorCount))

        # Weighted
        if self.voteType:
            colorCount = [0, 0, 0, 0, 0]
            for i in kdist:
                colorCount[int(i[2])-1] = colorCount[int(i[2])-1] + 1/(pow(i[3], 2))
            index = colorCount.index(max(colorCount))

        if colorCount.count(colorCount[index]) > 1:
            color = QColor(0, 0, 0)
        elif index == 0:
            color = QColor(255, 0, 0)
        elif index == 1:
            color = QColor(0, 255, 0)
        elif index == 2:
            color = QColor(0, 0, 255)
        elif index == 3:
            color = QColor(255, 255, 0)
        elif index == 4:
            color = QColor(0, 255, 255)
        else:
            color = QColor(255, 0, 0)

        self.painter.setBrush(QBrush(color))
        self.painter.setPen(QPen(color, 1, Qt.PenStyle.SolidLine))
        rect = QRectF(self.lastClick[0]-8, self.lastClick[1] - 8, 25, 25)
        self.painter.drawRect(rect)
        self.pixmapLabel.setPixmap(self.pixmap)

    # Eventy i sloty do ui / kliknięć myszką
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.lastClick = [event.x(), event.y()]
            self.getKNN()

    @QtCore.Slot()
    def update_slider(self, value):
        self.neighbourCount = value
        self.sliderLabel.setText("Liczba sąsiadów " + str(self.neighbourCount))
        self.getKNN()

    @QtCore.Slot()
    def update_metric(self):
        self.metricType = not self.metricType
        self.metricButton.setText(("Euklidesowa", "Miejska")[self.metricType])
        self.getKNN()

    @QtCore.Slot()
    def update_type(self):
        self.voteType = not self.voteType
        self.voteButton.setText(("Prosty", "Ważony")[self.voteType])
        self.getKNN()
