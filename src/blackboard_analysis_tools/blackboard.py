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
import shutil
import sys

from email.utils import parseaddr


class BlackboardAnalysisTools:
    """ Contains all the tools to analyse Blackboard assignments """
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
    studentlist_filename_temp = "studentlist_all.txt"
    studentlist_filename_final = "studentlist_final.txt"

    def __init__(self):
        self.set_logfile()
        self.logger.info("Starting analysis tool")
        self.generate_lists()
        self.txt_analyser()

    def run(self):
        """ Run the program (call this from main) """
        self.run_tests()
        self.write_statistics()

    def run_tests(self):
        """ Run all the tests """
        #try:
            #os.chdir(self.output_path)
        #except OSError:
            #print("Error: unable to open the output folder")
            #print("This should never happen...")
        self.create_student_folders()
        self.move_student_files()
        self.process_badly_named_files()

    def write_statistics(self):
        """ Write statistics to files """
        self.write_student_list()
        self.write_summary()

    def create_student_folders(self):
        """ Create the needed student folders """
        for student in self.email_list:
            if not os.path.exists(self.output_path + student):
                os.makedirs(self.output_path + student)

    def move_student_files(self):
        """ Move assignment files to student folders """
        for inputfile in os.listdir(self.output_path):
            if os.path.isfile(os.path.join(self.output_path, inputfile)):
                # TODO: use a list for this?
                if inputfile.endswith(".zip"):
                    self.move_files(inputfile)
                if inputfile.endswith(".rar"):
                    self.move_files(inputfile)
                if inputfile.endswith(".pdf"):
                    self.move_files(inputfile)
                if inputfile.endswith(".txt"):
                    self.move_files(inputfile)
                if inputfile.endswith(".docx"):
                    self.move_files(inputfile)
                if inputfile.endswith(".doc"):
                    self.move_files(inputfile)
                if inputfile.endswith(".7z"):
                    self.move_files(inputfile)
                if inputfile.endswith(".tar.gz"):
                    self.move_files(inputfile)
                if inputfile.endswith(".tar.bz"):
                    self.move_files(inputfile)
                if inputfile.endswith(".tar.bz2"):
                    self.move_files(inputfile)

    def move_files(self, inputfile):
        """ Move assignment file to the correct student folder """
        for student in self.email_list:
            if student in inputfile:
                if os.path.exists(student):
                    shutil.copy2(inputfile, self.output_path + student)
                    #os.remove(inputfile)

    def set_logfile(self):
        """Set the logfile: for error & info messages"""
        try:
            logging.basicConfig(filename=self.logfile,
                                level=logging.DEBUG,
                                format="%(asctime)s %(name)s %(levelname)s %(message)s")
            self.logger = logging.getLogger(__name__)
        except IOError:
            print("Unable to open LOGFILE")
            print("Do you have write access in the current folder?")
            sys.exit(0)

    def generate_lists(self):
        """ Generate the needed lists: zip files, unzip, txt files """
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
        for inputfile in os.listdir(self.input_path):
            if os.path.isfile(os.path.join(self.input_path, inputfile)):
                if inputfile.endswith(".zip"):
                    self.zip_files_list.append(inputfile)
                    self.assignment_counter += 1

    def unzipper(self):
        """ Unzip all the .zip assignment files """
        print(".zip files: ", end="")
        counter = 0
        for index, current_file in enumerate(self.zip_files_list):
            counter += 1
            with zipfile.ZipFile(current_file, 'r') as myzip:
                myzip.extractall(self.output_path)
        print(counter)

    def generate_txt_files_list(self):
        """ Generate the list with the txt files """
        try:
            os.chdir(self.output_path)
        except OSError:
            print("Error: unable to open the assignments folder")
            print("This should never happen...")
        for inputfile in os.listdir(self.output_path):
            if inputfile.endswith(".txt"):
                self.txt_files_list.append(inputfile)

    def txt_analyser(self):
        """ Analyse all the .txt files """
        for txtfile in self.txt_files_list:
            self.get_studentname(txtfile)

    def remove_duplicate_students(self):
        """ Remove duplicate students in the students_list """
        """ TODO: does not work? """
        lines_seen = set()  # holds lines already seen
        outfile = open(self.studentlist_filename_final, "w+")
        for line in open(self.studentlist_filename_temp, "r+"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
                self.student_counter += 1
        outfile.close()

    def get_studentname(self, txtfile):
        """ Get the student name from a given txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.name_detection_string in line:
                    email = parseaddr(line)[0]
                    self.email_list.append(email)
                    inputfile.close()
                    return(email)
            inputfile.close()

    def get_filename(self, txtfile):
        """ Get the assignment filename from a given txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.filename_detection_string in line:
                    # detect bad bad filename (not containing student email)
                    if line.find(self.filename_analysis_string) == -1:
                        line = line.lstrip('\t')
                        line = line.lstrip(self.filename_detection_string)
                        line = line.lstrip(" ")
                        line = line.rstrip()
                        return(line)

    def get_assignment(self, txtfile):
        """ Get the assignment name from a given .txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.assignmentname_detection_string in line:
                    line = line.lstrip(self.assignmentname_detection_string)
                    #line = line.rstrip("NM\n")
                    return(line)

    def write_student_list(self):
        """ Write a list with the name of all students to a file """
        outfile = open(self.studentlist_filename_temp, 'w+')
        for email in self.email_list:
            outfile.write(email + "\n")
        outfile.close()
        self.remove_duplicate_students()

    def write_summary(self):
        """ Write a summary of the analysis process to a logfile """
        outfile = open('summary.txt', 'w+')
        outfile.write("Build summary:\n")
        outfile.write("--------------\n")
        outfile.write(" Total students: ")
        outfile.write(str(self.student_counter))
        outfile.write("\n Total assignments: ")
        outfile.write(str(self.assignment_counter))
        outfile.write("\n Bad filesnames: \n")
        outfile.write(str(self.bad_filenames))

    def check_filename(self):
        """ Check the .zip file -or other files- using some pattern? """
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
                self.bad_filenames += str(filename) + " --> in assignment: " + assignment
                shutil.copy2(filename, self.output_path + studentname)

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
