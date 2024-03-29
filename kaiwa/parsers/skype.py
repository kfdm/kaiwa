import logging
import os
import shutil
import sqlite3
import time
import xml.etree.ElementTree as ET

from kaiwa import paths

logger = logging.getLogger(__name__)


class Conversation(object):
    def __init__(self, row, output):
        self.raw = row
        self.id = row['id']
        self.title = row['displayname'] if row['displayname'] else ""
        self.slug = "".join([x if x.isalnum() else "_" for x in self.title])
        self.path = os.path.join(output, '{0}-{1}'.format(self.id, self.slug))

    def write(self, row):
        with open(self.path + '.txt', 'a') as fp:
            try:
                fp.write('{0} - {1}: {2}\n'.format(
                    time.ctime(int(row['timestamp'])),
                    row['author'],
                    row['body_xml']
                ))
            except (AttributeError, UnicodeEncodeError):
                pass


class Skype(object):
    def __init__(self, skype_root, skype_user, output_root):
        self.root = skype_root

        if skype_user is None:
            skype_user = self._find_default_user()

        self.user = os.path.join(self.root, skype_user)
        self.output = output_root
        self.chat = os.path.join(self.user, 'main.db')

        if not os.path.exists(self.output):
            logger.info('Creating output directory: %s', self.output)
            os.makedirs(self.output)

    def _find_default_user(self):
        default_path = os.path.join(self.root, 'shared.xml')
        tree = ET.parse(default_path)
        root = tree.getroot()
        return root.find("*/Account/Default").text

    def convert_logs(self):
        conn = sqlite3.connect(self.chat)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        conversations = {}

        logger.info('Reading conversations')
        c.execute('SELECT * FROM Conversations')
        while True:
            row = c.fetchone()
            if row is None:
                break
            conversations[row['id']] = Conversation(row, self.output)

        logger.info('Reading messages')
        c.execute('SELECT * FROM Messages')
        while True:
            row = c.fetchone()
            if row is None:
                break
            conversations[row['convo_id']].write(row)


class SkypeCommand(object):
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('skype')
        self.parser.add_argument(
            '--account',
            help="Skype account handle"
        )
        self.parser.add_argument(
            '--output',
            default=os.path.join(paths.OUTPUT, 'Skype'),
            help="Output path for logs (%(default)s)"
        )
        self.parser.add_argument(
            '-v', '--verbosity',
            choices=['warn', 'info', 'debug'],
            default='warn'
        )
        self.parser.set_defaults(execute=self.execute)

    def execute(self, options):
        logging.basicConfig(level=logging.getLevelName(options.verbosity.upper()))
        if os.path.exists(options.output):
            logger.info('Removing %s', options.output)
            shutil.rmtree(options.output)
        Skype(paths.SKYPE_ROOT, options.account, options.output).convert_logs()
