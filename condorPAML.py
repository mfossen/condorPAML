#!/usr/bin/env python2.6

import os,glob,sys,subprocess,getopt

#fastaDir = "./fastafiles"
fastaDir = os.path.realpath("./fastafiles")
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"
submitFileLocation = "/opt/PepPrograms/genewisepaml/submit.condor"

def submit(fastaDir, genewisePAMLLocation, submitFileLocation):
    if not os.path.isdir(fastaDir): os.mkdir(fastaDir)

    topdir = os.getcwd()+"/"+fastaDir

    for root, dirs, files in os.walk('.'):
        for fastafile in files: 
            #if root == fastaDir : break
            if fastafile.endswith(".fasta"):
                fullpath = os.path.realpath( root+"/%s" % str(fastafile) )
                runpath = os.path.realpath( topdir + "/%s" % str(fastafile)[:-6] )

                if not os.path.isdir(runpath): os.mkdir(runpath)

                filename = runpath+"/%s" % str(fastafile) 
                if os.path.lexists(filename):
                    os.remove(filename)		
                os.symlink(fullpath , filename)
                
                #submitFile = runpath + "/" + os.path.basename(submitFileLocation)
                #if os.path.lexists(submitFile): os.remove(submitFile)
                #os.symlink(submitFileLocation , submitFile )

    os.chdir(topdir)

    #for fastaDir in glob.glob(topdir+"/*"):
    for dir in os.listdir(topdir):
        if os.path.isdir(dir):
            os.chdir(dir)
            if debug == True:
                out = err = None
                print os.getcwd()
            else: out = err = open(os.devnull,"w")

            procList = []
            for num in range( int( singleNum ) ):
                process = subprocess.Popen([genewisepamlLocation,"-a", glob.glob("*.fasta")[0] ] \
                    ,stdout=out,stderr=err)

                procList.append(process)

            if single: 
                for proc in procList:
                    if debug: print "PID is %s" % proc.pid
                    proc.wait()
                
            os.chdir(topdir)


def cat():
    nfile = open("results_neutral.txt","w")
    sfile = open("results_significant.txt","w")
    os.chdir(fastaDir)
    for dir in os.listdir(fastaDir):
        if os.path.isdir(dir):
            os.chdir(dir)
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
    
    nfile.close()
    sfile.close()

def usage():
    print """Usage: %s <command> <command> ...
commands:
help\tprint out usage information

submit\tset up directories, make symlinks, and run genewisePAML.py

debug\toutput more information than usual to the terminal

single <num>\t submit <num> jobs at a time, useful to keep an eye on output or if the server is being used heavily by other processes
""" % sys.argv[0]
    
def main(argv):
    if len(argv) == 0 or argv[0] == "help":
        usage()
        sys.exit(1)

    global debug
    debug = True if ("debug" in argv) else False

    if "submit" in argv:
        global singleNum
        global single

        single = True if "single" in argv else False
        try: singleNum = argv[ argv.index("single") + 1 ]
        except: singleNum = 1

        print singleNum
        submit(fastaDir,genewisepamlLocation,submitFileLocation)


main(sys.argv[1:])
