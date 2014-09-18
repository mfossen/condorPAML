#!/usr/bin/env python2.6

import os
import glob
import sys
import subprocess
import getopt

# default paths the file locations
inputDir = os.path.realpath(".")
fastaDir = os.path.realpath("./fastafiles")
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"

# submit will create the necessary directories and set up symlinks before calling
#  genewisePAML.py that uses wrappersCondor.py (modified from the normal wrappers.py
#  that egglib normally provides) to submit a job to condor
def submit(fastaDir, genewisepamlLocation):

    # create a directory to hold the files, if it doesn't already exist
    if not os.path.isdir(fastaDir): os.mkdir(fastaDir)

    numFiles = 0 # keep track of how many files have been processed and how many are left

    # get a list of every file and directory in "inputDir" and loop through them
    for fastafile in os.listdir(inputDir):

        if os.path.isfile(fastafile): # only process files in the current working directory

            if fastafile.endswith(".fasta"):

                fullpath = os.path.realpath(fastafile)

                # create folders under "fastaDir" using the name of the fasta file without the extension
                runpath = os.path.realpath( fastaDir + "/%s" % str(fastafile)[:-6] )

                if not os.path.isdir(runpath): os.mkdir(runpath)

                filename = runpath+"/%s" % str(fastafile) 

                # use a symlink from the original file to the working directories to save on 
                #  time and space that would be spent copying them
                try: os.symlink(fullpath , filename)
                except: pass

                os.chdir(runpath) # change into the created folder
                open("SUBMITTED","w").close() # create a file to show the job has been submitted 

                numFiles += 1 
                os.chdir(inputDir) # change back into the folder containing the .fasta files
                

    os.chdir(fastaDir) # change into the folder where the jobs will be submitted

    procList = [] # keep a list of processes that have been submitted to control resource usage
    curFile = 0 # keep track of the progress

    for dir in os.listdir(fastaDir): # loop through every directory that was created in the last loop
        if os.path.isdir(dir): # make sure it's a directory, and change into it
            os.chdir(dir)
            if debug:
                out = err = None
                print "Current Directory:\t%s" % os.getcwd()

                curFile += 1
                print "On file %d out of %d" % (curFile,numFiles)

            else: out = err = open(os.devnull,"w") # if condorPAML.py isn't called with the debug
                                                   #  option, send output to /dev/null

            # submit the job in the background and add the object that is returned to the process lit
            process = subprocess.Popen([genewisepamlLocation,"-a", glob.glob("*.fasta")[0] ] \
                ,stdout=out,stderr=err)

            procList.append(process)
            
            # if the single option was used, start the number of jobs that was specified and
            #  wait for them to finish before removing the process from the list and continuing
            if single and len(procList) == singleNum: 
                for item in procList:
                    if debug: 
                        print "PID is %s" % item.pid
                        print "List length:\t%d" % len(procList)
                    try:
                        if debug:print "Waiting"
                        item.wait()
                        procList.remove(item)
                    except: break

            os.chdir(fastaDir) # change back into the fastaDir and process the next folder that contains a fasta file

    
# the cat function will find all the individual results and concatenate them and sort them 
#  into two overall results files
def cat():
    # open two files for reading and writing
    nfile = open("results_neutral.txt","w+")
    sfile = open("results_significant.txt","w+")

    # Process the folders that have the fasta files and make sure they contain the file
    #  DONE before trying to open the result files for reading, and write their contents 
    #  into the two concatenated results files
    os.chdir(fastaDir)
    for dir in os.listdir(fastaDir):
        if os.path.isdir(dir):
            os.chdir(dir)
            if not os.path.isfile("./DONE"):
                os.chdir(fastaDir)
                continue;
        try: 
            file = open("pamlResults_neutral.txt","r")
            nfile.write( file.read() )
            file.close()
        except: pass

        try:
            file = open("pamlResults_significant.txt","r")
            sfile.write( file.read() )
            file.close()
        except: pass
        os.chdir(fastaDir) 
    
    # Return to the beginning of the files using seek(0), then read the lines into a list and again 
    #  return to the beginning of the file before writing out the sorted results and closing.
    nfile.seek(0)
    lines = nfile.readlines()
    nfile.seek(0)
    nfile.writelines( sorted(lines) )
    nfile.close()

    sfile.seek(0)
    lines = sfile.readlines()
    sfile.seek(0)
    sfile.writelines( sorted(lines) )
    sfile.close()

def remove():
   os.chdir(fastaDir)
   for dir in os.listdir(fastaDir):
    if os.path.isdir(dir):
      os.chdir(dir)
      if os.path.isfile("./SUBMITTED") and not os.path.isfile("./DONE"):
        try: 
          submit = os.path.realpath("./SUBMITTED")
          os.unlink(submit)
          if debug:
            print "Removed %s" % submit
        except: pass

    os.chdir(fastaDir)




def usage():
    print """Usage: %s <command> <command> ...
commands:
help\tprint out usage information

submit\tset up directories, make symlinks, and run genewisePAML.py

debug\toutput more information to the terminal

single [num]\t submit <num> jobs at a time, useful to keep an eye on output or if the server is being used heavily by other processes

cat\t concatenate all the pamlResults_neutral.txt files into results_neutral.txt and pamlResults_significant.txt files into results_significant.txt in the current working directory



The submit command will have to be used twice - once to submit the jobs to condor, then once more to process the file that gets returned and write out the results
""" % sys.argv[0]
    
def main(argv):
    if len(argv) == 0 or argv[0] == "help":
        usage()
        sys.exit(1)

    global debug
    debug = True if "debug" in argv else False

    if "submit" in argv:
        global singleNum
        global single

        single = True if "single" in argv else False
        try: 
            singleNum = int( argv[ argv.index("single") + 1 ] )

        except: singleNum = 1
        
        submit(fastaDir,genewisepamlLocation)
    
    if "cat" in argv:
        cat()

    if "remove" in argv:
      remove()


main(sys.argv[1:])
