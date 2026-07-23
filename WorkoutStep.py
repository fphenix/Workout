from dataclasses import dataclass
from setup import INTENSITY_DICT, INTENSITY_COLORS

@dataclass
class WorkoutStep:
    duration_minutes: float
    cpm: int
    intensity: str

    @property
    def duration_seconds(self):
        return int(self.duration_minutes * 60.0)
    
    @property
    def intensity_text(self):
        return f"{INTENSITY_DICT[self.intensity]}"

    @property
    def intensity_color(self):
         return f"{INTENSITY_COLORS[self.intensity]}"
