#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import sys
import json
import csv

import cgitb
#import cgi
def begin():
    print "Content-type: text/html"
    print 

def create_xml(cells, headers, length, total, xml_id):
    print "Content-type: text/xml" 
    print 'Content-Disposition: attachment; filename="CSV Convert.xml"'
    print
    #print total, "p",  length
    print '<?xml version="1.0" encoding="UTF-8"?>'
    print "<xmlkfi object_id='%s'>" %xml_id
    for i in range(0, total, len(headers)):
        print '<record>'
        j = 0
        hdr = ''
        for header in range(len(headers)):
            header_text = headers[header].value.replace(" ", "")
            hdr = hdr + '<%s>%s</%s>' %(header_text, cells[ i + header ].value, header_text)
        print hdr
        print "</record>\n"
    print '</xmlkfi>'

def create_csv(cells, headers, length, total):
    print "Content-type: text/csv" 
    print 'Content-Disposition: attachment; filename="CSV Convert.csv"'
    print
    csv_file = csv.writer(sys.stdout)
    csv_file.writerow([h.value for h in headers])
    for row in range(0, total, len(headers)):
        out_row = []
        for j in range(len(headers)):
            out_row.append(cells[ row + j ].value )
        csv_file.writerow( out_row )

def main():
    cgitb.enable()

    form = cgi.FieldStorage()
    #print form["test"]
    total = len(form["cell"])
    #print form["test"][0].value
    #length = int(form["length"].value)
    length =  int(form["length"].value)
    #print form["format"]
    type = form["format"].value

    #print form["headers"]
    if type == "XML":
        if "xml_id" not in form.keys() or not form["xml_id"].value:
            begin()
            print "XML configuration does not contain an 'xml_id'."
            print "Please rectify this error then try agin."
        else:
            xml_id = form["xml_id"].value
            create_xml(form["cell"], form["headers"], length, total, xml_id)
    else:
        create_csv(form["cell"], form["headers"], length, total)

    #print dir(cgi.cgi.cgi.cgi)
    #print "<html><p>Pet er</p></br>Hello World!<br/>YESSS</html>" 

main()
