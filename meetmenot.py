#!/usr/bin/env python

import datetime
import json
import sys

import gcal
from heuristics import get_heuristics


def main(calendar='primary'):
    """
    Main MeetMeNot engine

    Retrieves events, collects heuristic classes to run each of them through,
    for the ones with issues, prepares an email to send over.
    """

    now = datetime.datetime.utcnow()
    full_day = datetime.timedelta(days=1)
    events = gcal.list_events(calendar,
                              now.isoformat() + 'Z',
                              (now + full_day).isoformat() + 'Z')

    output = {}

    heuristics = get_heuristics()

    for event in events:
        errors = []
        creator = ('email' in event['creator'] and
                   event['creator']['email'] or '?')

        for fname, heuristic in heuristics.iteritems():
            invalid, message = heuristic(event)
            if invalid:
                errors.append(message)

        output[event['id']] = {'summary': event['summary'],
                               'creator': creator,
                               'errors': errors}

    print json.dumps(output)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print 'Usage: %s [calendar/email]' % sys.argv[0]
