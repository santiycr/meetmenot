#!/usr/bin/env python

IDEAL_MAX_ATTENDEES = 5


def validate(event):
    """
    Check attendees for the event
    """
    if len(event['attendees']) > IDEAL_MAX_ATTENDEES:
        return True, '%s is too many attendees for an effective meeting' % len(event['attendees'])
    return False, None
