#!/usr/bin/env python2.6

import os,glob,sys,subprocess,getopt

inputDir = os.path.realpath(".")
fastaDir = os.path.realpath("./fastafiles")
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"

def submit(fastaDir, genewisePAMLLocation):
    if not os.path.isdir(fastaDir): os.mkdir(fastaDir)

    numFiles = 0
    for fastafile in os.listdir(inputDir):
        if os.path.isfile(fastafile): 

            if fastafile.endswith(".fasta"):

                fullpath = os.path.realpath(fastafile)
                runpath = os.path.realpath( fastaDir + "/%s" % str(fastafile)[:-6] )

                if not os.path.isdir(runpath): os.mkdir(runpath)

                filename = runpath+"/%s" % str(fastafile) 

                try: os.symlink(fullpath , filename)
                except: pass
                os.chdir(runpath)
                open("SUBMITTED","w").close()

                numFiles += 1
                os.chdir(inputDir)
                
    os.chdir(fastaDir)

    procList = []
    curFile = 0

    for dir in os.listdir(fastaDir):
        if os.path.isdir(dir):
            os.chdir(dir)
            if debug:
                out = err = None
                print "Current Directory:\t%s" % os.getcwd()

                curFile += 1
                print "On file %d out of %d" % (curFile,numFiles)

            else: out = err = open(os.devnull,"w")


            process = subprocess.Popen([genewisepamlLocation,"-a", glob.glob("*.fasta")[0] ] \
                ,stdout=out,stderr=err)

            procList.append(process)
            
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

            os.chdir(fastaDir)

    
def cat():
    nfile = open("results_neutral.txt","w+")
    sfile = open("results_significant.txt","w+")
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

def usage():
    print """Usage: %s <command> <command> ...
commands:
help\tprint out usage information

submit\tset up directories, make symlinks, and run genewisePAML.py

debug\toutput more information to the terminal

single [num]\t submit <num> jobs at a time, useful to keep an eye on output or if the server is being used heavily by other processes

cat\t concatenate all the pamlResults_neutral.txt files into results_neutral.txt and pamlResults_significant.txt files into results_significant.txt in the current working directory
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

main(sys.argv[1:])
