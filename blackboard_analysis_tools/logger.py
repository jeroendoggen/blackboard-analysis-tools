"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import logging
import sys


class Logger():
    """ Logging class """
    logger = 0

    def __init__(self, logfile):
        self.set_logfile(logfile)
        self.info("Starting 'analysis tool': ")

    def set_logfile(self, logfile):
        """Set the logfile: for error & info messages"""
        try:
            self.logfile = logfile
            logging.basicConfig(filename=self.logfile,
                                level=logging.DEBUG,
                                format="%(asctime)s %(name)s %(levelname)s %(message)s")
            self.logger = logging.getLogger(__name__)
        except IOError:
            self.exit_program("opening the logfile (do you have write permission?)")

    def exit_program(self, message):
        """ Exit the program with a message
           TODO: this should move somewhere else (needed in multiple places)
        """
        print("Error while " + message)
        print("Closing application")
        sys.exit()

    def info(self, message):
        self.logger.info(message)
