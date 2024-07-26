maildev plugin for `Tutor <https://docs.tutor.edly.io>`__
###############################################################################

This plugin enabled local maildev server for Tutor development.


Installation
************

.. code-block:: bash

    tutor config save --set MAILDEV_SMTP_PORT=1025
    pip install git+https://github.com/andrii-hantkovskyi/tutor-contrib-maildev

Usage
*****

.. code-block:: bash

    tutor plugins enable maildev
    tutor dev launch
License
*******

This software is licensed under the terms of the AGPLv3.
