==============================================================
MINITAGE.DJANGO BUILDOUT FOR bv.client
==============================================================

WARNING ABOUT BUILOOUT BOOTSTRAP WARNING
--------------------------------------------

        !!!    Be sure to use zc.buildout >= 1.5.0 or you ll have errors or bugs.    !!!

If you are using the standalone (choose to answer inside_minitage=no), you must ensure to do the
$python bootstrap.py dance with a python compatible with the targeted zope installation (python 2.4/plone3 python 2.6/plone4)
eg: cd bv.client && python2.4 bootstrap.py && bin/buildout -vvvvvvc <CONFIG_FILE>


Minitage users, don't worry about that, all is setted for you in the two minibuilds created for you,
just issue minimerge -v <MINIBUILD_NAME> after installing the minilay in your MINITAGE/minilays directory.


ALWAYS USE THE MINITAGE ENVIRONMENT FILE INSIDE A MINITAGE
--------------------------------------------------------------

Before doing anything in your project just after being installed, just source the environment file in your current shell::

    source $MT/zope/bv.client/sys/share/minitage/minitage.env # env file is generated with $MT/bin/paster create -t minitage.instances.env bv.client


INSTALLING THIS PROJECT VITH MINITAGE
--------------------------------------
::

    export MT=/minitage
    virtualenv --no-site-packages --distribute $MT
    source /minitage/bin/activate
    easy_install -U minitage.core minitage.paste
    svn co https://github.com/bisonvert/bv.client.git/minilays/bv.client $MT/minilays/bv.client
    minimerge -v bv.client
    #minimerge -v bv.client-prod
    $MT/bin/paster create -t minitage.instances.env bv.client #(-prod)
    source $MT/zope/bv.client/sys/share/minitage/minitage.env
    cd $INS #enjoy !


DEVELOP MODE
---------------
To develop your application, run the ``(minitage.)buildout-dev.cfg`` buildout:

  * it comes with development tools.
  * it configures the instance to be more verbose
  * it has only one instance and not all the hassles from production.


PRODUCTION MODE
---------------
To make your application safe for production, run the ``(minitage.)buildout-prod.cfg`` buildout'.
It extends this one with additionnal crontabs and backup scripts and some additionnal instances creation.


BASE BUILDOUTS WHICH DO ONLY AGGREGATE PARTS FROM THERE & THERE
-------------------------------------------------------------------
Love to know that Minitage support includes xml libs, ldap, dbs; python, dependencies & common eggs cache for things like lxml or PIL), subversion & much more.
::

    |-- minitage.buildout-dev.cfg   -> buildout for development with minitage support
    |-- buildout-dev.cfg                     -> buildout for development
    |-- minitage.buildout-prod.cfg  -> buildout for production  with minitage support
    |-- buildout-prod.cfg                    -> buildout for production
    |-- etc/minitage/minitage.cfg   -> some buildout tweaks to run in the best of the world with minitage
    |-- etc/base.cfg                -> The base buildout



