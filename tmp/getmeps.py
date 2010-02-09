#!/usr/bin/env python

import xlrd

xlsfile = 'meps_jan25.xls'

def do_one_sheet(s):
    for r in range(1,s.nrows):
        row = s.row_values(r)
        if row[1] == '':
            print('"'+row[0][0:2]+" "+row[2].strip()+'",')

def get_meps(file):
    wb = xlrd.open_workbook(file)
    for sn in wb.sheet_names():
        s = wb.sheet_by_name(sn)
        print('"'+sn+'": [')
        do_one_sheet(s)
        print("],")

if __name__ == "__main__":
    print("meps = {")
    get_meps(xlsfile)
    print("}")

# vim: set ts=4 sw=4 expandtab :
