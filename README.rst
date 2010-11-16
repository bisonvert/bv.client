BisonVert client
================

This repository is the main repository of a client wrote in Django, for
BisonVert, a carpooling system.

The infrastructure is in 4 parts, which can all be found at: https://github.com/bisonvert/.

For further informations, **see the wiki at:** https://github.com/djcoin/bv.client/wiki/

What is Bisonvert ?
-------------------

BisonVert is a simple carpooling web application developped by `Makina Corpus <http://www.makina-corpus.com/>`_. The primary goal is to match
carpool demands with carpool offers.

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

* bvclientlib: https://github.com/djcoin/bv.libclient
* django-oauthclient: https://github.com/djcoin/django-oauthclient
* the excellent restkit lib, by Benoît Chesneau: https://github.com/benoitc/restkit/

