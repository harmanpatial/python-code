#!/usr/bin/env python
#
# This File contains classes for each kind of XML find.
#
# Harman Patial
# UDEL/CSHEL
# September 2011
#
# These classes should be called for parsing the data 
# in the log directory.
# Any additional functionality should be added here.
#

import sys
import errno
import scipy as sci
import copy
from simplekml import *

from parsexmllogs import CHparse,CountElements,parsexmllogs

# This was calculated from other script.
# Just statically placed here.
distanceTravelled = {
    "20080112_Bonaire":14.54,
    "20080113_Bonaire":19.81,
    "20080114_Bonaire": 4.85,
    "20080114_dropoff_evening":11.47,
    "20080116_KleinBonaire":24.98,
    "20080117_NewCove_2": 9.98,
    "20080118_NationalPark":10.72,
    "20080119_KleinBonaire":15.84,
    "20080530_hafravatn":11.71,
    "20080601":11.71,
    "20080603_hafravatn":13.05,
    "20080613_ins_test": 1.05,
    "20080716":13.05,
    "20080721":31.52,
    "20080722":22.30,
    "20080722_PM":39.12,
    "20080725":33.87,
    "20080726":127.39,
    "20080807":60.23,
    "20090126":599.46,
    "20090601_MendumsPondDay1":10.40,
    "20090603_M1":10.66,
    "20090605":10.62,
    "20090605_PostLunch":15.25,
    "20090608":34.41,
    "20090609_Sponge_Garden":39.84,
    "20090610": 9.37,
    "20090615_AUVfest":21.73,
    "20090712_testing":1502.80,
    "20090713_RVSharp":30.71,
    "20090714_ADCP_site":68.89,
    "20090727_Nantucket_Sound":20.21,
    "20090728_MarthasVin":14.22,
    "20090729_MVCO":60.40,
    "20090811_Tahoe":19.88,
    "20090813_Tahoe":78.75,
    "20090815_Tahoe":15.65,
    "20091116_Port_Mahon":14.19,
    "20100111_NZ": 3.59,
    "20100112_NZ":21.12,
    "20100113_NZ":28.62,
    "20100118_NZ": 8.36,
    "20100119_NZ":24.23,
    "20100120_NZ":17.04,
    "20100412_MIMO_TEST":21.18,
    "20100503_BroadkillSlough":44.22,
    "20100526": 0.41,
    "20100601_Spartan":14.54,
    "20100602_SandCamp":28.57,
    "20100610_Swains_lake": 3.17,
    "20100611_Swains_Lake":24.91,
    "20100628": 3.53,
    "20100629":25.12,
    "20100629_AM_and_PM":25.12,
    "20100630":12.29,
    "20100701_north":13.70,
    "20100702":21.05,
    "20100703":29.34,
    "20100704_america_day":18.49,
    "20100705_kelly":15.28,
    "20100706": 9.11,
    "20100707":13.93,
    "20100809_Sharp":37.67,
    "20100826_MIMO":25.59,
    "20100914_Broadkillslough":18.97,
    "20101006_RVSharp":12.06,
    "20101021_Abaco_ballasting_test":1352.63,
    "20101021_Abaco_dbcay_test1":1355.42,
    "20101022_Abaco":44.29,
    "20101023_Abaco":21.39,
    "20101024_Abaco":12.97,
    "20101026_Abaco":47.28,
    "20101027_Abaco":46.40,
    "20110217_UDEL_AFTER_SERVICE_DAY_2": 6.60,
    "20110218_b": 2.80,
    "20110218_d":15.22,
    "20110218_UDEL_AFTER_SERVICE_DAY3_NEW_BATT": 4.93,
    "20110218_UDEL_DOPCAL_4":20.23,
    "20110219_UDEL_INSDVLCAL_5":911.42,
    "20110220_udel_dopcal_6":41.11,
    "20110329_shakedown":11.40,
    "20110330_sbp":40.76,
    "20110331_sbp":124.15,
    "20110502_Neemo1-1":18.86,
    "20110503_Neemo2":46.41,
    "20110504_Neemo3":27.89,
    "20110505_NEEMO":17.14,
    "20110707_Scallop1": 4.14,
    "20110707_ScallopDay1_2ndBattery": 6.98,
    "20110708_Scallop_DvoraRun":26.98,
    "20110708_ScallopD2":33.52,
    "20110708_ScallopD2_M4": 4.17,
    "20110708_SM2":10.10,
    "20110709_Scallop_D3_M1_Corey":16.34,
    "20110709_ScallopD3_M2": 5.26,
    "20110709_ScallopDay3_DV119":17218.23,
    "20110710_DV117":20.65,
    "20110710_DV118":15.11,
    "20110710_M1_ArtiesRun":15.36,
    "20110711_dockside": 0.25,
    "20110711_docksideM2": 0.32,
    "20110711_docksideM3": 0.24,
    "20110711_DV115":16.44,
    "20110726_ScallopD1_DV2_M2":47605.81,
    "20110726_ScallopD1_DV44_M3":32.69,
    "20110726_ScallopD1_M1":14.72,
    "20110727_D2_R2_M2":14.23,
    "20110727_D2_R3_M3":19.31,
    "20110727_D2_R5_M5":10.05,
    "20110727_ScallopD2_R1_M1":20.18,
    "20110728_D3_DV062_M3":23.64,
    "20110728_D3_DV063_M4":15.46,
    "20110728_D3_R6_M1":41.43,
    "20110728_D3_R7_M2":14.33,
    "20110728_D3_R8_M5":21.02,
    "20110729_D4_DV0105_M2":16.66,
    "20110729_D4_DV0106_M1":38.08,
    "20110729_D4_DV0112_M3":40.44,
    "20110729_D4_DV0113_M4":20.68,
    "20110729_MohawkWreck":14.50,
    "20110730_MohawkWreckSBP":18.38,
    "20111214_magtest_Lewes":10.53,
    "20111215_magtest_Lewes":7.11,
    "20120326":8.62,
    "20120327":9.76,
    "20120328":27.21,
    "20120329":48.65,
}



