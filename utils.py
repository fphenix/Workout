from Workout import Workout, WorkoutStep

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

            #WORKOUT field
            elif upper.startswith("FIELD"):

                field = line[len("FIELD"):].strip()

                if field:
                    workout.field = field
                else:
                    workout.field = "Field"

                continue

            parts = line.split()

            if len(parts) != 2:
                raise ValueError(
                    f"Line {lineno}: expected 'minutes cpm'"
                )

            try:
                minutes = float(parts[0])
                cpm = int(parts[1])
            except ValueError:
                raise ValueError(
                    f"Line {lineno}: invalid integer"
                )

            if (minutes <= 0.0) or (minutes > 120.0):
                raise ValueError(
                    f"Line {lineno}: duration must be > 0 and <= 120"
                )

            if (cpm <= 0) or (cpm > 50):
                raise ValueError(
                    f"Line {lineno}: CPM must be > 0 and <= 50"
                )

            workout.steps.append(
                WorkoutStep(minutes, cpm)
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

