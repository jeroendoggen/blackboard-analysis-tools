""" 
    Blackboard Grade center analyser
    A tool to analyse assignments downloaded from the Blackboard grade center
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

# TODO: step 1: generate folder for each assignments
# TODO: step 2: generate folder for each student (by processing the results after step 1)
# TODO: report all students that hand in the assignment after the deadline
# TODO: list of the students who are not following the 'file naming' guidlines
# TODO: 


from __future__ import print_function, division  # We require Python 2.6+

import logging
import os
import zipfile
import time
import shutil
import glob
from email.utils import parseaddr

logger = 0


"""Global variables
TODO: make them local
"""
SEARCH_STRING = "Bestandsnaam:"
LOGFILE = "blackboard_analysis_tools.log"

class Blackboard_analysis_tools:
    errors = 0
    zip_files_list = []
    txt_files_list = []
    email_list = []
    name_detection_string = "Naam:"
    script_path = os.getcwd()
    input_path = script_path + "/input"
    output_path = script_path + "/output"
    
    def init(self):
        self.set_logfile()
        logger.info("Starting analysis tool")
        self.generate_lists()
        
    def run(self):
        self.run_tests()
        self.write_statistics()
       
    def run_tests(self):
        """ Run all the tests """
        self.txt_analyser()
        self.create_student_folders()
        #self.move_student_files()
        #self.check_folder_list(self.zip_files_list)
    
    def write_statistics(self):
        """ Write statistics to files """
        self.write_student_list()
        #self.write_report()
        
    def create_student_folders(self):
        for student in self.email_list:
            if not os.path.exists(self.output_path + student):
                os.makedirs(student)
                
    def move_student_files(self):
        for file in os.listdir(INPUTPATH):
            if os.path.isfile(os.path.join(INPUTPATH, file)):
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
                #types = ('*.*')
                ##types = ('*.rar', '*.zip', '*.pdf', '*.doc', '*.docx', '*.cs')
                #files_grabbed = []
                #for files in types:
                    #files_grabbed.extend(glob.glob(files))
                #for filename in files_grabbed:
                    #if os.path.isfile(filename):
                        #print(filename)
                        #os.remove(filename)
    
    def move_files(self, file):
        for student in self.email_list:
            if student in file:
                if os.path.exists(student):
                    #print(file)
                    shutil.copy2(file, OUTPUTPATH + student)
                    #os.remove(file)
        
    def set_logfile(self):
        """Set the LOGFILE where we will write error & info messages"""
        try:
            global logger
            logging.basicConfig(filename=LOGFILE,
                level=logging.DEBUG,
                format="%(asctime)s %(name)s %(levelname)s %(message)s")
            logger = logging.getLogger(__name__)
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
            print("Error: unable to open the folder where the assignment files are located")
            print("This should never happen...")
        for file in os.listdir(self.input_path):
            if os.path.isfile(os.path.join(self.input_path, file)):
                if file.endswith(".zip"):
                    self.zip_files_list.append(file)

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
            print("Error: unable to open the folder where the assignment files are located")
            print("This should never happen...")
        for file in os.listdir(self.output_path):
            if file.endswith(".txt"):
                #print(file, end=", ")
                self.txt_files_list.append(file)
            #print(self.txt_files_list)
            
    
    def txt_analyser(self):
        for txtfile in self.txt_files_list:
            self.get_studentname(txtfile)
        
    def get_studentname(self, txtfile):
        with open(txtfile, 'r') as inF:
            for line in inF:
                if self.name_detection_string in line:
                    self.email_list.append(parseaddr(line)[0]) # get email
   
    def write_student_list(self):
        f = open('studentlist.txt', 'w+')
        for email in self.email_list:
            f.write(email + "\n")
    #def grab_email(files = []):
       

    def check_folder_list(self, files_list):
        """ Check a list with folders """
        for index, current_file in enumerate(files_list):
            print(current_file, end="")
            print(": ", end="")
            status = self.check(current_file, SEARCH_STRING)
            print(status)
        
    def check_filename(self):
        pass
        
    def check(self, datafile, string):
        """ Check if a 'datafile' contains a 'sting' """
        found = False
        #print(datafile)
        with open(datafile, 'r') as inF:
            for line in inF:
                #print(line)
                if string in line:
                    found = True
        return found

    def write_report(self, folderlist):
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


