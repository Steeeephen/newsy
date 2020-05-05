module.exports = (app) => {
    const channels = require('../controllers/channel.controllers.js');

    // Create a new channel, the channel will be created according to the infroamtion passed, can recognise form data
    app.post('/channel', channels.createNewChannel);

    // get all channel names, listed by name. We can use this for when an editor wishes to add a new channel
    app.get('/channel/', channels.getAll);

    //get a channel by ID, as the url is in the form :channelID, the url for the channel with ID 4567819 would be '/channel/4567819'
    app.get('/channel/:channelId', channels.getOne);

    //updates the channel, is passed an id, updates its record in the database according to the request body.
    app.patch('/channel/:channelId', channels.update);

    //deletes the channel whose id is passed.
    app.delete('/channel/:channelId', channels.deleteChannel);
}
