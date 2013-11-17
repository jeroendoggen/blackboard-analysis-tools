"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

# TODO: report all students that hand in the assignment after the deadline
# TODO: ...


from __future__ import print_function, division  # We require Python 2.6+

#import logging
import os
#import zipfile
#import shutil
#import sys
#import datetime
#import time
#import StringIO
#from multiprocessing import Process

#try:
    #from Queue import Queue
#except ImportError:
    #from queue import Queue

#from email.utils import parseaddr

from blackboard_analysis_tools.settings import Settings
from blackboard_analysis_tools.timing_analyser import TimingAnalyser
from blackboard_analysis_tools.logger import Logger
from blackboard_analysis_tools.unzipper import Unzipper
from blackboard_analysis_tools.analyser import Analyser
from blackboard_analysis_tools.reporter import Reporter
from blackboard_analysis_tools.input_output import InputOutput


class BlackboardAnalysisTools:
    """ Contains all the tools to analyse Blackboard assignments """

    def __init__(self):
        self.settings = Settings()
        self.timing_analyser = TimingAnalyser()
        self.mylogger = Logger(self.settings.logfile)
        self.reporter = Reporter(self.settings)
        self.unzipper = Unzipper(self.settings.input_path, self.settings.output_path, self.mylogger, self.reporter)
        self.analyser = Analyser(self.settings.input_path, self.settings.output_path, self.mylogger, self.settings, self.reporter)
        self.input_output = InputOutput(self.settings.input_path, self.settings.output_path, self.mylogger, self.settings, self.reporter, self.analyser)

    def run(self):
        #""" Run the program (call this from main) """
        self.unzipper.generate_zip_files_list()
        self.unzipper.unzip()
        self.analyser.generate_txt_files_list()
        self.analyser.analyse_txt_files()
        self.input_output.run()
        #TODO does not work because of cyclic passing of instances
        self.reporter.write_statistics(self.analyser.studentnames_list)
        self.input_output.cleanup()

    def exit_value(self):
        #"""TODO: Generate the exit value for the application."""
        #if (self.errors == 0):
        if (True):
            return 0
        else:
            return 42
