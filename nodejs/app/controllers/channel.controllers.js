var Channel = require('/app/models/channels.model.js');
const mongoose = require('mongoose');


//create channel
exports.createNewChannel = (req, res) => {
  var new_Channel = new Channel({
    _id: new mongoose.Types.ObjectId(),
    url: req.body.url,
    name: req.body.name
  });
  new_Channel.save()
    .then(result => {
      res.status(201).json({
        message: "Created Feed successfully",
        new_Channel: {
          url: result.url,
          name: result.name,
          _id: result._id,
        }
      });
    })
    .catch(err => {
      console.log(err);
      res.status(500).json({
        error: err
      });
    });
};

exports.getOne = (req, res) => {
  const id = req.params.channelId;
  Channel.findById(id)
    .select("name url _id")
    .exec()
    .then(doc => {
      if (doc) {
        res.status(200).json(doc);
      } else {
        res
          .status(404)
          .json({ message: "No valid entry found for provided ID" });
      }
    })
    .catch(err => {
      res.status(500).json({error: err});
    });
};


//display the rss feed; this will get the url of the rss, which can then be parsed
exports.display = (req, res) => {
  const id = req.params.channelId;
  Channel.findById(id)
    .select("name url _id")
    .exec()
    .then(doc => {
      if (doc) {
        res.status(200).json(doc);
      } else {
        res
          .status(404)
          .json({ message: "No valid entry found for provided ID" });
      }
    })
    .catch(err => {
      res.status(500).json({error: err});
    });
};


//get all channels
exports.getAll = (req, res) => {
  Channel.find({})
    .select("name url _id")
    .exec()
    .then(docs => {
      const response = {
        count: docs.length,
        feeds: docs.map(doc => {
          return {
            name: doc.name,
            url: doc.url,
            _id: doc._id,
          };
        })
      };
      res.status(200).json(response);
    })
    .catch(err => {
      console.log(err);
      res.status(500).json({
        error: err
      });
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
exports.update = (req, res, next) => {
  const id = req.params.channelId;
  Channel.update({ _id: id }, req.body)//{name: req.params.name},  {url: req.body.url}, {new: true})
  .exec()
    .then(result => {
      res.status(200).json({
        message: "Channel updated",
      });
    })
    .catch(err => {
      console.log(err);
      res.status(500).json({
        error: err
      });
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
  const id = req.params.channelId;
  //var channelName = document.getElementById("Title")
  Channel.remove({ _id: id})
  .exec()
    .then(result => {
      res.status(200).json({
        message: "Channel deleted",
      });
    })
    .catch(err => {
      console.log(err);
      res.status(500).json({
        error: err
      });
    });
};

