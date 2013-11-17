# Blackboard Analysis Tool
An analysis automation tool to avoid repetitive task while grading student assignments that have been handed in through the Blackboard learning system.

For example:
 * Extract hundreds of .zip files
 * Sort the files per assignment, student
 * Create statistics: number of students, late assignments,...

## Usage:
 * Download assignment files from Blackboard (e.g. gradebook_ART_EA-38302_Assignment1_2013-06-11-20-50-44.zip).
 * Place these .zip files in the "input" folder.
 * Run the program: ``python -m blackboard_analysis_tools``.
 * Wait... (about 10 seconds when processing around 100MB of assignments) (time will vary).
 * Open the "output" folder to see the results (all files sorted per student, a summary, logfile, ...).

## Installation:
 * Download the source and run ``python setup.py install``.
 * Python Package available in the Python Package Index at: http://pypi.python.org/pypi/blackboard_analysis_tools/.
 * Install using pip: ``pip install blackboard_analysis_tools``.

## Limitations:
 * Currently only tested on Linux.
 * The program was created with other OS users in mind, so it will eventually get full cross-platform support.

## License:
If not stated otherwise blackboard_analysis_tools is distributed in terms of the MIT license.
See LICENSE in the distribution for details.

## Bug reports:
 * Post issues to GitHub http://github.com/jeroendoggen/blackboard-analysis-tools/issues.

## What is happening behind the scenes:
 1. Scan for .zip files
 2. Extract the .zip files
 3. Scan for .txt files (these contain the metadata that describes the student reports/assignments)
 4. Analyse the .txt files
 5. Create a folder for each student
 6. Move all the files to the correct folder (including those with filenames that have been 'mangled' by Blackboard)
 7. Write some statistics: a list of all students that have handed something in
 8. Write a summary of the process: number of students, number of assignments, number of 'mangled' files,...

## Changelog:
0.0.3:
 * Cleanup temp folders
 * Debug code for timing analysis
 * Parallel processing (no speedup)
 * Python 3.3 compatible
 * Partially Windows compatible
 * Sorting output folders
 * Print build summary
 * Detect late files

0.0.2:
 * Detect 'mangled' files
 * Statistics: logfile, summary, student list
 * using input & output folders
 * Code cleanup: pep8, pylint

0.0.1: Basic features
 * Extract .zip files
 * Create student folders
 * Move files to folder
