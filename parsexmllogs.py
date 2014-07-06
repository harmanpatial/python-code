#!/usr/bin/env python
#
# This Contain Classes that is utilized by the gaviaxmllog
# module.
#
# Harman Patial
# UDEL/CSHEL
# September 2011
#
# Before editing this file look at the gaviaxmllog file.
# From outside the file, do not create direct object of 
# these classes, instead INHERIT.
#

import string as s
import exceptions
import scipy as sci
import scipy.io as sio
import sys, os, math
import fnmatch, copy
import errno
import datetime as d
import logging

from time import mktime

from xml.sax import ContentHandler, ErrorHandler
from xml.sax import make_parser

import xml.dom.minidom
from xml.dom.minidom import Node
from xml.sax._exceptions import SAXParseException

parser_logger = logging.getLogger('parsexmlfiles')

# Class : parsexmllogs
#
# This is a "ABSTRACT" class, do not create a object of this.
# create a child for every type(autopilot, collision, etc.) 
# of XML logs that we need to parse.
#
class parsexmllogs(object):

    def __init__(self, inputFile):
        self.data = []
        self.inputfiles = []
        self.newnames = {}
        self.elmtstoparse = {}
        self.totalEntries = 0
        
        self.inputfiles.append(inputFile)
        
        return;

    # Method to be implemented by child.
    def parse(self):
        pass
    
    # Method to be implemented by child.
    def saveXLS(self,outputXLSfile): 
        pass
        
    def internalfillElmtsToParse(self,filename):
        # Set the elmtstoparse data structure.
        firstLevelDic = {}
        try:
            doc = xml.dom.minidom.parse(filename)
            firstLayers = doc.getElementsByTagName('elementstoparse').item(0).childNodes

            for firstLayer in firstLayers:
                if firstLayer.nodeType is firstLayer.ELEMENT_NODE:
                    parser_logger.info("First Layer node : " + firstLayer.nodeName)
                    for firstLayerAttr in firstLayer.attributes.keys():
                        parser_logger.info("Attribute Name : " + firstLayerAttr + " <> Value : " + firstLayer.attributes[firstLayerAttr].value)
                        if(firstLayer.attributes[firstLayerAttr].value == "parent"):
                            firstLevelDic[str(firstLayer.nodeName)] = {}
                            secondLayers = firstLayer.childNodes
                            for secondLayer in secondLayers:
                                if secondLayer.nodeType is secondLayer.ELEMENT_NODE:
                                    parser_logger.info("Second Layer node : " + secondLayer.nodeName)
                                    if str(secondLayer.nodeName) not in firstLevelDic[str(firstLayer.nodeName)]:
                                        firstLevelDic[str(firstLayer.nodeName)][str(secondLayer.nodeName)] = {}
                                    for secondLayerAttr in secondLayer.attributes.keys():
                                        parser_logger.info("Second Layer node : " + secondLayerAttr)
                                        if str(secondLayerAttr) not in firstLevelDic[str(firstLayer.nodeName)][str(secondLayer.nodeName)]:
                                            firstLevelDic[str(firstLayer.nodeName)][str(secondLayer.nodeName)][str(secondLayerAttr)] = []
                                        firstLevelDic[str(firstLayer.nodeName)][str(secondLayer.nodeName)][str(secondLayerAttr)].append(str(secondLayer.attributes[secondLayerAttr].value))
             
            print "The whole dictinory : " + str(firstLevelDic)
            #node = str(ch.nodeName)      # Converting from Unicode to Normal String.
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
         
    # Currently, this should only be called by "nav" class.   
    def internalfillKMLElmtsToParse(self,filename):
        try:
            doc = xml.dom.minidom.parse(filename)
            childnodes = doc.getElementsByTagName('kmldatatoparse').item(0).childNodes

            for ch in childnodes:
                if ch.nodeType is ch.ELEMENT_NODE:
                    node = str(ch.nodeName)      # Converting from Unicode to Normal String.
                    self.elmtstoparse.append(node)
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        
    def internalParse(self):
        for file in self.inputfiles:
            parser_logger.debug("Parsing file : " + file)
            try:
                Nentries = 0;
                # Calculate the Number of Entries.
                parser = make_parser()
                ce = CountElements()
                ee = EHparse()
                parser.setContentHandler(ce)
                parser.setErrorHandler(ee)
                parser.parse(file)
                Nentries = ce.getNumofEntries()
                self.totalEntries = self.totalEntries + Nentries

                datatoparse = {}
                for ch in self.elmtstoparse:
                    datatoparse[ch] = sci.zeros((Nentries,1),'double')
                
                # Initialize to nans.
                for key in datatoparse.keys():
                    datatoparse[key].fill(sci.nan)
                dh = CHparse(datatoparse)
                eh = EHparse()
                parser.setContentHandler(dh)
                parser.setErrorHandler(eh)
                parser.parse(file);  # The file to parse.
                self.data.append(datatoparse) # Storing in the data structure.
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except CSHELParseError as cshel:
                errormessage = ""
                errormessage = errormessage + "FileName = " + str(file)
                errormessage = errormessage + str(cshel.__str__())
                raise CSHELParseError(errormessage)
            except SAXParseException:
                print "\n Failed to parse file1: " + file
                thing = SAXParseException.getMessage(self);
                print thing
            except Exception as e:
                parser_logger.info("Failed to parse : " + file);
                print type(e)     # the exception instance
                print e.args      # arguments stored in .args
                print e           # __str__ allows args to printed directly
                #x, y = e          # __getitem__ allows args to be unpacked directly
                #print 'x =', x
                #print 'y =', y
            
    def internalsetnewnames(self,filename):
        try:
            doc = xml.dom.minidom.parse(filename)
            childnodes = doc.getElementsByTagName("newnames").item(0).childNodes;

            for ch in childnodes:
                if ch.nodeType is ch.ELEMENT_NODE:
                    # Converting from Unicode to Normal String.
                    old1 = ch.getAttribute("old")
                    old2 = str(old1)
                    new1 = ch.getAttribute("new")
                    new2 = str(new1)
                    # Store it in the Newnames.
                    self.newnames[old2] = new2;
        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

    def internalsaveXLS(self,outputXLSfile, string):
        matData = {}
        temp = {}
        matData[string] = temp
        globalCount = 0;
                
        temp1 = {}
        done = 0
        
        for ch in self.elmtstoparse:
            temp[ch] = sci.zeros((self.totalEntries,1),'double')

        # Initialize to nans.
        for ch in self.elmtstoparse:
            temp[ch].fill(sci.nan)

        for key in temp.keys():
            if key not in self.newnames.keys():
                continue
            temp[self.newnames[key]] = temp[key]
            del temp[key]

        for c in self.data:
            temp1 = copy.deepcopy(c)
            try:
                # rename stuff that needs renaming.
                for key in temp1.keys():
                    if key not in self.newnames.keys():
                        continue
                    temp1[self.newnames[key]] = temp1[key]
                    del temp1[key]
          
                
                # Copy the temp1 into temp
                for key in temp.keys():
                    localCount = globalCount;
                    for val in temp1[key]:
                        (temp[key])[localCount] = val
                        localCount = localCount + 1
                
                globalCount = localCount                
                done = 1
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
        
        if done == 1:
            # Saving the Matlab file , using compression.
            parser_logger.debug("Saving the File : " + outputMATfile)
            sio.savemat(outputMATfile, matData,
                        do_compression=True, oned_as ='row')

