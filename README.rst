=========================
teirubrics
=========================

Collates rubrics from multiple TEI XML files and creates static HTML reports


Installation
==================================

Install using pip:

.. code-block:: bash

    pip install git+https://github.com/rbturnbull/teirubrics.git


Usage
==================================

To collate by date, use the following command:

.. code-block:: bash

    teirubrics by-date S155.xml S73.xml --output reports/dates.html

To collate by vse, use the following command:

.. code-block:: bash

    teirubrics by-verse S155.xml S73.xml --verse-list ArabGr1-Verses.txt --output reports/verses.html

Credit
============

See the forthcoming chapter 'Hagiopolite Rubrics in an Arabic Version of Paul' for more details.

Robert Turnbull https://robturnbull.com