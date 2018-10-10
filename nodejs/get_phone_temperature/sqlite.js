"use strict";
var fs = require('fs');
var sqlite3 = require('sqlite3').verbose();

var DB = DB || {};

DB.SqliteDB = function(file){
    DB.db = new sqlite3.Database(file);
    DB.exist = fs.existsSync(file);
    if(!DB.exist){
        console.log("create db files!");
        fs.openSync(file, "w");
    };
};

DB.printErrorInfo = function(err){
    console.log("error message:" + err.message + " errorNumber:" + errno);
}

DB.SqliteDB.prototype.createTable = function(sql){
    DB.db.serialize(function(){
        DB.db.run(sql, function(err){
            if(err != null){
                DB.printErrorInfo(err);
                return;
            }
        });
    });
}


DB.SqliteDB.prototype.insertData = function(sql, objects){
    DB.db.serialize(function(){
        var stmt = DB.db.prepare(sql);
        for(var i = 0; i < objects.length; ++i){
            stmt.run(objects[i]);
        }
        stmt.finalize();
    })
};

DB.SqliteDB.prototype.queryData = function(sql, callback){
    DB.db.all(sql, function(err, rows){
        if(err != null){
            DB.printErrorInfo(err);
            return;
        }

        if(callback){
            callback(rows);
        }
    });
};


DB.SqliteDB.prototype.executeSql = function(sql){
    DB.db.run(sql, function(err){
        if(err != null){
            DB.printErrorInfo(err);
        }
    });
};

DB.SqliteDB.prototype.close = function(){
    DB.db.close();
};

exports.SqliteDB = DB.SqliteDB;