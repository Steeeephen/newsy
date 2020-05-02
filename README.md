![test](/static/logo.jpg)
# Newsy


Newsy is a news aggregation portal built to incorporate a RESTful API based around RSS feeds. Newsy is capable of selecting & serving news articles based on pre-defined topics. The site runs as a Flask app and connects to a MongoDB database. The frontend is enhanced with Bootstrap and the API was created using NodeJS, Express & Mongoose. Developed as part of a Masters-Level group project in Maynooth University

## Installation & Setup: 
### Ubuntu 18.04

Install libraries:

```
$ pip install requirements.txt
$ npm install --save express
$ npm install --save mongoose
```

Run API

```
$ cd nodejs
$ node index.js
```

Run site backend

```
$ python app.py
```

## Usage

### Editors

Editors are responsible for curating the content shown on the site. They can enable & disable certain RSS feeds, as well as add new ones through the RSS url. They can also define certain case-insensitive topics to filter saved articles. The format of topics is as such:

* \<topic> will return all articles containing the word 'topic' in the title (e.g. 'ireland')
* \<topic1 topic2> with a space in between will return all articles with either the word 'topic1' or 'topic2' in the title (e.g. 'Ronaldo Messi')
* \<topic1 AND topic2> with an 'AND' separating the two will return all articles with the words 'topic1' and 'topic2' in them (e.g. 'Coronavirus AND China')

### Users

Users can log into their profile and see the articles as well as the articles for each topic. They must log in to view the content and all of their clicked links are anonymously logged