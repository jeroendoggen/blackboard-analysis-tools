"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
"""

# TODO: report all students that hand in the assignment after the deadline
# TODO: ...

import os


class Settings:
    """ Contains all the tools to analyse Blackboard assignments """
    logfile = "blackboard_analysis_tools.log"
    script_path = os.getcwd()
    input_path = script_path + "/input/"
    output_path = script_path + "/output/"
    name_detection_string = "Naam:"
    email_domain_length = 5
    filename_detection_string = "Bestandsnaam:"
    assignmentname_detection_string = "Opdracht:"
    filename_analysis_string = "s.ap"
    assignment_late_detection_string = "juni"

    logfile = "blackboard_analysis_tools.log"
    studentlist_filename_temp = "studentlist_all.txt"
    studentlist_filename_final = "studentlist_final.txt"
    summary_file = 'summary.txt'

    def __init__(self):
        pass
