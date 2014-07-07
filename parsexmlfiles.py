#!/usr/bin/env python
#
# This File contains classes for each kind of XML find.
#
# This is the Main File, that should be run inorder to start the
# parsing, it takes two arguments.
#
# The structure of the data directory should be 
#

import sys, os
import errno
import getopt
import fnmatch, copy
import logging
from logging.handlers import RotatingFileHandler 

from tms import buildClass
from tms import on_gallery_episodes

from parsexmllogs import DIRECTParserError

parser_logger = logging.getLogger('parsexmlfiles')


# parseall
#
# Parse all the files in the inDir and store the output 
# in the outDir.
# Can well start multiple threads and run them in parallel.
#
def parseXLSfiles(inDir, outDir):
    currDir = os.path.dirname(os.path.realpath(__file__))

    parser_logger.info("\n +++++++++++++++++++++++++++++++++++")
    try:
        lsFiles = []
        for sName in os.listdir(inDir):
            if os.path.isfile(os.path.join(inDir, sName)):
                lsFiles.append(sName)

	# Take the first file and find which template is applicable 

        build = buildClass()

        for inputFile in lsFiles:
            compOutputFileName = outDir + inputFile[0:-3] + "xls"
            parser_logger.debug("Input File : " + inputFile )
            parser_logger.debug("Output File : " + compOutputFileName)
            # For Testing ---- Trying to fail
            # className = className + "red"
            # Make a call to the className
            parserObject = build.construct(inputFile, inDir)
            if parserObject is None:  # No matching class for this file
                parser_logger.warning(" *************************************** ")
                parser_logger.info("FAILURE : NO FILE CLASS FOR FILE : " + inputFile)
                parser_logger.warning(" *************************************** ")
                continue # Continue to the next file
      
            # Parse the file.
            parserObject.parse(compOutputFileName)
        return;
    except DIRECTParserError as direct:
        errormessage = "ERROR : " + direct.__str__()
        parser_logger.error(errormessage)
    return;

# Method : set_logger()
#
# Set the Logging Mechanism. If script is started as a daemon,
# the Log File Name should be given through the command line.
# Else we will just dump everything to the standard output.
#
def set_logger(logFile,debugmode):
    # Setting the format
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    parser_logger = logging.getLogger('parsexmlfiles')
    
    if not logFile is None:
        # Log into a Log File.
        rotatingFH = RotatingFileHandler(logFile, mode='a', 
                                         maxBytes=20970020, backupCount=7,
                                         encoding=None, delay=False)
        rotatingFH.setFormatter(logging.Formatter(
                                    fmt="%(asctime)s : %(levelname)s : %(message)s", 
                                    datefmt=None))
        parser_logger.addHandler(rotatingFH)
    else:
        # Else dump to the stout.
        toScreen = logging.StreamHandler(sys.stdout);
        parser_logger.addHandler(toScreen);
    
    if debugmode is True:
        parser_logger.setLevel(logging.DEBUG)
    else:
        parser_logger.setLevel(logging.INFO)
    
    return

# Method : usage()
#
# This is a simple method that would print how the script should be 
# initiated.
def usage():
    print "\nNAME "
    print "\tparsexmlfiles.py -- Parse XML files\n"

    print "SYNOPSIS \n"
    print "\tpython parsexmlfiles.py --datadir=[directory] --logfile=[filename]"
    print "\tpython parsexmlfiles.py --datadir=[directory] --logfile=[filename]"
    print "\tpython parsexmlfiles.py --datadir=[directory] --logfile=[filename ]"

    print "\nDESCRIPTION"
    print "\tparsexmlfile.py script would parse XML files and store them is SQL database."
    
    print "\nOPTIONS"
    print "\tThese are the options."

    print "\n\t--datadir=[directory]"
    print "\t\tThe datadir is mandatory."

    print "\n\t--logfile=[filename]"
    print "\t\tThe full path of the file that would store the logs."

    print "\n\t--parseAndSaveSQL"
    print "\t\tIf you only want the XLS files to be generated."

    print "\n\t--debug"
    print "\t\tUsed only for debugging purposes. Would print a lot of log messages."
    
    print "\nEXAMPLES"
    print "\n\tThe following would parse the XML files located in \"/root/dataproducts/\" and generate the XLS file"
    print "\t\tEg: python parsexmlfiles.py --datadir=/root/dataproducts/ --logfile=/tmp/logfile"

    print "\n\tThe following would parse the XML files located in \"/root/dataproducts/\" and generate the XLS file"
    print "\t\tEg: python parsexmlfiles.py --datadir=/root/dataproducts/ --parsexls --logfile=/tmp/logfile"
    
def main(argv):
    datadir = None
    logfile = None
    debugmode = False
    isdaemon = False
    parseXLS = False;
    parseKML = False;
    try:
        opts,args = getopt.getopt(argv, "dmlb:h", ["datadir=", "logfile=", "debug", "parsemat", "parsekml", "help"])
    except getopt.GetoptError:
        print "error"
        usage();
        sys.exit(2)                     

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage();
            sys.exit()
        elif opt in ("-d", "--datadir"):
            datadir = arg;
        elif opt in ("-l", "--logfile"):
            logfile = arg;
        elif opt in ( "--parsexls"):
            parseXLS = True;
        elif opt in ("--debug"):
            debugmode = True;
        else:
            print 'Last \n'
            usage()
            sys.exit()

    if datadir is None:
        print(" Cannot Start : No Data Directory Given\n")
        usage()
        sys.exit()
    
    # Arguments are good.

    # Force XLS parsing.
    if (parseXLS == False):
        parseXLS = True;

    # Set Logger.
    set_logger(logfile,debugmode)
    decay = []
    
    # FOR TESTING I am making the same structure locally.
    # parsing the xml logs from the actual data and storing the 
    # mat files locally.
    outputdir = "/Users/harmanpatial/temp/kalpana/xlsfiles/";
    inputdir = datadir;
    count = 0;
        
    try:
        parser_logger.info("Processing Directory : " + datadir)

        parser_logger.info("Input Dir : " + inputdir)
        parser_logger.info("Output Dir : " + outputdir)
                
        # Let's parse the XML files.
        if (parseXLS == True):
	    parseXLSfiles(datadir, outputdir) #parseXLSFiles
        else:
            decay.append(inputdir)
    except IOError (errno, os.strerror):
        print "I/O error({0}): {1}".format(errno, os.strerror)
 
    print " Parsing in Complete, go for a Run"

# Call the Main Function
if __name__ == "__main__":
    main(sys.argv[1:])
