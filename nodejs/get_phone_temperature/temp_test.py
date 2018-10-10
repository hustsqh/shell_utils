import os, sys, sqlite3, time

print os.getcwd()
conn = sqlite3.connect("tempData.db")
query = """create table IF NOT EXISTS temperature(
    thermal VARCHAR(20),
    type VARCHAR(20),
    temperature Integer,
    time Integer   
);"""
conn.execute(query)
conn.commit()
print "create table succ!!"

process = os.popen('adb shell ls /sys/class/thermal/', "r", -1)
dirs=process.read().split("\r\n")
dirs.remove("")
print dirs


timeStamp = int(time.time())
print timeStamp
for dir in dirs:
    type = os.popen("adb shell cat /sys/class/thermal/" + dir + "/type", "r", -1).read().strip("\r\n")
    temp = os.popen("adb shell cat /sys/class/thermal/" + dir + "/temp", "r", -1).read().strip("\r\n")
    print "value:", type, " :", temp
    cmd = "insert into temperature(thermal, type, temperature, time) values (" + dir + "," + type + "," +  temp + "," + str(timeStamp) + ")"
    print cmd
    conn.execute(cmd)
    conn.commit()

    


