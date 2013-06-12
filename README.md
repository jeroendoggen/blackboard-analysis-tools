blackboard-analysis-tools
=========================

Some tools to automate the analysis of student assignments that have been handed in using the Blackboard learning system.

Usage:
------
 * Download assignment files from Blackboard (e.g. gradebook_ART_EA-38302_Assignment1_2013-06-11-20-50-44.zip)
 * Place these .zip files in the "input" folder
 * Run the program: ``python -m blackboard_analysis_tools``
 * Wait... (about 10 seconds when processing around 100MB of assignments) (time will vary)
 * Open the "output" folder to see the results (all files sorted per student, a summary, logfile, ...)
 * Post issues to GitHub http://github.com/jeroendoggen/Arduino-TestSuite/issues.

Installation:
-------------
 * Download the source and run python setup.py install
 * Python Package available in the Python Package Index at: (coming soon)
 * Install using pip: pip install arduino_testsuite


What is it does (step by step):
-------------------------------
 * Scan for .zip files
 * Extract the .zip files
 * Scan for .txt files (these contain the metadata that describes the student reports/assignments)
 * Analyse the .txt files
 * Create a folder for each student
 * Move all the files to the correct folder (including the filenames that have been 'mangled' by Blackboard)
 * Write some statistics: a list of all students that have handed something in
 * Write a summary of the process: number of students, number of assignments, number of 'mangled' files,...

