#!/usr/bin/env python
#
# This File contains classes for each kind of XML find.
#
# These classes should be called for parsing the data 
# in the log directory.
# Any additional functionality should be added here.
#

import sys
import errno
import fnmatch, copy
import copy
import types
import logging
from logging.handlers import RotatingFileHandler 

from parsexmllogs import CHparse,CountElements,parsexmllogs

parser_logger = logging.getLogger('parsexmlfiles')

# Class : on_gallery_episodes.
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class on_gallery_episodes(parsexmllogs):
    def __init__(self,inputFile):
        # Initialize all the variables.
        parser_logger.info("Trying to initialize");
        super(on_gallery_episodes, self).__init__(inputFile)

    def parse(self, outputFile):
        parser_logger.info("Trying lasfd  asfd sadf");
        self.internalfillElmtsToParse('datatoextract/template_on_gallery_episodes-db.xml');  # Template File
        parser_logger.info("Performing Internal Parse");
        self.internalParse(outputFile, True); # Parent Method, actual parsing.
    
    def saveXLS(self,outputXLSfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/template_on_gallery_episodes-db.xml");
        self.internalsaveXLS(outputXLSfile, "o2"); # Parent method, actual saving.

# NOTE : If a new template file is created, a entry should be added here.
#        className is matched with file name to know which class to call.
classNames = { "on_gallery_episodes" : on_gallery_episodes };

#
# Class : buildClass
#
#
class buildClass:
    def __init__(self): pass

    def construct(self, inputFile, inDir):
        instance = None
        try:
            for className in classNames.keys():
                parser_logger.debug("Input File : " + inputFile)
                toSearch = className + "*"
                parser_logger.debug("To Search : " + toSearch)
                if fnmatch.fnmatch(inputFile, toSearch):
                    parser_logger.debug("Class Name : " + className) 
                    parser_logger.info("What What " + classNames[className].__name__)
                    compInputFileName = inDir + inputFile
                    instance = classNames[className](compInputFileName)
                    break
            return instance
        except AttributeError:
            parser_logger.info("No matching class for this File : " + builderName)
            return None
            
 
# Class : adcp().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class adcp(parsexmllogs):
    
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(adcp, self).__init__(path, isDir,"adcp-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/adcptoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).

        self.internalsetnewnames("datatoextract/adcptoparse.xml");
        self.internalsaveMAT(outputMATfile, "adcp"); # Parent method, actual saving.

# Class : autopilot().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class autopilot(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(autopilot, self).__init__(path, isDir,"autopilot-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/autopilottoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/autopilottoparse.xml");
        self.internalsaveMAT(outputMATfile,"autopilot"); # Parent Method, actual parsing.

# Class : mag().
#
# This Class is not meant to be inherited.
# Just create a object of the class and  
class mag(parsexmllogs):
    def __init__(self,path,isDir):
        # data, inputfiles, elmtstoparse is in parent.
        # Just initialize it here.
        super(mag, self).__init__(path,isDir,"mag-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/magtoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/magtoparse.xml");
        self.internalsaveMAT(outputMATfile, "mag"); # Parent Method, actual parsing.

# Class : magfg().
#
# This Class is not meant to be inherited.
# Just create a object of the class and  
class magfg(parsexmllogs):
    def __init__(self,path,isDir):
        # data, inputfiles, elmtstoparse is in parent.
        # Just initialize it here.
        super(magfg, self).__init__(path, isDir, "magfg-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/magfgtoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/magfgtoparse.xml");
        self.internalsaveMAT(outputMATfile,"magfg"); # Parent Method, actual parsing.


# Class : collision().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class collision(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(collision, self).__init__(path, isDir,"collision-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/collisiontoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/collisiontoparse.xml");
        self.internalsaveMAT(outputMATfile,"col"); # Parent Method, actual parsing.

# Class : depth().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class depth(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(depth, self).__init__(path, isDir,"depth-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/depthtoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        depth = []
        self.internalsetnewnames("datatoextract/depthtoparse.xml");
        self.internalsaveMAT(outputMATfile,"depth"); # Parent Method, actual parsing.

# Class : engineer().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class engineer(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(engineer, self).__init__(path, isDir,"engineer-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/engineertoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/engineertoparse.xml");
        self.internalsaveMAT(outputMATfile,"eng"); # Parent Method, actual parsing.

# Class : flntu().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class flntu(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(flntu, self).__init__(path, isDir,"flntu-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/flntutoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/flntutoparse.xml");
        self.internalsaveMAT(outputMATfile,"flntu"); # Parent Method, actual parsing.

# Class : gps().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class gps(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(gps, self).__init__(path, isDir,"gps-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/gpstoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/gpstoparse.xml");
        self.internalsaveMAT(outputMATfile,"gps"); # Parent Method, actual parsing.
     
# Class : gyro().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class gyro(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(gyro, self).__init__(path, isDir,"gyro-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/gyrotoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/gyrotoparse.xml");
        self.internalsaveMAT(outputMATfile,"gyro"); # Parent Method, actual parsing.

# Class : imagemetadata().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class imagemetadata(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(imagemetadata, self).__init__(path, isDir,"imagemetadata-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/imagemetadatatoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/imagemetadatatoparse.xml");
        self.internalsaveMAT(outputMATfile,"camera"); # Parent Method, actual parsing.
       
# Class : navigator().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class navigator(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(navigator, self).__init__(path, isDir,"navigator-*.xml")
        #self.new(path, isDir,"navigator-*.xml") # Set the Input files.

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/navigatortoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def parseKML(self):
        self.internalfillKMLElmtsToParse('datatoextract/navigatortoparse.xml');
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        self.internalsetnewnames("datatoextract/navigatortoparse.xml");
        self.internalsaveMAT(outputMATfile,"nav"); # Parent Method, actual parsing.

# Class : pressure().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class pressure(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(pressure, self).__init__(path, isDir,"pressure-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/pressuretoparse.xml');  # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        self.internalsetnewnames("datatoextract/pressuretoparse.xml");
        self.internalsaveMAT(outputMATfile,"pressure"); # Parent Method, actual parsing.
   
# Class : seanav().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class seanav(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(seanav, self).__init__(path, isDir,"seanav-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/seanavtoparse.xml');   # Template File
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        self.internalsetnewnames("datatoextract/seanavtoparse.xml");
        self.internalsaveMAT(outputMATfile,"sea"); # Parent Method, actual parsing.


def intToMonth(month):
    if month == 1:
        return "January";
    elif month == 2:
        return "February";
    elif month == 3:
        return "March";
    elif month == 4:
        return "April";
    elif month == 5:
        return "May";
    elif month == 6:
        return "June";
    elif month == 7:
        return "July";
    elif month == 8:
        return "August";
    elif month == 9:
        return "September";
    elif month == 10:
        return "October";
    elif month == 11:
        return "November";
    elif month == 12:
        return "December";
    else:
        return "";
