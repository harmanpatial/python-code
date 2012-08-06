#!/usr/bin/env python
#
# This File contains classes for each kind of XML find.
#
# Harman Patial
# UDEL/CSHEL
# October 2011
#
# This is the Main File, that should be run inorder to start the
# parsing, it takes two arguments.
#
# The structure of the data directory should be 
#
# --dataset
#   --gaviaxmllogs
#     --parsed       # where mat files go.
#     --unzipped     # where xml files should be.
#   --kml
#
import sys, os
import errno
import getopt
import fnmatch, copy
import logging
from logging.handlers import RotatingFileHandler 

from gaviaxmllog import aanderaaoxygen, adcp, autopilot, collision, mag, magfg
from gaviaxmllog import depth, engineer, flntu, gps, gyro, navigator, seanav, imagemetadata

from parsexmllogs import CSHELParseError

parser_logger = logging.getLogger('parsexmlfiles')

# parseall
#
# Parse all the files in the indir and store the output 
# in the outdir.
# Can well start multiple threads and run them in parallel.
#
def parseMATfiles(indir, outdir):
    
    try:
        parser_logger.info("aanderaaoxygen")
        outaanderaaoxygen = outdir + "aanderaaoxygen.mat"
        parseaanderaaoxygen = aanderaaoxygen(indir, 1);
        if ( os.path.exists(outaanderaaoxygen) == False):
            parseaanderaaoxygen.parse();
            parseaanderaaoxygen.saveMAT(outaanderaaoxygen)
        
        del(parseaanderaaoxygen)
         
        parser_logger.info("adcp")
        outadcp = outdir + "adcp.mat"
        parseadcp = adcp(indir, 1);
        if ( os.path.exists(outadcp) == False):
            parseadcp.parse();
            parseadcp.saveMAT(outadcp)
 
        del(parseadcp)
        
        parser_logger.info("autopilot")
        outautopilot = outdir + "autopilot.mat"
        parseautopilot = autopilot(indir, 1);
        if ( os.path.exists(outautopilot) == False):
            parseautopilot.parse();
            parseautopilot.saveMAT(outautopilot)
        
        del(parseautopilot)
        
        parser_logger.info("mag")
        outmag = outdir + "mag.mat"
        parsemag = mag(indir, 1);
        if ( os.path.exists(outmag) == False):
            parsemag.parse();
            parsemag.saveMAT(outmag)
        
        del(parsemag)        
        
        parser_logger.info("magfg")
        outmagfg = outdir + "magfg.mat"
        parsemagfg = magfg(indir, 1);
        if ( os.path.exists(outmagfg) == False):
            parsemagfg.parse();
            parsemagfg.saveMAT(outmagfg)
        
        del(parsemagfg) 

        parser_logger.info("collision")
        outcollision = outdir + "col.mat"
        parsecollision = collision(indir, 1);
        if ( os.path.exists(outcollision) == False):
            parsecollision.parse();
            parsecollision.saveMAT(outcollision)
    
        del(parsecollision)
    
        parser_logger.info("depth")
        outdepth = outdir + "depth.mat"
        parsedepth = depth(indir, 1);
        if ( os.path.exists(outdepth) == False):
            parsedepth.parse();
            parsedepth.saveMAT(outdepth)
    
        del(parsedepth)
    
#        parser_logger.info("engineer")
#        outengineer = outdir + "engineer.mat" 
        # Problem with the binary type data.
#        parseeng = engineer(indir, 1);
#        if ( os.path.exists(outengineer) == False):
#            parseeng.parse();
#            parseeng.saveMAT(outengineer)
            
