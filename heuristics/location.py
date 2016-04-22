import validators


def find_zoom_room(event):
    if 'description' in event:
        desc = event['description']
        for w in desc:
            if validators.url(w) is True and 'zoom.us' in w:
                return True


def find_conference_room(event):
    return 'location' in event


def find_hangout(event):
    return 'hangoutLink' in event


def validate(event):
    """
    Check if there's an agenda for this event.
    """
    location_found = False
    for find_location in [find_hangout, find_conference_room, find_zoom_room]:
        location_found = find_location(event)
        if location_found:
            return False, None

    return True, 'No zoom, hangout or conference room found for event.'
