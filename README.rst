=========================
teirubrics
=========================

Collates rubrics from multiple TEI XML files and creates static HTML reports

Installation
==================================

Install using pip:

.. code-block:: bash

    pip install git+https://github.com/rbturnbull/teirubrics.git


Encoding
==================================

To use this library, lectionary rubrics are represented using the
`Text Encoding Initiative (TEI) <https://tei-c.org>`_.  
TEI provides a hierarchical markup language capable of expressing the complex
textual features typically found in manuscript sources—such as corrections,
unclear readings, marginal notes, or line breaks—within a consistent and
machine-readable structure.

Header Structure
----------------

Each TEI file begins with a header that documents the manuscript witness and
its encoding conventions.

**Manuscript Description**

The ``<msDesc>`` element records the details of each witness, including
its physical and bibliographic information. Each manuscript is assigned
a unique XML identifier (``xml:id``). If the siglum used for the manuscript
differs from the identifier, it can be supplied in the ``n`` attribute.

The following subelements are used:

* ``<msIdentifier>`` — identification and location of the manuscript
* ``<msContents>`` — summary of the manuscript’s content
* ``<physDesc>`` — description of the support material, format, and foliation

For example, here is an example of the encoding of BnF 378/8:

.. code-block:: xml

    <msDesc xml:id="BnF_syr_378_VIII" n="BnF378/8">
        <msIdentifier>
        <settlement>Bibliothèque nationale de France</settlement>
        <idno>Syr. 378, Part VIII</idno>
        </msIdentifier>
        <msContents>
        <summary>Summa Theologiae Arabica, chapters 12 and 13</summary>
        </msContents>
        <physDesc>
        <objectDesc form="codex">
            <supportDesc material="parch">
            <support>
                <p>Parchment</p>
            </support>
            <extent>2 folios</extent>
            </supportDesc>
        </objectDesc>
        </physDesc>
    </msDesc>

**Encoding Description**

An ``<encodingDesc>`` section specifies the conventions used for markup.  
This includes:

* a description of the ``@rend`` attributes used to indicate ink color,
  decoration, or other visual properties of rubrics
* a taxonomy of encoding categories
* links to shared definitions stored in a separate file and included
  using the `XInclude <https://www.w3.org/TR/xinclude/>`_ standard

This modular structure allows all TEI files to share a consistent encoding
description.

Stand-off Lists
---------------

The ``<standOff>`` element provides centralized lists of entities that
can be referenced throughout the TEI documents.

**Events**

Each liturgical event (e.g., a feast or commemoration) is represented by
an ``<event>`` element with a unique ``xml:id`` and a human-readable label.
If the calendar date is fixed, it is recorded in the ``@when`` attribute.

For example:

.. code-block:: xml

    <event xml:id="FortyMartyrs" when="--03-09">
      <label>Forty Martyrs of Sebaste</label>
    </event>

**Places**

Topographical references are encoded as ``<place>`` elements. Each has a unique identifier, a
``<placeName>``, and optionally geospatial data (latitude, longitude, etc.)
for mapping purposes.

Both the events and places lists are stored in separate TEI files and linked
into each witness file via XInclude.

For example:

.. code-block:: xml

  <place xml:id="Jerusalem">
    <placeName>Jerusalem</placeName>
    <location>
      <geo decls="wgs84">31.778333 35.229722</geo>
      <precision match="city"/>
    </location>  
  </place>


Body Structure
--------------

The ``<body>`` of each TEI file contains the encoded rubrics for the biblical
books.

**Rubric Divisions**

Each biblical book is wrapped in a ``<div type="Epistle">`` (or analogous
division type). Individual lectionary headings appear in
``<div type="rubric">`` elements. Although TEI defines a ``<rubric>`` tag, it
is only valid inside ``<msItem>`` and thus not appropriate for the body of
the text.

Attributes for ``<div type="rubric">``:

* ``@corresp`` — corresponds to a biblical verse reference  
* ``@source`` — links to the ``xml:id`` of the manuscript in the header  
* ``@n`` — the folio number  
* ``@facs`` — URL or path to a facsimile image, if available

**Text of the Heading**

The rubric heading itself is encoded within a ``<head>`` element.  
The ``@rend`` attribute records typographic or stylistic features according to
the encoding taxonomy.

Alternative forms of the text are represented with a ``<choice>`` element,
typically containing:

* ``<orig xml:lang="ar">`` — the original text, preserving line breaks,
  gaps, and corrections
* ``<reg type="translation" xml:lang="en">`` — a formal translation,
  with embedded ``<place>`` and ``<date>`` elements linking to the
  stand-off lists

For example:

.. code-block:: xml

    <div type="rubric" corresp="ICor10:1">
        <anchor source="#S155" n="66r" facs="https://iiif.sinaimanuscripts.library.ucla.edu/iiif/2/ark%3A%2F21198%2Fz1bs09w9%2F9071641s/full/1500,/0/default.jpg"/>
        <head rend="red cross-decorated">
        <choice>
            <orig xml:lang="ar">
            <l>تقرا في يوم صوم القلند في القدس</l>
            </orig>
            <reg type="translation" xml:lang="en">
            Read on the <date when-custom="#TheophanyVigil">day of the Fast of Kalends</date>
            in <placeName ref="#Jerusalem">Jerusalem</placeName>.
            </reg>
        </choice>
        </head>
    </div>


Usage of teirubrics
===================

The TEI XML serves as the *single source of truth*.  
Derived representations—such as collations or visualizations—can be generated
programmatically.

The `teirubrics <https://github.com/rbturnbull/teirubrics>`_ Python library
is provided to process multiple TEI XML files and generate static HTML reports.
These reports collate rubrics by **liturgical date** or **biblical verse** and
include links to translations and facsimile images.

Command-line options include:

* specifying multiple TEI XML files (each becomes a column in the table)
* generating rows by date or verse
* filtering rubrics by referenced place names

The resulting HTML reports enable cross-witness comparison of rubrics across
languages and traditions.

To collate by date, use the following command:

.. code-block:: bash

    teirubrics by-date S155.xml S73.xml --output reports/dates.html

To collate by vse, use the following command:

.. code-block:: bash

    teirubrics by-verse S155.xml S73.xml --verse-list ArabGr1-Verses.txt --output reports/verses.html

More options are available, see:

.. code-block:: bash

    teirubrics --help


Example
================

To see examples of using this encoding scheme, go to https://github.com/rbturnbull/ArabGr1Rubrics

It has TEI XML files for two manuscripts (S155 and S73) released under a
`Creative Commons Attribution 4.0 License (CC BY 4.0)
<https://creativecommons.org/licenses/by/4.0/>`_.

The GitHub repository includes continuous integration (CI) testing to validate the TEI XML files at every push. 
The repository includes the static HTML reports with collations by verse and by date which are published at https://rbturnbull.github.io/ArabGr1Rubrics/


Credit
============

See the forthcoming chapter 'Hagiopolite Rubrics in an Arabic Version of Paul' for more details.

Robert Turnbull https://robturnbull.com