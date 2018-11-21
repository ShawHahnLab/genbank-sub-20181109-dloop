#!/usr/bin/env python

"""
Take original annotations spreadsheet and create a GenBank-compatible features
table, optionally excluding a single entry (via the first command-line
argument).  This is very much dependent on this specific annotation
spreadsheet!
"""

import csv
import sys

writer = csv.writer(sys.stdout, delimiter='\t')
reader = csv.reader(sys.stdin, delimiter='\t')

# First five columns in input:
#     Sequence Name
#     Name
#     Type
#     Minimum
#     Maximum

# A seqID to exclude from parsing.
# (We have a custom .tbl chunk for SY94.)
try:
    exclude = sys.argv[1]
except IndexError:
    exclude = None

next(reader) # skip header
seqid_current = None
feature_current = None
for line in reader:
    seqid    = line[0]
    modifier = line[1]
    feature  = line[2]
    start    = line[3]
    stop     = line[4]
    if exclude and exclude == seqid:
        continue
    # For new seqid, write SeqID line, and ensure we'll take in new Feature
    # line too.
    if not seqid_current or seqid_current != seqid:
        seqid_current = seqid
        feature_current = None
        writer.writerow([">Feature %s" % seqid, "", "", "", ""])
    # For new feature, write Feature line
    #if not feature_current or feature_current != feature:
    #    feature_current = feature
    # Without this, we get an error:
    # "ERROR: Bad location on feature tRNA (start -1, stop -1)"
    # and there will be no tRNA entry in the output.
    if feature == "tRNA":
        stop = stop.strip("<>")
    writer.writerow([start, stop, feature, "", ""])
    # Anything else is modifier line
    # D-loop should have no modifier specified.
    # tRNA should use the modifier name "product".
    if feature == "tRNA":
        mod_name = "product"
        writer.writerow(["", "", "", mod_name, modifier])
    elif feature == "gene":
        mod_name = "gene"
        writer.writerow(["", "", "", mod_name, modifier])
    elif feature == "D-loop":
        pass
    # That's everything I've tried to handle here.
    else:
        raise Warning("feature modifier not known: %s" % modifier)
        mod_name = modifier
        writer.writerow(["", "", "", mod_name, modifier])