# Class : CountElements
#
# A very simple class just to count the number of 
# "entry" elements in the XML file.
class CountElements(ContentHandler):
        def __init__(self):
            self.__entries = 0
        def startElement(self, name, attrs):
            if (name == 'entry'):
                self.__entries = self.__entries + 1
        def getNumofEntries(self):
            return self.__entries;

# Class : CHparse
#
# Read a bit about SAX parser before doing anything here.
# This is the basic parsing class, during "__init__",
# give it a list of the elements that is to be parsed.
class CHparse(ContentHandler):
    
    # Method : __init__
    #
    # Initialize data structures.
    def __init__(self,elementstoparse):
        # Define the data structures.
        self.__elementstoparse = elementstoparse
        self.__temp = 0
        self.__count = 0
        self.__capture = 0
        
    # Method : setDocumentLocator(self, locator)
    # Setting the locator of the file.    
    def setDocumentLocator(self, locator):
        self.__locator = locator
    
    # Method : startDocument(self)
    # Event indicating the start of the Document.    
    def startDocument(self):
        self.__document_started = 1

    # Method : endDocument(self)
    def endDocument(self):
        return
        
    # Method : startElement()
    # Event indicating the start of a Element.
    # Parse for the start of elements and if the 
    # element is of our interest "set" the local flag.
    def startElement(self, name, attrs):
        
        if not(self.__document_started == 1):
            return
        
        # Set the local flags accordingly. Simple if-else-if
        # We should change this to switch case.
        if (name == 'entry'):
            self.__elementstoparse['time'][self.__count] = float(attrs.getValue('timestamp'))
        else:
            for keys in self.__elementstoparse:
                if (name == keys):
                    self.__capture = 1
                    break
    
    # Method : endElement()
    #
    # Parse for the start of elements and if the 
    # element is of our interest "unset" the local flag.
    # Apart from the special case, when we meet the end of "entry" element, 
    def endElement(self, name):
        try: 
            if not(self.__document_started == 1):
                return
 
            if (name == 'entry'):
                self.__flag_entry = 0
                self.__count = self.__count + 1
            else:
                for keys in self.__elementstoparse:
                    if (name == keys):
                        if (name == 'lat' and self.__temp != '0'):
                            hem = self.__temp[-1]
                            if ( hem != 'N' and hem != 'S'): # lat is in DD.DDDD format.
                                self.__elementstoparse[name][self.__count] = float(self.__temp)
                            else: # lon is in DDMM.MMMMC format.
                                deg = self.__temp[0:2]
                                minute = self.__temp[2:-1]
                                if hem == 'S':
                                    self.__elementstoparse[name][self.__count] = - (s.atof(deg)+s.atof(minute)/60)
                                else:
                                    self.__elementstoparse[name][self.__count] = s.atof(deg) + s.atof(minute)/60
                        elif (name == 'lon' and self.__temp != '0'):
                            hem = self.__temp[-1]
                            if ( hem != 'E' and hem != 'W'): # lon is in DD.DDDD format.
                                self.__elementstoparse[name][self.__count] = float(self.__temp)
                            else: # lon is in DDMM.MMMMC format.
                                deg = self.__temp[0:3]
                                minute = self.__temp[3:-1]
                                if hem == 'W':
                                    self.__elementstoparse[name][self.__count] = - (s.atof(deg)+s.atof(minute)/60)
                                else:
                                    self.__elementstoparse[name][self.__count] = s.atof(deg) + s.atof(minute)/60
                        elif(name == "eta" and self.__temp != '0'):
                            year = int(self.__temp[0:4])
                            month = int(self.__temp[5:7])
                            day = int(self.__temp[8:10])
                            hour = int(self.__temp[11:13])
                            minute = int(self.__temp[14:16])
                            second = int(self.__temp[17:19])
                            msecond = self.__temp[20:self.__temp.__len__()]
                            usecond = int(msecond)*1000
                            dts = d.datetime(year,month,day,hour,minute,second,usecond)
                            self.__elementstoparse[name][self.__count] = mktime(dts.timetuple()) + 1e-6*dts.microsecond
                        else:
                            self.__elementstoparse[name][self.__count] = float(self.__temp) # THIS IS WHERE DATA IS STORED 
                        self.__capture = 0
                        self.__temp = 0
                        break
        except ValueError as v:
            errormessage = ""
            errormessage = errormessage + " ElementName = "
            errormessage = errormessage + str(name)
            errormessage = errormessage + " :: Value = "
            errormessage = errormessage + str(self.__temp)
            errormessage = errormessage + " :: Count = "
            errormessage = errormessage + str(self.__count)
            raise CSHELParseError(errormessage)

    # Method : characters()
    # This is where the data is copied in the local 
    def characters(self, content):
        
        if not(self.__document_started is 1):
            return
        if ( self.__capture is 1 ):
            if not (self.__temp == 0):
                self.__temp = str(self.__temp) + str(content)
            else:
                self.__temp = str(content);

