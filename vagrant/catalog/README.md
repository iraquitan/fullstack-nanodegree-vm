# catalog-app
A project for a catalog app, where users can sign up with email and password or Google or Facebook accounts. Logged users can add, edit and delete categories and items. Anonymous users can only view the items and categories. Logged users can only edit and delete their onw categories and items. There is also a Json API for all the catalog, for category items, for items and categories. Also features a sitemap.xml file with static, categories and items loc and images.

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
```python
DEBUG = True
SECRET_KEY = 'your_super_secret_key'
SQLALCHEMY_DATABASE_URI = "sqlite:///../catalog/catalog.db"
OAUTH_CREDENTIALS = {
    'google': {
        'id': "Google__client__id.apps.googleusercontent.com",
        'secret': "Google_client_secret_"
    },
    'facebook': {
        'id': "Facebook_client_id",
        'secret': "Facebook_client_secret"
    }
}
```
* Run the following code on terminal to populate DB: `python populate_db.py`.
* Run the following code on terminal to run the server locally: `python runserver.py`.

## Creator
**Iraquitan Cordeiro Filho**

* <https://twitter.com/iraquitan_filho>
* <https://github.com/iraquitan>