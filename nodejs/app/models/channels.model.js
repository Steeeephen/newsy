const mongoose = require('mongoose');


//dummy schema for testing
var ChannelSchema = mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  name: String,
  url: String,
  enabled: Boolean
});

module.exports = mongoose.model('Channel', ChannelSchema);
