import argparse
import os
import random
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
    def collect_filepaths(path: str) -> list[str]:
        filepaths = []

        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for filename in filenames:
                    filepaths.append(os.path.join(dirpath, filename))
        else:
            filepaths.append(path)

        return filepaths

    def collect_leaves(
            node: str | dict | list, path: str, leaves: list[str] | None = None
            ) -> list[str]:
        if leaves is None:
            leaves = []

        if isinstance(node, dict):
            for key, value in node.items():
                collect_leaves(value, os.path.join(path, key), leaves)
        elif isinstance(node, list):
            for item in node:
                collect_leaves(item, path, leaves)
        else:
            leaves.append(os.path.join(path, node))

        return leaves

    def format_path(path: str) -> str:
        return path.replace('\\', ' -> ').replace('.yaml', '')

    filepaths = collect_filepaths(path)
    leaves = []

    for filepath in filepaths:
        with open(filepath) as file:
            data = yaml.safe_load(file)
        leaves.extend(collect_leaves(data, filepath))

    return format_path(random.choice(leaves))


def weighted_pick(path: str) -> str:
    while os.path.isdir(path):
        pick = random.choice(os.listdir(path))
        path = os.path.join(path, pick)
    print(path)

    with open(path) as file:
        path = random.choice(yaml.safe_load(file))
    print(path)

    while type(path) is dict or type(path) is list:
        if type(path) is dict:
            for k, v in path.items():
                print(k, end=' -> ')
                path = v

        if type(path) is list:
            path = random.choice(path)

    return path


def main():
    path, mode = get_arguments()
    print(path, mode)

    match mode:
        case 'uniform':
            pick = uniform_pick(path)
        case 'weighted':
            pick = weighted_pick(path)

    print(pick)


if __name__ == '__main__':
    main()
