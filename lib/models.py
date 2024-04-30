import cv2 as cv
import numpy as np
import tflite_runtime.interpreter as tflite

from lib.detections import Detection


class TFLiteModel(tflite.Interpreter):
    def __init__(self, model_path: str) -> None:
        super().__init__(model_path, num_threads=4)
        self.allocate_tensors()

        input_details = self.get_input_details()
        self.input_index = input_details[0]['index']
        self.input_dtype = input_details[0]['dtype']
        self.input_shape = input_details[0]['shape'][1:-1]

        output_details = self.get_output_details()
        self.output_indices = [output['index'] for output in output_details]

    def preprocess(self, input_tensor: np.ndarray) -> np.ndarray:
        tensor = cv.cvtColor(input_tensor, cv.COLOR_BGR2RGB)
        tensor = cv.resize(tensor, self.input_shape)
        tensor = tensor.astype(self.input_dtype)
        tensor = np.expand_dims(tensor, 0)

        return tensor

    def predict(self, input_tensor: np.ndarray) -> list[np.ndarray]:
        self.set_tensor(self.input_index, input_tensor)
        self.invoke()

        return [
            np.squeeze(self.get_tensor(output_index))
            for output_index in self.output_indices
        ]

    @staticmethod
    def postprocess(predictions: list[np.ndarray]) -> list[Detection]:
        detections = []

        bboxes, categories, scores, _ = predictions
        for bbox, category, score in zip(bboxes, categories, scores):
            label = category

            y_min, x_min, y_max, x_max = bbox
            position = [x_min, y_min, x_max, y_max]

            detection = Detection(position, score, label)
            detections.append(detection)

        return detections
