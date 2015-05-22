# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from collections import namedtuple

pi = ''
Found = namedtuple('Found', ['index', 'substring'])

with open('Pi-OneMillion.txt', 'r') as f:
    pi = f.read()


def find(needle):
    location = pi.find(needle)
    if location is -1:
        needle = needle[:-4] + needle[-2:]  # remove century
        location = pi.find(needle)
    if location is -1:
        needle = needle[:-2]  # remove decade
        location = pi.find(needle)
    return Found(location, needle)


def constructSentence(found, dateFormat):
    if found.index is -1:
        # return 'Today not found using ' + dateFormat + ' format.'
        return None
    else:
        formatter = (found.index, found.substring, dateFormat)
        return 'Today found at the %i digit of π! (%s in the %s format)' % formatter


def findDateInPi(date, raw=False):
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
    return findDateInPi(datetime.now(timezone.utc))
