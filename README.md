Running genewisePAML.py on Condor
============

All the necessary files are stored in SNPsnap under the directory /opt/PepPrograms/genewisepaml

The script that handles everything is named `condorPAML.py` and can be copied wherever you like (or run using /opt/PepPrograms/genewisepaml/condorPAML.py), it only requires that a modified genewisePAML.py and submit.condor exist in /opt/PepPrograms/genewisepaml

condorPAML.py should be run in a directory that contains .fasta files, and will create a directory that is named `fastafiles` to work in unless you edit the script to something different.

So it will look like this after running `./condorPAML.py submit` in a directory named `files` that contains file1.fasta, file2.fasta, and file3.fasta

```
/home/user/files
                      |--file1.fasta
                      |--file2.fasta
                      |--file3.fasta
                      |--condorPAML.py
                      |--fastafiles/
                                       |--file1/
                                                |--file1.fasta
                                                |--other files...
                                       |--file2/
                                                 |--file2.fasta
                                                 |--other files...
                                       |--file3/
                                                 |--file3.fasta
                                                 |--other files...
```

The basic commands can be seen by running `./condorPAML.py help`

Usually, it should be enough to enter `./condorPAML.py submit` but that will max out the server, so using `submit` with `single` like: `./condorPAML.py submit single 10` will limit it to 10 processes at a time or fewer and be easier on SNPsnap.
Adding the `debug` option at the end of the line will print out a bunch of info to the terminal if you want to see what's going on.

Once the jobs are submitted, Condor runs codeml on the file generated in the last step. You can keep an eye on them using `condor_q` to see when they finish.

Once the jobs finish on Condor or if you want to get some preliminary results, run the same submit command again, such as `./condorPAML.py submit single 15 debug` and it will finish processing the files returned from Condor.

It's also possible to run `./condorPAML.py cat` to have it collect all the individual results and write them to the files `results_neutral.txt` and `results_significant.txt` in the current directory.

If the condor jobs were interrupted before completing, you can run `./condorPAML.py submit single 15 debug` which will process the files, and then run `./condorPAML.py remove debug` which will let you resubmit jobs to condor if genewisePAML.py didn't complete successfully.

