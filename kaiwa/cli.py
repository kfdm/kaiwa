from pprint import pprint

from kaiwa import paths
from kaiwa.parsers.skype import Skype


def main():
    skype = Skype(paths.SKYPE_ROOT)
    pprint(skype.__dict__)

if __name__ == '__main__':
    main()
