#!/usr/bin/env python
import sys
import warnings

from myhacker.crew import MyHackerCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    MyHackerCrew().crew().kickoff() # run once for one vulnerability
    # PizzaHackers().crew().kickoff_for_each([0, 1, 2, 3, 4, 5]) # run for each vulnerability


    
