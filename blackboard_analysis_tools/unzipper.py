"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import os
import zipfile

from blackboard_analysis_tools.logger import Logger


class Unzipper():
    """ Timer to check the speed of the tool itself (benchmarking) """
    zip_files_list = []

    def __init__(self, input_path, output_path, logger, reporter):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = logger
        self.reporter = reporter

    def generate_zip_files_list(self):
        """ Generate the list with the zip files """
        try:
            os.chdir(self.input_path)
            for inputfile in os.listdir(self.input_path):
                if os.path.isfile(os.path.join(self.input_path, inputfile)):
                    if inputfile.endswith(".zip"):
                        self.zip_files_list.append(inputfile)
                        self.reporter.assignment_counter += 1
        except OSError:
            self.logger.exit_program("reading the .zip files (does the output folder exist?)")

    def unzip(self):
        """ Unzip all the .zip assignment files """
        print("Number of .zip files: ", end="")
        counter = 0
        for index, current_file in enumerate(self.zip_files_list):
            counter += 1
        print(counter)
        print("")
        for index, current_file in enumerate(self.zip_files_list):
            shortname = str(counter) + ".zip"
            self.unzip_onefile(current_file, shortname)
            counter += 1

    def unzip_onefile(self, current_file, shortname):
        """ Unzip one file """
        os.rename(current_file, shortname)
        myzip = zipfile.ZipFile(shortname)
        myzip.extractall(self.output_path)
        myzip.close()
        os.rename(shortname, current_file)
