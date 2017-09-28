# Essentially like C inclusions...probably a better way of doing this
from numpy import *
from miscFunc import *
import os
import subprocess

# Read in from master file
execfile('master_input')

# Start of file (consider main def. and guard)
L = len(fieldNames)
N = subFieldNumVar.prod()
x = zeros(L,int)
col = columnLength(L,subFieldNumVar)

# Outer Loop over total number of fields
for i in range(N):
    for j in range(L):
        x[j] = floor(i/col[j])
        x[j] = x[j] % subFieldNumVar[j]

    # Call the title making / file editing (nested likely) function
    titleMake(x,L,subFieldVarName,subFieldVarVal,fileExt,template,fieldNames)
    x[:] = 0


# Just copy and edit a single input file....
#f = open('confluent_benchmark.py','r')
#g = open('b3.m0.c0.config','r')
#h = open('b3.m0.c0_benchmark.py','w')

#for line in f:
#    rec = line.strip()
#    if rec.startswith('conf'):
        # Drop the final "}"
#        line = line[:-2] + ',' + '\n'
#        print(line)
        # Add each entry from config file
#        for confline in g:
#            confline = confline.rstrip('\n')
#            line = line + confline + ',' + '\n'        
#            print(line)
        # Edit the final part
#        line = line[:-2] + '}' + '\n'
#        print(line)

        # write the new line in place of the old one
#        h.write(line)
        
#    else:
#        h.write(line)

# close everything
#f.close()
#g.close()
#h.close()

# Fix indentation
#command = "autopep8 -i %s" % b3.m0.c0_benchmark.py
#subprocess.call(command , shell=True)
