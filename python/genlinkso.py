#!/usr/bin/python

import os, sys

TOOL_LDD="output/host/usr/bin/arm-linux-gnueabihf-ldd"
ROOT_DIR="output/target/"

if len(sys.argv) < 2:
    print "param invalid!"
    sys.exit(1)

checkLibList = []

i = 1
while i < len(sys.argv):
    checkLibList.append(sys.argv[i])
    i += 1

print "checkLibList:", checkLibList

linkLibList = []

def getAllLinkLib(lib, resultList, dolist):
    cmd = TOOL_LDD + " --root " + ROOT_DIR + " " + ROOT_DIR + lib
    r = os.popen(cmd)
    lines = r.readlines()
    for l in lines:
        print "line-> " + l
        sl = l.split()
        tmpLib = sl[2]
        print "value-> " + tmpLib
        #print "tmp lib:",sl
        if tmpLib not in resultList:
            if tmpLib != lib:
                if "usr" in tmpLib:
                    #print "tmp:",tmpLib," lib:",lib
                    #if tmpLib not in dolist:
                    #    dolist.append(tmpLib)
                    getAllLinkLib(tmpLib, resultList, dolist)
                else:
                    print "append lib:" + tmpLib
                    resultList.append(tmpLib)
            else:
                print "append lib:" + tmpLib
                resultList.append(tmpLib)
    r.close()
    resultList.append(lib)
    return resultList

doingLibList = []

for lib in checkLibList:
    getAllLinkLib(lib, linkLibList, doingLibList)

print "linkLibList:"
print linkLibList

def getRealPathIfLink(filepath):
    #print "getRealPathIfLink:" + filepath
    if os.path.islink(filepath):
        link = os.readlink(filepath)
        if link[0] == '/':
            return link
        else:
            return os.path.dirname(filepath) + "/" + link
    return filepath

def getTotalListSize(libList):
    sizeAll = 0
    for lib in libList:
        if "usr" not in lib:
            continue
        reallink = getRealPathIfLink(ROOT_DIR + lib)
        size = os.path.getsize(reallink)
        print "file:", lib, " size:", size
        sizeAll += size
    return sizeAll

totalSize = getTotalListSize(linkLibList)
print "total size:", totalSize


def getAllFileDir(dir, filelist):
    files = os.listdir(dir)
    for file in files:
        next = dir + "/" + file
        if not os.path.isdir(next):
            filelist.append(next)
        else:
            getAllFileDir(next, filelist)

fileList = []
getAllFileDir(ROOT_DIR + "/usr/lib/samba", fileList)
print "get samba lib!!!:", fileList

needDelFiles = []
def getNeedDelFiles(allFiles, useFiles, needDelFiles):
    for file in allFiles:
        find = 0
        for use in useFiles:
            name = os.path.basename(use)
            base = name.split(".", 1)[0]
            if base in file:
                find = 1
                break
        if find == 0:
            needDelFiles.append(file)


getNeedDelFiles(fileList, linkLibList, needDelFiles)
print "need del file:", needDelFiles