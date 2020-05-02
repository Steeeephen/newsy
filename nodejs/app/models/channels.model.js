const mongoose = require('mongoose');

//defines how one of our channels should be represented in mongodb, _id is a convention, there is always a _id in every mongodb entry
var channelSchema = mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  name: String,
  url: String,
  enabled: Boolean
});

//Every 'Channel' can now be used elsewhere to perform operations on
module.exports = mongoose.model('Channel', channelSchema);

