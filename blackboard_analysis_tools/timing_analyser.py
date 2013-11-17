"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import datetime


class TimingAnalyser:
    """ Timer to check the speed of the tool itself (benchmarking) """
    starttime = 0
    lasttime = 0

    def __init__(self):
        self.starttime = datetime.datetime.now()
        self.lasttime = datetime.datetime.now()

    def timedebug(self, function, message):
        """Print the current runtime + a message to the terminal """
        ##TODO timing is off by one!
        now = datetime.datetime.now()
        print(message, end=" ")
        function()
        delta = now - self.lasttime
        delta = delta.total_seconds()
        print("this took: " + str(delta) + " seconds")
        self.lasttime = datetime.datetime.now()
