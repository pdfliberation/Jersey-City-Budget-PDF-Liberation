#!/usr/bin/python

#
# Get the list of pdf file names and urls from the webpage
#

import requests
import re

def get_pdf_files(env):

    page = requests.get(env["budget_url"]).content
    
    links = re.findall(r"<a.*?\s*href=\"(.*?)\".*?>(.*?)</a>", page) 
    
    #got all the links on the page, but need only pdf's
    pdf_files = []
   
    for link in links: 
        if link[0].endswith(".pdf") or link[0].endswith("PDF"):
            pdf_file = link[0]
            #remove spaces and braces from the file names
            local_file = link[1].replace(" ","")
            local_file = local_file.replace("(","")
            local_file = local_file.replace(")","")
            local_file = local_file.replace("<br/>","")+".pdf"
            # TODO: convert pdf_files to dictionary....
            pdf_files.append( {
                "url"                : env["url"]+pdf_file, 
                "pdf_file"           : pdf_file, 
                "download_file_name" : env["dir_download"]+local_file,
                "ocr_file_name"      : env["dir_ocr"]+local_file,
                "csv_file_name"      : env["dir_csv"]+local_file,
                "dir_final"          : env["dir_final"]+local_file
            } )
    return pdf_files    

#
# Download the files into local directory ./download
#

import urllib

def download_file(url, output_file_name):

    if os.path.isfile(output_file_name):
        print "The url ",url, " was already dowloaded as ", output_file_name, ".  Skipping..."
    else:
        print "loading ", url, " to ", output_file_name
        r = urllib.urlretrieve(url, output_file_name)
        print r
        print "done..."

#
# Test if file is image or text
# TODO: Replace with PyPDF.extractText() that returns empty string if not searchable
#

import envoy

def is_searchable(file_name):
    rr = envoy.run('strings ' + file_name + ' | grep Font')
    #print rr.status_code
    #print rr.std_out
    #print rr.std_err
    #print "done..."
    if "Font" in rr.std_out:
        return True
    else:
        return False

#
# Files that are not searchable (image) are OCR'ed by ABBYY
#

import process

def convert_to_searchable_format(file_name, output_file_name):
    if is_searchable(file_name):
        print "The file ",file_name, " is already searchable."
    elif os.path.isfile(output_file_name):
        print "The file ",file_name, " was already converted to ", output_file_name, ".  Skipping..."
    else:
        process.recognizeFile(file_name, output_file_name, "English", "pdfSearchable")

#
# Determine number of pages
# TODO: it throws a warning first time, check out why

from PyPDF2 import PdfFileReader

def num_pages( file_name ):
    if os.path.isfile(file_name):
	try:
    		pdf = PdfFileReader(open( file_name ))
    		return ( pdf.getNumPages() )
        except:
		return -1
    else:
	return -1


#
# Tabula will split one CSV file per each page of PDF file.  
# Need to figure out the name of each CSV file.
#

def calcualte_csv_output_file_name(file_name, page_number=1):
    elems = file_name.split('/')
    elems.reverse()
    output_file_name = elems[0]
    output_file_name = output_file_name.replace(".pdf","_"+str(page_number)+".csv")
    return output_file_name

#
# Using tabula-extractor to convert searchable PDF to CSV
#

import envoy
import os

def convert_page_to_csv(file_name,page_number=1 ):

    if not is_searchable( file_name ):
            print "Can't convert non-searchable pdf ", file_name ," to csv."        
    else:   
        # Ensure we have output directory
        dir_csv = "./csv/"
        if not os.path.exists(dir_csv):
            os.makedirs(dir_csv)
        
        output_file_name = dir_csv+calcualte_csv_output_file_name(file_name, page_number)

        if os.path.isfile(output_file_name):
            print "The file ",file_name, " was already converted to ", output_file_name, ".  Skipping..."
        else:
            cmd = "./tabula-extractor/bin/tabula"
            cmd += " -p " + str(page_number) #page number option
            cmd += " -f CSV " #output format CSV
            cmd += " -n " #non-spreadsheet verion
            cmd += " -o "+output_file_name #output file name file_name_[1-9].csv
            cmd += " " + file_name #name of file to convert
            print cmd
            rr = envoy.run(cmd)
            print rr.status_code
            print rr.std_out
            print rr.std_err
            print "done..."

#
# Test is file was sucessfully processed.
# Used in all phases of the process.

import os

def file_exists(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False

#
# Get status of the process
#

import pandas as pd

def get_status(pdf_files):
    # url
    # file name
    # Download Status
    # num_pages
    # is_searchable
    # OCR Status - TODO
    # Raw CSV Status - TODO
    # Merged CSV Status - TODO

    data = ([
        pdf_file["url"],
        pdf_file["download_file_name"].replace("./download/",""),
        file_exists(pdf_file["download_file_name"]),
        num_pages(pdf_file["download_file_name"]),
        is_searchable(pdf_file["download_file_name"]),
        file_exists(pdf_file["ocr_file_name"]) #applies only if not searchable
        ] for pdf_file in pdf_files)

    idx = ([pdf_file["download_file_name"].replace("./download/","") for pdf_file in pdf_files])

    cols = ("url","file_name","download_status","num_pages","is_searchable","ocr_status")

    df = pd.DataFrame(list(data),index=list(idx),columns=cols)
    
    return df

