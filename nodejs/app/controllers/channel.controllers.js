var Channel = require('/app/models/channels.model.js');

//create channel according to details in request body (req.body)
exports.createNewChannel = (req, res) => {
  var new_Channel = new Channel(req.body);
  new_Channel.save(function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//get single channel, display its name and url, accroding to req.params.name
exports.getOne = (req, res) => {
  Channel.find({name: req.params.name}, {name:1, url:1, _id:0} ,function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

exports.display = (req, res) => {
  Channel.find( {url: req.params.url},function(err, channel){
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

// //updates the channel according to what is sent in the request params
//NOT CURRENTLY WORKING, TO BE TESTED!
// exports.update = (req, res) => {
//   Channel.findOneAndUpdate({name: req.params.name},  {url: req.body.url}, {new: true},
//   function(err, channel){
//     if(err)
//       res.send(err);
//     res.send(channel);
//   });
// };

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
