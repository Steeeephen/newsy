module.exports = (app) => {
    const channels = require('../controllers/channel.controllers.js');

    // Create a new channel, the channel will be created according to the infroamtion passed, can recognise form data
    app.post('/channel', channels.createNewChannel);

    // get all channel names, listed by name. We can use this for when an editor wishes to add a new channel
    app.get('/channel/', channels.getAll);

    //get a channel by ID, as the url is in the form :channelID, the url for the channel with ID 4567819 would be '/channel/4567819'
    app.get('/channel/:channelId', channels.getOne);

    //get a channel matching the url, will just display
    app.get('/channel/:url', channels.display);

    //returns all channels matching a regex term passed by the user, as long as the channel name contains that term, it will return
    app.get('/channel/namesearch', channels.search);

    //updates the channel, is passed an id, updates its record in the database according to the request body.
    app.patch('/channel/:channelId', channels.update);

    //enables or disables the channel (opposite of the current value of enabled) when a button is clicked
    app.put('channel/enabled', channels.toggleEnableChannel);

    //deletes the channel whose id is passed.
    app.delete('/channel/:channelId', channels.deleteChannel);
}
