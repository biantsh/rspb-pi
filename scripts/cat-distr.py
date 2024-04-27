"""Provide the category distribution (no. of occurrences) for a COCO dataset.

Example usage:
    python3 cat-distr.py  \
      --input_path train.json
"""

import argparse
import json
from collections import defaultdict


def get_instance_counts(dataset: dict) -> dict:
    category_map = {cat['id']: cat['name'] for cat in dataset['categories']}
    instance_counts = defaultdict(lambda: 0)

    for anno in dataset['annotations']:
        cat_id = anno['category_id']
        cat_name = category_map[cat_id]

        instance_counts[cat_name] += 1

    return instance_counts


def main(input_path: str) -> None:
    with open(input_path, 'r') as json_file:
        coco_dataset = json.load(json_file)

    instance_counts = get_instance_counts(coco_dataset)
    for category, count in instance_counts.items():
        print(f'{category.title()}: {count:,} instances')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True)

    args = parser.parse_args()
    main(args.input_path)
