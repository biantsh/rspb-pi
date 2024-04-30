import time
from collections import deque
from threading import Thread

import cv2 as cv
import numpy as np


class WebcamReader(cv.VideoCapture):
    def __init__(self, mirrored=True, show_fps=False) -> None:
        super().__init__(0)

        self.mirrored = mirrored
        self.framerate_tracker = FramerateTracker() \
            if show_fps else None

        self.native_framerate = self.get(cv.CAP_PROP_FPS)
        self.latency = 1. / self.native_framerate

        self.prev_update_time = time.process_time()
        self.is_opened = False
        self.frame = None

    def _update(self) -> None:
        while self.is_opened:
            # Ensure frames are read at same speed as innate framerate
            current_time = time.process_time()
            elapsed_time = current_time - self.prev_update_time

            if elapsed_time < self.latency:
                continue

            self.prev_update_time = current_time
            success, self.frame = self.read()

            if not success:
                self.close()

    def start(self) -> None:
        self.is_opened = True
        Thread(target=self._update).start()

    def close(self) -> None:
        self.is_opened = False

    def get_frame(self) -> np.ndarray | None:
        return cv.flip(self.frame, 1) \
            if self.mirrored else self.frame

    def wait_key(self, close_key: str) -> None:
        pressed_key = cv.waitKey(1)

        if pressed_key & 0xFF == ord(close_key):
            self.close()

    def show(self, frame: np.ndarray) -> None:
        if self.framerate_tracker:
            self.framerate_tracker.update()
            self.framerate_tracker.show_framerate(frame)

        cv.imshow('Webcam Inference', frame)


class FramerateTracker:
    def __init__(self, buffer_length: int = 30) -> None:
        self.updates = deque(maxlen=buffer_length)

    def update(self) -> None:
        self.updates.append(time.process_time())

    def get_framerate(self) -> float:
        if len(self.updates) < 2:
            return 0.

        latency = np.mean(np.diff(list(self.updates)))
        framerate = (1. / latency).astype(float)

        return framerate

    def show_framerate(self, frame: np.ndarray) -> None:
        framerate = self.get_framerate()
        cv.putText(frame, f'{framerate:.2f} FPS',
                   (0, 30), 2, 1, (255, 0, 0), 1)
