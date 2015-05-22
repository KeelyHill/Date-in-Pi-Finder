"""
Copyright (c) 2015 Keely Hill

A small little module for finding a date in π.
"""

from datetime import datetime, timezone
from collections import namedtuple

__author__ = "Keely Hill"
__copyright__ = "Copyright 2015 Keely Hill"
__version__ = "0.1.0"

__license__ = "MIT"
__email__ = "KeelyHill@gmx.com"
__status__ = "Production/Development"  # like a crazy person

pi = ''
Found = namedtuple('Found', ['index', 'substring'])

with open('Pi-OneMillion.txt', 'r') as f:
    pi = f.read()


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
