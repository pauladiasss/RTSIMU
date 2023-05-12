"""IMU namespace for data management."""

from collections import UserList
from csv import writer
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import numpy as np


class IMUSensorLabels:
    """Define the available sensor names."""
    ACCELEROMETER = "A"
    GYROSCOPE = "G"
    MAGNETOMETER = "M"

    def __iter__(self):
        return iter([self.ACCELEROMETER, self.GYROSCOPE, self.MAGNETOMETER])


@dataclass(frozen=True)
class IMUData:
    """Define the data structure for the IMU data."""
    time: float = 0.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_numpy(self):
        """Converts instance to numpy array."""
        return np.array([self.time, self.x, self.y, self.z])


@dataclass
class QuaternionData:
    """Define the data structure for the IMU quaternion data."""
    time: float = 0.0
    w: float = 0.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_numpy(self):
        """Converts instance to numpy array."""
        return np.array([self.time, self.w, self.x, self.y, self.z])


class IMUCollection(UserList):
    """Data collection for the IMU data."""

    def __init__(self, init_list: List[Union[IMUData, QuaternionData]] = None) -> None:
        super().__init__(init_list or [])

    def flush(self, num: int) -> "IMUCollection":
        """Flush the first num elements of the collection."""
        flushed_data, self.data = self.data[:num], self.data[num:]
        return IMUCollection(flushed_data)

    def to_csv(self, path: Path, mode: str = "w", header: bool = True) -> None:
        """Write the data to a CSV file."""
        header_data = self.data[0].__annotations__.keys()
        with path.open(mode=mode, encoding="utf-8", newline='\n') as file_ptr:
            wrt = writer(file_ptr)
            if header:
                wrt.writerow(header_data)
            for data in self.data:
                if len(header_data) == 4:
                    wrt.writerow([data.time, data.x, data.y, data.z])
                else:
                    wrt.writerow([data.time, data.w, data.x, data.y, data.z])

    def to_numpy(self) -> np.ndarray:
        """Convert the data to a numpy array."""
        if isinstance(self.data[0], QuaternionData):
            return np.array([np.array([d.time, d.w, d.x, d.y, d.z]) for d in self.data])
        return np.array([np.array([d.time, d.x, d.y, d.z]) for d in self.data])