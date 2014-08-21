#!/usr/bin/env python2.6

import os,glob,sys,subprocess,getopt

fastaDir = "./fastafiles"
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"
submitFileLocation = "/opt/PepPrograms/genewisepaml/submit.sub"
debug = False

def submit(fastaDir, genewisePAMLLocation, submitFileLocation, debug=False):
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
                
                submitFile = runpath + "/" + os.path.basename(submitFileLocation)
                if os.path.lexists(submitFile): os.remove(submitFile)
                os.symlink(submitFileLocation , submitFile )

    os.chdir(topdir)

    for fastaDir in glob.glob(topdir+"/*"):
        if os.path.isdir(fastaDir):
            os.chdir(fastaDir)
            if debug == True: print os.getcwd()
            subprocess.Popen([genewisepamlLocation,"-a",glob.glob("*.fasta")[0] ])

def usage():
    print """Usage: ./condorPAML.py 
-h, --help\tprint out usage information

-s, --submit\tset up directories, make symlinks, and submit jobs to run on Condor

--debug\toutput more information to the terminal
"""
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs", ["help","submit","debug"] )
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if "-h" or "--help" in opt:
            usage()
            sys.exit(0)

        if "--debug" in opt: debug = True
        
        if "-s" or "--submit" in opt:
            submit(fastaDir,genewisepamlLocation,submitFileLocation,debug)

        else: usage()

    sys.exit(0)    

main(sys.argv[1:])
