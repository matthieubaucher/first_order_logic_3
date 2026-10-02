# Goal

Your goal is to produce a working version of a SAT planner.

# Reference docs

Guide for Z3 solver : https://ericpony.github.io/z3py-tutorial/guide-examples.htm

One reference for SATPLAN : https://www.cs.toronto.edu/~sheila/2542/s14/material/CSC2542s14_SATPlan.pdf

# What you get

There are several scripts in this repository to help you.

## Python scripts

- `z3_planner.py`: this is the main file to complete. Read the docstrings of each function. For you to complete are the places marked with 'TODO'.
- `test.py`: this script will randomly generate blocks problems and try your code on it. You can call it with `python test.py`. It will print cases on which your script failed. Use these cases to call the relevant functions from `z3_planner.py` directly and debug your code.
- `problem_generator.py`: util functions to generate blocks world problems.
- `strips.py`: a solver for planning problems in the STRIPS format. You can run `python strips.py blocks.txt`.
- `scaling.py`: if you are done with the main part of the lab session, you can try to adjust this script to reproduce Figure 2 from Mitchel *et al*, *Hard and Easy Distributions of SAT Problems*, AAAI 1992.

## Other files

- `blocks.txt`: STRIPS encoding of the blocks world.
- `monkeys.txt`: STRIPS encoding of the monkeys world.
- `requirements.txt`: to install the relevant packages, e.g. `pip install -r requirements.txt`. Use Python 3.11+.
