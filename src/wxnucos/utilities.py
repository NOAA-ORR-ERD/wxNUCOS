#!/usr/bin/env python

"""
Utilities used by Conveter
"""

def NoCaseCompare(str1, str2):
    """
    A comparison function that will allow a sort of a list of string case-insentivly
    """
    return cmp(str1.lower(), str2.lower())

def SignificantFigures(inString, Min=3, Max=8):
    """
    returns how many significant figures the output should have, given the input

    inString: input string
    Min:   minumum number of figures allowed
    Max:   maximum number of figures allowed

    """
    # this is not quite really sigfigs, as all zeros are
    # counted, but it looks better it is set to a minimum of 4
    # figures and maximum of 7, as there are no more than 7
    # digits in the conversion factors
    return min( max(len(inString.split("e")[0].replace(".","").lstrip("0")), Min), Max)


if __name__ == "__main__":
    # some test code
    test_inputs =  ["123"
                    "123.23",
                    "1e34",
                    "1.3456e-5",
                    "1.00",
                    "1.000000",
                    "123.45659834657869",
                    "34.00000000000e45",
                    "0.000123",
                    ]
    for s in test_inputs:
        print("input:", s ,  SignificantFigures(s))

