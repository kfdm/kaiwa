import argparse

from kaiwa.parsers.skype import SkypeCommand
from kaiwa.parsers.adium import AdiumCommand


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    SkypeCommand(subparsers)
    AdiumCommand(subparsers)

    args = parser.parse_args()
    args.execute(args)

if __name__ == '__main__':
    main()
