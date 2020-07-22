from sourceCode import Chuncker

import numpy as np

from itertools import product
from bs4 import BeautifulSoup


def table_to_2d(table_tag):
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1.
        # a colspan of 0 means “fill until the end” but can really only apply
        # to the last cell; ignore it elsewhere.
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom.
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table


class Holder:
    def __init__(self):
        None

    def get_table_text(self, table_text):
        table2 = BeautifulSoup(table_text, 'html.parser')

        try:
            table_data_list = table_to_2d(table_tag=table2)

            tr_lines = table_text.split('<tr>')
            tr_lines.pop(0)

            table_heads = []
            table_data = []

            if len(tr_lines) == len(table_data_list):
                for i in range(len(tr_lines)):
                    if tr_lines[i].find('<th') != -1:
                        table_heads.append(table_data_list[i])
                    else:
                        table_data.append(table_data_list[i])
            # print(len(table_heads), len(table_data))
            if len(table_heads) > 0:
                self.table_head = table_heads[-1]
            else:
                self.table_head = table_data[0]
            self.table_data = table_data

            transposed_table = True
            for line in tr_lines:
                if line.find('<th') == -1:
                    transposed_table = False

            if transposed_table is True:
                self.table_head = []
                self.table_data = []
                for table_data in table_data_list:
                    head_word = table_data.pop(0)
                    self.table_head.append(head_word)
                    self.table_data.append(table_data)

        except:
            self.table_head = []
            self.table_data = []
            return

    def get_data_line(self, question):
        chuncker = Chuncker.Chuncker()
        chuncker.get_feautre(question)

        scores = []

        for data in self.table_data:
            string = ''
            for word in data:
                if word is not None:
                    string += word + ' '

            scores.append(chuncker.get_chunk_score(string))

        if len(scores) == 0:
            return 0

        return np.array(scores, dtype=np.float32).argmax()

