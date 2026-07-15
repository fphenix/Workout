from dataclasses import dataclass

@dataclass
class WorkoutStep:
    duration_minutes: float
    cpm: int

    @property
    def duration_seconds(self):
        return int(self.duration_minutes * 60.0)


class Workout:
    def __init__(self):
        self.title = "Workout"
        self.field = "Field"
        self.steps = []

    @property
    def total_seconds(self):
        return sum(step.duration_seconds for step in self.steps)

    def clear(self):
        self.title = "Workout"
        self.field = "Field"
        self.steps.clear()