# Class : EHparse
#
# Error Handling for the Content Handler.
# Just handle some primitive error.
class EHparse(ErrorHandler):
    def __init__(self):
        return

    # A Recoverable error has been encountered.
    def error(e):
        # Raise a exception, this exception is 
        # handled by internalParse method in the parsexmllogs class. 
        errormessage = "lineNumber"
        errormessage.append(self.getLineNumber())
        errormessage = "ColumnNumber"
        errormessage.append(self.getColumnNumber())
        print "\nLine Number :", getLineNumber(), " Column Number : ", getColumnNumber()
        raise CSHELParseError(errormessage)
    
    # A Fatal error has been encountered.
    def fatalError(e):
        # Raise a exception, this exception is 
        # handled by internalParse method in the parsexmllogs class. 
        errormessage = "lineNumber"
        errormessage.append(self.getLineNumber())
        errormessage = "ColumnNumber"
        errormessage.append(self.getColumnNumber())
        print "\nLine Number :", getLineNumber(), " Column Number : ", getColumnNumber()
        raise CSHELParseError(errormessage)
        
    # Just a warning.
    # Can log the warning, if we are running as a daemon.
    def warning(e):
        print "\n Just a Warning : I am not sure what to do"
        return

# Class : CSHELParseError
#
# A User-Defined Exception Class.
# This error is ultimately handled by parsexmlfiles 
# script for two purposes
# 
# 1. To log the Error message (in log file or just to console).
# 2. To stop parsing in a particular folder (only one kind of *.xml files).
#
class CSHELParseError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value);
    
    def __append__(selfself,val):
        self.value.append(val);
