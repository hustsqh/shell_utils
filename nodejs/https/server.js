var http = require('http');
var https = require('https');
var fs = require('fs');
var url = require('url');
var querystring = require('querystring');

var opts = {
    key:fs.readFileSync("./key/server.key"),
    //cert:fs.readFileSync("./key/server.crt"),
    cert:fs.readFileSync("./key/server-ca.crt"),
    ca:[fs.readFileSync("./key/ca.crt")],
    rejectUnauthorized:true,
    requestCert:true
};

https.createServer(opts, function(request, response){
    var pathname = url.parse(request.url).pathname;
    //var arg = url.parse(request.url).query;
    //var params = querystring.parse(arg);

    response.writeHead(200, {'Context-Type':'text/plain'});
    // response.end('hello world\n');
    response.end('{"status":1,"content":{"from":"en-EU","to":"zh-CN","out":"\u793a\u4f8b","vendor":"ciba","err_no":0}}');

    console.log("method " + request.method);
    if(request.method == "GET"){
        var params = url.parse(request.url);
        var query = params.query
        console.log("query: " + query);
        // var json = JSON.stringify(query);
        // console.log("json:" + json);
        // var jsonObj = JSON.parse(json);
        // console.log("jsonobj:" + jsonObj);
    }else if(request.url == "/posssssssssssssss" && request.method == "POST"){
        console.log("sssssssssssssssssssssssssssssssss");
        console.log("url:" + request.url);
        var data = '';
        request.on('data', function(chunk){
            data += chunk;
        });
        request.on('end', function(){
            data = decodeURI(data);
            console.log("get pos data:" + data);
             var dataObject = querystring.parse(data);
             console.log(dataObject);
        });
    }else if(request.method == "POST"){
        var params = url.parse(request.url);
        var query = params.query
        console.log("query: " + query);
        var data = '';
        request.on('data', function(chunk){
            data += chunk;
        });
        request.on('end', function(){
            data = decodeURI(data);
            console.log("get pos data:" + data);
             var dataObject = querystring.parse(data);
             console.log(dataObject);
        });
    }
}).listen(443);

console.log("server running at https://127.0.0.1:443");