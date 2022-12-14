import logging
from colorama import Fore, Back


class LogWrapper:
    """Logging wrapper class"""

    def __init__(self, config={}, quiet=False):

        self.verbose = config.get('verbose', False)
        self.warn = not config.get('no_warn', not self.verbose)
        self.file = config.get('file', False)
        self.colors = config.get('colors', True)
        self.enabled = not quiet

        # Get new logger.
        self.logger = logging.getLogger('main_logger')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(module)s][%(levelname)s] %(message)s')

        if self.enabled:
            # File Handler.
            if self.file:
                fh = logging.FileHandler('output.log')
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

            # Console Handler.
            if self.colors:
                formatter = _CustomFormatter()

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        else:
            self.logger.disabled = True

    def lverbose(self, debug_text):
        """Log verbose messages"""
        if self.verbose:
            self.logger.debug(debug_text)

    def linfo(self, info_text):
        """Log execution information."""
        self.logger.info(info_text)

    def lwarn(self, warning):
        """Log warnings."""
        if self.warn:
            self.logger.warning(warning)

    def lerr(self, message):
        """Log errors."""
        self.logger.error(message)


class _CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors"""

    yellow = Fore.LIGHTYELLOW_EX
    red = Fore.LIGHTRED_EX
    reset = Fore.RESET + Back.RESET
    format = "[%(levelname)s] %(message)s"

    FORMATS = {
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
