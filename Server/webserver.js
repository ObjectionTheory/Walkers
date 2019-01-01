

var http = require('http').createServer(handler); //require http server, and create server with function handler()
var fs = require('fs'); //require filesystem module
var io = require('socket.io')(http) //require socket.io module and pass the http object (server)
var i2cBus = require("i2c-bus");
var Driver = require("pca9685").Pca9685Driver;
var options = {
    i2c: i2cBus.openSync(1),
    address: 0x40,
    frequency: 60,
    debug: false
};
pwm = new Driver(options, function(err) {
    if (err) {
        console.error("Error initializing PCA9685");
        process.exit(-1);
    }
    for (var i = 0; i < 12; i ++) {
        pwm.setPulseLength(i, 1500);
    }
    console.log("Initialization done");
 
});
http.listen(8080); //listen to port 8080

function handler (req, res) { //create server
  fs.readFile(__dirname + '/public/index.html', function(err, data) { //read file index.html in public folder
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'}); //display 404 on error
      return res.end("404 Not Found");
    } 
    res.writeHead(200, {'Content-Type': 'text/html'}); //write HTML
    res.write(data); //write data from index.html
    return res.end();
  });
}

io.sockets.on('connection', function (socket) {// WebSocket Connection
  var lightvalue = 0; //static variable for current status
  
  socket.on('light', function(data) { //get light switch status from client
    
    
  });
  socket.on("reset", function() {
      setServos();
  })

  socket.on("change:interval", function(data) {
    servoValues[0] = mapValues(data, 100, 1000, 0, 180);
  })
});

var setServos = function(i) {
  if (i == 12) {
    return;
  }

  angle = mapValues(servoValues[i], 0, 180, 1000, 2000);
  pwm.setPulseLength(i, angle);

  setTimeout(function() {
    setServos(i+1);
  }, 10);
}

var servoValues = [90, 90, 90, 90, 90, 90, 90, 90];

var mapValues = function(z, xmin, xmax, ymin, ymax) {
  var p = (z-xmin) / (xmax - xmin);
  return (ymax-ymin) * p + ymin;
}

process.on('SIGINT', function () { //on ctrl+c
  
  process.exit(); //exit completely
});