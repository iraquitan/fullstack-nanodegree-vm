# catalog-app
Project description

## Table of contents
* [Requirements](#requirements)
* [Quick start](#quick-start)
* [Creator](#creator)

## Requirements
* Python 2.7
* Git
* Vagrant
* Building bcrypt dependencies on Ubuntu Linux: `sudo apt-get install build-essential libssl-dev libffi-dev python-dev`
* Install bcrypt library: `sudo pip install bcrypt`
* Install libraries in the `requirements.txt` file using pip.

## Quick start 
* Clone the repo: `git clone https://github.com/iraquitan/fullstack-nanodegree-vm.git`.
* Change directory to the recently cloned repository and then to the `/vagrant` directory.
* Start vagrant virtual machine with `vagrant up`.
* Change to the `/catalog` directory.
* Create a local config file in `instance/config.py`.
* And fill with local config like database location and Oauth credentials as in the example below:
<code>
DEBUG = True
SECRET_KEY = 'your_super_secret_key'
SQLALCHEMY_DATABASE_URI = "sqlite:///../catalog/catalog.db"
OAUTH_CREDENTIALS = {
&nbsp;&nbsp;&nbsp;&nbsp;'google': {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': "Google__client__id.apps.googleusercontent.com",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'secret': "Google_client_secret_"
&nbsp;&nbsp;&nbsp;&nbsp;},
&nbsp;&nbsp;&nbsp;&nbsp;'facebook': {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': "Facebook_client_id",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'secret': "Facebook_client_secret"
&nbsp;&nbsp;&nbsp;&nbsp;}
}
<code>
* Run the following code on terminal to populate DB: `python populate_db.py`.
* Run the following code on terminal to run the server locally: `python runserver.py`.

## Creator
**Iraquitan Cordeiro Filho**

* <https://twitter.com/iraquitan_filho>
* <https://github.com/iraquitan>