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

//get all channels
exports.getAll = (req, res) => {
  Channel.find({}, function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

// get single channel, currently hardcoded where id = a1
exports.getOne = (req, res) => {
  Channel.find({ id: a1 }, function(err, channel){
    if(err)
      res.send(err);
    res.send(channel);
  });
};

//update channel
exports.disableChannel = (req, res) => {
  var myquery = { id: "a1" };
  var newvalues = { $set: { enabled: false } };
  Channel.updateOne(myquery, newvalues, function(err, res) {
    if (err)
      res.send(err);
    res.json(channel);
  });
};
