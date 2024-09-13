`MailDev`_ plugin for `Tutor`_
================================

This plugin enables local `MailDev`_  server for Open edX development with Tutor.


Installation
------------

::

  pip install "git+https://github.com/raccoongang/tutor-contrib-maildev.git@VERSION"

Usage
-----


Enable the plugin with:

::

  tutor plugins enable maildev

Then, restart your platform and run the initialization scripts using:

::

  tutor dev launch

Using MailDev service
~~~~~~~~~~~~~~~~~~~~~
The MailDev user interface will be available at `http://maildev.local.edly.io:1080/` for a development instance.
`MailDev`_ is a simple way to test your project's generated emails during development with an easy to use web interface that runs on your machine.

.. image:: https://raw.githubusercontent.com/raccoongang/tutor-contrib-maildev/master/static/images/maildev-ui.png
    :alt: MailDev UI

Configuration
-------------


License
-------

This software is licensed under the terms of the AGPLv3.

.. _MailDev: https://maildev.github.io/maildev/
.. _Tutor:  https://docs.tutor.edly.io
