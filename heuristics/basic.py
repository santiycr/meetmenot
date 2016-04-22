#!/usr/bin/env python


def validate(event):
    """
    Basic validation heuristic example

    all heuristic validations will be called with an event
    and are expected to return a tuple:
      - bool: indicating whether the event is invalid
      - message: if the event is invalid, includes an error message to be used
        for the notification
    """
    return False, None
