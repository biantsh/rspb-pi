import argparse

from lib.models import TFLiteModel
from lib.webcam import WebcamReader


def main(model_path: str) -> None:
    webcam = WebcamReader(show_fps=True)
    model = TFLiteModel(model_path)

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
            if detection.score > 0.3:
                detection.draw(frame)

        webcam.show(frame)
        webcam.wait_key(close_key='q')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_path', type=str, required=True)

    args = parser.parse_args()
    main(args.model_path)
