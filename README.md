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

# Digital Ocean - Droplet

The application is deployed using digital ocean $10 monthly droplet with 2GB RAM, 1 CPU and 50 GB SSD disk.

# Automation

The automation of the ETL processes is done with the help of the cron jobs. Due to lack of ressource. The job is only being run once. The job will run a bash script with parameter of the state's e.g. Hamburg, Berlin, Hessen, etc. name. The following is the content of the cron job inside the machine, which could be edited with command `crontab -e`

```bash
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
0 6 * * * /home/dwhpitch/dwh/immonet_script.sh schleswig-holstein >> /home/dwhpitch/dwh/log/immonet-schleswig-holstein.log 2>&1
10 6 * * * /home/dwhpitch/dwh/immonet_script.sh hamburg >> /home/dwhpitch/dwh/log/immonet-hamburg.log 2>&1
20 6 * * * /home/dwhpitch/dwh/immonet_script.sh niedersachsen >> /home/dwhpitch/dwh/log/immonet-niedersachsen.log 2>&1
30 6 * * * /home/dwhpitch/dwh/immonet_script.sh bremen >> /home/dwhpitch/dwh/log/immonet-bremen.log 2>&1
40 6 * * * /home/dwhpitch/dwh/immonet_script.sh nordrhein-westfalen >> /home/dwhpitch/dwh/log/immonet-nordrhein-westfalen.log 2>&1
50 6 * * * /home/dwhpitch/dwh/immonet_script.sh hessen >> /home/dwhpitch/dwh/log/immonet-hessen.log 2>&1
0 7 * * * /home/dwhpitch/dwh/immonet_script.sh rheinland-pfalz >> /home/dwhpitch/dwh/log/immonet-rheinland-pfalz.log 2>&1
10 7 * * * /home/dwhpitch/dwh/immonet_script.sh baden-wuerttemberg >> /home/dwhpitch/dwh/log/immonet-baden-wuerttemberg.log 2>&1
20 7 * * * /home/dwhpitch/dwh/immonet_script.sh bayern >> /home/dwhpitch/dwh/log/immonet-bayern.log 2>&1
30 7 * * * /home/dwhpitch/dwh/immonet_script.sh saarland >> /home/dwhpitch/dwh/log/immonet-saarland.log 2>&1
40 7 * * * /home/dwhpitch/dwh/immonet_script.sh berlin >> /home/dwhpitch/dwh/log/immonet-berlin.log 2>&1
50 7 * * * /home/dwhpitch/dwh/immonet_script.sh brandenburg >> /home/dwhpitch/dwh/log/immonet-brandenburg.log 2>&1
0 8 * * * /home/dwhpitch/dwh/immonet_script.sh mecklenburg-vorpommern >> /home/dwhpitch/dwh/log/immonet-mecklenburg-vorpommern.log 2>&1
10 8 * * * /home/dwhpitch/dwh/immonet_script.sh sachsen >> /home/dwhpitch/dwh/log/immonet-sachsen.log 2>&1
20 8 * * * /home/dwhpitch/dwh/immonet_script.sh sachsen-anhalt >> /home/dwhpitch/dwh/log/immonet-sachsen-anhalt.log 2>&1
30 8 * * * /home/dwhpitch/dwh/immonet_script.sh thueringen >> /home/dwhpitch/dwh/log/immonet-thueringen.log 2>&1

0 6 * * * /home/dwhpitch/dwh/immowelt_script.sh schleswig-holstein >> /home/dwhpitch/dwh/log/immowelt-schleswig-holstein.log 2>&1
10 6 * * * /home/dwhpitch/dwh/immowelt_script.sh hamburg >> /home/dwhpitch/dwh/log/immowelt-hamburg.log 2>&1
20 6 * * * /home/dwhpitch/dwh/immowelt_script.sh niedersachsen >> /home/dwhpitch/dwh/log/immowelt-niedersachsen.log 2>&1
30 6 * * * /home/dwhpitch/dwh/immowelt_script.sh bremen >> /home/dwhpitch/dwh/log/immowelt-bremen.log 2>&1
40 6 * * * /home/dwhpitch/dwh/immowelt_script.sh nordrhein-westfalen >> /home/dwhpitch/dwh/log/immowelt-nordrhein-westfalen.log 2>&1
50 6 * * * /home/dwhpitch/dwh/immowelt_script.sh hessen >> /home/dwhpitch/dwh/log/immowelt-hessen.log 2>&1
0 7 * * * /home/dwhpitch/dwh/immowelt_script.sh rheinland-pfalz >> /home/dwhpitch/dwh/log/immowelt-rheinland-pfalz.log 2>&1
10 7 * * * /home/dwhpitch/dwh/immowelt_script.sh baden-wuerttemberg >> /home/dwhpitch/dwh/log/immowelt-baden-wuerttemberg.log 2>&1
20 7 * * * /home/dwhpitch/dwh/immowelt_script.sh bayern >> /home/dwhpitch/dwh/log/immowelt-bayern.log 2>&1
30 7 * * * /home/dwhpitch/dwh/immowelt_script.sh saarland >> /home/dwhpitch/dwh/log/immowelt-saarland.log 2>&1
40 7 * * * /home/dwhpitch/dwh/immowelt_script.sh berlin >> /home/dwhpitch/dwh/log/immowelt-berlin.log 2>&1
50 7 * * * /home/dwhpitch/dwh/immowelt_script.sh brandenburg >> /home/dwhpitch/dwh/log/immowelt-brandenburg.log 2>&1
0 8 * * * /home/dwhpitch/dwh/immowelt_script.sh mecklenburg-vorpommern >> /home/dwhpitch/dwh/log/immowelt-mecklenburg-vorpommern.log 2>&1
10 8 * * * /home/dwhpitch/dwh/immowelt_script.sh sachsen >> /home/dwhpitch/dwh/log/immowelt-sachsen.log 2>&1
20 8 * * * /home/dwhpitch/dwh/immowelt_script.sh sachsen-anhalt >> /home/dwhpitch/dwh/log/immowelt-sachsen-anhalt.log 2>&1
30 8 * * * /home/dwhpitch/dwh/immowelt_script.sh thueringen >> /home/dwhpitch/dwh/log/immowelt-thueringen.log 2>&1
```

# Important commands

## Dump postgres immobilien tables

This command will dump all relevant tables. (with prefix immobilien_)

``docker exec <container_name> pg_dump -p 5432 --username=<username> -t 'immobilien_*' dwh_database > dwhpitch_immobilien_dump.sql``