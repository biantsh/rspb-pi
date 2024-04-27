"""Filter a COCO dataset to only include the specified categories.

Example usage:
    python3 filter-coco.py  \
      --input_path train.json
      --output_path train-filtered.json
      --categories person bicycle car motorcycle

Note: Download the dataset from: https://cocodataset.org/#download
"""

import argparse
import json


def filter_dataset(dataset: dict, categories: list[str]) -> dict:
    id_map = {cat['id']: cat['name'] for cat in dataset['categories']}

    dataset['categories'] = [cat for cat in dataset['categories']
                             if cat['name'] in categories]

    dataset['annotations'] = [anno for anno in dataset['annotations']
                              if id_map[anno['category_id']] in categories]

    return dataset


def main(input_path: str, output_path: str, categories: list[str]) -> None:
    with open(input_path, 'r') as json_file:
        coco_dataset = json.load(json_file)

    coco_dataset = filter_dataset(coco_dataset, categories)

    with open(output_path, 'w') as json_file:
        json.dump(coco_dataset, json_file, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True)
    parser.add_argument('-o', '--output_path', type=str, required=True)
    parser.add_argument('-c', '--categories', type=list, nargs='+',
                        default=['person', 'bicycle', 'car', 'motorcycle'])

    args = parser.parse_args()
    main(args.input_path, args.output_path, args.categories)
