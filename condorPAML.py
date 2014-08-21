#!/usr/bin/env python2.6

import os
import glob
import sys
import subprocess

fastaDir = "./fastafiles"
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"
submitFileLocation = "/opt/PepPrograms/genewisepaml/submit.sub"
# get options and list help info first




# make directory to run from

# make dirs within directory, using os.walk possibly


# os.symlink codeml and submit.sub into the created directories, make sure they copy correctly when condor_submit is called, possibly symlink the .fasta files in as well?

if not os.path.isdir(fastaDir): os.mkdir(fastaDir)

topdir = os.getcwd()+"/"+fastaDir

for root, dirs, files in os.walk('.'):
    for fastafile in files: 
        if root == fastaDir : break
        if fastafile.endswith(".fasta"):
            fullpath = os.path.realpath( root+"/%s" % str(fastafile) )
            runpath = os.path.realpath( topdir + "/%s" % str(fastafile)[:-6] )

            if not os.path.isdir(runpath): os.mkdir(runpath)

            filename = runpath+"/%s" % str(fastafile) 
            if os.path.lexists(filename):
                os.remove(filename)		
            os.symlink(fullpath , filename)
            
            submitFile = runpath + "/submit.sub"
            if os.path.lexists(submitFile): os.remove(submitFile)
            os.symlink(submitFileLocation , submitFile )

os.chdir(topdir)

for fastaDir in glob.glob(topdir+"/*"):
    if os.path.isdir(fastaDir):
        os.chdir(fastaDir)
        print os.getcwd()
        subprocess.Popen([genewisepamlLocation,"-a",glob.glob("*.fasta")[0] ])



sys.exit(0)    
