=============================
Django Emulate AWS Env
=============================

.. image:: https://badge.fury.io/py/django-emulate-aws-env.svg
    :target: https://badge.fury.io/py/django-emulate-aws-env

.. image:: https://travis-ci.org/danielholmes/django-emulate-aws-env.svg?branch=master
    :target: https://travis-ci.org/danielholmes/django-emulate-aws-env

.. image:: https://codecov.io/gh/danielholmes/django-emulate-aws-env/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/danielholmes/django-emulate-aws-env

Emulates the conditions of an AWS "Serverless" environment (`API Gateway`_ + Lambda_) in your test and development
environments (such as those deployed by Zappa_).

Quickstart
----------

Install Django Emulate AWS Env::

    pip install django-emulate-aws-env

Add the Django Emulate AWS Env middleware. This should be the highest possible priority in your list and just in your
development and test environments:

.. code-block:: python

    MIDDLEWARE = [
        'emulate_aws_env.middleware.modify_request',
        ...
    ]

Or if you're using a dedicated settings file for tests/development:

.. code-block:: python

    from .base import *

    ...

    MIDDLEWARE = ['emulate_aws_env.middleware.modify_request'] + MIDDLEWARE


Features
--------

The `API Gateway`_ service has the following restrictions which aren't present in the default environment used to test
Django projects:

 - `It doesn't allow duplicate query string names`_
 - `The request content length can't exceed 10485760 bytes`_

The provided middleware modifies the request to these restrictions.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _`API Gateway`: https://aws.amazon.com/api-gateway/
.. _Lambda: https://aws.amazon.com/lambda/
.. _Zappa: https://github.com/Miserlou/django-zappa
.. _`It doesn't allow duplicate query string names`: https://forums.aws.amazon.com/message.jspa?messageID=676456
.. _`The request content length can't exceed 10485760 bytes`: http://stackoverflow.com/questions/33762259/increase-maximum-post-size-for-amazon-api-gateway
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
