import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-d','--deep', action='store_true')
    parser.add_argument('-f','--flat', action='store_true')

    arguments = parser.parse_args()

    return (
        arguments.path,
        'deep' if arguments.deep else 'flat',
        )


def main():
    node, mode = get_arguments()
    print(node, mode)


if __name__ == '__main__':
    main()
