"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import os

from email.utils import parseaddr

from blackboard_analysis_tools.logger import Logger


class Analyser():
    """ Timer to check the speed of the tool itself (benchmarking) """
    txt_files_list = []
    studentnames_list = []

    def __init__(self, input_path, output_path, logger, settings, reporter):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = logger
        self.settings = settings
        self.reporter = reporter

    def generate_txt_files_list(self):
        """ Generate the list with the txt files """
        try:
            os.chdir(self.output_path)
            for inputfile in os.listdir(self.output_path):
                    if os.path.isfile(os.path.join(self.output_path, inputfile)):
                        if self.is_not_analysistool_file(inputfile):
                            self.reporter.txt_files_counter += 1
                            if inputfile.endswith(".txt"):
                                self.txt_files_list.append(inputfile)
            #print(self.txt_files_list)
        except OSError:
            self.exit_program("reading the .txt files")

    def analyse_txt_files(self):
        """ Analyse all the .txt files """
        self.generate_studentnames_list()
        #print(self.studentnames_list)
        self.studentnames_list.sort()
        #print(self.studentnames_list)
        self.detect_late_assignments()

    def generate_studentnames_list(self):
        """ Get the student name from a given txt file """
        for txtfile in self.txt_files_list:
            self.studentnames_list.append(self.get_studentname(txtfile))

    def get_studentname(self, txtfile):
        """ Get the student name from a given txt file """
        studentname = ""
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.settings.name_detection_string in line:
                    studentname = parseaddr(line)[0]
                    #print(email)
                    #print(studentname)
                    studentname = studentname[:-self.settings.email_domain_length]
                    #print(studentname)
                    studentname = self.swap_string(studentname)
                    #print(email)
            inputfile.close()
        return(studentname)

    def is_not_analysistool_file(self, inputfile):
        """ Detect is a file is a logfile, outputfile from this tool """
        if inputfile != self.settings.studentlist_filename_final:
            if inputfile != self.settings.logfile:
                if inputfile != self.settings.summary_file:
                    return(True)
        else:
            return(False)
    def swap_string(self, string):
        """ Swap strings around '.' symbol (for email address processing)"""
        #print(string)
        string0 = string.split(".")[0]
        #print(string0)
        string1 = string.split(".")[1]
        #print(string1)
        string = string1 + "." + string0
        #print(string)
        return(string)

    def detect_late_assignments(self):
        """ Detect is an assignment is handed in late from a given .txt file """
        for txtfile in self.txt_files_list:
            with open(txtfile, 'r') as inputfile:
                for line in inputfile:
                    if self.settings.assignment_late_detection_string in line:
                        self.reporter.late_assignment_counter += 1
                        print("Late file: ", end="")
                        print(inputfile.name)
                        #print(line)
                        line = line.lstrip(self.assignmentname_detection_string)
                        #line = line.rstrip("NM\n")
                        #print(line)
                        #TODO: this should return something and go to the report (was not available in previous version)

    def get_filename(self, txtfile):
        """ Get the assignment filename from a given txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.settings.filename_detection_string in line:
                    # detect bad bad filename (not containing student email)
                    if line.find(self.settings.filename_analysis_string) == -1:
                        line = line.lstrip('\t')
                        line = line.lstrip(self.settings.filename_detection_string)
                        line = line.lstrip(" ")
                        line = line.rstrip()
                        return(line)

    def get_assignment(self, txtfile):
        """ Get the assignment name from a given .txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.settings.assignmentname_detection_string in line:
                    line = line.lstrip(self.settings.assignmentname_detection_string)
                    #line = line.rstrip("NM\n")
                    return(line)
