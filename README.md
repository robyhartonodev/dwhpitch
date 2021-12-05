# DWH - Pitch

This repository contains the pitch(es) for the Datenwarehouse module.

# How to run 

- Install ``docker`` and ``docker-compose``
- Install ``python`` 3.9+ and ``pip``. Then run ``pip install -r requirements.txt``
- Or install ``conda`` and create a new virtual environment. Then run ``pip install -r requirements.txt``
- Create ``.env`` file based on ``.env.example`` file and adjust the variables inside the file.
- Run ``docker-compose up`` to start the database and splash service.
- Run ``python manage.py migrate`` to run the migrations.
- Run ``scrapy crawl <spider_name>`` inside the scrapy project (``scrapper``) accordingly using scheduling service e.g. CronJob.

# Directory structure

- ``html`` - where the raw html data are being stored.
- ``scrapper`` - is a scrappy project for web scrapping process.
- ``immobilien`` - is a django startproject application. Where models and migrations being defined.

# Why Django?

- Admin panel - Django has an admin panel that could be used to browse the stored data and create dummy data.
- ORM - Django ORM makes it safe to do CRUD operations and easier to maintain the database through its migrations system.
- Python based - Python is mostly the go-to language for data processing.