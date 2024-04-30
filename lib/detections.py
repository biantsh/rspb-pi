import cv2 as cv
import numpy as np


class Detection:
    def __init__(self,
                 position: list[float],
                 score: float,
                 label: str
                 ) -> None:
        self.position = position
        self.score = score
        self.label = label

    def draw(self, frame: np.ndarray) -> None:
        x_min, y_min, x_max, y_max = self.position
        height, width, _ = frame.shape

        x_min, x_max = int(x_min * width), int(x_max * width)
        y_min, y_max = int(y_min * height), int(y_max * height)

        label_text = f'{self.label} ({int(self.score * 100)}%)'
        cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv.putText(frame, label_text, (x_min, y_min - 5), 2, 1, (0, 255, 0), 1)
