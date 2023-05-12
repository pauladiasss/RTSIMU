"""Frames namespace for data management."""

from collections import UserList
from csv import writer
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np


@dataclass(frozen=True)
class Frame:
    """Frame class for data management."""

    time: float = 0.0
    right_abduction: float = 0.0
    right_flexion: float = 0.0
    right_rotation: float = 0.0
    right_elevation: float = 0.0
    left_abduction: float = 0.0
    left_flexion: float = 0.0
    left_rotation: float = 0.0
    left_elevation: float = 0.0

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __eq__(self, other):
        return self.time == other.time

    def to_numpy(self):
        """Converts frame to numpy array."""
        return np.array(
            [
                self.time, self.right_abduction, self.right_flexion,
                self.right_rotation, self.right_elevation, self.left_abduction,
                self.left_flexion, self.left_rotation, self.left_elevation
            ]
        )


class FrameCollection(UserList):
    """Collection of Frames."""

    def __init__(self, init_list: List[Frame] = None) -> None:
        super().__init__(init_list or [])

    def flush(self, num: int) -> "FrameCollection":
        """Flush the first num elements of the collection."""
        flushed_data, self.data = self.data[:num], self.data[num:]
        return FrameCollection(flushed_data)

    def to_csv(self, path: Path, mode: str = "w", header: bool = True) -> None:
        """Write the data to a CSV file."""
        with path.open(mode=mode, encoding="utf-8", newline='\n') as file_ptr:
            wrt = writer(file_ptr)
            if header:
                wrt.writerow(Frame.__annotations__.keys())
            for frame in self.data:
                wrt.writerow(frame.to_numpy())

    def to_numpy(self) -> np.ndarray:
        """Convert the data to a numpy array."""
        return np.array([d.to_numpy() for d in self.data])
