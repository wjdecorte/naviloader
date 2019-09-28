Navis Loader
============

Navis Loader will process all source files in JSON format saved in the
source data directory and save without duplicates in the target data directory.

Look how easy it is to use::

    $ naviload --help
    $ naviload sample --help
    $ naviload loader --help

Features
--------

- Create sample data for testing
- Saves data in date specific files in `Parquet <https://parquet.apache.org/>`_ format
- Removes any duplicate records

Installation
------------

Install naviload by running::

    $ cd /path/to/project/
    $ python3 -m venv test_navis_loader
    $ cd test_navis_loader
    $ source bin/activate
    $ pip install git+https://github.com/wjdecorte/navis_loader.git@master


Contribute
----------

- Issue Tracker: `<https://github.com/wjdecorte/navis_loader/issues>`_
- Source Code: `<https://github.com/wjdecorte/navis_loader>`_

Support
-------

If you are having issues, please let us know.
Contact the author at `jdecorte@decorteindustries.com <mailto:jdecorte@decorteindustries.com>`_.

License
-------

The project is licensed under the <TBD> license.

