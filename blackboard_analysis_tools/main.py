"""
    Blackboard Analysis Tools
    Copyright 2013, Jeroen Doggen, jeroendoggen@gmail.com
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
