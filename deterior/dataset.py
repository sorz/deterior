from collections import namedtuple, defaultdict
from csv import DictReader
from datetime import datetime
from typing import TextIO, BinaryIO
from configparser import ConfigParser
import sys
from openpyxl import load_workbook


Record = namedtuple('Record', ['s0', 's1', 't'])
Inspect = namedtuple('Inspect', ['id', 'state', 'date'])


class DataSetReader:
    """Read inspection log file according to the format config.
    """
    def __init__(self, config: TextIO = None) -> None:
        cfg = ConfigParser(interpolation=None)
        cfg.read_dict({
            'ID': {'column': 'ID'},
            'State': {'column': 'State'},
            'Time': {
                'column': 'Time',
                'format': '%Y-%m-%d'
            },
        })
        if config is not None:
            cfg.read_file(config)
        self.col_id = cfg['ID']['column']
        self.col_state = cfg['State']['column']
        self.col_time = cfg['Time']['column']
        self.time_format = cfg['Time']['format']

    def _load(self, rows) -> ([Record], int):
        inpsects = []
        for n, (sid, state, date) in enumerate(rows):
            if not sid:
                raise ValueError(f'blank ID in row {n + 2}')
            if not state or not date:
                print(f'In row {n + 2}, {sid} '
                      'has blank state or time, ignored.', file=sys.stderr)
                continue
            if isinstance(date, str):
                date = datetime.strptime(date, self.time_format)
            inpsects.append(Inspect(sid, state, date))
        print(f'{len(inpsects)} inspection records loaded')
        return _inpsects_to_records(inpsects)

    def load_csv(self, csvfile: TextIO) -> ([Record], int):
        csv = DictReader(csvfile)
        rows = (
            (
                row[self.col_id],
                row[self.col_state],
                row[self.col_time],
            ) for row in csv
        )
        return self._load(rows)

    def load_xls(self, xlsfile: BinaryIO) -> ([Record], int):
        book = load_workbook(xlsfile, read_only=True)
        sheet = book.worksheets[0]  # use the first sheet only
        header = sheet[1]

        col_id, col_state, col_time = [None] * 3
        for i, col in enumerate(header):
            value = col.value.strip()
            if value == self.col_id:
                col_id = i
            elif value == self.col_state:
                col_state = i
            elif value == self.col_time:
                col_time = i
        if None in (col_id, col_state, col_time):
            raise ValueError('Missing column in dataset file')

        rows = (
            (
                row[col_id].value,
                row[col_state].value,
                row[col_time].value,
            ) for row in sheet.iter_rows(min_row=2)
        )
        return self._load(rows)


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