# Class : aanderaaoxygen().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class aanderaaoxygen(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(aanderaaoxygen, self).__init__(path, isDir,"aanderaaoxygen-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/aanderaaoxygentoparse.xml');
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        # Parse the file(s).
        self.internalsetnewnames("datatoextract/aanderaaoxygentoparse.xml");
        self.internalsaveMAT(outputMATfile, "o2"); # Parent method, actual saving.

# Class : adcp().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class adcp(parsexmllogs):
    
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(adcp, self).__init__(path, isDir,"adcp-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/adcptoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/autopilottoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/magtoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/magfgtoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/collisiontoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/depthtoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/engineertoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/flntutoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/gpstoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/gyrotoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/imagemetadatatoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/navigatortoparse.xml');
        self.internalParse(); # Parent Method, actual parsing.
    
    def parseKML(self):
        self.internalfillKMLElmtsToParse('datatoextract/navigatortoparse.xml');
        self.internalParse(); # Parent Method, actual parsing.
    
    def saveMAT(self,outputMATfile):
        # Now parse all the files and create a MAT file.
        self.internalsetnewnames("datatoextract/navigatortoparse.xml");
        self.internalsaveMAT(outputMATfile,"nav"); # Parent Method, actual parsing.

    def saveKML(self,outKMLnav, kmlName):
        # TODO : Place holder for the KML file creation.
        temp = {}
        globalCount = 0;
        
        temp1 = {}
        done = 0
        
        for ch in self.elmtstoparse:
            temp[ch] = sci.zeros((self.totalEntries,1),'double')

        # Initialize to nans.
        for ch in self.elmtstoparse:
            temp[ch].fill(sci.nan)

        for c in self.data:
            temp1 = copy.deepcopy(c)
            try:
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
        
        lat_array = temp['lat'];
        lon_array = temp['lon'];
        
        lat_lon = []
        length = 0
        count = 0
        
        for x in lat_array:
            length = length + 1;
        
        # If there is no lat, lon in XML, just return.
        if ( length == 0 ):
            print "\nNo lat lon available";
            return;

        while ( count < length):
            if ( not sci.isnan(lat_array[count][0])):
                lat_lon.append((lon_array[count][0],lat_array[count][0]));
            count = count + 1;
        
#        print " \n Trying to save the KML file : ";        
#        print lat_lon;

        #Creating the KML file
        kml = Kml(name=kmlName, open=1)

        total = 0
        count = 0
        
        for x in lat_array:
            if ( not sci.isnan(x[0])):
                total = total + x[0];
                count = count + 1;

        # If there is no (non-nan) lat, lon in XML, just return.
        if ( count == 0 ):
            print "\nNo lat here : Go Home";
            return;
     
        latmean = total/count;

        x = 0;
        total = 0;
        count = 0;

        for x in lon_array:
            if ( not sci.isnan(x[0])):
                total = total + x[0];
                count = count + 1;

        # If there is no (non-nan) lat, lon in XML, just return.
        if ( count == 0 ):
            print "\nNo lon here : Go Home";
            return;
          
        lonmean = total/count;
        
        #print lat_lon;
        
        # A Linestring
        lin = kml.newlinestring(name="LineString", coords=lat_lon)
        lin.altitudemode = AltitudeMode.relativetoground
        #lin.linestyle.color = Color.lightyellow
        #lin.linestyle.color = 'ffd4af37';
        lin.linestyle.color = "ff2fddff";
        lin.linestyle.width= 3  # 3 pixels
        
        # Color Zooming in.
        lin.lookat = LookAt(latitude=latmean,longitude=lonmean, altitude=25000,tilt=0,altitudemode=AltitudeMode.relativetoground, range=50)
        lin.tessellate = 1
        lin.extrude = 1

        # A Point.
        pnt = kml.newpoint(name=kmlName, description="The Median", coords=[(lonmean, latmean)])
        
        pnt.iconstyle.scale = 1.399999976158142;
        pnt.iconstyle.icon.href = 'http://www.eecis.udel.edu/~hapatial/golden_star.png';
        
        year = kmlName[0:4];
        month = int(kmlName[4:6]);
        date = kmlName[6:8];
        
        #From integer to actual name of the month.
        month = intToMonth(month);
        
        pnt.balloonstyle.text = '<head><h4> Cruise Name : ' + kmlName + '</h4></head> <p>Date of the cruise : ' + date + " " + month + " " + year + "."; 
        pnt.balloonstyle.text += '<br /> Distance Travelled : ' + str(distanceTravelled[kmlName]) + ' kms.</p>';
#        pnt.balloonstyle.text += '<br /> Distance Travelled : ' + "Unknown Distance " + ' kms.</p>';
        
        pnt.balloonstyle.bgcolor = Color.white
        pnt.balloonstyle.textcolor = Color.black

        # Saving
        kml.save(outKMLnav);    
        
# Class : pressure().
#
# This Class is not meant to be inherited.
# Just create a object of the class and parse data.
class pressure(parsexmllogs):
    def __init__(self,path,isDir):
        # Initialize all the variables.
        super(pressure, self).__init__(path, isDir,"pressure-*.xml")

    def parse(self):
        self.internalfillElmtsToParse('datatoextract/pressuretoparse.xml');
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
        self.internalfillElmtsToParse('datatoextract/seanavtoparse.xml');
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
