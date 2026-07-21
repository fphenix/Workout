"""
plotwidget.py

Matplotlib canvas embedded in a PySide6 widget.
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

from parser import total_time


class PlotWidget(FigureCanvas):

    VERTICAL_STYLE = "none"      # "none", "gray", "color"
    
    LINE_WIDTH = 4

    Y_MIN = 14
    Y_MAX = 34

    COLORS = {
        "R": "#7FDBFF",   # light blue
        "E": "#0055FF",   # blue
        "N": "#00AA00",   # green
        "F": "#DD2222",   # red
        "M": "#BB44DD",   # violet
    }

    def __init__(self, parent=None):
        self.current_workout = None

        self.figure = Figure(figsize=(10, 5))
        super().__init__(self.figure)

        self.setParent(parent)

        self.axes = self.figure.add_subplot(111)

        self.figure.tight_layout()

    def clear(self):

        self.axes.clear()

        self.axes.set_xlim(0, 60)
        self.axes.set_ylim(PlotWidget.Y_MIN, PlotWidget.Y_MAX)

        self.axes.set_xlabel("Time (minutes)")
        self.axes.set_ylabel("Stroke rate (spm)")

        self.axes.grid(True, color="0.85")

        self.draw()

    def refresh(self):
        if self.current_workout:
            self.plot_workout(self.current_workout)

    def set_vertical_style(self, style):

        PlotWidget.VERTICAL_STYLE = style

        if self.current_workout:
            self.plot_workout(self.current_workout)

    def plot_workout(self, workout):
        self.current_workout = workout

        ax = self.axes
        ax.clear()

        xmax = max(1, total_time(workout))

        ax.grid(
            True,
            which="major",
            axis="both",        # axis="y" et "x"
            color="#808080",
            linewidth=1.0,
        )

        ax.grid(
            True,
            which="minor",
            axis="both",        # axis="y" et "x"
            color="#c0c0c0", 
            linewidth=0.5,
        )

        ax.set_xlim(0, xmax)
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_minor_locator(MultipleLocator(1))

        ax.set_ylim(PlotWidget.Y_MIN, PlotWidget.Y_MAX)
        ax.yaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Stroke Rate (spm)")

        ax.set_facecolor("white")

        current_time = 0.0
        previous_spm = None

        for interval in workout.intervals:

            x0 = current_time
            x1 = current_time + interval.duration

            color = PlotWidget.COLORS.get(interval.zone, "black")

            # Horizontal interval
            ax.plot(
                [x0, x1],
                [interval.spm, interval.spm],
                color=color,
                linewidth=PlotWidget.LINE_WIDTH,
                solid_capstyle="round",
                zorder=2,
            )

            # Vertical transition
            
            if previous_spm is not None:

                if PlotWidget.VERTICAL_STYLE == "gray":
                    vcolor = "lightgray"
                    vwidth = 1

                elif PlotWidget.VERTICAL_STYLE == "color":
                    vcolor = color
                    vwidth = PlotWidget.LINE_WIDTH

                else:
                    vcolor = None
                    vwidth = 0

                ax.plot(
                    [x0, x0],
                    [previous_spm, interval.spm],
                    color=vcolor,
                    linewidth=vwidth,
                    solid_capstyle="round",
                    zorder=1,
                )

            previous_spm = interval.spm
            current_time = x1

        # Title & Subtitle
        self.figure.suptitle(
            workout.title,
            fontsize=16,
            fontweight="bold",
        )

        if workout.field:
            ax.set_title(
                workout.field,
                fontsize=11,
                color="dimgray",
                pad=10,
            )

        # Legend
        legend = [
            Line2D([0], [0], color=PlotWidget.COLORS["M"], lw=4, label="M"),
            Line2D([0], [0], color=PlotWidget.COLORS["F"], lw=4, label="F"),
            Line2D([0], [0], color=PlotWidget.COLORS["N"], lw=4, label="N"),
            Line2D([0], [0], color=PlotWidget.COLORS["E"], lw=4, label="E"),
            Line2D([0], [0], color=PlotWidget.COLORS["R"], lw=4, label="R"),
        ]

        ax.legend(
            handles=legend,
            loc="upper right",
            title="Zones",
        )

        self.figure.tight_layout(rect=[0, 0, 1, 0.93])

        self.draw()
