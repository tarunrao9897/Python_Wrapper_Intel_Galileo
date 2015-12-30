var http = require('http'); 
var Galileo = require("galileo-io");

var board = new Galileo();
var delayTime = 1000;
var targetPin = 13

var intervalHandler;
var byte = 0;


var intervalFunction = function() {
    console.log("Interval Reached - " + byte + " - " + delayTime);
    board.digitalWrite(targetPin, (byte ^= 1));
}


board.on("ready", function() {
  console.log("Ready Function Reached!");
  this.pinMode(targetPin, this.MODES.OUTPUT);
  intervalHandler = setInterval(intervalFunction, delayTime);
});


http.createServer(function (req, res){ 
   console.log("Request Received!");
   var url = req.url;

   clearInterval(intervalHandler);

   console.log("Current Delay Time: " + delayTime);
   if(delayTime > 200) delayTime = delayTime - 200;
   else delayTime = 1000;

   console.log("New Delay Time:" + delayTime);


   res.writeHead(200,{'Content-Type': 'text/plain'});
   res.end('Hello World\n' + url); 

   intervalHandler = setInterval(intervalFunction, delayTime);


}).listen(1337, '169.254.1.1');

console.log('Server running at http://169.254.1.1:1337');