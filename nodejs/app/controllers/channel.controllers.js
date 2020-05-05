var Channel = require('../models/channels.model.js');
const mongoose = require('mongoose');

//create channel, the new channel will have information accordig to the request body, which will match accordingly
exports.createNewChannel = (req, res) => {
  var new_Channel = new Channel({
    _id: new mongoose.Types.ObjectId(),
    url: req.body.url,
    name: req.body.name,
    enabled: req.body.enabled
  });
  //saves the new channel in the db, sends a 201 status
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
    //handles errors
    .catch(err => {
      console.log(err);
      res.status(500).json({
        error: err
      });
    });
};


//gets one channel based on its id
exports.getOne = (req, res) => {
  const id = req.params.channelId;
  //findById is inbuilt mongoose function, it will find an entry in the database matching the id in the request
  Channel.findById(id)
  //returns the name, url and id
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
  //find is an inbuilt mongoose function, but as we pass nothing, it will return everything
  Channel.find({})
    .select("name url _id enabled")
    .exec()
    .then(docs => {
      const response = {

        feeds: docs.map(doc => {
          return {
            name: doc.name,
            url: doc.url,
            enabled: doc.enabled,
            _id: doc._id
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


//update the channel, will change the attribute sent, and leave the ones that are blank
exports.update = (req, res, next) => {
  const id = req.params.channelId;
  Channel.update({ _id: id }, req.body)
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


//removes a channel from the database, based on ID
exports.deleteChannel = (req, res) => {
  const id = req.params.channelId;
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
