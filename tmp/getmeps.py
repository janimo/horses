#!/usr/bin/env python

import xlrd

xlsfile = 'meps_jan25.xls'

def do_one_sheet(s):
    for r in range(1,s.nrows):
        row = s.row_values(r)
        if row[1] == '':
            print(row[0], row[2])

def get_meps(file):
    wb = xlrd.open_workbook(file)
    for sn in wb.sheet_names():
        s = wb.sheet_by_name(sn)
        print(sn)
        do_one_sheet(s)

if __name__ == "__main__":
    get_meps(xlsfile)

# vim: set ts=4 sw=4 expandtab :
