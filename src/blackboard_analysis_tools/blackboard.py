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
import datetime
import time
import StringIO
from multiprocessing import Process

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

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
    assignment_late_detection_string = "juni"
    script_path = os.getcwd()
    input_path = script_path + "/input/"
    output_path = script_path + "/output/"
    logfile = "blackboard_analysis_tools.log"
    logger = 0
    student_counter = 0
    bad_filenames_counter = 0
    assignment_counter = 0
    late_assignment_counter = 0
    files_counter = 0
    bad_filenames = ""
    studentlist_filename_temp = "studentlist_all.txt"
    studentlist_filename_final = "studentlist_final.txt"
    summary_file = 'summary.txt'
    starttime = 0
    lasttime = 0
    email_domain_length = 23

    def __init__(self):
        self.starttime = datetime.datetime.now()
        self.lasttime = datetime.datetime.now()
        self.set_logfile()
        self.logger.info("Starting 'analysis tool': ")
        #self.timedebug("Logger: ")
        self.generate_lists()
        self.txt_analyser()
        #self.timedebug("Txt_analyser: ")

    def run(self):
        """ Run the program (call this from main) """
        self.run_tests()
        self.write_statistics()
        #self.timedebug("Statistics: ")
        self.cleanup()
        #self.timedebug("Cleanup: ")

    def run_tests(self):
        """ Run all the tests """
        #try:
            #os.chdir(self.output_path)
        #except OSError:
            #print("Error: unable to open the output folder")
            #print("This should never happen...")
        self.create_student_folders()
        #self.timedebug("Create student folders: ")
        self.move_student_files()
        #self.timedebug("Move student files: (single) ")
        #self.move_student_files_parallel()
        #self.timedebug("Move student files: (multi) ")
        self.process_badly_named_files()
        #self.timedebug("Process bad names: ")


    def timedebug(self, message):
        """Print the current runtime + a message to the terminal """
        #TODO timing is off by one!
        now = datetime.datetime.now()
        print(message, end=" ")
        delta = now - self.lasttime
        delta = delta.total_seconds()
        print("this took: " + str(delta) + " seconds")
        self.lasttime = datetime.datetime.now()


    def is_not_analysistool_file(self, inputfile):
        """ Detect is a file is a logfile, outputfile from this tool """
        if inputfile != self.studentlist_filename_final:
            if inputfile != self.logfile:
                if inputfile != self.summary_file:
                    return(True)
        else:
            return(False)      
   
    def cleanup(self):
        """ Clean up the output folder by removing all 'temp files' """
        try:
            for inputfile in os.listdir(self.output_path):
                if os.path.isfile(os.path.join(self.output_path, inputfile)):
                    if self.is_not_analysistool_file(inputfile):
                        #print(inputfile)
                        os.remove(inputfile)
        except OSError:
            self.exit_program("cleaning up folders")

    def exit_program(self, message):
        print("Error while " + message)
        print("Closing application")
        sys.exit()

    def write_statistics(self):
        """ Write statistics to files """
        #self.timedebug("Write student list: ")
        self.write_student_list()
        #self.timedebug("Write summary: ")
        self.write_summary()

    def create_student_folders(self):
        """ Create the needed student folders """
        for student in self.email_list:
            if not os.path.exists(self.output_path + student):
                os.makedirs(self.output_path + student)

    def move_student_files(self):
        """ Move assignment files to student folders (using one process)"""
        try:
            for inputfile in os.listdir(self.output_path):
                if os.path.isfile(os.path.join(self.output_path, inputfile)):
                    # TODO: use a list for this?
                    self.move_files(inputfile)
        except OSError:
            self.exit_program("moving student files to output folder")

    def move_student_files_parallel(self):
        """ Move assignment files to student folders (using multiple processes in parallel) """
        q = Queue.Queue()
        for inputfile in os.listdir(self.output_path):
            if os.path.isfile(os.path.join(self.output_path, inputfile)):
                #print("Moving: " + inputfile)
                index = Process(target=self.move_files, args=(inputfile,))
                index.start()
                q.put(index)
                time.sleep(0.1)
                #index = Process(target=builder_task, args=(current_chapter,"_handout"))
                #index.start()
                #q.put(index) 

            #Wait for all processes to finish and print a down counter
        #print("")
        #print("Remaining processes:")
        total = q.qsize()
        while (q.qsize() > 0):
            top = q.get()
            #print(q.qsize()+1, end="/")
            #print(total)
            while (top.is_alive()):
                time.sleep(1)

    def move_files(self, inputfile):
        """ Move assignment file to the correct student folder """
        for student in self.email_list:
            student = self.swap_string(student)
            if student in inputfile:
                student = self.swap_string(student)
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
            self.exit_program("opening the logfile (do you have write permission?)")

    def generate_lists(self):
        """ Generate the needed lists: zip files, unzip, txt files """
        self.generate_zip_files_list()
        self.unzipper()
        #self.timedebug("Unzipper single: ")
        #self.unzipper_parallel()
        #self.timedebug("Unzipper parallel: ")
        self.generate_txt_files_list()

    def generate_zip_files_list(self):
        """ Generate the list with the zip files """
        try:
            os.chdir(self.input_path)
            for inputfile in os.listdir(self.input_path):
                if os.path.isfile(os.path.join(self.input_path, inputfile)):
                    if inputfile.endswith(".zip"):
                        self.zip_files_list.append(inputfile)
                        self.assignment_counter += 1
        except OSError:
            self.exit_program("reading the .zip files (does the output folder exist?)")

    def unzipper(self):
        """ Unzip all the .zip assignment files """
        print(".zip files: ", end="")
        counter = 0
        for index, current_file in enumerate(self.zip_files_list):
            counter += 1
        print(counter)
        print("")
        for index, current_file in enumerate(self.zip_files_list):
            shortname = str(counter) + ".zip"
            self.unzip_onefile(current_file, shortname)


    def unzip_onefile(self, current_file, shortname):
        """ Unzip one file """
        os.rename(current_file, shortname)
        myzip = zipfile.ZipFile(shortname)
        myzip.extractall(self.output_path)
        os.rename(shortname, current_file)

    def unzipper_parallel(self):
        """ Unzip all the .zip assignment files """
        """ Unzip all the .zip assignment files """
        q = Queue.Queue()
        print(".zip files: ", end="")
        counter = 0
        for index, current_file in enumerate(self.zip_files_list):
            shortname = str(counter) + ".zip"
            index = Process(target=self.unzip_onefile, args=(current_file, shortname,))
            index.start()
            q.put(index)
            counter += 1
            time.sleep(0.1)
        print(counter)

        ##Wait for all processes to finish and print a down counter
        #print("")
        #print("Remaining processes:")
        total = q.qsize()
        while (q.qsize() > 0):
            top = q.get()
            #print(q.qsize()+1, end="/")
            #print(total)
            while (top.is_alive()):
                time.sleep(1)

    def generate_txt_files_list(self):
        """ Generate the list with the txt files """
        try:
            os.chdir(self.output_path)
            for inputfile in os.listdir(self.output_path):
                    if os.path.isfile(os.path.join(self.output_path, inputfile)):
                        if self.is_not_analysistool_file(inputfile):
                            self.files_counter += 1
                            if inputfile.endswith(".txt"):
                                self.txt_files_list.append(inputfile)
        except OSError:
            self.exit_program("reading the .txt files")

    def txt_analyser(self):
        """ Analyse all the .txt files """
        for txtfile in self.txt_files_list:
            self.get_studentname(txtfile)
            self.get_late_assignments(txtfile)
        self.email_list.sort()

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


    def swap_string(self, string):
        """ Swap strings around '.' symbol (for email address processing)"""
        string0 = string.split(".")[0]
        string1 = string.split(".")[1]
        string = string1 + "." + string0
        return(string)
    
    
    def get_studentname(self, txtfile):
        """ Get the student name from a given txt file """
        email = ""
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.name_detection_string in line:
                    email = parseaddr(line)[0]
                    #print(email)
                    email = email[:-self.email_domain_length]
                    email = self.swap_string(email)
                    #print(email)
                    self.email_list.append(email)
            inputfile.close()
        return(email)

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

    def get_late_assignments(self, txtfile):
        """ Detect is an assignment is handed in late from a given .txt file """
        with open(txtfile, 'r') as inputfile:
            for line in inputfile:
                if self.assignment_late_detection_string in line:
                    self.late_assignment_counter += 1
                    print("Late file: ", end="")
                    print(inputfile.name)
                    print(line)
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
        try:
            os.chdir(self.output_path)
            outfile = open(self.summary_file, 'w+')
            outfile.write("Build summary:\n")
            outfile.write("--------------\n")
            outfile.write(" Total students: ")
            outfile.write(str(self.student_counter))
            outfile.write("\n Total assignments: ")
            outfile.write(str(self.assignment_counter))
            outfile.write("\n Total files: ")
            outfile.write(str(self.files_counter))
            outfile.write("\n Late files: ")
            outfile.write(str(self.late_assignment_counter))
            outfile.write("\n Bad filesnames: \n")
            outfile.write(str(self.bad_filenames))
            outfile.close()
            with open(self.summary_file) as f:
                content = f.read()
                print(content)
            outfile.close()
        except OSError:
            self.exit_program("writing the summary")

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
