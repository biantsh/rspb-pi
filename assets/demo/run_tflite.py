"""Run a TFLite model and display average latency.

Usage: python3 --model model.tflite
"""

import argparse
import time

import tflite_runtime.interpreter as tflite
import numpy as np


def main(model_path: str) -> None:
    interpreter = tflite.Interpreter(model_path, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    input_index = input_details[0]['index']
    input_shape = input_details[0]['shape']

    for _ in range(100):
        time_start = time.time()

        input_data = np.array(np.random.random(input_shape), dtype=np.float32)
        interpreter.set_tensor(input_index, input_data)
        interpreter.invoke()

        process_time = time.time() - time_start
        print(f'Latency (seconds): {process_time}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, required=True)

    args = parser.parse_args()
    main(args.model)
