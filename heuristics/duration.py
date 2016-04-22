#!/usr/bin/env python

import iso8601

MAX_DURATION = 60


def validate(event):
    """
    Check duration for the event
    """
    if not ('dateTime' in event['start'] and 'dateTime' in event['end']):
        return False, None

    start = iso8601.parse_date(event['start']['dateTime'])
    end = iso8601.parse_date(event['end']['dateTime'])
    duration_minutes = (end - start).seconds / 60
    if duration_minutes > MAX_DURATION:
        return True, "Meeting duration of %sm is not ideal" % duration_minutes
    return False, None
