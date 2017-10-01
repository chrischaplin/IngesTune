#
#
# Executable that generates the "grid-search" config files 
# (all config key-value pairs are defined in master_input)
#
#


# This module contains all of the helper functions
from miscFunc import *

# Read in from master file
execfile('master_input')

L = len(fieldNames)
N = subFieldNumVar.prod()
x = zeros(L,int)
col = columnLength(L,subFieldNumVar)

# Outer Loop over total number of fields
for i in range(N):
    for j in range(L):
        x[j] = floor(i/col[j])
        x[j] = x[j] % subFieldNumVar[j]
        
        # Call the title making / file editing function
        titleMake(x,L,subFieldVarName,subFieldVarVal,fileExt,template,fieldNames)
    x[:] = 0
