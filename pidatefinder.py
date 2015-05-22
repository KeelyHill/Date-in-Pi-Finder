"""
Copyright (c) 2015 Keely Hill

A small little module for finding a date in π.
"""

from datetime import datetime, timezone, timedelta
from collections import namedtuple
import PiOneMillion

__author__ = "Keely Hill"
__copyright__ = "Copyright 2015 Keely Hill"
__version__ = "0.1.0"

__license__ = "MIT"
__email__ = "KeelyHill@gmx.com"
__status__ = "Production/Development"  # like a crazy person

pi = PiOneMillion.pi

# Old pi importing
# pi = ''
# with open('Pi-OneMillion.txt', 'r') as f:
#     pi = f.read()

Found = namedtuple('Found', ['index', 'substring'])


def find(needle):
    """
    Searches the first million digits of pi for the string.

    If it cannot find the raw needle first the decade is removed
    followed by the entire year.

    Returns a named tuple Found:
        Found.index returns -1 if it is not found.
        Found.substring always returns the last needle.
    """
    location = pi.find(needle)
    if location is -1:
        needle = needle[:-4] + needle[-2:]  # remove century
        location = pi.find(needle)
    if location is -1:
        needle = needle[:-2]  # remove decade
        location = pi.find(needle)
    return Found(location, needle)


def constructSentence(found, dateFormat):
    """
    Uses results of find() to create an English sentence.
    """
    if found.index is -1:
        # return 'Today not found using ' + dateFormat + ' format.'
        return None
    else:
        formatter = (found.index, found.substring, dateFormat)
        return 'Today found at the %i digit of π! (%s in the %s format)' % formatter


def findDateInPi(date, raw=False):
    """
    Finds the current date within pi.

    Looks with both American and European date formats.

    Returns a dict with each format in sentence form unless raw=True where
    the raw named tuple is returned in a dict instead.
    """
    # American Date Format
    american = find(date.strftime('%-m%-d%Y'))

    # European Date Format
    european = find(date.strftime('%d%m%Y'))
    if european.index is -1:
        european = find(date.strftime('%-d%-m%Y'))

    if raw:
        return dict(american=american, european=european)

    return dict(
        american=constructSentence(american, 'American'),
        european=constructSentence(european, 'European')
    )


def findTodayInPi():
    """
    Searches for the current date UTC within pi.
    """
    return findDateInPi(datetime.now(timezone.utc))


def searchTheNextDays(days, raw=False):
    """
    Returns an array of the next amount of days based on findDateInPi().

    Each element in the array is a tuple containing the ISO 8601 date and the
    named tuple from findDateInPi().

    Raw will remove sentences and only return named tuple's.
    """
    date = datetime.now(timezone.utc)
    results = []

    for i in range(days):
        date += timedelta(days=1)
        results.append((date.strftime('%Y-%m-%d'), findDateInPi(date, raw)))

    return results
