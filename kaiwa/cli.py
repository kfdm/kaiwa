import argparse

from kaiwa.parsers.skype import SkypeCommand


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    SkypeCommand(subparsers)

    args = parser.parse_args()
    args.execute(args)

if __name__ == '__main__':
    main()
