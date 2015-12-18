"""
	setup.py file for package rr_scorers
"""

# Metadata
__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'


from setuptools import setup
from setuptools import find_packages

setup(
	name='rr_scorers',
	version='1.0',
	description='Custom Scorers for the Retrieve & Rank service on Bluemix',
	author='Vincent Dowling',
	author_email='vdowlin@us.ibm.com',
	packages=find_packages()
)
