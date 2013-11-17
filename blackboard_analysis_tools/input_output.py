"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import os
import shutil


class InputOutput():
    """ Timer to check the speed of the tool itself (benchmarking) """

    def __init__(self, input_path, output_path, logger, settings, reporter, analyser):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = logger
        self.settings = settings
        self.reporter = reporter
        self.analyser = analyser

    def run(self):
        """ Run all the tests """
        self.create_student_folders()
        self.move_student_files()
        self.process_badly_named_files()

    def create_student_folders(self):
        """ Create the needed student folders """
        for student in self.analyser.studentnames_list:
            if not os.path.exists(self.settings.output_path + student):
                os.makedirs(self.settings.output_path + student)

    def move_student_files(self):
        """ Move assignment files to student folders (using one process)"""
        try:
            for inputfile in os.listdir(self.settings.output_path):
                if os.path.isfile(os.path.join(self.settings.output_path, inputfile)):
                    # TODO: use a list for this?
                    self.move_files(inputfile)
        except OSError:
            self.exit_program("moving student files to output folder")

    def move_files(self, inputfile):
        """ Move assignment file to the correct student folder """
        #print(inputfile)
        for student in self.analyser.studentnames_list:
            #print(student)
            if '.' in student:
                student = self.swap_string(student)
                if student in inputfile:
                    #print(student)
                    student = self.swap_string(student)
                    if os.path.exists(student):
                        shutil.copy2(inputfile, self.output_path + student)
                        #os.remove(inputfile)

    def process_badly_named_files(self):
        #"""
        #Scan for bad filenames (where student mail is not in the filename)
        #Copy these files to 'studentname' folder anyway
        #Add logging to provide some feedback
        #"""
        for txtfile in self.analyser.txt_files_list:
            studentname = self.analyser.get_studentname(txtfile)
            filename = self.analyser.get_filename(txtfile)
            if filename is not None:
                assignment = self.analyser.get_assignment(txtfile)
                self.reporter.bad_filenames_counter += 1
                self.reporter.bad_filenames += " - " + str(studentname) + ": "
                self.reporter.bad_filenames += str(filename) + " --> in assignment: " + assignment
                shutil.copy2(filename, self.output_path + studentname)

    def swap_string(self, string):
        """ Swap strings around '.' symbol (for email address processing)"""
        #TODO: used multiple times (move to 'tools' class?
        string0 = string.split(".")[0]
        string1 = string.split(".")[1]
        string = string1 + "." + string0
        return(string)

    def cleanup(self):
        """ Clean up the output folder by removing all 'temp files' """
        try:
            for inputfile in os.listdir(self.settings.output_path):
                if os.path.isfile(os.path.join(self.settings.output_path, inputfile)):
                    if self.analyser.is_not_analysistool_file(inputfile):
                        #print(inputfile)
                        os.remove(inputfile)
        except OSError:
            self.logger.exit_program("cleaning up folders")
