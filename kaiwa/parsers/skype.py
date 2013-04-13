import os
import sqlite3
import xml.etree.ElementTree as ET
import shutil

from kaiwa import paths


class Conversation(object):
    def __init__(self, row, output):
        self.raw = row
        self.id = row['id']
        self.title = row['displayname'] if row['displayname'] else ""
        self.slug = "".join([x if x.isalnum() else "_" for x in self.title])
        self.path = os.path.join(output, '{0}-{1}'.format(self.id, self.slug))

    def __str__(self):
        return self.title.encode('utf8', 'replace')

    def write(self, row):
        with open(self.path + '.txt', 'a') as fp:
            try:
                fp.write('{0} - {1}: {2}\n'.format(
                    row['timestamp'],
                    row['author'],
                    row['body_xml']
                ))
            except (AttributeError, UnicodeEncodeError):
                pass


class Skype(object):
    def __init__(self, skype_root, skype_user=None, output=None):
        self.root = skype_root
        if skype_user:
            self.user = os.path.join(self.root, skype_user)
        else:
            self.user = os.path.join(self.root, self._find_user_root())
        self.output = output
        self.chat = os.path.join(self.user, 'main.db')

        if not os.path.exists(self.output):
            os.makedirs(self.output)

    def _find_user_root(self):
        default_path = os.path.join(self.root, 'shared.xml')
        tree = ET.parse(default_path)
        root = tree.getroot()
        return root.find("*/Account/Default").text

    def convert_logs(self):
        conn = sqlite3.connect(self.chat)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('SELECT * FROM Conversations')

        conversations = {}

        while True:
            row = c.fetchone()
            if row is None:
                break
            conversations[row['id']] = Conversation(row, self.output)

        c.execute('SELECT * FROM Messages')
        while True:
            row = c.fetchone()
            if row is None:
                break
            conversations[row['convo_id']].write(row)


class SkypeCommand(object):
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('skype')
        self.parser.add_argument('--account')
        self.parser.add_argument(
            '--output',
            default=os.path.join(paths.OUTPUT, 'Skype')
        )
        self.parser.add_argument('--clear', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, options):
        if options.clear:
            if os.path.exists(options.output):
                print 'Removing', options.output
                shutil.rmtree(options.output)
        Skype(paths.SKYPE_ROOT, options.account, options.output).convert_logs()
