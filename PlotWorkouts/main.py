"""
main.py

Workout Viewer : It'll plot the data in the ../workout/<***>.wo files

%> pip install pyside6 matplotlib
"""

import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
