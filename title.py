"""
This module was written for printing the title of each program in the package.
"""
from __future__ import print_function

def print_title(program, version):
    totleng = 66
    shrtlen = 66 - 4

    print("*" * totleng)
    welcmstrg = "Welcome to use the " + program + " program"
    print("*", welcmstrg.center(shrtlen), "*")
    versnstrg = "Version " + version
    print("*", versnstrg.center(shrtlen), "*")
    print("*", "Author: Pengfei Li".center(shrtlen), "*")
    print("*", "Merz Research Group".center(shrtlen), "*")
    print("*", "Michigan State University".center(shrtlen), "*")
    print("*" * totleng)

