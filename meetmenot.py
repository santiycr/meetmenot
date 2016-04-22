#!/usr/bin/env python

import datetime
import json
import sys
from datetime import datetime as dt

import gcal
from heuristics import get_heuristics


def get_date(x):
    if 'date' in x:
        return x['date']
    elif 'dateTime' in x:
        # 2016-04-14T22:00:11.000Z
        date = dt.strptime(x['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')
        return str(date.month) + '/' + str(date.day) + ' ' + str(date.hour) + ':' + str(date.minute)
    return '?'


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
                               'start': get_date(event['start']),
                               'end': get_date(event['end']),
                               'errors': errors}
        if 'attendees' in event:
            output[event['id']]['attendees'] = [a['email'] for a in event['attendees']],

    print json.dumps(output)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
        sys.exit(0)
    elif len(sys.argv) == 2:
        main(sys.argv[1])
        sys.exit(0)
    else:
        print 'Usage: %s [calendar/email]' % sys.argv[0]
        sys.exit(1)
