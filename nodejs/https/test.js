var event = require('events');
var eventEmitter = new event.EventEmitter();

var connectHandler = function connected(){
    console.log("connect succ!");
    eventEmitter.emit('data_recv');
}

eventEmitter.on('connection', connectHandler);
eventEmitter.on('data_recv', function(){
    console.log("recv data succ");
});

eventEmitter.emit('connection');

console.log("over!");