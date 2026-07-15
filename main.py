import sys

from setup import WIN_HEIGHT, WIN_WIDTH

from PySide6.QtWidgets import (
    QApplication
)

from MainWindow import MainWindow

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.resize(
        WIN_WIDTH,
        WIN_HEIGHT
    )

    window.show()

    sys.exit(
        app.exec()
    )
    