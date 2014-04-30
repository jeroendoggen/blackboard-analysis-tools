"""Setup file for "Blackboard Analysis Tools"

Define the options for the "blackboard_analysis_tools" package
Create source Python packages (python setup.py sdist)
Create binary Python packages (python setup.py bdist)

"""
from distutils.core import setup

from blackboard_analysis_tools import __version__


with open('README.txt') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(name='blackboard_analysis_tools',
      version=__version__,
      description='Blackboard analysis tools',
      long_description=LONG_DESCRIPTION,
      author='Jeroen Doggen',
      author_email='jeroendoggen@gmail.com',
      url='none',
      packages=['blackboard_analysis_tools'],
      package_data={'blackboard_analysis_tools': ['*.py', '*.conf']},
      license='LGPL-v2',
      platforms=['Linux'],
      )
