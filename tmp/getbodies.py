#!/usr/bin/env python

import glob
import textwrap

def do_bodies():
    print("# coding: utf-8\n")
    print("bodies = {")
    for fn in glob.glob("docs/*txt"):
        t = file(fn).read()
        print('"'+fn.split('.')[0].split('/')[1]+'": """')
        #t = textwrap.fill(t, replace_whitespace=False)
        print(t)
        print('""",')
    print("}")

if __name__ == "__main__":
    do_bodies()

# vim: set ts=4 sw=4 expandtab :
