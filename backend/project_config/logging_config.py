import logging


class ConsoleStyleFilter(logging.Filter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles = {
            'DEBUG': '\u001b[1;36m',
            'INFO': '\u001b[1;32m',
            'WARNING': '\u001b[1;33m',
            'ERROR': '\u001b[1;31m',
            'CRITICAL': '\u001b[1;33;41m',
        }
        self.reset_styles = '\u001b[0m'

    def filter(self, record):
        record.style = self.styles.get(record.levelname, self.reset_styles)
        record.reset_styles = self.reset_styles
        return True