PROJECT SETTINGS
~~~~~~~~~~~~~~~~~~~~~~~~
- Think you have the most important sections of this buildout configuration in etc/bv.client.cfg
Set the project developement  specific settings there
::

    etc/project/
    |-- bv.client.cfg       -> your project needs (packages, sources, products)
    |-- sources.cfg          -> externals sources of your project:
    |                           - Sources not packaged as python eggs.
    |                           - Eggs Grabbed from svn, add here your develoment eggs.
    |                           - Links to find distributions.
    |-- patches.cfg          -> patches used on the project
    |-- cluster.cfg          -> define new zope instances here & also their FileSystemStorage if any.
    |-- bv.client-kgs.cfg   -> Generated KGS for your project (minitage's printer or buildout.dumppickledversion)
    `-- versions.cfg         -> minimal version pinning for installing your project


SYSTEM ADMINISTRATORS RELATED FILES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    etc/init.d/                 -> various init script (eg supervisor)
    etc/logrotate.d/            -> various logrotate configuration files
    etc/sys/
    |-- high-availability.cfg   -> Project production settings like supervision, loadbalancer and so on
    |-- maintenance.cfg         -> Project maintenance settings (crons, logs)
    `-- settings.cfg            -> various settings (crons hours, hosts, installation paths, ports, passwords)
    `-- settings-prod.cfg       -> TO BE MANUAL CREATED IN PRODUCTION : production critical settings like passwords.


CRONS
~~~~~~
::

    |-- etc/cron_scripts/backup_pgsql.sh   -> backup script for pgsql


SETTINGS
~~~~~~~~~


REVERSE PROXY
--------------
We generate two virtualhosts for a cliassical apache setup, mostly ready but feel free to copy/adapt.
::
    etc/apache/
    |-- 100-bv.client.reverseproxy.conf                     -> a vhost for ruse with a standalone plone (even with haproxy in front of.)
    |-- 100-bv.client.reverseproxy.deliverance.conf         -> a vhost for use with a plone behind a deliverance server.
    `-- apache.cfg
    etc/templates/apache/
    |-- 100-bv.client.reverseproxy.conf.in                  -> Template for a vhost for ruse with a standalone plone (even with haproxy in front of.)
    `-- 100-bv.client.reverseproxy.deliverance.conf.in      -> Template for a vhost for use with a plone behind a deliverance server.

In settings.cfg you have now some settings for declaring which host is your reverse proxy backend & the vhost mounting:

    * hosts:zope-front / ports:zope-front                              -> zope front backend
    * reverseproxy:host / reverseproxy:port / reverseproxy:mount-point -> host / port / mountpoint on the reverse proxy)


KGS FILE
----------
We provide a part to generate the etc/bv.client-kgs.cfg file.
This will allow you to freeze software versions known to work with your project and make reproducible environment.
This file will be generated the first time that you run buildout.
To un it, just run bin/buildout -vvvvvvc <CONFIG_FILE> install kgs
To unlock the versions, cmment out the according statement ``etc/project/bv.client-kgs}.cfg`` in the extends option of the bv.client.cfg gile.

PRODUCTION
-----------

    You have some backups than you can enable in the buildout-prod.cfg, specially for the pgsql cron scripts and its related cron.
    Think that the user for the postgresql cron must be authorized to connect locally without password.

A word about minitage.paste instances
--------------------------------------
You are maybe wondering why this big buildout do not have out of the box those fancy monitoring, load-balancing or speedy databases support.
#
For the author, System programs that are not well integrated via buildout and most of all not written in python don't really have to be deployed via that buildout.
And most of all, you ll surelly have head aches to make those init-scripts or rotation logs configurations right.
Because the recipe which do them don't support it or other problems more or less spiritual.
#
Keep in mind that in Unix, one thing must do one purpose, and do it well. And many sysadmins don't want to run a buildout
to generate a configuration file or build their loadbalancer, They want to edit in place, at most fetch the configuration file from somewhere and adapt,that's all.
#
Nevertheless, as usual, they are exceptions:
     - supervisord which is well integrated. So supervisor is deployed along in the production buildout if any.
     - We generate through buildout a haproxy configuration file or hudson related stuff
#
That's because we support that throught 'minitage.paste.instances'. Those are templates which create some instance of some program
inside a subdirectory which is:
   - sys/ inside a minitage project
   - ADirectoryOfYourChoice/ if your are not using minitage
#
This significate that you can install a lot of things along with your project with:
   - minitage/bin/easy_install -U minitage.paste(.extras) (or get it via buildout)
   - paster create -t <TEMPLATE_NAME> projectname_OR_subdirectoryName inside_minitage=y/n
     Where TEMPLATE_NAME can be (run paster create --list-templates|grep minitage.instances to get an up2date version):
#
     * minitage.instances.apache:          Template for creating an apache instance
     * minitage.instances.env:             Template for creating a file to source to get the needed environnment variables for playing in the shell or for other templates
     * minitage.instances.mysql:           Template for creating a postgresql instance
     * minitage.instances.nginx:           Template for creating a nginx instance
     * minitage.instances.paste-initd:     Template for creating init script for paster serve
     * minitage.instances.postgresql:      Template for creating a postgresql instance
     * minitage.instances.varnish:         Template for creating a varnish instance
     * minitage.instances.varnish2:        Template for creating a varnish2 instance
#
     The minitage.paste package as the following extras:
#
     * minitage.instances.openldap:      Template for creating an openldap instance
     * minitage.instances.tomcat:        Template for creating a tomcat instance
     * minitage.instances.cas:           Template for creating a Jisag CAS instance
     * minitage.instances.hudson:        Template for creating an hudson instance
#
Note that if you are using minitage, you ll have better to add dependencies inside your minibuild and run minimerge to build them prior to run the paster command
#
For example, to add a postgresql instance to your project, you will have to issue those steps:
    * $EDITOR minitage/minilays/bv.client_minilay/bv.client -> add postgresql-8.4 to the dependencies list
    * minimerge -v  bv.client install what was not, and surely at least postgresql-8.4
    * minitage/bin/paster create -t minitage.instance.postgresql bv.client
    * Then to start the postgres : zope/bv.client/sys/etc/init.d/bv.client_postgresql restart


# vim:set ft=rest:
