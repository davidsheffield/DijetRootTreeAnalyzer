#! /usr/bin/env python

import os
import sys
import optparse
import datetime
import subprocess
import re

usage = "usage: To be run from DijetRootTreeAnalyzer/ :  python scripts/check_batch_EOS_split.py -i batchDir -s storageDir"

parser = optparse.OptionParser(usage)

parser.add_option("-i", "--input", dest="inputDir",
    help="batch directory",
    )

parser.add_option("-s", "--inputStorage", dest="storageDir",
    help="storage directory",
    )

(opt, args) = parser.parse_args()

proc = subprocess.Popen(["ls %s | grep .src | grep -v \"\~\"" % opt.inputDir], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out = out.splitlines()
#print out

procResub = subprocess.Popen(["less %s" % opt.inputDir+"/bsub_commands.txt"], stdout=subprocess.PIPE, shell=True)
(outResub, errResub) = procResub.communicate()
outResub = outResub.splitlines()
#print outResub

overallresubmit = 0

for srcFile in out:   

    resubmit = 0

    srcFile.rstrip('\n')
    numberOfJob = ((srcFile.split(".")[0]).split("_"))[-1]
    print numberOfJob + " " + srcFile

    logfile =  "logfile"+((srcFile.split("submit")[1]).split(".src")[0])+".log"
    #print logfile

    crablogfile =  "crablogfile"+((srcFile.split("submit")[1]).split(".src")[0])+".crablog"
    #print crablogfile

    datfile =  "cutEfficiencyFile"+((srcFile.split("submit")[1]).split(".src")[0])+".dat"
    #print datfile

    rootfile =  "rootfile"+((srcFile.split("submit")[1]).split(".src")[0])+".root"
    #print rootfile

    rootfilereduced =  "rootfile"+((srcFile.split("submit")[1]).split(".src")[0])+"_reduced_skim.root"
    #print rootfilereduced


    #check presence of logfile
    proclog = subprocess.Popen(["ls %s" % opt.inputDir+"/"+logfile], stdout=subprocess.PIPE, shell=True)
    (outlog, errlog) = proclog.communicate()
    #print "len(outlog)="+str(len(outlog))
    if len(outlog) == 0:
        resubmit = 1
        overallresubmit = 1

    #check presence of crablogfile
    proccrablog = subprocess.Popen(["ls %s" % opt.inputDir+"/"+crablogfile], stdout=subprocess.PIPE, shell=True)
    (outcrablog, errcrablog) = proccrablog.communicate()
    #print "len(outcrablog)="+str(len(outcrablog))
    if len(outcrablog) == 0:
        resubmit = 1
        overallresubmit = 1

    #check content of crablogfile
    proccrablogcont = subprocess.Popen(["less %s" % opt.inputDir+"/"+crablogfile], stdout=subprocess.PIPE, shell=True)
    (outcrablogcont, errcrablogcont) = proccrablogcont.communicate()
    #print outcrablogcont
    if ("Successfully completed." in outcrablogcont)==False:
        resubmit = 1
        overallresubmit = 1


    if resubmit == 1:
        print "=== job "+numberOfJob+" should be resubmmitted"
        print outResub[int(numberOfJob)]
        os.system(outResub[int(numberOfJob)])

        
    
if  overallresubmit == 0:
    print "All jobs are done successfully"




