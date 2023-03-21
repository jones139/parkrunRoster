#!/usr/bin/env python
""" Imports a folder of html files into the database.
It is assumed that each html file is a parkrun results page saved from the
web site.
"""
from bs4 import BeautifulSoup
import argparse
import os
import PIL
import PIL.Image, PIL.ImageDraw, PIL.ImageColor, PIL.ImageFont

import getRosterHtml

rosterLimits = {
            "date": {"Need": 1, "Preferred": 1},
            "Run Director": {"Need": 1, "Preferred": 1},
            "Finish Tokens": {"Need": 1, "Preferred": 1},
            "Timekeeper": {"Need": 1, "Preferred": 2}, 
            "Barcode Scanning": {"Need": 1, "Preferred": 2},
            "Marshal": {"Need": 2, "Preferred": 3}, 
            "Tail Walker": {"Need": 1, "Preferred": 1},
            "Event Day Course Check": {"Need": 1, "Preferred": 1}
}

STATUS_RED = 0
STATUS_AMBER = 1
STATUS_GREEN = 2



def getRosterData(htmlStr, columnNo=0, debug=False):
    '''
    Retrieve the volunteer roster data from the futureroster html data 'htmlStr', for column columnNo of the table (zero indexed)
    '''
    soup = BeautifulSoup(htmlStr, 'html.parser')

    resultsTable = soup.find( "table", {"id":"rosterTable"})

    rosterData = {'date': None,
                "Run Director": [],
                "Event Day Course Check": [],
                "Tail Walker":[],
                "Finish Tokens": [],
                "Barcode Scanning": [],
                "Timekeeper": [], 
                "Marshal": [],
    }


    # Populate event dates list - first column is not used because that is the roles column.
    firstRow = resultsTable.find("tr")
    dateElem = firstRow.findAll("th")[columnNo+1]
    rosterData['date'] = dateElem.contents[0]

    # Loop through the roster table, and extract the names associated with the roles in the rosterData template above
    row = firstRow
    while True:
        row = row.find_next("tr")
        if row is None: 
            if (debug): print("row is None - end of table")
            break
        taskElement = row.find("th").find("a")
        #print(taskElement)
        if taskElement is not None:
            taskStr = taskElement.contents[0]
            if (debug): print(taskStr)
            #taskLst.append(taskStr)
            if (taskStr in rosterData.keys()):
                if (debug): print("found %s" % taskStr)
                data = row.findAll("td")
                if (debug): print(data[columnNo])
                if (len(data[columnNo].contents)>0):
                    if (debug): print(data[columnNo].contents[0])
                    rosterData[taskStr].append(data[columnNo].contents[0])
        else:
            pass
            

    return(rosterData)


def calcRosterStatus(rosterData, debug=False):
    '''
    Calculate the status red/amber/green for each role in the roster rosterData,
    and an overall status for the roster.
    The 'date' field is used for the overall status of the roster, which is the worst status of all the roles
    '''
    rosterStatus = {}

    for role in rosterData.keys():
        if (debug): print(role)
        rosterStatus[role] = STATUS_RED
        have = len(rosterData[role])
        if (have >= rosterLimits[role]["Need"]):
            rosterStatus[role] = STATUS_AMBER
        if (have >= rosterLimits[role]["Preferred"]):
            rosterStatus[role] = STATUS_GREEN

    minStatus = 2
    for role in rosterStatus.keys():
        if rosterStatus[role]<minStatus:
            minStatus=rosterStatus[role]
    rosterStatus['date'] = minStatus

    return(rosterStatus)
    

def status2ColourRGB(statusInt):
    if (statusInt == 0):
        return((180, 0, 0))
    elif (statusInt == 1):
        return((200, 200,0))
    elif (statusInt == 2):
        return((100,200,100))
    else:
        print("status2ColourName = invalid status %d" % statusInt)
        exit(-1)


