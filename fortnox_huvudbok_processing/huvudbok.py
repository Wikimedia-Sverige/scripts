#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Crunch Huvudbok export."""
import json
import os
import sys
from collections import defaultdict


class Huvudbok(object):

    COL_NAME = {
        'konto': 0,  # A
        'namn': 1,  # B
        'ks': 2,  # C
        'datum': 4,  # E
        'debet': 7,  # H
        'kredit': 8,  # I
    }
    KS_DEFAULT = 'saknar ks'

    def __init__(self, filename, projects=None, year='2018'):
        self.year = year
        self.all_konto = {}
        self.konto = ''
        self.results = {}
        self.all_ks = set()
        self.projects = {}

        if projects:
            self.projects = Huvudbok.load_projects(projects)

        i = 0
        for row in Huvudbok.load_file(filename):
            i += 1
            try:
                self.process_row(row)
            except (IndexError, KeyError, ValueError, TypeError):
                print('row {}: {}'.format(i, row))
                raise

        if year == '2018':
            self.tweak_2018()

        basename = os.path.splitext(filename)[0]
        out_name = '{}_crunched.tsv'.format(basename)
        with open(out_name, 'w') as self.f_out:
            self.output()

    @staticmethod
    def load_file(filename):
        with open(filename, encoding='latin-1') as f:
            return f.readlines()

    @staticmethod
    def load_projects(filename):
        with open(filename) as f:
            return json.load(f)

    def get_col(self, cols, col_name):
        col_num = Huvudbok.COL_NAME.get(col_name)
        if len(cols) < col_num:
            return None
        return cols[col_num].strip()

    def process_row(self, row):
        cols = row.split('\t')

        # Load konto
        if is_int(self.get_col(cols, 'konto')):
            self.konto = self.get_col(cols, 'konto')
            self.results[self.konto] = defaultdict(float)

            self.all_konto[self.konto] = self.get_col(cols, 'namn')

        # load lines with data
        date = self.get_col(cols, 'datum')
        if not date or not date.startswith(self.year):
            return
        ks = self.get_col(cols, 'ks') or Huvudbok.KS_DEFAULT
        self.all_ks.add(ks)

        debet = fix_num(self.get_col(cols, 'debet'))
        kredit = fix_num(self.get_col(cols, 'kredit'))
        self.results[self.konto][ks] += kredit - debet

    def tweak_2018(self):
        """2018 was a messy year so merge several konto."""
        merge = {
            '3890': '3010',  # medlemsavgift privat
            '3891': '3011',  # medlemsavgift juridisk person
            '3869': '3018',  # donationer övriga
            '3860': '3012',  # donationer privat
            '3861': '3013',  # donationer juridisk person
            '4610': '4910',  # Projektkonsulter
            '6212': '6211',  # Mobiltelefon
            '7632': '7631',  # Personalrepresentation, ej avdragsgill
        }

        for old_konto, new_konto in merge.items():
            if new_konto not in self.results.keys():
                self.results[new_konto] = self.results.pop(old_konto)
            else:
                for ks, val in self.results[old_konto].items():
                    self.results[new_konto][ks] += val
                del self.results[old_konto]
            self.all_konto[new_konto] = self.all_konto.pop(old_konto)

    def output(self):
        # Header lines
        line = ['', '', '']
        line += sorted(self.all_ks)
        self.print_line(line)

        line = ['konto', 'namn', 'Total']
        line += [self.projects.get(ks, '') for ks in sorted(self.all_ks)]
        self.print_line(line)

        # Each lines
        ks_sums = defaultdict(float)
        for konto in sorted(self.results.keys()):
            line = [konto, self.all_konto.get(konto)]

            # skip empty konto
            if not any(val != 0 for val in self.results[konto].values()):
                continue

            line.append('{:.2f}'.format(sum(self.results[konto].values())))
            for ks in sorted(self.all_ks):
                val = self.results[konto].get(ks) or 0
                ks_sums[ks] += val
                line.append('{:.2f}'.format(val))
            self.print_line(line)

        # summation lines
        self.print_line([])
        line = ['', 'Total', '']
        for ks in sorted(self.all_ks):
            line.append('{:.2f}'.format(ks_sums.get(ks)))
        self.print_line(line)

    def print_line(self, line):
        self.f_out.write('\t'.join(line) + '\n')


def fix_num(cell_value):
    """Convert Swedish style numbering to standard format."""
    if not cell_value.strip():
        return 0
    value = cell_value.replace(' ', '').replace(',', '.')
    return float(value)


def is_int(value):
    """
    Check if the given value is an integer.

    @param value: The value to check
    @type value: str, or int
    @return: if value can be interpreted as an integer
    @rtype: bool
    """
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":
    args = sys.argv[1:]
    Huvudbok(*args)
