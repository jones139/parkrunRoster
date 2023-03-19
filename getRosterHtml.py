#!/usr/bin/env python
""" 
Download the latest version of the volunteer roster html file from the parkrun web site.

*** Note, I don't think we are allowed to use this - instead use a web browser to open the future roster page and do File->SaveAs ***

"""
import urllib.request
import argparse
import os


def getRosterHtml(eventName, debug=False):
    '''
    Retrieve the official volunteer roster for parkrun event called eventName
    '''
    baseUrl = "http://www.parkrun.org.uk/%s/futureroster"
    url = baseUrl % (eventName)
    if (debug): print(url)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(req)
    if (debug): print(response.info())
    htmlStr = response.read()
    response.close()

    if (debug): print(htmlStr)
    return htmlStr



if __name__ == "__main__":
    print("getRosterHtml.main()")



    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug",
                    help="produce verbose output for debugging",
                    action="store_true")
    ap.add_argument("-p", "--parkrun",
                    help="parkrun name - defaults to 'hartlepool'")
    ap.add_argument("-o", "--outFile",
                    help="Output File Name (defaults to futureroster_<parkrun>.html)")
    args = ap.parse_args()

    debug = args.debug
    print(args)


    if (args.parkrun!=None):
        parkrun = args.parkrun
    else:
        parkrun = "hartlepool"

    if (args.outFile!=None):
        outFile = args.outFile
    else:
        outFile = "futureroster_%s.html" % parkrun



    rosterHtml = getRosterHtml(parkrun, debug)

    outf = open(outFile,"w")
    outf.write(rosterHtml.decode("utf-8"))
    outf.close()

    print("Output saved to file %s" % outFile)



