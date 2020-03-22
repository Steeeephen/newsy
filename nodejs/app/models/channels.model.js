const mongoose = require('mongoose');


//dummy schema for testing
var ChannelSchema = mongoose.Schema({
  id: String,
  name: String,
  url: String,
  enabled: Boolean
});

module.exports = mongoose.model('Channel', ChannelSchema);
