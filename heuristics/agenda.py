import validators

MIN_DESC_LENGTH = 100


def check_description(desc):
    for w in desc:
        if validators.url(w) is True:
            return False, None
        if 'agenda' in w.lower():
            return False, None

    if len(desc) > MIN_DESC_LENGTH:
        return False, None

    return True, 'No valid agenda found for event.'


def validate(event):
    """
    Check if there's an agenda for this event.
    """
    if 'description' in event:
        return check_description(event['description'])

    return True, 'No description found for event.'
