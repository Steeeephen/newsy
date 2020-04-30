var express = require('express');
var app = express();
const port = process.env.PORT || 3000;
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
const cors = require('cors')
//sets up database, pointing to file below
var dbConfig = require('/config/database.config.js');


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
var routes = require('/app/routes/channel.routes.js')(app);

app.use(cors())

app.use((req, res, next) => {
  const error = new Error("Not found");
  error.status = 404;
  next(error);
});

app.use((error, req, res, next) => {
  res.status(error.status || 500);
  res.json({
    error: {
      message: error.message
    }
  });
});


app.listen(port, () => {
    console.log(`Server listening on port ${port}!`)
});
