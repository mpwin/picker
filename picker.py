import argparse
import os
import random
from typing import Iterator
import yaml


def get_arguments() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument(
        '-u','--uniform',
        action='store_true',
        help='uniform sampling (default)',
        )
    parser.add_argument(
        '-w','--weighted',
        action='store_true',
        help='weighted sampling',
        )

    arguments = parser.parse_args()

    return (
        arguments.path,
        'weighted' if arguments.weighted else 'uniform',
        )


def uniform_pick(path: str) -> str:
    def yield_filepaths(path: str) -> Iterator[str]:
        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for filename in filenames:
                    yield os.path.join(dirpath, filename)
        else:
            yield path

    def collect_leaves(
            node: str | dict | list, path: str, leaves: list[str] | None = None
            ) -> list[str]:
        if leaves is None:
            leaves = []

        if isinstance(node, dict):
            for key, value in node.items():
                collect_leaves(value, os.path.join(path, str(key)), leaves)
        elif isinstance(node, list):
            for item in node:
                collect_leaves(item, path, leaves)
        else:
            leaves.append(os.path.join(path, str(node)))

        return leaves

    leaves = []

    for filepath in yield_filepaths(path):
        with open(filepath) as file:
            data = yaml.safe_load(file)
        leaves.extend(collect_leaves(data, filepath))

    print(f'Uniform Pick | {len(leaves)} Leaves')
    return format_path(random.choice(leaves))


def weighted_pick(path: str) -> str:
    while os.path.isdir(path):
        pick = random.choice(os.listdir(path))
        path = os.path.join(path, pick)

    with open(path) as file:
        pick = random.choice(yaml.safe_load(file))

    while type(pick) is dict or type(pick) is list:
        if type(pick) is dict:
            for key, value in pick.items():
                path = os.path.join(path, key)
                pick = value

        if type(pick) is list:
            pick = random.choice(pick)

    print('Weighted Pick')
    return format_path(os.path.join(path, pick))


def format_path(path: str) -> str:
    return path.replace('\\', ' -> ').replace('.yaml', '')


def main():
    path, mode = get_arguments()

    match mode:
        case 'uniform':
            pick = uniform_pick(path)
        case 'weighted':
            pick = weighted_pick(path)

    print(pick)


if __name__ == '__main__':
    main()
