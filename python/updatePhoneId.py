#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import sys
import os
import json
import re
import datetime
import time
import copy


def getNewPhoneInfo(phoneInfo, list):
    index = 0
    phoneNew = copy.deepcopy(phoneInfo)
    for i in list:
        if index == 0:
            phoneNew['phonesn'] = i
        elif index == 1 and (('devicesn' not in phoneNew.keys()) or (phoneNew["devicesn"] == "null") or (i != "null")):
            phoneNew["devicesn"] = i
        elif index == 2:
            phoneNew["brand"] = i
        elif index == 3:
            phoneNew["model"] = i
        elif index == 4:
            phoneNew["sdk"] = i
        elif index == 5:
            phoneNew["serial"] = i
        elif index == 6:
            phoneNew["memory"] = i
        elif index == 7:
            phoneNew["flash"] = i
        index += 1

    return phoneNew

def readFile(filename, phoneSnSet):
    print("process file:", filename)

    file = open(filename)
    while 1:
        line = file.readline()
        if not line:
            break

        list = line.strip("\n").split(',')
        if list and list.__len__() > 0 and list[0].__len__() > 0:
            print("get list ok!", line, list)
            if phoneSnSet.find({"phonesn": list[0]}).count() == 0:
                phoneInfoNew = getNewPhoneInfo({},list)
                phoneSnSet.insert(phoneInfoNew)
            else:
                for info in  phoneSnSet.find({"phonesn": list[0]}):
                    print("phoneInfo", info)
                    phoneInfoNew = getNewPhoneInfo(info, list)
                    phoneSnSet.update({'_id': info['_id']}, phoneInfoNew)
                    break
    file.close()

def checkFileValid(name):
    if not name.__contains__("comm_topic.VM_0_6_centos."):
        print("file invalid:" + name)
        return False
    if not name.endswith(".log"):
        print("file invalid:" + name)
        return False

    return True

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.mydb
phoneSnSet = db.phoneSnSet

print("start to update phoneid info")

if len(sys.argv) < 2:
    print("usage:", sys.argv[0], "process dir or file")
    exit(-1)

dir = sys.argv[1]

if os.path.isdir(dir):
    for dirpath, dirname, filenames in os.walk(dir):
        for name in filenames:
            fullpath = os.path.join(dirpath, name)
            if not checkFileValid(name):
                continue
            readFile(fullpath, phoneSnSet)
elif os.path.isfile(dir):
    basename = os.path.basename(dir)
    if checkFileValid(basename):
        readFile(dir, phoneSnSet)
else:
    print("file invalid ", dir)
