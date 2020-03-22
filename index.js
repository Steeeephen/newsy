var express = require('express');
var app = express();
var port = 3000;
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
//sets up database, pointing to file below
var dbConfig = require('C:/Users/Stephen/Documents/College Work/CS615/Project/config/database.config.js');


// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }))

// parse requests of content-type - application/json
app.use(bodyParser.json())

mongoose.Promise = global.Promise;

// Connecting to the database
mongoose.connect(dbConfig.url, {
    useNewUrlParser: true
}).then(() => {
    console.log("Successfully connected to the database");
}).catch(err => {
    console.log('Could not connect to the database. Exiting now...', err);
    process.exit();
});

//sets up routes to the endpoints defined in file below
var routes = require('C:/Users/Stephen/Documents/College Work/CS615/Project/app/routes/channel.routes.js')(app);

app.listen(port, () => {
  console.log(`Server listening on port ${port}!`)
});