def makeDashboardImage(rosterData, formatStr, outFile, debug=False):
    '''
    Create a PNG image showng the essential roster roles as a dashboard
    '''
    rosterStatus = calcRosterStatus(rosterData, debug)
    if (debug): print("makeDashboardImage: rosterData=",rosterData,"\nrosterStatus=",rosterStatus)

    imgW = 640
    imgH = 480
    colW = imgW/2
    rowH = imgH / len(rosterData.keys())
    txtH = 18
    txtMargin = 3
    #fnt = PIL.ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", txtH)
    #fnt = PIL.ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", txtH)
    #fntBold = PIL.ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", txtH)
    fnt = PIL.ImageFont.truetype("FreeMono.ttf", txtH)
    fntBold = PIL.ImageFont.truetype("FreeMonoBold.ttf", txtH)
    bgCol = (220, 220, 220)

    if formatStr == "png":
        print("Using PIL to create png image")
        img = PIL.Image.new("RGB", (imgW,imgH))

        imgD = PIL.ImageDraw.Draw(img)
        
        curY = 0
        # Overall
        # Background colour
        imgD.rectangle([0,curY,colW,rowH],fill=status2ColourRGB(rosterStatus['date']), outline=PIL.ImageColor.getrgb('blue'))
        imgD.rectangle([colW,curY,colW+colW,rowH],fill=status2ColourRGB(rosterStatus['date']), outline=PIL.ImageColor.getrgb('blue'))
        # Text
        if (rosterStatus['date'] == STATUS_RED):
            imgD.text((0+txtMargin,curY),"Volunteer Dashboard for:", fill=(255,255,255), font=fntBold)
            imgD.text((colW+txtMargin,curY),rosterData['date'], fill=(255,255,255), font=fntBold)
        else:
            imgD.text((0+txtMargin,curY),"Volunteer Dashboard for:", fill=(0,0,0), font=fntBold)
            imgD.text((colW+txtMargin,curY),rosterData['date'], fill=(0,0,0), font=fnt)

        for role in rosterData.keys():
            if (role!="date"):
                curY += rowH
                if (debug): print(role, curY)
                # Background Colour
                imgD.rectangle([0,curY,colW,curY+rowH],fill=status2ColourRGB(rosterStatus[role]), outline=PIL.ImageColor.getrgb('blue'))
                imgD.rectangle([colW,curY,colW+colW,curY+rowH],fill=status2ColourRGB(rosterStatus[role]), outline=PIL.ImageColor.getrgb('blue'))
                # Role Text
                if (rosterStatus[role] == STATUS_RED):
                    imgD.text((0+txtMargin,curY),role, fill=(255,255,255), font=fntBold)
                else:
                    imgD.text((0+txtMargin,curY),role, fill=(0,0,0), font=fntBold)
                # Volunteer Name Text
                txtY = curY
                for roleName in rosterData[role]:
                    if (debug): print(roleName, txtY)
                    if (rosterStatus[role] == STATUS_RED):
                        imgD.text((colW+txtMargin,txtY),roleName, fill=(255,255,255), font=fnt)
                    else:
                        imgD.text((colW+txtMargin,txtY),roleName, fill=(0,0,0), font=fnt)
                    txtY += txtH

        if (debug): img.show()
        img.save(outFile, formatStr)
        print("Image saved fo file %s" % outFile)

    elif formatStr == "svg":
        print("Making SVG Image")
        print("**** SORRY - NOT IMPLEMENTED - not doing anything ****")
        
    else:
        print("***** Invalid Format String %s - not doing anyting *****" % formatStr)





if __name__ == "__main__":
    print("makeRosterImg.main()")


    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug",
                    help="produce verbose output for debugging",
                    action="store_true")
    ap.add_argument("-p", "--parkrun",
                    help="parkrun name - defaults to 'hartlepool'")
    ap.add_argument("-c", "--column", default=0,
                    help="Table Column Number to analyse (Defaults to zero)")
    ap.add_argument("-i", "--inFile",
                    help="Input File Name for future roster html file (defaults to futureroster_<parkrun>.html)")
    ap.add_argument("-o", "--outFile",
                    help="Output Filename root (defaults to roster_<parkrun>")
    ap.add_argument("-f", "--format",
                    help="output format - defaults to 'png'")
    ap.add_argument("--dl",
                    help="Download the roster from the web site rather than loading from file",
                    action="store_true")


    args = ap.parse_args()

    debug = args.debug
    print(args)

    if (args.column!=None):
        column = int(args.column)
    else:
        column = 0

    if (args.parkrun!=None):
        parkrun = args.parkrun
    else:
        parkrun = "hartlepool"

    if (args.format!=None):
        filext = int(args.format)
    else:
        filext = "png"


    if (args.inFile!=None):
        inFile = args.inFile
    else:
        inFile = "futureroster_%s.html" % parkrun


    if (args.outFile!=None):
        outFile = args.outFile
    else:
        outFile = "roster_%s.%s" % (parkrun, filext)


    if args.dl:
        print("Downloading Roster from Web Site")
        htmlStr = getRosterHtml.getRosterHtml(parkrun, debug)
    else:
        print("Loading Roster from file %s" % inFile)
        inf = open(inFile,"r")
        htmlStr = inf.read()
        inf.close()

    rosterData = getRosterData(htmlStr,column,debug)
    makeDashboardImage(rosterData,filext, outFile, debug)


