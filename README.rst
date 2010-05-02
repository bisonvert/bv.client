BisonVert client
================

A simple django application client for the BisonVert carpooling service.

Dependencies

Dependencies
------------

BisonVert depends on few existing django apps and packages:
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

