BisonVert client
================

This repository is the main repository of a client wrote in django, for
bisonvert, a carpooling system.

What is Bisonvert ?
-------------------

Bisonvert is a simple carpooling web application. The primary goal is to match
carpool demands with carpool offers.

The infrastructure is in 4 parts, which can all be found in the bitbucket page
http://bitbucket.org/bisonvert/.

The server
~~~~~~~~~~

The main application logic of the carpooling service is contained in the server.
This includes:

* A carpooling system: basic operations on offer/demand.
* A ranking system for the users.
* A system to contact the users.
* Availability of the data trought an API
* A management system for API tokens (oauth)

The server uses internally Python and Django for the web application, PostGIS
for Geographic informations and requests, and Mapnik to return the layers.

The server *does not* provides a web interface to create and search trips: this
is the role of the client.

The library
~~~~~~~~~~~

A library to consume the API is provided. It's wrote in python, and not tied at
all to a specific framework. You could imagine using this lib to wrote
Zope/Plone applications as of Django applications.


The client
~~~~~~~~~~

A client is also provided. It's goal is to provide a simple interface to consume
the API (served by the server). It's a Django application too, and that's the
repository you're browsing currently.


Dependencies
------------

BisonVert client depends on few existing django apps and packages:

* bvclientlib: http://bitbucket.org/bisonvert/bvlibclient
* django-oauthclient: http://bitbucket.org/bisonvert/django-oauthclient
* the excellent restkit lib, by Benoît Chesneau: http://github.com/benoitc/restkit/

Installation
------------

You can both install bisonvert from the mercurial repositories, and from pip.

Pip install
~~~~~~~~~~~

The best way is to install bisonvert from pip::

    $ pip install bisonvert-client

Install from sources
~~~~~~~~~~~~~~~~~~~~

To be sure to have the last dev version, follow these steps::

    $ hg clone http://bitbucket.org/bisonvert/bvclient/
    $ hg clone http://bitbucket.org/bisonvert/bvlibclient/
    $ hg clone http://bitbucket.org/bisonvert/django-oauthclient/

Once the source fetched, you need to configure your client.

Launch bisonvert
~~~~~~~~~~~~~~~~

To launch the client, just go to the source lib, and do::

    $ python manage.py runserver

