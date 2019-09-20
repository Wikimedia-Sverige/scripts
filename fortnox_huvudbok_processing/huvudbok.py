#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Crunch Huvudbok export.

python Crunch_huvudbok path_to_huvudbok.txt path_to_projects.json, year, fancy
"""
import json
import os
import string
import sys
from collections import defaultdict


class Huvudbok(object):
    """A representation of the Fortnox huvudbok."""

    COL_NAME = {
        'konto': 0,  # A
        'namn': 1,  # B
        'ks': 2,  # C
        'datum': 4,  # E
        'debet': 7,  # H
        'kredit': 8,  # I
    }
    KS_DEFAULT = 'saknar ks'

    def __init__(self, filename, projects=None, year='2018', fancy=False):
        self.year = year
        self.all_konto = {}
        self.konto = ''
        self.results = {}
        self.all_ks = set()
        self.projects = {}
        self.last_written_row = 0  # need to keep track of row labels

        if projects:
            self.projects = Huvudbok.load_projects(projects)

        self.process_and_output(filename, fancy)

    @staticmethod
    def load_file(filename):
        with open(filename, encoding='latin-1') as f:
            return f.readlines()

    @staticmethod
    def load_projects(filename):
        with open(filename) as f:
            return json.load(f)

    def process_and_output(self, filename, fancy):
        """Crunch the huvudbok and output the results."""
        i = 0
        for row in Huvudbok.load_file(filename):
            i += 1
            try:
                self.process_row(row)
            except (IndexError, KeyError, ValueError, TypeError):
                print('row {}: {}'.format(i, row))
                raise

        if self.year == '2018':
            self.tweak_2018()

        basename = os.path.splitext(filename)[0]
        if not fancy:
            out_name = '{}_crunched.tsv'.format(basename)
            with open(out_name, 'w') as self.f_out:
                self.basic_output()
        else:
            out_name = '{}_crunched_fancy.tsv'.format(basename)
            with open(out_name, 'w') as self.f_out:
                self.fancy_output()

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

    def basic_output(self):
        """Produce basic .tsv output containing only static data.

        Adds two header rows one with project ids and one with project names,
        along with a single summation line.
        """
        self.print_header_lines()

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
            self.print_tsv_line(line)

        # summation lines
        self.print_tsv_line([])
        line = ['', 'Total', '']
        for ks in sorted(self.all_ks):
            line.append('{:.2f}'.format(ks_sums.get(ks)))
        self.print_tsv_line(line)

    def fancy_output(self):
        """Produce .tsv output with sections and spreadsheet functions.

        Adds two header rows one with project ids and one with project names,
        along with a single summation line.

        Splits the konto output into sections with totals for each.

        The output is only suitable for being used in a spreadsheet supporting
        the SUM(A1:Z9)-function.
        """
        #@TODO:
        # Add functionality to output empty sections
        # Add end section summing between sections
        self.sections = (
            Section('Balanskonton', 1000, 3000, hide=True),
            Section('Verksamhetsintäkter', 3000, 3900),
            # this is actually 3520-3740 which lies inside the above range
            Section('Försäljningsintäkter', 3900, 3900),
            Section('Övriga intäkter', 3900, 4000),
            Section('Kostnader', 4000, 5000),
            Section('Övriga externa kostnader', 5000, 7000),
            Section('Personalkostnader', 7000, 8000),
            Section('Finansiella intäkter', 8000, 8400),
            Section('Finansiella kostnader', 8400, 8500),
        )
        self.print_header_lines()

        # Each lines
        active_section = None
        data_cols = self.get_data_cols(3)  # column letters in use for data
        for konto in sorted(self.results.keys()):
            # skip empty konto
            if not any(val != 0 for val in self.results[konto].values()):
                continue

            # handle sections
            if not active_section:
                active_section = self.get_active_section(
                    konto, write_header=True)
            elif int(konto) not in active_section.range:
                active_section = self.swap_section(
                    active_section, data_cols, konto)

            if not (active_section and active_section.hide):
                line = [konto, self.all_konto.get(konto),
                        self.current_row_sum_cell(data_cols)]  # id, name, sum
                for ks in sorted(self.all_ks):
                    val = self.results[konto].get(ks) or 0
                    line.append('{:.2f}'.format(val))
                self.print_tsv_line(line)

        # close any open section
        if active_section:
            self.close_current_section(active_section, data_cols)

        #add fancy final rows
        # want to insert Summa intäkter before Kostnader section
        # want to insert Summa kostnader + Verksamhetens över-/underskott before Finansiella intäkter section
        # want to insert RESULTAT in after last one

    def print_tsv_line(self, line):
        """Write a list as a .tsv row. to the output file."""
        self.f_out.write('\t'.join(line) + '\n')
        self.last_written_row += 1

    def print_header_lines(self):
        """Write two header rows, one with project names and one with ids.

        Also add headers for the leading columns.
        """
        line = ['', '', '']
        line += sorted(self.all_ks)
        self.print_tsv_line(line)

        line = ['konto', 'namn', 'Total']
        line += [self.projects.get(ks, '') for ks in sorted(self.all_ks)]
        self.print_tsv_line(line)

    def get_data_cols(self, leading_cols):
        """Return a list of column letters to which data is outputted.

        @param leading_cols: Number of columns with non-data
        """
        num_dat_cols = len(self.all_ks)  #+1 for unknown
        col_letters = list(string.ascii_uppercase)
        col_letters += ['A' + s for s in string.ascii_uppercase]
        return col_letters[leading_cols:][:num_dat_cols]

    def current_row_sum_cell(self, data_cols):
        """Create a string for a summation over the next row to be written.

        @param data_cols: list of data column letters to sum over
        """
        row = self.last_written_row + 1
        base_string = '=SUM({first_col}{row}:{last_col}{row})'
        return base_string.format(
            row=row, first_col=data_cols[0], last_col=data_cols[-1])

    def close_current_section(self, current_section, data_cols):
        """Close the current section and output a summation row."""
        current_section.end_row = self.last_written_row

        # output summation row
        if not current_section.hide:
            line = ['Summa {}'.format(current_section.name), '',
                    self.current_row_sum_cell(data_cols)]
            line += [current_section.col_sum_cell(col) for col in data_cols]
            self.print_tsv_line(line)
            self.print_tsv_line([])

    def swap_section(self, current_section, data_cols, konto):
        """Close the current section and return the new section."""
        self.close_current_section(current_section, data_cols)

        return self.get_active_section(konto, True)

    def get_active_section(self, konto, write_header=True):
        """Return the section applicable to the current konto."""
        for section in self.sections:
            if int(konto) in section.range:
                if write_header and not section.hide:
                    self.print_tsv_line([section.name])
                section.start_row = self.last_written_row
                return section


class Section(object):
    """A section represents a series of konto to be grouped together."""

    def __init__(self, name, start_konto, end_konto, hide=False):
        self.name = name
        self.range = range(start_konto, end_konto)
        self.hide = hide  # whether this section should not be outputted
        self.start_row = None  # row number for first outputted section data
        self.end_row = None  # row number for last outputted section data

    def col_sum_cell(self, col):
        """Create a string for a summation over a column of the section.

        @param col: The column letter to sum over
        """
        base_string = '=SUM({col}{start_row}:{col}{end_row})'
        return base_string.format(
            col=col, start_row=self.start_row, end_row=self.end_row)


def fix_num(cell_value):
    """Convert Swedish style numbering to standard format."""
    if not cell_value.strip():
        return 0
    value = cell_value.replace(' ', '').replace(',', '.')
    return float(value)


def is_int(value):
    """Check if the given value is an integer.

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