#!/usr/bin/env python

import datetime

import gcal
from heuristics import get_heuristics


def main():
    """
    Main MeetMeNot engine

    Retrieves events, collects heuristic classes to run each of them through,
    for the ones with issues, prepares an email to send over.
    """

    now = datetime.datetime.utcnow()
    full_day = datetime.timedelta(days=1)
    events = gcal.list_events('primary',
                              now.isoformat() + 'Z',
                              (now + full_day).isoformat() + 'Z')
    errors = {}
    heuristics = get_heuristics()
    for event in events:
        errors = []

        for fname, heuristic in heuristics.iteritems():
            invalid, message = heuristic(event)
            if invalid:
                errors.append(message)

        for error in errors:
            print(event['summary'], error)

if __name__ == '__main__':
    main()
