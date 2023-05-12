"""Risk namespace for data management."""

from collections import Counter, UserList
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import List
from csv import writer

import numpy as np


@dataclass(frozen=True)
class Risk:
    """Define the data structure for the risk data."""

    time: float = 0.0
    right_abduction: bool = False
    right_flexion: bool = False
    right_rotation: bool = False
    right_elevation: bool = False
    left_abduction: bool = False
    left_flexion: bool = False
    left_rotation: bool = False
    left_elevation: bool = False

    def __and__(self, other: "Risk"):
        return Risk(
            time=self.time,
            right_abduction=self.right_abduction and other.right_abduction,
            right_flexion=self.right_flexion and other.right_flexion,
            right_rotation=self.right_rotation and other.right_rotation,
            right_elevation=self.right_elevation and other.right_elevation,
            left_abduction=self.left_abduction and other.left_abduction,
            left_flexion=self.left_flexion and other.left_flexion,
            left_rotation=self.left_rotation and other.left_rotation,
            left_elevation=self.left_elevation and other.left_elevation,
        )

    def __or__(self, other: "Risk"):
        return Risk(
            time=self.time,
            right_abduction=self.right_abduction or other.right_abduction,
            right_flexion=self.right_flexion or other.right_flexion,
            right_rotation=self.right_rotation or other.right_rotation,
            right_elevation=self.right_elevation or other.right_elevation,
            left_abduction=self.left_abduction or other.left_abduction,
            left_flexion=self.left_flexion or other.left_flexion,
            left_rotation=self.left_rotation or other.left_rotation,
            left_elevation=self.left_elevation or other.left_elevation,
        )

    def __invert__(self):
        return Risk(
            time=self.time,
            right_abduction=not self.right_abduction,
            right_flexion=not self.right_flexion,
            right_rotation=not self.right_rotation,
            right_elevation=not self.right_elevation,
            left_abduction=not self.left_abduction,
            left_flexion=not self.left_flexion,
            left_rotation=not self.left_rotation,
            left_elevation=not self.left_elevation,
        )

    def to_numpy(self) -> np.ndarray:
        """
            Convert the data to a numpy array.
            :return: A numpy array with the data.
            :rtype: np.ndarray
        """
        return np.array([
            self.time,
            self.right_abduction,
            self.right_flexion,
            self.right_rotation,
            self.right_elevation,
            self.left_abduction,
            self.left_flexion,
            self.left_rotation,
            self.left_elevation
        ])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Risk(time={self.time}, right_abduction={self.right_abduction}, right_flexion={self.right_flexion}, right_rotation" \
               f"={self.right_rotation}, right_elevation={self.right_elevation}, left_abduction={self.left_abduction}, left_flexion" \
               f"={self.left_flexion}, left_rotation={self.left_rotation}, left_elevation={self.left_elevation})"


class RiskCollection(UserList):
    """Collection of Risks"""

    def __init__(self, init_list: List[Risk] = None) -> None:
        super().__init__(init_list or [])

    def flush(self, num: int) -> "RiskCollection":
        """Flush the first num elements of the collection."""
        flushed_data, self.data = self.data[:num], self.data[num:]
        return RiskCollection(flushed_data)

    def to_numpy(self) -> np.ndarray:
        """
            Convert the data to a numpy array.
            :return: A numpy array with the data.
            :rtype: np.ndarray
        """
        return np.array([d.to_numpy() for d in self.data])

    class Aggregation:
        """Aggregation of the data."""

        def __init__(self, data: List[Risk]):
            self.data = data

        def logical_and(self) -> Risk:
            """Return the logical and of all the risks."""
            return reduce(lambda x, y: x & y, self.data)

        def logical_or(self) -> Risk:
            """Return the logical or of all the risks."""
            return reduce(lambda x, y: x | y, self.data)

        def most_common(self) -> Risk:
            """Return the most common value of all the risks."""
            return Risk(
                time=self.data[0].time,
                right_abduction=Counter([d.right_abduction for d in self.data]).most_common(1)[0][0],
                right_flexion=Counter([d.right_flexion for d in self.data]).most_common(1)[0][0],
                right_rotation=Counter([d.right_rotation for d in self.data]).most_common(1)[0][0],
                right_elevation=Counter([d.right_elevation for d in self.data]).most_common(1)[0][0],
                left_abduction=Counter([d.left_abduction for d in self.data]).most_common(1)[0][0],
                left_flexion=Counter([d.left_flexion for d in self.data]).most_common(1)[0][0],
                left_rotation=Counter([d.left_rotation for d in self.data]).most_common(1)[0][0],
                left_elevation=Counter([d.left_elevation for d in self.data]).most_common(1)[0][0],
            )

    def aggregate(self) -> Aggregation:
        """Return an aggregation of the data."""
        return self.Aggregation(self.data)

    def to_csv(self, path: Path, mode: str = "w", header: bool = True) -> None:
        """Write the data to a CSV file."""
        header_data = self.data[0].__annotations__.keys()
        with path.open(mode=mode, encoding="utf-8", newline='\n') as file_ptr:
            wrt = writer(file_ptr)
            if header:
                wrt.writerow(header_data)
            for data in self.data:
                wrt.writerow(data.to_numpy())