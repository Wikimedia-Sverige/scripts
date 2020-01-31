# WMSE Scripts
This repository contains miscellaneous scripts used by [Wikimedia Sverige (WMSE)](https://www.wikimedia.se). Most of these scripts are single file.

* fortnox_huvudbok_processing - *Scripts and datafiles to crunch the "Huvudbok" export (in .txt format) from Fortnox into a manageable .tsv format.*
* google_drive_scripts
  * calc_burnchart.gs - *Script for the Burnchart document. Used to copy tab name
    to a cell and to calculate personnel costs.*
  * calc_getSheetName.gs - *Script for Calc to create a function which returns the name of the sheet where a given cell resides.*
  * listFiles.gs - *Script for listing directories and files on Drive.*
* python_scripts
  * AddressPoint.py - *script which formats an AddressPoint datafile*
  * extension_documentation.py - *generates wikitext strings to use on extension pages on the [MediaWiki-wiki](https://www.mediawiki.org).*
  * wikimania_program_list.py - *generate wikitext for program list used for Wikimania 2019.*
* fortnox.user.js - *Greasemonkey script for displaying project names in Fortnox.*
* phabricator.user.js - *Convenience script for Phabricator. Adds link to unread notifications in the top bar.*
* phabricator-compact-workboard.user.css - *Stylus CSS for removing the side menu in Phabricator workboards.*
* phabricator-floating-top-bar.user.css - *Stylus CSS for floating top bar in Phabricator.*

When adding a script, also add it to this list with a short description.
