#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import sys
import os
import json
import re
import datetime
import time


def readFile(filename, batterySet, eventSet, thermalSet, testSet, phoneSnSet):
    print("process file:", filename)
    phonesn = re.sub(pattern, "", os.path.basename(filename), 1)

    if not phonesn:
        print("phonesn invalid:" + phonesn)
        return

    if phoneSnSet.find({"phonesn": phonesn}).count() == 0:
        phoneSnSet.insert({"phonesn": phonesn})

    file = open(filename)
    while 1:
        line = file.readline()
        if not line:
            break

        if line.find("batteryLevel") != -1:
            data = json.loads(line)
            data["phonesn"] = phonesn
            data["timeISO"] = datetime.datetime.strptime(data['timeStamp'], '%Y-%m-%d %H:%M:%S')
            # if batterySet.find({"phonesn":phonesn, "timeStamp":data['timeStamp']}).count() == 0:
            batterySet.insert(data)

        if line.find("event") != -1:
            data = json.loads(line)
            data["phonesn"] = phonesn
            data["timeISO"] = datetime.datetime.strptime(data['timeStamp'], '%Y-%m-%d %H:%M:%S')
            # if eventSet.find({"phonesn": phonesn, "timeStamp": data['timeStamp']}).count() == 0:
            eventSet.insert(data)

        if line.find("thermalList") != -1:
            data = json.loads(line)
            data["phonesn"] = phonesn
            data["timeISO"] = datetime.datetime.strptime(data['timeStamp'], '%Y-%m-%d %H:%M:%S')
            # if thermalSet.find({"phonesn": phonesn, "timeStamp": data['timeStamp']}).count() == 0:
            thermalSet.insert(data)

        if line.find("testType") != -1:
            data = json.loads(line)
            data["phonesn"] = phonesn
            data["timeISO"] = datetime.datetime.strptime(data['timeStamp'], '%Y-%m-%d %H:%M:%S')
            # if testSet.find({"phonesn": phonesn, "timeStamp": data['timeStamp']}).count() == 0:
            testSet.insert(data)
    file.close()
    print("del file:", filename)
    os.remove(filename)


def getReadedFilelist(filename):
    list = []
    if os.path.exists(filename):
        file = open(filename)
        while 1:
            line = file.readline()
            if not line:
                break
            list.append(line)
        file.close()
    return list


def isFileInList(filename, list):
    for file in list:
        if file == filename:
            return True
    return False


def updateToFile(filename, list):
    if os.path.exists(filename):
        os.remove(filename)
    file = open(filename, "w+")
    for line in list:
        file.write(line + "\n")
    file.close()


def checkFileValid(name, fullpath, phoneSnSet):
    if not name.__contains__(".VM"):
        print("file invalid:" + name)
        return False
    if not name.endswith(".log"):
        print("file invalid:" + name)
        return False
    if phoneSnSet.find({"filename":name}).count() != 0:
        print("file has already processed! " + name)
        os.remove(fullpath)
        return False

    # 只处理当前时刻2小时前的log
    curTime = time.time()
    matchObj = re.search("\.(\d{4}-\d{2}-\d{2}_\d{2})\.log", name)
    if matchObj:
        timestr = matchObj.group(1)
        fileTime = time.mktime(time.strptime(timestr, "%Y-%m-%d_%H"))
        if curTime - fileTime > (3 * 60 * 60):
            return True
        else:
            print("file time not match:", name, timestr)
            return False
    else:
        print("file log name invalid!", name)
        return False


pattern = re.compile("\.VM.*?\.log")
conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.mydb
batterySet = db.batterySet
eventSet = db.eventSet
thermalSet = db.thermalSet
testSet = db.testSet
phoneSnSet = db.phoneSnSet
fileListSet = db.fileListSet

print("hello world")

if len(sys.argv) < 2:
    print("usage:", sys.argv[0], "process dir or file")
    exit(-1)

dir = sys.argv[1]

if os.path.isdir(dir):
    for dirpath, dirname, filenames in os.walk(dir):
        for name in filenames:
            fullpath = os.path.join(dirpath, name)
            if not checkFileValid(name, fullpath, fileListSet):
                continue
            readFile(fullpath, batterySet, eventSet, thermalSet, testSet, phoneSnSet)
            fileListSet.insert({"filename":name})
elif os.path.isfile(dir):
    basename = os.path.basename(dir)
    if checkFileValid(basename, dir, fileListSet):
        readFile(dir, batterySet, eventSet, thermalSet, testSet, phoneSnSet)
        fileListSet.insert({"filename": basename})
else:
    print("file invalid ", dir)
