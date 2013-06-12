"""
    Blackboard Grade center analyser
    A tool to analyse assignments downloaded from the Blackboard grade center
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

# TODO: report all students that hand in the assignment after the deadline
# TODO: ...


from __future__ import print_function, division  # We require Python 2.6+

import logging
import os
import zipfile
import time
import shutil
import glob
from email.utils import parseaddr


class Blackboard_analysis_tools:
    errors = 0
    zip_files_list = []
    txt_files_list = []
    email_list = []
    name_detection_string = "Naam:"
    filename_detection_string = "Bestandsnaam:"
    assignmentname_detection_string = "Opdracht:"
    filename_analysis_string = "@student.artesis.be"
    script_path = os.getcwd()
    input_path = script_path + "/input/"
    output_path = script_path + "/output/"
    logfile = "blackboard_analysis_tools.log"
    logger = 0
    student_counter = 0
    bad_filenames_counter = 0
    assignment_counter = 0
    bad_filenames = ""
    studentlist_filename = "studentlist_temp.txt"
    studentlist_filename_final = "studentlist.txt"

    def init(self):
        self.set_logfile()
        self.logger.info("Starting analysis tool")
        self.generate_lists()

    def run(self):
        self.run_tests()
        self.write_statistics()

    def run_tests(self):
        """ Run all the tests """
        self.txt_analyser()
        self.create_student_folders()
        self.move_student_files()
        self.process_badly_named_files()

    def write_statistics(self):
        """ Write statistics to files """
        self.write_student_list()
        self.write_summary()

    def create_student_folders(self):
        for student in self.email_list:
            if not os.path.exists(self.output_path + student):
                os.makedirs(self.output_path + student)

    def move_student_files(self):
        for file in os.listdir(self.output_path):
            if os.path.isfile(os.path.join(self.output_path, file)):
                # TODO: use a list for this?
                if file.endswith(".zip"):
                    self.move_files(file)
                if file.endswith(".rar"):
                    self.move_files(file)
                if file.endswith(".pdf"):
                    self.move_files(file)
                if file.endswith(".txt"):
                    self.move_files(file)
                if file.endswith(".docx"):
                    self.move_files(file)
                if file.endswith(".doc"):
                    self.move_files(file)
                if file.endswith(".7z"):
                    self.move_files(file)
                if file.endswith(".tar.gz"):
                    self.move_files(file)
                if file.endswith(".tar.bz"):
                    self.move_files(file)
                if file.endswith(".tar.bz2"):
                    self.move_files(file)

    def move_files(self, file):
        for student in self.email_list:
            if student in file:
                if os.path.exists(student):
                    #print(file)
                    shutil.copy2(file, self.output_path + student)
                    #os.remove(file)

    def set_logfile(self):
        """Set the LOGFILE where we will write error & info messages"""
        try:
            global logger
            logging.basicConfig(filename=self.logfile,
                                level=logging.DEBUG,
                                format="%(asctime)s %(name)s %(levelname)s %(message)s")
            self.logger = logging.getLogger(__name__)
        except IOError:
            print("Unable to open LOGFILE")
            print("Do you have write access in the current folder?")
            sys.exit(0)

    def generate_lists(self):
        self.generate_zip_files_list()
        self.unzipper()
        self.generate_txt_files_list()

    def generate_zip_files_list(self):
        """ Generate the list with the zip files """
        try:
            os.chdir(self.input_path)
        except OSError:
            print("Error: unable to open the assignments folder")
            print("This should never happen...")
        for file in os.listdir(self.input_path):
            if os.path.isfile(os.path.join(self.input_path, file)):
                if file.endswith(".zip"):
                    self.zip_files_list.append(file)
                    self.assignment_counter += 1

    def unzipper(self):
        """ Check a list with folders """
        print(".zip files: ", end="")
        counter = 0
        for index, current_file in enumerate(self.zip_files_list):
            counter += 1
            with zipfile.ZipFile(current_file, 'r') as myzip:
                #print(current_file, end=", ")
                myzip.extractall(self.output_path)
        print(counter)

    def generate_txt_files_list(self):
        """ Generate the list with the txt files """
        try:
            os.chdir(self.output_path)
        except OSError:
            print("Error: unable to open the assignments folder")
            print("This should never happen...")
        for file in os.listdir(self.output_path):
            if file.endswith(".txt"):
                #print(file, end=", ")
                self.txt_files_list.append(file)
            #print(self.txt_files_list)

    def txt_analyser(self):
        for txtfile in self.txt_files_list:
            self.get_studentname(txtfile)

    def remove_duplicate_students(self):
        """ TODO: implement this """
        lines_seen = set()  # holds lines already seen
        outfile = open(self.studentlist_filename_final, "w+")
        for line in open(self.studentlist_filename, "r+"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
                self.student_counter += 1
        outfile.close()

    def get_studentname(self, txtfile):
        with open(txtfile, 'r') as inF:
            for line in inF:
                if self.name_detection_string in line:
                    email = parseaddr(line)[0]
                    self.email_list.append(email)
                    return(email)

    def get_filename(self, txtfile):
        with open(txtfile, 'r') as inF:
            for line in inF:
                if self.filename_detection_string in line:
                    # detect bad bad filename (not containing student email)
                    if line.find(self.filename_analysis_string) == -1:
                        return(line)

    def get_assignment(self, txtfile):
        with open(txtfile, 'r') as inF:
            for line in inF:
                if self.assignmentname_detection_string in line:
                    line = line.lstrip(self.assignmentname_detection_string)
                    #line = line.rstrip("NM\n")
                    return(line)

    def write_student_list(self):
        f = open(self.studentlist_filename, 'w+')
        for email in self.email_list:
            f.write(email + "\n")
        self.remove_duplicate_students()

    def write_summary(self):
        f = open('summary.txt', 'w+')
        f.write("Build summary:\n")
        f.write("--------------\n")
        f.write(" Total students: ")
        f.write(str(self.student_counter))
        f.write("\n Total assignments: ")
        f.write(str(self.assignment_counter))
        f.write("\n Bad filesnames: \n")
        f.write(str(self.bad_filenames))

    def check_filename(self):
        pass

    def process_badly_named_files(self):
        """
        Scan for bad filenames (where student mail is not in the filename)
        Copy these files to 'studentname' folder anyway
        Add logging to provide some feedback
        """
        for txtfile in self.txt_files_list:
            studentname = self.get_studentname(txtfile)
            filename = self.get_filename(txtfile)
            if filename is not None:
                assignment = self.get_assignment(txtfile)
                self.bad_filenames_counter += 1
                self.bad_filenames += " - " + str(studentname) + ": "
                #print(studentname, end=": ")
                filename = filename.lstrip('\t')
                filename = filename.lstrip(self.filename_detection_string)
                filename = filename.lstrip(" ")
                filename = filename.rstrip()
                self.bad_filenames += str(filename) + " --> in assignment: " + assignment
                shutil.copy2(filename, self.output_path + studentname)
    #def check(self, datafile, string):
        #""" Check if a 'datafile' contains a 'sting' """
        #found = False
        ##print(datafile)
        #with open(datafile, 'r') as inF:
            #for line in inF:
                ##print(line)
                #if string in line:
                    #found = True
        #return found

    def write_report(self):
        """ Write a report: based on the complete folderlist """
        pass

    def cli_report(self, status):
        """ Report using the cli """
        if status:
            print ("true")
        else:
            print ("false")

    def exit_value(self):
        """TODO: Generate the exit value for the application."""
        if (self.errors == 0):
            return 0
        else:
            return 42
