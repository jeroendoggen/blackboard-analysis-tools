"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import os


class Reporter():
    """ Logging class """
    txt_files_counter = 0
    late_assignment_counter = 0
    student_counter = 0
    bad_filenames_counter = 0
    assignment_counter = 0
    bad_filenames = ""

    def __init__(self, settings):
        self.settings = settings
        #self.analyser = analyser

    def write_statistics(self, studentnames_list):
        """ Write statistics to files """
        self.write_student_list(studentnames_list)
        self.write_summary()

    def write_student_list(self, studentnames_list):
        """ Write a list with the name of all students to a file """
        outfile = open(self.settings.studentlist_filename_temp, 'w+')
        # TODO: does not work because of cyclic arguments
        for student in studentnames_list:
            outfile.write(student + "\n")
        outfile.close()
        # TODO: probably works, but uses an empty input file
        self.remove_duplicate_students()

    def remove_duplicate_students(self):
        """ Remove duplicate students in the students_list """
        """ TODO: does not work? """
        lines_seen = set()  # holds lines already seen
        outfile = open(self.settings.studentlist_filename_final, "w+")
        for line in open(self.settings.studentlist_filename_temp, "r+"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
                self.student_counter += 1
        outfile.close()

    def write_summary(self):
        """ Write a summary of the analysis process to a logfile """
        try:
            os.chdir(self.settings.output_path)
            outfile = open(self.settings.summary_file, 'w+')
            outfile.write("Build summary:\n")
            outfile.write("--------------\n")
            outfile.write(" Total students: ")
            outfile.write(str(self.student_counter))
            outfile.write("\n Total assignments: ")
            outfile.write(str(self.txt_files_counter))
            outfile.write("\n Total files: ")
            outfile.write(str(self.txt_files_counter))
            outfile.write("\n Late files: ")
            outfile.write(str(self.late_assignment_counter))
            outfile.write("\n Bad filesnames: \n")
            outfile.write(str(self.bad_filenames))
            outfile.close()
            with open(self.settings.summary_file) as f:
                content = f.read()
                print(content)
            outfile.close()
        except OSError:
            self.exit_program("writing the summary")
