module.exports = (app) => {
    const channels = require('/app/controllers/channel.controllers.js');

    // Create a new channel
    app.post('/channel', channels.createNewChannel);

    // get all channels
    app.get('/channel/', channels.getAll);

    // get a channel of a certain id
    app.get('/channel/:id', channels.getOne);

    // Update a channel of a certain id
    app.put('/channel/:id', channels.updateChannel);

}
