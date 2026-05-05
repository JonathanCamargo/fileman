import os
import json
import tempfile

PLAYGROUND=False

def downloadspath():
    paths=[os.path.join(os.path.expanduser('~'),'Downloads'),'D:\\Downloads']
    for path in paths:
        if os.path.isdir(path):
            break
        else:
            path=None
    return path

def temppath():
    return tempfile.tempdir

def keyspath():
    return os.path.join(dropboxpath(),'myshared','Personal','automatizamesta','keys.json')

def loadKeys():
    f=open(keyspath())
    keys=json.load(f)
    f.close()
    return keys

def dropboxpath():
    ''' Finds the path for dropbox'''
    folders=['Dropbox','Dropbox (Personal)']
    dbpaths=[os.path.join(os.path.expanduser('~'),f) for f in folders]
    dbpaths=dbpaths+[os.path.join('D:\\',f) for f in folders]
    for dbpath in dbpaths:
        if os.path.isdir(dbpath):
            break
        else:
            dbpath=None
    if dbpath==None:
        raise(Exception('Dropbox folder not found'))
    return dbpath

def mkdirfile(outfile):
    outfolder,outextension=os.path.splitext(outfile)
    if outextension=='':
        os.makedirs(outfolder,exist_ok=True)
    else:
        outfolder,_=os.path.split(outfolder)
        os.makedirs(outfolder,exist_ok=True)

def fileparts(filename):
    filepath,file=os.path.split(filename)
    filename=str.split(file,'.')[0]
    fileext=str.split(file,'.')[1]
    return filepath,filename,fileext
