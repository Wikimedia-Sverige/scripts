# Fortnox_huvudbok_processing

Scripts and datafiles to crunch the *Huvudbok* export (in .txt format) from
Fortnox into a manageable tsv format.

## Running
To run the script execute the command

    $ ./huvudbok.py path-to-data-file

For flags, see command line help (`$ ./huvudbok.py --help`).
The `-f` flag in particular may be of interest.

## Files
*   `huvudbok.py`: contains the main processing code
*   `projects_YEAR.json`: contain mapping tables for *kostnadsställe* (project ids)
to project names.
