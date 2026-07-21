"""
mainwindow.py

Main application window.
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from parser import load_workout
from plotwidget import PlotWidget


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Workout Viewer")
        self.resize(1000, 600)

        # Central widget
        self.plot = PlotWidget(self)
        self.setCentralWidget(self.plot)

        # Empty graph at startup
        self.plot.clear()

        # Build menus
        self.create_menus()

    def create_menus(self):

        menu = self.menuBar().addMenu("&File")

        load_action = menu.addAction("&Load...")
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_workout)

        menu.addSeparator()

        quit_action = menu.addAction("&Quit")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)

    def load_workout(self):

        # workouts directory beside the program
        start_dir = Path(__file__).parent.parent / "workouts"

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load workout",
            str(start_dir),
            "Workout files (*.wo);;All files (*)"
        )

        if not filename:
            return

        try:
            workout = load_workout(filename)
            self.plot.plot_workout(workout)

            self.setWindowTitle(
                f"Workout Viewer - {Path(filename).name}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to load workout.\n\n{e}"
            )
