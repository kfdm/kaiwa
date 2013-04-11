from pprint import pprint
import os
import xml.etree.ElementTree as ET

from kaiwa import paths


class Skype(object):
    def __init__(self, skype_root, skype_user=None):
        self.root = skype_root
        if skype_user:
            self.user = os.path.join(self.root, skype_user)
        else:
            self.user = os.path.join(self.root, self._find_user_root())
        self.chat = os.path.join(self.user, 'main.db')

    def _find_user_root(self):
        default_path = os.path.join(self.root, 'shared.xml')
        tree = ET.parse(default_path)
        root = tree.getroot()
        return root.find("*/Account/Default").text


class SkypeCommand(object):
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('skype')
        self.parser.add_argument('--account')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, options):
        skype = Skype(paths.SKYPE_ROOT, options.account)
        pprint(skype.__dict__)
