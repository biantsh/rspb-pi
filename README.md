# Raspberry Pi

Security camera project for Computer Systems Engineering, involving a Raspberry
Pi powered by AI object detection.

*(Work in progress.)*

## Environment Setup

Make sure you have a valid installation of Python 3.10, then from the project's
root run:

```commandline
pip install -e ../rspb-pi/
```

## Assets

- `assets/demo/` contains the model and code required to test a dummy model and
gauge its runtime latency.

- `assets/emulator` contains the necessary files for creating a Raspberry Pi 3B
virtual machine. See `docs/emulator-setup.md` for instructions.

- `assets/models` contains fully trained models to be run on the final project.

## Scripts

- To prepare and filter the dataset for training the object detection model, 
see `scripts/filter-coco.py`.

- To get an idea of the distribution of categories in the filtered dataset
see `scripts/cat-distr.py`.

- To run the object detection model on your device's webcam, see
`scripts/run-tflite.py`.

## Lib

Contains reusable modules to be imported into scripts and application code.
