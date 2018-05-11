from collections import namedtuple, defaultdict
from csv import DictReader
from datetime import datetime
import sys


COLUMN_ID = 'ID'
COLUMN_S0 = 'State'
COLUMN_S1 = 'Next State'
COLUMN_TIME = 'Time'

Record = namedtuple('Record', ['s0', 's1', 't'])
Inspect = namedtuple('Inspect', ['id', 'state', 'date'])

def load_transit_log(path: str) -> ([Record], int):
    records = []
    max_state = 0
    with open(path, newline='') as csv:
        for row in DictReader(csv):
            s0 = int(row[COLUMN_S0])
            s1 = int(row[COLUMN_S1])
            t = int(row[COLUMN_TIME])
            records.append(Record(s0, s1, t))
            max_state = max(max_state, s0, s1)
    return records, max_state


def load_inspect_log(path: str, date_format='%Y-%m-%d') -> ([Record], int):
    inpsects = []
    with open(path, newline='') as csv:
        csv = DictReader(csv)
        for row in csv:
            sid = row[COLUMN_ID]
            state = row[COLUMN_S0]
            date = row[COLUMN_TIME]
            if not sid:
                raise ValueError(f'blank ID in row {csv.line_num}')
            if not state or not date:
                print(f'In row {csv.line_num}, {sid} '
                      'has blank state or time, ignored.', file=sys.stderr)
                continue
            date = datetime.strptime(date, date_format)
            inpsects.append(Inspect(sid, state, date))
    print(f'{len(inpsects)} inspection records loaded')
    return _inpsects_to_records(inpsects)


def _inpsects_to_records(inspects: [Inspect]) -> ([Record], int):
    """Return list of records and the total number of states."""
    states = set()
    id_inspects = defaultdict(list)
    for sid, state, date in inspects:
        states.add(state)
        id_inspects[sid].append((state, date))

    states = sorted(states)
    smap = {s: n for n, s in enumerate(states)}
    for state in states:
        if state != str(smap[state]):
            print(f'Mapping state "{state}" to S{smap[state]}')
    print(f'Found {len(smap)} states in total')

    records = []
    for states_dates in id_inspects.values():
        if len(states_dates) < 2:
            continue
        states_dates = sorted(states_dates)
        for i in range(len(states_dates) - 1):
            (s0, t0), (s1, t1) = states_dates[i], states_dates[i+1]
            days = (t1 - t0).days
            if days <= 0:
                continue
            records.append(Record(smap[s0], smap[s1], days))
    return records, len(states)
