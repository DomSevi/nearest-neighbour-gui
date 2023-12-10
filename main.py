import sys
from PySide6 import QtWidgets
from app import App

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
# Projekt można znaleźć na repozytorium
# https://github.com/DomSevi/nearest-neighbour-gui
#
# Dominik Sobieraj

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
