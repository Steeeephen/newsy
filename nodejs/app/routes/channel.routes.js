module.exports = (app) => {
    const channels = require('/app/controllers/channel.controllers.js');

    // Create a new channel, for editors
    app.post('/channel', channels.createNewChannel);

    // get all channel names, listed by name. We can use this for when an editor wishes to add a new channel
    app.get('/channel/names', channels.getAll);
    
    //return a single channel, with its name and url
    app.get('/channel/:name', channels.getOne);
    
    //return a single channel url
    app.get('/channel/:url', channels.display);
    
    // search for channel based on name, will return all names that contain a user regex
    app.get('/channel/namesearch', channels.search);
    
    //update the channel according to name
    app.put('channel/:name', channels.updateName);
    
    //toggle whether the channel is enabled or disabled according to a button click
    app.put('channel/enable', channels.toggleEnableChannel);
    
    //Delete a selected channel from the database
    app.put('channel/name', channels.deleteChannel);
}
