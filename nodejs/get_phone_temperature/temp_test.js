var process = require('child_process');
var SqliteDB = require('./sqlite.js').SqliteDB;

var file = "data.db";
var SqliteDB = new SqliteDB(file);


function createTable(){
    var createTableSql = "create table if not exists tempTable(name varchar(128), type varchar(128), temp float, date double)";
    SqliteDB.createTable(createTableSql);
}

function insertData(item, type, temp, date){
    var insertSql = "insert into tempTable(name, type, temp, date) values (?, ?, ?, ?)";
    SqliteDB.insertData(insertSql, [[item, type, temp, date]]);
}


function runProcess(date){
    var value = process.execSync("adb shell ls /sys/class/thermal/");
    console.log("value is " + value.toString());
    var strs = value.toString().split("\n");
    console.log("strs:" + strs[0]);
    
    strs.forEach(function(item,index){
        try{
            var type = process.execSync("adb shell cat /sys/class/thermal/" + item + "/type").toString().replace(/[\r\n]/g,"").trim();
            var temp = process.execSync("adb shell cat /sys/class/thermal/" + item + "/temp").toString().replace(/[\r\n]/g,"").trim();
            var tempInt = parseInt(temp);
            var tempReal = 0.0
            if (tempInt > 1000){
                tempReal =  tempInt / 1000;
            }else if(tempInt > 100){
                tempReal = tempInt / 10;
            }else{
                tempReal = temp;
            }
            console.log("item:" + item.toString());
            console.log("temp:" + tempReal);
            console.log("type:" + type);
            if(temp != 0){
                // write to database
                insertData(item, type, tempReal, date);
            }
        }catch(e){
            console.log("catch exception! " + item);
        }
    });
}


createTable()
setInterval(function(){
    var date = Date.now();
    runProcess(date)
}, 30 * 1000);

console.log("OVER??");
