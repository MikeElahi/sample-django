# Time Tracking - Sample Django Project
[![Build](https://github.com/WiGeeky/sample-django/actions/workflows/tests.yml/badge.svg)](https://github.com/WiGeeky/sample-django/actions/workflows/tests.yml)
[![GitHub license](https://img.shields.io/github/license/WiGeeky/sample-django)](https://github.com/WiGeeky/sample-django/blob/main/LICENSE)

This project presents a RESTful Time Tracking API with support for multiple users and projects. It is implemented using Django and Django Rest Framework!

## Setup
This project uses Django with Django Rest Framework, it was written in Python 3.8 but is compabtible with Python 3.9 as well:
```shell
git clone https://github.com/WiGeeky/sample-django.git
cd sample-django
python3 -m venv venv 
./venv/bin/activate
python -m pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
```
## REST-ful API
Navigate to [127.0.0.1:8000/api/v1](http://127.0.0.1:8000/api/v1/) for a DRF-generated document of the APIs:
![image](https://user-images.githubusercontent.com/21097871/185767198-0b8b07f2-2433-4c13-9eac-d05253858494.png)


> Note: the `/api/v1/users` path is only available during debugging as this app isn't supposed to provide an interface for users.

## Entities
There are three main entities in this project: **Users**, **Projects**, and **TimeLogs**. The **User** entity is contrib.auth's [User](https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#user-model) model. 

### Projects
Projects are entities that act as categories in time tracking. See the schema below: 
```sql
CREATE TABLE "time_tracker_project" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "title" text NOT NULL, "slug" varchar(50) NOT NULL
);
CREATE TABLE "time_tracker_project_users" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "project_id" bigint NOT NULL REFERENCES "time_tracker_project" ("id") DEFERRABLE INITIALLY DEFERRED,
  "user_id" integer NOT NULL REFERENCES 
  "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
```

### TimeLogs
TimeLogs are the main entity of the time tracking project.
```sql
CREATE TABLE "time_tracker_timelog" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "start_at" datetime NULL, "finish_at" datetime NULL,
  "duration" integer NULL, "project_id" bigint NOT NULL REFERENCES "time_tracker_project" ("id") DEFERRABLE INITIALLY DEFERRED,
  "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
```

Timelogs also have a *computed* **status** value which is:
- A Timelog with both `start_at` and `duration` set to null is considered **INVALID**
- A Timelog with NOT NULL `duration` is considered **FINISHED**
- A Timelog with NULL `duration` and NOT NULL `start_at` and NOT NULL `finish_at` is considered **FINISHED**
- A Timelog with NULL `duration` and NULL `finish_at` is considered **ONGOING**
