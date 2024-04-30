import argparse

import cv2 as cv

from lib.models import TFLiteModel


def main(model_path: str) -> None:
    model = TFLiteModel(model_path)
    cap = cv.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        frame_height, frame_width, _ = frame.shape

        input_tensor = model.preprocess(frame)
        predictions = model.predict(input_tensor)
        detections = model.postprocess(predictions)

        for detection in detections:
            if detection.score > 0.3:
                detection.draw(frame)

        cv.imshow('Webcam Inference', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            cap.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_path', type=str, required=True)

    args = parser.parse_args()
    main(args.model_path)
