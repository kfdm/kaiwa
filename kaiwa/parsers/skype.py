import os
import xml.etree.ElementTree as ET


class Skype(object):
    def __init__(self, skype_root, skype_user=None):
        self.root = skype_root
        self.user = skype_user if skype_user else \
            os.path.join(self.root, self._find_user_root())
        self.chat = os.path.join(self.user, 'main.db')

    def _find_user_root(self):
        default_path = os.path.join(self.root, 'shared.xml')
        tree = ET.parse(default_path)
        root = tree.getroot()
        return root.find("*/Account/Default").text
