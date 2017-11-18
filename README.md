**Game of Thrones Scrape v2**

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/cjacobs27/gotscrapev2/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/cjacobs27/gotscrapev2/?branch=master)

[![Build Status](https://travis-ci.org/cjacobs27/gotscrapev2.svg?branch=master)](https://travis-ci.org/cjacobs27/gotscrapev2)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/32285230bd5743cf92657043245634aa)](https://www.codacy.com/app/cjacobs27/gotscrapev2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cjacobs27/gotscrapev2&amp;utm_campaign=Badge_Grade)

This is still a work in progress and only runs on your local machine at the moment.

If you're happy to install the required packages, and Django, open command line in unzipped gotscrapev2 folder:

`pip install -r requirements.txt`

In the same folder, create a file called:

`db.sqlite3`

Then in command line:

`python manage.py runserver`

In your browser, go to:

`http://localhost:8000/gotsv2/update`

To populate the database for the first time.

Once this is done, at any time you can either go to gotsv2/update in your browser
to update the database again, or to see the info in it, go to:

`http://localhost:8000/gotsv2/`

Here you'll see the list of characters with links to their Wikipedia pages,
along with their gender info.

Here's a guide to what pages do so far:
-

`http://localhost:8000/gotsv2`

View list of names of the Characters that are already in the database: names are displayed
as links to the URLs of character pages. Gender is also listed & more info will
be available in the future.

`http://localhost:8000/gotsv2/update`

Updates the database with freshly scraped data - only adds records which are new to
the database, eg. if a new Character Page is published, it will
bring the relevant info into the database. At the moment each record is printed to the terminal
to show whether it is 'already in there' or 'just added'.

`http://localhost:8000/gotsv2/graph`

Generates and displays a gender split pie chart. More graphs will be
available to choose from soon.

This has been a project to help me learn about automated web scraping,
Django, and SQLite databases.



