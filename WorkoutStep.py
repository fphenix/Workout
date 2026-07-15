from dataclasses import dataclass
from setup import INTENSITY_DICT

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
