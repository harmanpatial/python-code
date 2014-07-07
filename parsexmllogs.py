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
        self.elmtstoparse = {}
        try:
            doc = xml.dom.minidom.parse(filename)
            firstLayers = doc.getElementsByTagName('elementstoparse').item(0).childNodes

            for firstLayer in firstLayers:
                if firstLayer.nodeType is firstLayer.ELEMENT_NODE:
                    parser_logger.debug("First Layer node : " + firstLayer.nodeName)
                    for firstLayerAttr in firstLayer.attributes.keys():
                        parser_logger.debug("Attribute Name : " + firstLayerAttr + " <> Value : " + firstLayer.attributes[firstLayerAttr].value)
                        if(firstLayer.attributes[firstLayerAttr].value == "parent"):
                            self.elmtstoparse[str(firstLayer.nodeName)] = {}
                            secondLayers = firstLayer.childNodes
                            for secondLayer in secondLayers:
                                if secondLayer.nodeType is secondLayer.ELEMENT_NODE:
                                    parser_logger.debug("Second Layer node : " + secondLayer.nodeName)
                                    if str(secondLayer.nodeName) not in self.elmtstoparse[str(firstLayer.nodeName)]:
                                        self.elmtstoparse[str(firstLayer.nodeName)][str(secondLayer.nodeName)] = {}
                                    for secondLayerAttr in secondLayer.attributes.keys():
                                        parser_logger.debug("Second Layer node : " + secondLayerAttr)
                                        if str(secondLayerAttr) not in self.elmtstoparse[str(firstLayer.nodeName)][str(secondLayer.nodeName)]:
                                            self.elmtstoparse[str(firstLayer.nodeName)][str(secondLayer.nodeName)][str(secondLayerAttr)] = []
                                        self.elmtstoparse[str(firstLayer.nodeName)][str(secondLayer.nodeName)][str(secondLayerAttr)].append(str(secondLayer.attributes[secondLayerAttr].value))
             
            parser_logger.debug("The whole dictionary : " + str(self.elmtstoparse))
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
        
    def internalParse(self, outputFile, saveinXLS):
        for file in self.inputfiles:
            parser_logger.debug("internalParse file : " + file)
            try:
                Nentries = 0;
                parser = make_parser()
                datatoparse = {}
                dh = CHparse(self.elmtstoparse)
                eh = EHparse()
                parser.setContentHandler(dh)
                parser.setErrorHandler(eh)
                parser.parse(file);  # The file to parse.
                self.data.append(datatoparse) # Storing in the data structure.
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except DIRECTParserError as direct:
                errormessage = ""
                errormessage = errormessage + "FileName = " + str(file)
                errormessage = errormessage + str(direct.__str__())
                raise DIRECTParserError(errormessage)
            except SAXParseException:
                print "\n Failed to parse file1: " + file
                thing = SAXParseException.getMessage(self);
                print thing
            except Exception as e:
                parser_logger.warning("Failed to parse : " + file);
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
        self.__document_started = 0
        self.__data = {}
        self.__dataKey = {}
        self.__temp = 0
        self.__count = 0
        self.__startCapture = 0
        self.__capture = 0
        self.__localDic = {}
        
    # Method : setDocumentLocator(self, locator)
    # Setting the locator of the file.    
    def setDocumentLocator(self, locator):
        self.__locator = locator
    
    # Method : startDocument(self)
    # Event indicating the start of the Document.    
    def startDocument(self):
        self.__document_started = 1
        for firstLevelKey in self.__elementstoparse.keys():
            #keyInData = str(firstLevelKey)  # Pushed "media"
            keyInData = ""
            parser_logger.debug("First keyInData")
            parser_logger.debug("keyInData : " + keyInData)
            for secondLevelKey in self.__elementstoparse[firstLevelKey].keys():
                secondkeyInData = keyInData + str(secondLevelKey)  # Pushed title or id
                parser_logger.debug("keyInData : " + keyInData)
                if not self.__elementstoparse[firstLevelKey][secondLevelKey]:
                    self.__data[secondkeyInData] = []
                else:
                    for thirdLayerKeys in self.__elementstoparse[firstLevelKey][secondLevelKey].keys():
                        thirdkeyInData = secondkeyInData + "|" + str(thirdLayerKeys) # Pushed key
                        for fourthLayerData in self.__elementstoparse[firstLevelKey][secondLevelKey][thirdLayerKeys]:
                            temp = ""
                            temp = thirdkeyInData + "|" + fourthLayerData
                            parser_logger.debug("temp : " + temp)
                            self.__data[temp] = []

        parser_logger.debug("self.__data : " + str(self.__data))
        return

    # Method : endDocument(self)
    def endDocument(self):
        parser_logger.info("File Name : " + str(self.__count))
        parser_logger.info("Total number of entries parsed : " + str(self.__count))
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
        for key in self.__elementstoparse.keys():
            if (name == key):
                self.__startCapture = 1
                self.__localDic = self.__elementstoparse[key]
                for what in self.__data.keys():
                    self.__data[what] = []
                #self.__dataKey = str(name)
                return

        if (self.__startCapture == 1):
            for secondLevelKey in self.__localDic.keys():
                if(name == secondLevelKey):
                    self.__dataKey =  str(name)
                    if not self.__localDic[secondLevelKey]: # Capture this
                        parser_logger.debug("__dataKey : " + self.__dataKey)
                        self.__capture = 1
                    else:
                        # Compare all the attributes for this node with the thirdLevel of Keys
                        for thirdLevelKey in self.__localDic[secondLevelKey].keys():
                            for attr in attrs.getNames():
                                if(thirdLevelKey == attr):
                                    self.__dataKey = self.__dataKey + "|" + str(attr)
                                    for thirdLevelValues in self.__localDic[secondLevelKey][thirdLevelKey]:
                                        if thirdLevelValues == attrs.getValue(attr):
                                            self.__dataKey = self.__dataKey + "|" + str(thirdLevelValues)
                                            parser_logger.debug("__dataKey : " + self.__dataKey)
                                            self.__capture = 1
                        
                            
    # Method : endElement()
    #
    # Parse for the start of elements and if the 
    # element is of our interest "unset" the local flag.
    # Apart from the special case, when we meet the end of "entry" element, 
    def endElement(self, name):
        try: 
            if not(self.__document_started == 1):
                return
            if not (self.__startCapture == 1):
                return
        
            for key in self.__elementstoparse.keys():
                if (name == key):
                    self.__startCapture = 0
                    # TODO : This is where the data should be pushed to SQL Database
                    for what in self.__data.keys():
                        parser_logger.debug("DATA KEY : " + str(what))
                        parser_logger.debug("DATA VALUE : " + str(self.__data[what]))
                        self.__count = self.__count + 1 
                        self.__data[what] = []

            if self.__capture == 1:
                self.__data[self.__dataKey].append(self.__temp) # THIS IS WHERE DATA IS STORED 
                #parser_logger.info("self.__dataKey : " + str(self.__data[self.__dataKey]))
            self.__dataKey = ""
            self.__capture = 0
            self.__temp = 0

        except ValueError as v:
            errormessage = ""
            errormessage = errormessage + " Line Number = "
            errormessage = errormessage + str(self.__locator.getLineNumber())
            errormessage = errormessage + " Column Number = "
            errormessage = errormessage + str(self.__locator.getColumnNumber())
            errormessage = errormessage + " ElementName = "
            errormessage = errormessage + str(name)
            errormessage = errormessage + " Total Count = "
            errormessage = errormessage + str(self.__count)
            self.__startCapture = 0
            self.__capture = 0
            self.__temp = 0
            for what in self.__data.keys():
                self.__data[what] = []
            parser_logger.warning(errormessage)
            parser_logger.warning(v)
            #raise DIRECTParserError(errormessage)

    # Method : characters()
    # This is where the data is copied in the local 
    def characters(self, content):
        
        try:
            if not(self.__document_started == 1):
                return
            if (self.__capture is 1):
                if not (self.__temp == 0):
                    self.__temp = u' '.join((self.__temp, content)).encode('utf-8').strip()
                else:
                    self.__temp = content.encode('utf-8').strip()
        except (UnicodeEncodeError, ValueError) as v:
            errormessage = ""
            errormessage = errormessage + " Line Number = "
            errormessage = errormessage + str(self.__locator.getLineNumber())
            errormessage = errormessage + " Column Number = "
            errormessage = errormessage + str(self.__locator.getColumnNumber())
            errormessage = errormessage + " Total Count = "
            errormessage = errormessage + str(self.__count)
            parser_logger.warning(errormessage)
            self.__startCapture = 0
            self.__capture = 0
            self.__temp = 0
            for what in self.__data.keys():
                self.__data[what] = []
            parser_logger.warning(v)
            return
            raise DIRECTParserError(errormessage)

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
        raise DIRECTParserError(errormessage)
    
    # A Fatal error has been encountered.
    def fatalError(e):
        # Raise a exception, this exception is 
        # handled by internalParse method in the parsexmllogs class. 
        errormessage = "lineNumber"
        errormessage.append(self.getLineNumber())
        errormessage = "ColumnNumber"
        errormessage.append(self.getColumnNumber())
        print "\nLine Number :", getLineNumber(), " Column Number : ", getColumnNumber()
        raise DIRECTParserError(errormessage)
        
    # Just a warning.
    # Can log the warning, if we are running as a daemon.
    def warning(e):
        print "\n Just a Warning : I am not sure what to do"
        return

# Class : DIRECTParserError
#
# A User-Defined Exception Class.
# This error is ultimately handled by parsexmlfiles 
# script for two purposes
# 
# 1. To log the Error message (in log file or just to console).
# 2. To stop parsing in a particular folder (only one kind of *.xml files).
#
class DIRECTParserError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value);
    
    def __append__(selfself,val):
        self.value.append(val);
