import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-d','--deep', action='store_true')
    parser.add_argument('-f','--flat', action='store_true')

    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
