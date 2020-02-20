============
Installation
============
This document will show you how to get 911maps running on your system.

Currently install has been tested with Ubuntu, but will work with any system that can run Python and Django.

System Prerequisites
====================

* Linux Machine (tested with WSL bash on Windows)
* `Python`_ 3.6+
* `Virtualenv`_
* `PIP`_  Should be installed with Python 3
* `git`_

.. _Python: https://www.python.org/
.. _Virtualenv: https://virtualenv.pypa.io/en/stable/
.. _PIP: https://pypi.python.org/pypi/pip
.. _git: https://git-scm.com/


Using apt-get:

.. code-block:: console

    $ sudo apt-get install python3-dev python3-virtualenv python3-pip git gdal-bin python-psycopg2


Assumptions
===========

* `Data export`_ obtained from an Active911 instance (see test data folder for an example)
* Virtualenv with a name of env

.. _Data export: 

Getting 911maps
====================

The source is on GitHub, use git to clone the repository. Starting from your home directory of ``/home/911maps``

.. code-block:: console

  $ git clone https://github.com/gavinrozzi/911maps.git

This command will download the latest version of 911maps

Setup Virtual Environment
=========================

Setup a new Python 3.x virtual environment in the ``env`` direcory. Set the visual prompt to ``(911maps)``.

.. code-block:: console

    $ cd 911maps
    $ virtualenv -p python3 env --prompt='(911maps)'

Activate Virtual Environment
============================

You will need to re run this step each time you start a new shell or log into your machine.

.. code-block:: console

  $ source env/bin/activate

This will set you into a new python environment any packages you install via ``pip`` will only live in this area and do not touch your system files. This allowed you to have multiple projects with different dependencies. 


You can use the command ``deactivate`` to exit back to your normal system environment.

Install Python Packages
=======================

Using pip install all required packages from the ``requirements.txt`` file.

.. code-block:: console

  (911maps)$ pip3 install -r requirements.txt

Get Ready For First Use
=======================

Initialize Database
===================

Using the `django manage.py`_ command to build the new database.

.. _django manage.py: https://docs.djangoproject.com/en/dev/ref/django-admin/


.. code-block:: console

  (911maps)$ ./manage.py migrate

Create Admin Account
====================

.. code-block:: console

  (911maps)$ ./manage.py createsuperuser
  Username: test
  Email address: test@sample.com
  Password: mypassword
  Password (again): mypassword
  Superuser created successfully.

Collect Static Files 
====================

Using the ``manage.py`` command 

.. code-block:: console

  (911maps)$ ./manage.py collectstatic

Start Test Web Server
============================

First note this is not full producation ready server. It can handle a couple users.

Using the ``manage.py`` command again

.. code-block:: console

  (911maps)$ ./manage.py runserver

This will start the server up listening on the local loopback address on port ``8000``. Start your web browser and go to `http://localhost:8000/calls`_. You should seen the main page
Visit ``localhost:8000/admin/`` to log into the admin area with the account you created.

.. _`http://localhost:8000`: http://localhost:8000

If you are running this on a remote server you need to have the web server use its public IP adress so you can connect.

.. code-block:: console

   (911maps)$ ./manage.py runserver 0.0.0.0:8000

This will run the server also on port 8000 but will be accessible via the server's IP address or dns name on port ``8000`` also.

Do not attempt to use the test web server in a production deployment, it can only handle a few users and is not suitable for production.