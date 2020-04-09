module.exports = (app) => {
    const channels = require('/app/controllers/channel.controllers.js');

    // Create a new channel, fro editors
    app.post('/channel', channels.createNewChannel);

    // get all channel names, listed by name. We can use this for when an editor wishes to add a new channel
    app.get('/channel/name', channels.getAll);

    app.get('/channel/namesearch', channels.search);

    app.put('channel/name', channels.updateName);

    app.put('channel/url', channels.updateURL);

    app.put('channel/enable', channels.enableChannel);

}
