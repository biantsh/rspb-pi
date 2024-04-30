"""Run a TFLite CenterNet object detection model on the native webcam.

Example usage:
    python3 run-tflite.py  \
      --model_path model.tflite
      --category_file categories.json

Note: The required files can be found under assets/models.
"""

import argparse

from lib.models import TFLiteModel
from lib.webcam import WebcamReader


def main(model_path: str, category_file: str) -> None:
    model = TFLiteModel(model_path, category_file)
    webcam = WebcamReader(show_fps=True)
    webcam.start()

    while webcam.is_opened:
        frame = webcam.get_frame()
        if frame is None:
            continue

        frame_height, frame_width, _ = frame.shape

        input_tensor = model.preprocess(frame)
        predictions = model.predict(input_tensor)
        detections = model.postprocess(predictions)

        for detection in detections:
            detection.draw(frame)

        webcam.show(frame)
        webcam.wait_key(close_key='q')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_path', type=str, required=True)
    parser.add_argument('-c', '--category_file', type=str, required=True)

    args = parser.parse_args()
    main(args.model_path, args.category_file)
