#!/usr/bin/env python2.6

import os,glob,sys,subprocess,getopt

fastaDir = "./fastafiles"
genewisepamlLocation = "/opt/PepPrograms/genewisepaml/genewisePAML.py"
submitFileLocation = "/opt/PepPrograms/genewisepaml/submit.condor"

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
            else: out = err = open("/dev/null","w")
            process = subprocess.Popen([genewisepamlLocation,"-a", glob.glob("*.fasta")[0] ] \
                    ,stdout=out,stderr=err)

def usage():
    print """Usage: %s <command>
commands:
help\tprint out usage information

submit\tset up directories, make symlinks, and run genewisePAML.py

debug\toutput more information than usual to the terminal
""" % sys.argv[0]
    
def main(argv):
    if len(argv) == 0 or argv[0] == "help":
        usage()
        sys.exit(1)

        #if opt == "--debug": debug = True
        debug = True if (opt == "--debug") else False
        if opt in ("-s", "--submit"):
            submit(fastaDir,genewisepamlLocation,submitFileLocation,debug)


main(sys.argv[1:])
