module.exports = (app) => {
    const channels = require('../controllers/channel.controllers.js');

    app.post('/channel', channels.createNewChannel);

    // get all channel names, listed by name. We can use this for when an editor wishes to add a new channel
    app.get('/channel/', channels.getAll);

    app.get('/channel/names', channels.getAllByName);

    app.get('/channel/:channelId', channels.getOne);

    app.get('/channel/namesearch', channels.search);

    app.patch('/channel/:channelId', channels.update);

    app.put('channel/enabled', channels.toggleEnableChannel);

    app.delete('/channel/:channelId', channels.deleteChannel);
    // // get a channel of a certain id
}
