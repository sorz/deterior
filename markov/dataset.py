from collections import namedtuple, defaultdict
from csv import DictReader
from datetime import datetime
import re
import sys


COLUMN_ID = 'ID'
COLUMN_S0 = 'State'
COLUMN_S1 = 'Next State'
COLUMN_TIME = 'Time'

Record = namedtuple('Record', ['s0', 's1', 't'])


def load_transit_log(path: str) -> ([Record], int):
    records = []
    max_state = 0
    with open(path, newline='') as csv:
        for row in DictReader(csv):
            s0 = int(row[COLUMN_S0])
            s1 = int(row[COLUMN_S1])
            t = int(row[COLUMN_TIME])
            records.append(Record(s0, s1, t))
            max_state = max(max_state, state)
    return records, max_state


def load_inspect_log(path: str, date_format='%Y-%m-%d') -> ([Record], int):
    states = set()
    id_inspects = defaultdict(list)
    with open(path, newline='') as csv:
        csv = DictReader(csv)
        for row in csv:
            rid = row[COLUMN_ID]
            state = row[COLUMN_S0]
            date = row[COLUMN_TIME]
            if not rid:
                raise ValueError(f'blank ID in row {csv.line_num}')
            if not state or not date:
                print(f'In row {csv.line_num}, {rid}'
                       'has blank state or time, ignored.', file=sys.stderr)
                continue
            date = datetime.strptime(date, date_format)
            id_inspects[rid].append((state, date))
            states.add(state)
    print(f'{sum(map(len, id_inspects.values()))} records loaded')
    states = sorted(states)
    smap = { s: n for n, s in enumerate(states) }
    for s in states:
        if s != str(smap[s]):
            print(f'Mapping state "{s}" to S{smap[s]}')
    print(f'Found {len(smap)} states in total')

    records = []
    for inspects in id_inspects.values():
        if len(inspects) < 2:
            continue
        inspects = sorted(inspects)
        for i in range(len(inspects) - 1):
            (s0, t0), (s1, t1) = inspects[i], inspects[i+1]
            days = (t1 - t0).days
            if days <= 0:
                continue
            records.append(Record(smap[s0], smap[s1], days))
    return records, len(states)
