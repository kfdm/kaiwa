class AdiumCommand(object):
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('adium')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, options):
        raise NotImplementedError()
