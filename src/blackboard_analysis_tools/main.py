""" 
    Blackboard Grade center analyser
    A tool to analyse assignments downloaded from the Blackboard grade center
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com

    This file is needed to import the module properly

# TODO: step 1: generate folder for each assignments
# TODO: step 2: generate folder for each student (by processing the results after step 1)
# TODO: report all students that hand in the assignment after the deadline
# TODO: list of the students who are not following the 'file naming' guidlines
# TODO: 
"""

import sys

from blackboard_analysis_tools.blackboard import Blackboard_analysis_tools


def run():
    """Run the main program"""
    assignment_analyser = Blackboard_analysis_tools()
    assignment_analyser.init()
    assignment_analyser.run()
    return(assignment_analyser.exit_value())


if __name__ == "__main__":
    sys.exit(run())
