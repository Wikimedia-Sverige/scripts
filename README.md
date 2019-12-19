# WMSE Scripts
This repository contains miscellaneous scripts used by [Wikimedia Sverige (WMSE)](https://www.wikimedia.se). Most of these scripts are single file.

* fortnox_huvudbok_processing - *Scripts and datafiles to crunch the *Huvudbok* export (in .txt format) from Fortnox into a manageable tsv format.*
* google_drive_scripts
  * calc_burnchart.gs - *Script for the Burnchart document. Used to copy tab name
    to a cell and to calculate personnel costs.*
  * calc_getSheetName.gs - *Script for Calc to create a function which returns the name of the sheet where a given cell resides.*
  * listFiles.gs - *Script for listing directories and files on Drive.*
* python_scripts
  * AddressPoint.py - *script which formats an AddressPoint datafile*
  * extension_documentation.py - *generates wikitext strings to use on extension pages on the [MediaWiki-wiki](https://www.mediawiki.org).*
  * replace_templates.py - *pywikibot script for replacing template usages throughout the WMSE wiki.*
  * wikimania_program_list.py - *generate wikitext for program list used for Wikimania 2019.*
* fortnox.user.js - *Greasemonkey script for displaying project names in Fortnox.*
* phabricator-floating-top-bar.user.css - *Stylus CSS for floating top bar in Phabricator.*

When adding a script, also add it to the list with a short description.
