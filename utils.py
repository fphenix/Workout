from Workout import Workout
from WorkoutStep import WorkoutStep

from setup import INTENSITY_DICT

# -----------------------------------------------------------------------------
# Setup file loader
# -----------------------------------------------------------------------------

def load_workout(filename):
    workout = Workout()

    with open(filename, "r", encoding="utf-8") as f:

        for lineno, raw in enumerate(f, start=1):

            line = raw.strip()

            # Empty line : ignore
            if not line:
                continue

            # Comment line : ignore
            if line.startswith("#"):
                continue

            upper = line.upper()

            # WORKOUT title
            if upper.startswith("WORKOUT"):

                title = line[len("WORKOUT"):].strip()

                if title:
                    workout.title = title
                else:
                    workout.title = "Workout"

                continue

            # FIELD field
            elif upper.startswith("FIELD"):

                field = line[len("FIELD"):].strip()

                if field:
                    workout.field = field
                else:
                    workout.field = "Field"

                continue

            parts = line.split()

            if len(parts) != 3:
                raise ValueError(
                    f"Line {lineno}: expected 'minutes cpm intensity'"
                )

            try:
                minutes = float(parts[0])
                cpm = int(parts[1])
                intensity = str(parts[2])
            except ValueError:
                raise ValueError(
                    f"Line {lineno}: invalid data type"
                )

            if (minutes <= 0.0) or (minutes > 120.0):
                raise ValueError(
                    f"Line {lineno}: duration must be > 0 and <= 120"
                )

            if (cpm <= 0) or (cpm > 50):
                raise ValueError(
                    f"Line {lineno}: CPM must be > 0 and <= 50"
                )
            
            if intensity not in INTENSITY_DICT:
                raise ValueError(
                    f"Line {lineno}: intensity must be one of R, E, N, F or M"
                )
            
            workout.steps.append(
                WorkoutStep(minutes, cpm, intensity)
            )

    if not workout.steps:
        raise ValueError("Workout is empty.")

    return workout


# -----------------------------------------------------------------------------

def format_time(seconds):

    seconds = max(0, int(seconds))

    m = seconds // 60
    s = seconds % 60

    return f"{m:02d}:{s:02d}"