#        del(parseeng)
    
        parser_logger.info("flntu")
        outflntu = outdir + "flntu.mat"
        parseflntu = flntu(indir, 1);
        if ( os.path.exists(outflntu) == False):
            parseflntu.parse();
            parseflntu.saveMAT(outflntu)
    
        del(parseflntu)
        
        parser_logger.info("gps")
        outgps = outdir + "gps.mat"
        parsegps = gps(indir, 1);
        if ( os.path.exists(outgps) == False):
            parsegps.parse();
            parsegps.saveMAT(outgps)

        del(parsegps)
        
        parser_logger.info("gyro")
        outgyro = outdir + "gyro.mat"
        parsegyro = gyro(indir, 1);
        if ( os.path.exists(outgyro) == False):
            parsegyro.parse();
            parsegyro.saveMAT(outgyro)
    
        del(parsegyro)
        
        parser_logger.info("navigator")
        outnav = outdir + "nav.mat"
        parsenav = navigator(indir, 1);
        if ( os.path.exists(outnav) == False):
            parsenav.parse();
            parsenav.saveMAT(outnav)
    
        del(parsenav)
        
        parser_logger.info("imagemetadata")
        outimagemetadata = outdir + "imagemetadata.mat"
        parseimagemetadata = navigator(indir, 1);
        if ( os.path.exists(outimagemetadata) == False):
            parseimagemetadata.parse();
            parseimagemetadata.saveMAT(outimagemetadata)
    
        del(parseimagemetadata)
        
        parser_logger.info("seanav")
        outsea = outdir + "sea.mat"
        parsesea = seanav(indir, 1);
        if ( os.path.exists(outsea) == False):
            parsesea.parse();
            parsesea.saveMAT(outsea)

        del(parsesea)
        
    except CSHELParseError as cshel:
        errormessage = "ERROR : " + cshel.__str__()
        parser_logger.error(errormessage)
    return;


# Method : parseKMLfiles()
#
# To parse and store the KML files.
#
def parseKMLfiles(indir, outputKMLdir, kmlName):
    parser_logger.info("KML navigator")
    outKMLnav = outputKMLdir + "navigator.kml"
    
    # Only parse data, if a KML does not exist.
    if ( os.path.exists(outKMLnav) == False):
        parseKMLnav = navigator(indir, 1);
        parseKMLnav.parseKML();
        parseKMLnav.saveKML(outKMLnav, kmlName);
    
        del(parseKMLnav)

    return;

