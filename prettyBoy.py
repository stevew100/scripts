#!/usr/bin/python

import sys
import re

# This wee script processes the output from HP-UX swlist into a form suitable for a pivot table.

# Usage: ssh root@<host> swlist | ./prettyBoy.py


################################# Sample Output ..... #################################
# # Initializing...
# # Contacting target "nzlhp05"...
# #
# # Target:  nzlhp05:/
# #
#
# #
# # Bundle(s):
# #
#   B2491BA                               B.11.23        MirrorDisk/UX (Server)
#   B3901BA                               C.11.23.09     HP C/ANSI C Developer's Bundle (S800)
#   B3913DB                               C.11.23.09     HP aC++ Compiler (S800)
#   ...
#   vParProvider                          B.11.23.01.07  vPar Provider - HP-UX
# #
# # Product(s) not contained in a Bundle:
# #
#
#   HP_LTT417                             4.17.0.0       Library & Tape Tools - HP-UX
#   MCPS-AVC                              A.02.06.00.00214 HP Availability Collector
#   MCPS-COLLECT                          A.01.04.00.00  HP Technology Assessments ISEE Manual Collector
#   ...
#   sapr                                   0.9.18         apr
#   apr_util                              0.9.17         apr_util
#   bash                                  3.2            bash
#   ...
#################################                    #################################

type='';
data = sys.stdin.read()

lines = data.splitlines()
for line in lines:
    # convert tabs
    line = re.sub('\t+',' ',line)
    # reduce multiple spaces
    line = re.sub(' +',' ',line)

    #Grab the host name
    if line.find('target') >= 0:
        bits = line.split(' ',4)
        host = str(bits.pop()).translate(None, '".');
        continue;

    # Detect type of Package
    if line.find('# Bundle(s)') == 0:
        type='Bundle';
        continue;
    if line.find('not contained in a Bundle') > 0:
        type='Package';
        continue;

    # Ignore comments and empty lines
    if line.find('#') >= 0:
        continue;

    if len(line) == 0:
        continue;

    # Process package/bundle
    bits = line.split(' ',3)

    package = bits.pop()
    version = bits.pop()
    description = bits.pop()

    if version != 'target':
        print host + "|" + type  + "|" + package + "|" + version + "|" + description
