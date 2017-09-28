# Not the best strategy, but works for identifying numpy funcs within
# For using copyfile function
# For linecaching
from numpy import *
from shutil import *
import os
import subprocess

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

def titleMake(a_x,a_L,a_varName,a_varValue,a_fileExt,a_template,a_fName):
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
   #genBenchmark(m_str)

def editFile(a_L,a_str,a_template,a_values,a_fName):
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

   finalfile = open(a_str,'w')
   
   with open('temp','r+b') as outfile:
      for line in outfile:
        if not line.isspace():
            finalfile.write(line)

   os.remove('temp')


""" def genBenchmark(a_str):

   f = open('confluent_benchmark.py','r')
   g = open(a_str,'r')

   bench_str = a_str
   bench_str.rsplit('.',1)[0]
   bench_str = bench_str + '_benchmark.py'
   
   h = open(bench_str,'w')

   for line in f:
      rec = line.strip()
      if rec.startswith('conf'):
         # Drop the final "}"
         line = line[:-2] + ',' + '\n'
         print(line)
         # Add each entry from config file
         for confline in g:
            confline = confline.rstrip('\n')
            line = line + confline + ',' + '\n'        
            print(line)
         # Edit the final part
         line = line[:-2] + '}' + '\n'
         print(line)

         # write the new line in place of the old one
         h.write(line)
        
      else:
        h.write(line)

   # close everything
   f.close()
   g.close()
   h.close()

   # Fix indentation
   command = "autopep8 -i %s" % bench_str
   subprocess.call(command , shell=True) """