# Method : set_logger()
#
# Set the Logging Mechanism. If script is started as a daemon,
# the Log File Name should be given through the command line.
# Else we will just dump everything to the standard output.
#
def set_logger(isdaemon,logfile,debugmode):
    # Setting the format
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    parser_logger = logging.getLogger('parsexmlfiles')
    
    if isdaemon is True:
        # Log into a Log File.
        rotatingFH = RotatingFileHandler(logfile, mode='a', 
                                         maxBytes=7340032, backupCount=4,
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
    print "\tparsexmlfiles.py -- Parse the Gavia XML files\n"

    print "SYNOPSIS \n"
    print "\tpython parsexmlfiles.py --datadir=[directory] --daemon --logfile=[filename]"
    print "\tpython parsexmlfiles.py --datadir=[directory] --daemon --logfile=[filename] --parsemat"
    print "\tpython parsexmlfiles.py --datadir=[directory] --daemon --logfile=[filename ] --parsekml"

    print "\nDESCRIPTION"
    print "\tparsexmlfile.py script would parse the Gavia XML files and generate MAT and KML files."
    print "\tThe MAT and KML files would be created per CRUISE."
    
    print "\nOPTIONS"
    print "\tThese are the options."

    print "\n\t--datadir=[directory]"
    print "\t\tThe datadir is mandatory."
    print "\t\tThe directory given here should have the following structure :- \n"
    print "\t\t--[directory]"
    print "\t\t    --cruise Name"
    print "\t\t      --gaviaxmllogs"
    print "\t\t        --parsed       # where mat files would be generated."
    print "\t\t        --unzipped     # where Gavia xml files should be."
    print "\t\t      --kml            # where the kml file would be generated"

    print "\n\t--daemon"
    print "\t\tIf this  parameter is provided, the parsing process would run in the background."
    print "\t\tIf --daemon is given, it is mandatory to give the --logfile parameter."

    print "\n\t--logfile=[filename]"
    print "\t\tThe full path of the file that would store the logs."
    print "\t\tThe logfile would be ignored if the --daemon flag is not given."
    print "\t\tIf --daemon is given, it is mandatory to give the --logfile parameter."

    print "\n\t--parsemat"
    print "\t\tIf you only want the MAT files to be generated."

    print "\n\t--parsekml"
    print "\t\tIf you only want the KML files to be generated."
    
    print "\n\t--debug"
    print "\t\tUsed only for debugging purposes. Would print a lot of log messages."
    
    print "\nEXAMPLES"
    print "\n\tThe following would parse the XML files located in \"/root/dataproducts/\" and generate the MAT and KML file"
    print "\t\tEg: python parsexmlfiles.py --datadir=/root/dataproducts/ --daemon --logfile=/tmp/logfile"

    print "\n\tThe following would parse the XML files located in \"/root/dataproducts/\" and generate the MAT file"
    print "\t\tEg: python parsexmlfiles.py --datadir=/root/dataproducts/ --parsemat --logfile=/tmp/logfile"

    print "\n\tThe following would parse the XML files located in \"/root/dataproducts/\" and generate the KML file"
    print "\t\tEg: python parsexmlfiles.py --datadir=/root/dataproducts/ --parsekml --logfile=/tmp/logfile"
    
    print "\nWARNING"
    print "If you don't understand background process in unix/linux, DO NOT GIVE --daemon option (IT WOULD BE BAD FOR YOU).\n"

def main(argv):
    datadir = None
    logfile = None
    debugmode = False
    isdaemon = False
    parseMAT = False;
    parseKML = False;
    try:
        opts,args = getopt.getopt(argv, "dmlb:h", ["datadir=", "daemon", "logfile=", "debug", "parsemat", "parsekml", "help"])
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
        elif opt in ("-m", "--daemon"):
            isdaemon = True;
        elif opt in ("-l", "--logfile"):
            logfile = arg;
        elif opt in ( "--parsemat"):
            parseMAT = True;
        elif opt in ( "--parsekml"):
            parseKML = True;
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
    
    if isdaemon is True:
        if logfile is None:
            print(" Cannot Start : No Log file given in Daemon mode.\n")
            usage()
            sys.exit()
            
    # Arguments are good.
    
    if (parseMAT == False and parseKML == False):
        parseMAT = True;
        parseKML = True;
        
    # Set Logger.
    set_logger(isdaemon,logfile,debugmode)
    decay = []
    
    # FOR TESTING I am making the same structure locally.
    # parsing the xml logs from the actual data and storing the 
    # mat files locally.
    outputdir = "/Users/gavia/harman/temp/";
    #outputdir = datadir;
    count = 0;
        
    # FOR TESTING.
    # Just creating a temp folder structure locally.
    # DO IT ONCE - It is not required.
#    try:
#        listing = os.listdir(datadir);
#        for infile in listing:
#            if ( str.isdigit(infile[0:2])): # First 2 char should be digits YYYYMMDD
#                print "Processing file : ", infile;
#                curr_dir = outputdir + infile; # adding the full name(or relative name)
#                os.mkdir(curr_dir)
#                gaviaxmllogs = curr_dir + "/gaviaxmllogs"
#                kmldir = curr_dir + "/kml/"
#                os.mkdir(gaviaxmllogs)
#                os.mkdir(kmldir)
#                #print "Current Dir : ", curr_dir
#                parsed_dir = gaviaxmllogs + "/parsed"
#                print "Parsed Dir : ", parsed_dir;
#                os.mkdir(parsed_dir)
#                count = count + 1
#            else:
#                decay.append(infile)
#    except IOError (errno, os.strerror):
#        print "I/O error({0}): {1}".format(errno, os.strerror)
    
    # Now parse directories
    try:
        listing = os.listdir(datadir);
        for indir in listing:
            if ( str.isdigit(indir[0:2])): # First 2 char should be digits YYYYMMDD
                parser_logger.info("Processing Directory : " + indir)
                curr_dir = outputdir + indir; # adding the full name(or relative name)
                inputdir = datadir + indir + "/gaviaxmllogs/unzipped/"
                matlabdir = curr_dir + "/gaviaxmllogs/parsed/"
                kmldir = curr_dir + "/kml/"
                
                #print "Input Dir : ", inputdir
                #print "Output Dir : ", matlabdir
                
                # Check if there are already MAT files.
                if (parseMAT == True):
                    parseMATfiles(inputdir, matlabdir) #parseMATFiles
                if (parseKML == True):
                    parseKMLfiles(inputdir, kmldir, indir); #parseKMLFiles
            else:
                decay.append(indir)
    except IOError (errno, os.strerror):
        print "I/O error({0}): {1}".format(errno, os.strerror)
 
    print " Parsing in Complete, go for a Run"

# Call the Main Function
if __name__ == "__main__":
    main(sys.argv[1:])
