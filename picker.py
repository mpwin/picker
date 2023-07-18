import argparse
import os
import random
import yaml


def get_arguments():
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


def uniform_pick(node):
    def get_leaves(node, leaves=None):
        if leaves is None:
            leaves = []

        if isinstance(node, dict):
            for value in node.values():
                get_leaves(value, leaves)
        elif isinstance(node, list):
            for item in node:
                get_leaves(item, leaves)
        else:
            leaves.append(node)

        return leaves

    while os.path.isdir(node):
        pick = random.choice(os.listdir(node))
        node = os.path.join(node, pick)

    with open(node) as file:
        data = yaml.safe_load(file)

    leaves = get_leaves(data)
    print(leaves)
    print(random.choice(leaves))


def weighted_pick(node):
    while os.path.isdir(node):
        pick = random.choice(os.listdir(node))
        node = os.path.join(node, pick)
    print(node)

    with open(node) as file:
        node = random.choice(yaml.safe_load(file))
    print(node)

    while type(node) is dict or type(node) is list:
        if type(node) is dict:
            for k, v in node.items():
                print(k, end=' -> ')
                node = v

        if type(node) is list:
            node = random.choice(node)
    print(node)


def main():
    node, mode = get_arguments()
    print(node, mode)

    match mode:
        case 'uniform':
            uniform_pick(node)
        case 'weighted':
            weighted_pick(node)


if __name__ == '__main__':
    main()
