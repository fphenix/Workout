import time

from setup import *
from utils import load_workout, format_time
from Workout import Workout

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

# -----------------------------------------------------------------------------
# Main Window
# -----------------------------------------------------------------------------

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cycle Workout")
        self.setStyleSheet(
            f"background-color: {WINDOW_BACKGROUND};"
        )

        self.workout = Workout()

        self.current_step = 0

        self.countdown_active = False
        self.running = False

        self.countdown_remaining = 0
        self.total_remaining = 0
        self.step_remaining = 0

        self.step_elapsed = 0

        self.beat_phase = 0.0
        self.last_elapsed = 0.0

        self.last_tick = time.perf_counter()

        self.create_menu()
        self.create_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

        self.timer.start(int(1000 / FPS))


    # -------------------------------------------------------------------------
    # Menu
    # -------------------------------------------------------------------------

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("Fichier")

        open_action = file_menu.addAction(
            "Ouvrir un setup..."
        )

        open_action.triggered.connect(
            self.open_setup
        )


    # -------------------------------------------------------------------------
    # Interface
    # -------------------------------------------------------------------------

    def create_ui(self):

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)

        layout.setSpacing(20)
        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        self.title_label = QLabel("Workout")

        self.field_label = QLabel("Field")

        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                color: {TEXT_COLOR};
                font: bold {TITLE_FONT}px Consolas;
            }}
            """
        )

        self.field_label.setAlignment(Qt.AlignCenter)

        self.field_label.setStyleSheet(
            f"""
            QLabel {{
                color: {TEXT_COLOR};
                font: bold {TITLE_FONT}px Consolas;
            }}
            """
        )

        self.state_label = QLabel(
            "Aucun workout chargé"
        )

        self.state_label.setAlignment(
            Qt.AlignCenter
        )

        self.state_label.setStyleSheet(
            f"""
            QLabel {{
                color: {TEXT_COLOR};
                font: {BIG_FONT}px Consolas;
            }}
            """
        )


        self.total_label = QLabel(
            "Temps total : 00:00"
        )

        self.exercise_label = QLabel(
            "Exercice : --"
        )

        self.rate_label = QLabel(
            "Cadence : -- CPM"
        )


        for label in (
            self.total_label,
            self.exercise_label,
            self.rate_label,
        ):

            label.setAlignment(
                Qt.AlignCenter
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color: {TEXT_COLOR};
                    font: {BIG_FONT}px Consolas;
                }}
                """
            )


        self.bar = QProgressBar()

        self.bar.setRange(
            0,
            1000
        )

        self.bar.setValue(
            0
        )

        self.bar.setTextVisible(
            False
        )

        self.bar.setFixedHeight(
            BAR_HEIGHT
        )

        self.bar.setFixedWidth(
            BAR_WIDTH
        )

        self.bar.setStyleSheet(
            f"""
            QProgressBar {{
                border: 1px solid {BAR_BORDER};
                border-radius: 4px;
                background: {BAR_BACKGROUND};
            }}

            QProgressBar::chunk {{
                background: {BAR_COLOR};
            }}
            """
        )


        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.field_label
        )

        layout.addWidget(
            self.state_label
        )

        layout.addWidget(
            self.total_label
        )

        layout.addWidget(
            self.exercise_label
        )

        layout.addWidget(
            self.rate_label
        )

        bar_layout = QHBoxLayout()
        bar_layout.addStretch()
        bar_layout.addWidget(self.bar)
        bar_layout.addStretch()

        layout.addLayout(bar_layout)


    # -------------------------------------------------------------------------
    # Loading setup
    # -------------------------------------------------------------------------

    def open_setup(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un setup",
            "./workouts",
            "Workout (*.wo);;Tous les fichiers (*)"
        )

        if not filename:
            return

        try:
            workout = load_workout(filename)

        except Exception as e:

            QMessageBox.warning(
                self,
                "Erreur",
                str(e)
            )

            return


        # Reset complet

        self.workout = workout

        self.current_step = 0

        self.countdown_active = True
        self.running = False

        self.countdown_remaining = DELAY_SECONDS

        self.total_remaining = (
            workout.total_seconds
        )

        self.step_remaining = 0

        self.bar.setValue(
            0
        )

        self.title_label.setText(
            workout.title
        )

        self.field_label.setText(
            workout.field
        )

        self.state_label.setText(
            f"Démarrage dans {format_time(self.countdown_remaining)}"
        )

        self.total_label.setText(
            f"Temps total : {format_time(self.total_remaining)}"
        )

        self.exercise_label.setText(
            "Préparation..."
        )

        self.rate_label.setText(
            "Cadence : -- CPM"
        )

        self.last_tick = time.perf_counter()

    # -------------------------------------------------------------------------
    # Timer update
    # -------------------------------------------------------------------------

    def update(self):

        now = time.perf_counter()

        elapsed = now - self.last_tick
        self.last_elapsed = elapsed

        # Protection contre les grands sauts éventuels
        if elapsed > 1:
            elapsed = 1

        self.last_tick = now

        # -------------------------------------------------------------
        # Phase de délai avant workout
        # -------------------------------------------------------------

        if self.countdown_active:
            self.countdown_remaining -= elapsed

            if self.countdown_remaining <= 0:
                self.countdown_active = False
                self.start_step()

            else:
                self.state_label.setText(
                    f"Démarrage dans "
                    f"{format_time(self.countdown_remaining)}"
                )

            return

        # -------------------------------------------------------------
        # Workout en cours
        # -------------------------------------------------------------

        if self.running:

            self.total_remaining -= elapsed
            self.step_remaining -= elapsed

            if self.total_remaining < 0:
                self.total_remaining = 0

            if self.step_remaining <= 0:
                self.next_step()

            else:
                self.update_progress()

            self.update_labels()

    # -------------------------------------------------------------------------
    # Start current step
    # -------------------------------------------------------------------------

    def start_step(self):

        if self.current_step >= len(self.workout.steps):

            self.finish_workout()
            return

        step = self.workout.steps[self.current_step]

        self.step_remaining = (step.duration_seconds)

        self.step_elapsed = 0
        self.beat_phase = 0.0

        self.running = True

        self.bar.setValue(0)

        self.state_label.setText("Workout en cours")

        self.update_labels()

    # -------------------------------------------------------------------------
    # Next step
    # -------------------------------------------------------------------------

    def next_step(self):

        self.current_step += 1

        if self.current_step >= len(self.workout.steps):

            self.finish_workout()
            return


        self.start_step()



    # -------------------------------------------------------------------------
    # Progress bar
    # -------------------------------------------------------------------------

    def update_progress(self):

        if not self.running:
            return

        step = self.workout.steps[self.current_step]

        cycle = 60.0 / step.cpm

        self.beat_phase += self.last_elapsed

        if self.beat_phase >= cycle:
            self.beat_phase -= cycle

        progress = self.beat_phase / cycle

        self.bar.setValue(
            int(progress * 1000)
        )



    # -------------------------------------------------------------------------
    # Labels update
    # -------------------------------------------------------------------------

    def update_labels(self):

        if not self.running:
            return


        step = self.workout.steps[self.current_step]


        self.total_label.setText(
            "Temps total : "
            + format_time(
                self.total_remaining
            )
        )


        self.exercise_label.setText(
            f"Exercice "
            f"{self.current_step + 1}/"
            f"{len(self.workout.steps)}  -  "
            f"Temps : "
            f"{format_time(self.step_remaining)}"
        )


        self.rate_label.setText(
            f"Cadence : {step.cpm} CPM"
        )



    # -------------------------------------------------------------------------
    # End workout
    # -------------------------------------------------------------------------

    def finish_workout(self):

        self.running = False

        self.bar.setValue(
            1000
        )

        self.state_label.setText(
            "Workout terminé"
        )

        self.exercise_label.setText(
            ""
        )

        self.rate_label.setText(
            ""
        )


