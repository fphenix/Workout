"""
parser.py

Reads .wo workout files.

Format:

    # comment
    WORKOUT My workout title
    Field UT2

    10 18 R
    5 20 E
    4 24 N
"""

from dataclasses import dataclass


@dataclass
class Interval:
    duration: float
    spm: int
    zone: str


@dataclass
class Workout:
    title: str
    field: str
    intervals: list


def load_workout(filename: str) -> Workout:
    """
    Load a workout file.

    Returns
    -------
    Workout
    """

    title = ""
    field = ""
    intervals = []

    with open(filename, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            parts = line.split()

            keyword = parts[0].upper()

            if keyword == "WORKOUT":
                title = " ".join(parts[1:])
                continue

            if keyword == "FIELD":
                field = " ".join(parts[1:])
                continue

            if len(parts) >= 3:

                duration = float(parts[0])
                spm = int(parts[1])
                zone = parts[2].upper()

                intervals.append(
                    Interval(duration, spm, zone)
                )

    return Workout(title, field, intervals)


def total_time(workout: Workout) -> float:
    """Total duration in minutes."""
    return sum(i.duration for i in workout.intervals)
