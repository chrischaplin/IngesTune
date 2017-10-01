#
# This is a collection of utility functions for 
# mapping the master_input designated key-value pair to
# the template file
#
#

from numpy import *
from shutil import *
import os
import subprocess

def titleMake(a_x,a_L,a_varName,a_varValue,a_fileExt,a_template,a_fName):

    # Generate the name for the set of configs
    m_str = a_varName[0][a_x[0]] + '.'
    m_val = [a_varValue[0][a_x[0]]]
    for i in range (a_L-1):

        m_str = m_str + a_varName[i+1][a_x[i+1]] + '.'
        
        if ( (type(a_varValue[i+1][a_x[i+1]]) == list)
             and (len(a_varValue[i+1][a_x[i+1]]) > 1) ):
            tempStr = arrayToString(a_varValue[i+1][a_x[i+1]])
        else:
            tempStr = a_varValue[i+1][a_x[i+1]]
                  
        m_val.append(tempStr)

    m_str = m_str + a_fileExt

    # Call file copying and editing functions
    copyfile(a_template,m_str)
    editFile(a_L,m_str,a_template,m_val,a_fName)
    fixFile(m_str)
    

def columnLength(a_length,a_numVar):
   m_col = zeros(a_length)
   for col in range(a_length, 0, -1):
      if (col == (a_length)):
         m_col[col-1] = 1;
      else:
         m_col[col-1] = a_numVar[col]*m_col[col]
   return m_col


def arrayToString(a_array):
   m_str = ' '.join(map(str,a_array))
   return m_str


def editFile(a_L,a_str,a_template,a_values,a_fName):
    # Copy the template and put in the new values
    
    datafile = file(a_template)
    outfile = open('temp','w')
    outfile.write("[producer_config]\n")
    for line in datafile:
        p = 0
        for ind in range (a_L):
         
            if (a_fName[ind] + ' =') in line:
                localVar = str(a_values[ind])
                confline = a_fName[ind] + " = " + localVar + '\n'
                outfile.write(confline)
                p = 1            
      

        if (p == 0 and line[0] != '#' ):
            outfile.write(line)

    outfile.close()


   
def fixFile(a_str):
    # Remove blank lines
    
    finalfile = open(a_str,'w')
    with open('temp','r+b') as outfile:
        for line in outfile:
            if not line.isspace():
                finalfile.write(line)

    os.remove('temp')
