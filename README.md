![test](/static/logo.jpg)
# Newsy

Newsy is a news aggregation portal built to incorporate a RESTful API based around RSS feeds. Newsy is capable of selecting & serving news articles based on pre-defined topics. The site runs as a Flask app and connects to a MongoDB database. The frontend is enhanced with Bootstrap and the API was created using NodeJS, Express & Mongoose. Developed as part of a Masters-Level group project in Maynooth University

## Installation & Setup: 

### Install python libraries: 

For Ubuntu 18.04:

```
$ pip install -r requirements_ubuntu1804.txt
```

For Windows:
```
$ pip install -r requirements_windows.txt
```

### Install node packages
```
$ cd nodejs
$ npm install
```

### MongoDB setup

Set up a MongoDB cluster with collections newsy.channels (For the API), newsy.login, newsy.topics & newsy.articles (For the site)

Change newsy/nodejs/config/database.config.js and the line in app.py

```
$ client = MongoClient("mongodb+srv://user:pw@newsy-98fzw.mongodb.net/test?retryWrites=true&w=majority")
``` 
To match your database.

### Run API

```
$ cd nodejs
$ node index.js
```

### Run site backend

```
$ python app.py
```

## Newsy

Newsy is a website designed for consumption of the new aggregation API. It handles login, user creation, password encryption & resetting, a UI for consumption of the API, article logging, feed parsing and topics (as mentioned in the Editors section). By default it will run on http://127.0.0.1:5000/

#### Editors

Editors are responsible for curating the content shown on the site. They can enable & disable certain RSS feeds, as well as add new ones through the RSS url. They can also define certain case-insensitive topics to filter saved articles. The format of topics is as such:

* \<topic> will return all articles containing the word 'topic' in the title (e.g. 'ireland')
* \<topic1 topic2> with a space in between will return all articles with either the word 'topic1' or 'topic2' in the title (e.g. 'Ronaldo Messi')
* \<topic1 AND topic2> with an 'AND' separating the two will return all articles with the words 'topic1' and 'topic2' in them (e.g. 'Coronavirus AND China')

Anytime an editor command is performed, the login manager will check the user's credentials to ensure no regular user is attempting them. Right now it is possible for any user to sign up as an editor, however it would be fairly trivial to change this if security was a concern to the project.

#### Users

Users can log into their profile and see the articles as well as the articles for each topic. They must log in to view the content and all of their clicked links are anonymously logged. Their passwords are stored using AES 256 encryption in the newsy.login database. 

## API

#### Endpoints

Format is http://\<url>/\<endpoint>, e.g GET: http://localhost:3000/channel/5eadd20cc33ff44bd3cc91ad

* POST: 
	* /channel : Create new channel with input format: 
		* 'name' : String denoting the channel name 
		* 'url' : String of the RSS feed url 
		* 'enabled' : Boolean value denoting whether the feed is enabled or not

* GET:
	* /channel/ : Get all channel names
	* /channel/\`channel_id\` : Get a channel based on a given channel ID 
	* /channel/\`channel_url\` : Get a channel based on a given RSS feed URL
	* /channel/namesearch : Get all channels matching a regex expression passed as input

* PATCH:
	* /channel/\`channel_id\` : Update a channel using the same format as the POST command

* PUT:
	* /channel/enabled : Enable/Disable the channel based on a given channel name

* DELETE:
	* /channel/\`channel_id\` : Delete a channel based on a given channel ID 

By default this will run on http://localhost:3000