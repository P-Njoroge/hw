#!/usr/bin/python
# -*- coding: utf-8 -*-
#This script was created by Peter Bidali (njoroge7@gmail.com)
#
#
#


import cgi
import sys
import os
import csv
import json

html_header = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><!--This file was converted to xhtml by LibreOffice - see http://cgit.freedesktop.org/libreoffice/core/tree/filter/source/xslt for the code.--><head profile="http://dublincore.org/documents/dcmi-terms/"><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8"/><title xml:lang="en-US">CSV CONVERTOR</title><meta name="DCTERMS.title" content="" xml:lang="en-US"/><meta name="DCTERMS.language" content="en-US" scheme="DCTERMS.RFC4646"/><meta name="DCTERMS.source" content="http://xml.openoffice.org/odf2xhtml"/><meta name="DCTERMS.issued" content="2016-04-13T17:18:34.521163198" scheme="DCTERMS.W3CDTF"/><meta name="DCTERMS.modified" content="2016-04-13T17:23:06.476407890" scheme="DCTERMS.W3CDTF"/><meta name="DCTERMS.provenance" content="" xml:lang="en-US"/><meta name="DCTERMS.subject" content="," xml:lang="en-US"/><link rel="schema.DC" href="http://purl.org/dc/elements/1.1/" hreflang="en"/><link rel="schema.DCTERMS" href="http://purl.org/dc/terms/" hreflang="en"/><link rel="schema.DCTYPE" href="http://purl.org/dc/dcmitype/" hreflang="en"/><link rel="schema.DCAM" href="http://purl.org/dc/dcam/" hreflang="en"/><style type="text/css">
	@page {  }
	table { border-collapse:collapse; border-spacing:0; empty-cells:show }
	td, th { vertical-align:top; font-size:12pt;}
	h1, h2, h3, h4, h5, h6 { clear:both }
	ol, ul { margin:0; padding:0;}
	li { list-style: none; margin:0; padding:0;}
	<!-- "li span.odfLiEnd" - IE 7 issue-->
	li span. { clear: both; line-height:0; width:0; height:0; margin:0; padding:0; }
	span.footnodeNumber { padding-right:1em; }
	span.annotation_style_by_filter { font-size:95%%; font-family:Arial; background-color:#fff000;  margin:0; border:0; padding:0;  }
	* { margin:0;}
	.P1 { font-size:24pt; font-family:Liberation Serif; writing-mode:page; text-align:center ! important; }
	.P2 { font-size:14pt; font-family:Liberation Serif; writing-mode:page; text-align:center ! important; }
	.P3 { font-size:14pt; font-family:Liberation Serif; writing-mode:page; text-align:left ! important; }
	.P4 { font-size:14pt; font-family:Liberation Serif; writing-mode:page; text-align:left ! important; }
        td { border:  1px; solid; #000000; }
	<!-- ODF styles with no properties representable as CSS -->
	.T1  { }
        .R1 { font-weight: bold }
	</style>

        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
        <script src="/jquery-1.12.3.min.js"  type="text/javascript"></script>
        <script src="/script.js" type="text/javascript"></script>
        <script type="text/javascript">
        var config = %s
        $(document).ready(function() {
            $("input").change(function(event) {
                row_id = $(this).parent().parent()[0].id
                index = $(this).parent().index();
                //field_size = config.fields[index].validation.fieldSize;

                flag = false // check whether row's conditions are met
                $( "#" + row_id + " input" ).each(function( index ){
                    if (config.fields[index].validation.fieldType == "string") {
                      field_size = config.fields[index].validation.fieldSize;
                        if ( $(this)[0].value.length > field_size ){
                            $(this)[0].style.color = "red" //set or get color
                            flag = true 
                                                                                                                         }
                        else {
                            $(this)[0].style.color = "blue"
                            //alert("no")
                              }
                                                                     }
                            //alert(flag)                               
                                                                     })
                if ( flag == true ){
                    $("#" + row_id)[0].style.border = "1px solid red"
                                    }
                else {
                    $("#" + row_id)[0].style.border = "1px solid blue"
                      }


        });
        });
        
        </script>



        </meta>

</head><body dir="ltr" style="max-width:8.2681in;margin-top:0.7874in; margin-bottom:0.7874in; margin-left:0.7874in; margin-right:0.7874in; writing-mode:lr-tb; ">
<p class="P1">SkunkWorks</p>
<p class="P2">CSV Converter</p><p class="P2"> </p>
<form method="POST" enctype="multipart/form-data" action="/cgi-bin/export.py">
<input type="hidden" name="length" value="%s"></input>

<lable>Export as: 
<select name="format">
<option value="XML" selected="true" required="true">XML</option>
<option value="CSV">CSV</option>
</select>
</lable>
<label>XML ID
<input name="xml_id"></input>
</label>

<br/><br/>

<table width="100%%" cellpadding="4" cellspacing="0">



</td>


''' #The config json

def test_headers(headers, config):
    """
    This function tests whether all the input csv file's
    headers are mapped in the  config file.
    If a header is not found in the config file, the header name is returned,
    otherwise, it returns a dict mapping the 
    """
    mapping = {} #This holds a mapping of the form: {'html_table_header': csv_row_index }
    for header in config["headers"]:

        #print header
        if header not in headers:
            return header
    #for header in config["headers"]:
        #if header in headers:
        mapping[header] = headers.index(header) # 
    return mapping

def process_error(fl):
    print "Content-type: text/html"
    print 
    print '<?xml version="1.0" encoding="UTF-8"?>'\
              '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><body><p>'\
              'Error while parsing csv file: %s file missing!'\
              '</p></body></html>' %fl
def csv_process(form, fl, config, row_id):
    """
    process CSV data, return the data as row-major matrix of data
    :type output: list(list(str))
    return output, row_id
    """
    file_obj = form[fl]
    #print file_obj.filename, "D"
    #print dir(file_obj.file)
    try:
        csv_file = csv.reader(file_obj.file)
    except:
        process_error(fl)
        return None, None
    #print dir(csv_file)
    #header_rows = csv_file.next() #The column header
    first_line = True
    
    #mapping = test_headers(header_rows, config)
    #if type(mapping) != list:
     #   process_error(fl, mapping)
      #  return None, None
    output = [] #Major matrix list of csv data
    for row in csv_file:
    #    print "CSV file"
        if first_line:
            first_line = False
            header_rows = row
            mapping = test_headers(header_rows, config)

        
            if type(mapping) != dict:

                process_error(fl)
                return None, None
            continue
        row2 = []
        for h in config["headers"]:
            if h in mapping:
                row2.append(row[mapping[h]])
            else:
                row2.append("")
        row2 = [i.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;") for i in row2] #html escape
        row2 = [ "row%s" %row_id ] + row2  # 'row_id' to mark each <tr id="rowX">. Necessary for the AJAX call
        output.append(row2)
        row_id += 1
    if not output:
        process_error(fl)
        return None, None
    
    return output, row_id

def parse_config_file(fp):
    #print fp.value
    try:
        config = json.loads(fp.value)
    except: 
        return None
    if config.get("fields"):
        config["columns"] = len(config.get("fields")) #The expected number of columns
    else:
        config["columns"] = 0
    sourceFields = []#List of config's source fields headers.
    for field in config["fields"]:
        sourceFields.append(field.get("sourceField", "")) # List of all the field headers expected from the input CSV files
    config["headers"] = sourceFields
    return config

def parse_data(config, cell_data, id):
    "return 'True' if 'cell_data' meets the requirements, else, return False"
    conf_len = False
    if config["fields"][id].get("validation") and config["fields"][id].get("validation", {}).get("fieldSize"):
        conf_len = int(config["fields"][id]["validation"]["fieldSize"] )
    if conf_len and len(cell_data) > conf_len:
        return False, None
    if config["fields"][id].get("validation") and config["fields"][id]["validation"].get("fieldType") == "integer":
        try:
            int(cell_data.strip())
            return True, int
        except:
            return False, int
    return True, None

def generate_html_table(table, config):
    print "Content-type: text/html"
    print
    print html_header %(json.dumps(config), len(config["fields"]))
   # print json.dumps(config)
    
    h = "<tr>"
    h2 = '<tr type="hidden">'
    for hdr in config["headers"]:
        hdr2 = '<td ><input name="headers" type="hidden" value="%s"></input></td>' %hdr.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
        hdr = '<th >%s</th>' %hdr.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
        
        
        h = h + hdr
        h2 = h2 + hdr2
    h = h + "</tr>"
    h2 = h2 + '</tr>'
    print h #Table header
    #print h2
    f = 0
    for row in table:
        t = 0
        #tr = '<tr id="%s" valign="top">' % (row[0])
        tr1 = ""
        valid_row = True
        for td in row[1:]:
            valid, cell_type = parse_data(config, td, t)
            if not valid:
                valid_row = False
            t = t + 1
            td = td.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            font = 2
            tr1 = tr1 + '<td ><input %s" value="%s" name="cell" %s></input></td>' %(['style="color:red"', 'style="color:blue"'][valid], td,
            ['type="integer"'][type(cell_type) == int])
        tr = '<tr id="%s" valign="top" style="%s">%s' % (row[0], ["border: 1px solid red", ""][valid_row], tr1)
        tr = tr + '</tr>'
        print tr #Table row
    print h2
    print """</table>
        <div class="Table2">
        <input type="submit" value="Export" />
        </div/>
        </p>
        </form>
        
        <body>
        </body>

        <p class="P4"> </p></body></html>
          """

def main():
    table = []
    form = cgi.FieldStorage()

    #print "Content-type: text/html"
    #print 

    row_id = 0 #The id  if the next html row
    files = form.keys() 
    #print "configfile", files
    if "configfile" in files:
        config = parse_config_file(form["configfile"])
        #print "configfile", config
    #print "configfile", config
    else:
        print '<?xml version="1.0" encoding="UTF-8"?>'\
              '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><body><p>'\
              'Configuration file missing!'\
              '</p></body></html>'
        return
    if not config:
        print '<?xml version="1.0" encoding="UTF-8"?>'\
              '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><body><p>'\
              'Error parsing Configuration file!'\
              '</p></body></html>' 
        return
    for fl in files:
        if str(fl).startswith("fileupload") and bool(form[fl].filename):
            #print fl,  bool(form[fl].filename)
            csv_list, row_id = csv_process(form, fl, config, row_id)
#            if not row_id: #an error occurred and the html reponse has been generated, so we quit
#                return
            table.extend(csv_list)
            continue
    if not table:
        process_error("csv ")
        return None, None
    generate_html_table(table, config)
        #print form[file]
    #print "%s<br/>XXX%s" %(str(dir(form)), str(fileitems))
    #print dir(config_file)
    #print config_file.file, 'e'
    #print form["fileupload2"].file.readline()
main()
