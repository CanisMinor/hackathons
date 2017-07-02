#!/usr/bin/env python3
import sys
import os
import pickle
import subprocess
import dateutil.parser as dp
import datetime as dt
import textract as tx

pp=1
if (pp):
    def ppr(*x):
        print(" ".join(map(str,x)))
else:
    def ppr(*x):
        pass

files = []

filetypes = { "docx": ("word", "Word document"),
              "doc": ("wordold", "Word document (old)"),
              "txt": ("text", "Text document"),
              "png": ("image", "Image"),
              "jpg": ("image", "Image"),
              "jpeg": ("image", "Image"),
              "mp3": ("audio", "Audio"),
              "wav": ("audio", "Audio"),
              "mp4": ("video", "Video"),
              "mov": ("video", "Video"),
              "pdf": ("pdf", "PDF document"),
              "msg": ("outlook", "E-mail")
              }
              

def M():
    if len(sys.argv)<2:
        print("Usage:\n./filer.py <Directory Name>")
        return
    filedir = sys.argv[1]
    outname = filedir + ".pickle"
    if len(sys.argv)>=3:
        outname = sys.argv[2]
    ppr("Processing directory",filedir)
    for file in os.listdir(filedir):
        processfile(os.path.join(filedir,file))
    ppr("Finished processing")
    with open(outname,"wb") as f:
        pickle.dump(files,f)
    return

def processfile(afile):
    ppr("Processing file",afile)
    tags = {}
    tags["name"] = afile
    files.append(tags)
    root,ext = [x.lower() for x in os.path.splitext(afile)]
    ppr("root ",root,", ext",ext)
    if len(ext)>0: ext = ext[1:]
    if ext in filetypes:
        ft = filetypes[ext]
        ftype = ft[0]
        ftypename = ft[1]
    else:
        ftype = "unknown"
        ftypename = "Unknown filetype"
    ppr("file type",ftype,ftypename)
    tags["filetype"] = ftype
    tags["filetypename"] = ftypename

    if ftype == "unknown" or ftype == "text":
        processtext(tags,afile)
    elif ftype == "image":
        processimage(tags,afile)
    elif ftype == "audio":
        processaudio(tags,afile)
    elif ftype == "video":
        processvideo(tags,afile)
    elif ftype == "pdf":
        processpdf(tags,afile)
    elif ftype == "outlook":
        processmsg(tags,afile)
    elif ftype == "word":
        processword(tags,afile)
    elif ftype == "wordold":
        processwordold(tags,afile)
    else:
        ppr("huh")
        assert(0)

def processtext(tags,afile):
    ppr("process text")
    with open(afile,"r") as f:
        for line in f:
            processtextline(tags,line)

# somewhat arbitrary minimum date (year), to
# avoid some false matches
mindate = 1800

def processtextline(tags,line):
    ls = line.strip()
    if type(ls) == bytes:
        ls = ls.decode("utf8")
    ppr("...",ls)
    try:
        date = dp.parse(ls, fuzzy=True, dayfirst=True, default=dt.datetime(1,1,1))
        if date.year >= mindate:
            adddate(tags, date.year, date.month, date.day)
    except:
        ppr("except!")
        pass
    lsl = ls.lower()
    if lsl.startswith("from:"):
        addperson(tags, ls[5:], True)
    if lsl.startswith("to:"):
        addperson(tags, ls[3:], True)
        

def adddate(tags,y,m,d,head = False):
    ppr("add date ",y,m,d)
    if "dates" not in tags:
        tags["dates"] = []
    if (y,m,d) not in tags["dates"]: # avoid repeats
        if head:
            tags["dates"].insert(0,(y,m,d))
        else:
            tags["dates"].append((y,m,d))
            

def addperson(tags, name, head = False):
    ppr("add person ",name,head)
    if "people" not in tags:
        tags["people"] = []
    if name not in tags["people"]:
        if head:
            tags["people"].insert(0,name)
        else:
            tags["people"].append(name)
            

def processimage(tags,afile):
    ppr("process image")
    textract(tags,afile)

def processaudio(tags,afile):
    ppr("process audio")

def processvideo(tags,afile):
    ppr("process video")

def processpdf(tags,afile):
    ppr("process pdf")
    ptxt = subprocess.check_output(["pdftotext",afile,"-"])
    for line in ptxt.splitlines():
        processtextline(tags,line)
    
def processmsg(tags,afile):
    ppr("process outlook msg")
    textract(tags,afile)

def processword(tags,afile):
    ppr("process outlook word")
    textract(tags,afile)

def processwordold(tags,afile):
    ppr("process outlook wordold")
    textract(tags,afile)

def textract(tags,afile):
    ptxt = tx.process(afile)
    for line in ptxt.splitlines():
        processtextline(tags,line)



M()
