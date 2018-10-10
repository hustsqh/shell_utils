var https = require('https');
var fs = require('fs');
var opt = {
    hostname:'127.0.0.1',
    port:8811,
    path:'/hello?abc=123',
    method:'GET',
    key:fs.readFileSync('./key/client.key'),
    cert:fs.readFileSync('./key/client-ca.crt'),
    ca:[fs.readFileSync('./key/ca.crt')],
    rejectUnauthorized:false,
    agent:false
};


opt.agent = new https.Agent(opt);
var req = https.request(opt, function(res){
    console.log(" status code:", res.statusCode);
    console.log("headers:", res.headers);
    res.setEncoding('utf-8');
    res.on('data', function(d){
        console.log(d);
    });
});

req.on('error', function(e){
    console.log(e);
});

req.end();