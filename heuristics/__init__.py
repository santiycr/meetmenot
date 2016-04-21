#!/usr/bin/env python

import os
import sys


def get_heuristics():
    """
    dynamically import different validation functions from files in this
    directory and return them as a list to be used by MeetMeNot for validation
    """
    pass
    heuristics = {}

    path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, path)
    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if fname == '__init__':
            continue
        if ext == '.py':
            mod = __import__(fname)
            heuristics[fname] = mod.validate
    sys.path.pop(0)

    return heuristics
