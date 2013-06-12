"""
    Blackboard Grade center analyser
    A tool to analyse assignments downloaded from the Blackboard grade center
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com

    This file is needed to import the module properly

"""

import sys

from blackboard_analysis_tools.blackboard import BlackboardAnalysisTools


def run():
    """Run the main program"""
    assignment_analyser = BlackboardAnalysisTools()
    #assignment_analyser.init()
    assignment_analyser.run()
    return(assignment_analyser.exit_value())


if __name__ == "__main__":
    sys.exit(run())
