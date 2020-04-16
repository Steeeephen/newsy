var Channel = require('/app/models/channels.model.js');

//create channel
exports.createNewChannel = (req, res) => {
  var new_Channel = new Channel(req.body);
  new_Channel.save(function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//get single channel, display its name and url, will find where the name mathces the name on the webpage
exports.getOne = (req, res) => {
  var channelName;
  //var channelName = document.getElementById("Title")
  Channel.find({ name: channelName}, {name:1, url:1, _id:0} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};


//display the rss feed; this will get the url of the rss, which can then be parsed
exports.display = (req, res) => {
  var channelName;
  //var channelName = document.getElementById("Title")
  Channel.find({ name: channelName}, {url:1, _id:0} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//get all channels, displays just their name
exports.getAll = (req, res) => {
  Channel.find({}, {name:1, _id:0} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//search; get all channels matching a regex, 'var term', which will be whatever the editor types in
exports.search = (req, res) => {
  var term;
  //var term = document.getElementById("searchbar");
  Channel.find({name: new RegExp('^.*'+term+'.*$', "i")}, {name:1, _id:0} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//update the channelName; original will read whatever the currently displayed name is, update, will be whatever the user typed
exports.updateName = (req, res) => {
  var original;
  //var original = document.getElementById("name");
  var update;
  //var update = document.getElementById("user-typed-name")
  Channel.updateOne({name: original},{name: update} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//update the channel URL (RSS XML FILE); original will read whatever the currently displayed URL is, update, will be whatever the user typed
exports.updateURL = (req, res) => {
  var original;
  //var original = document.getElementById("name");
  var update;
  //var update = document.getElementById("user-typed-name")
  Channel.updateOne({URL: original},{URL: update} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//enable/disable channel, var channelName will match whatever the channel name that is displayed in the HTML
exports.toggleEnableChannel = (req, res) => {
  var channelName;
  //var channelName = document.getElementById("Title")
  Channel.find({name: channelName}, function(err, channel){
    {$set: {enabled: !enabled}};
    Channel.save(function(err, channel){
      if(err)
        res.send(err);
      res.send(channel);
    });
  });
};

//delete channel from database
exports.deleteChannel = (req, res) => {
  var channelName;
  //var channelName = document.getElementById("Title")
  Channel.deleteOne({ name: channelName}, function(err, channel){
    if(err)
      res.send(err);
  });
};
