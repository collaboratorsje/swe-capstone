# Database Creation and Population

Python script to create database tables, populate basic data(user and test data later to come), and optionally recreate the database file

## Files
### TableSetup.py
```
usage: TableSetup.py [-h] [--recreate] [--createtables] [--populatebase]

options:
  -h, --help          show this help message and exit
  --recreate          Recreate database.db file, create tables, and repopulate with default data.
  --createtables, -c  Creates Tables.
  --populatebase      Populates base tables with no records added.
```
Example: Full refresh, creates a backup of the database.db file and makes a new file, tables and adds data

    python TableSetup.py --recreate --createtables --populatebase

Example: Create Tables and Populate data with no database.db file

    python TableSetup.py --createtables --populatebase

### CreateTables.sql

SQL commands for creating each table on the database. Used in the python script.