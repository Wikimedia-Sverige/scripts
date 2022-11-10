# WMSE Scripts
This repository contains miscellaneous scripts used by [Wikimedia Sverige (WMSE)](https://www.wikimedia.se). Most of these scripts are single file.

* fortnox_huvudbok_processing - *Scripts and datafiles to crunch the "Huvudbok" export (in .txt format) from Fortnox into a manageable .tsv format.*
* google_drive_scripts
  * calc_burnchart.gs - *Script for the Burnchart document. Used to copy tab name
    to a cell and to calculate personnel costs.*
  * calc_getSheetName.gs - *Script for Calc to create a function which returns the name of the sheet where a given cell resides.*
  * listFiles.gs - *Script for listing directories and files on Drive.*
  * mailAlert.gs - *Send mail alerts to a separate address when Gsuite address receives mail.*
* python_scripts
  * AddressPoint.py - *script which formats an AddressPoint datafile*
  * extension_documentation.py - *generates wikitext strings to use on extension pages on the [MediaWiki-wiki](https://www.mediawiki.org).*
  * verify_mbox.py - *Verifies that an MBOX file contains the messages of another.*
  * replace_templates.py - *pywikibot script for replacing template usages throughout the WMSE wiki.*
  * wikimania_program_list.py - *generate wikitext for program list used for Wikimania 2019.*
* disk-space-check - *Bash script for checking disk space remaining on a server. Sends email notification if space is running low.*
* fortnox.user.js - *Greasemonkey script for displaying project names in Fortnox.*
* phabricator.user.js - *Convenience script for Phabricator. Adds link to unread notifications in the top bar.*
* phabricator-compact-workboard.user.css - *Stylus CSS for removing the side menu in Phabricator workboards.*
* phabricator-floating-top-bar.user.css - *Stylus CSS for floating top bar in Phabricator.*
* google-flip-portrait.user.css - *Stylus CSS for flipping a portrait in google services.*

When adding a script, also add it to this list with a short description.
