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
