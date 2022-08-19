# Time Tracking (Sample Django Project)
This project presents a RESTful Time Tracking API with support for multiple users and projects. It is implemented using Django and Django Rest Framework!

## Entities (Models)
There are three main entities in this project: **Users**, **Projects**, and **TimeLogs**. The **User** entity is contrib.auth's [User](https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#user-model) model. 

### Projects
Projects are entities that act as categories in time tracking. 

In short, Projects...
- ... have a NOT NULL TEXT `title`
- ... have a NOT NULL VARCHAR(250) `slug` which can change arbitrarily
- ... are accessible by one or more users through a **Many-to-Many** relationship.

### TimeLogs
TimeLogs are the main entity of the time tracking project.

In short, TimeLogs...
- ... have a NOT NULL UNSIGNED BIG INTEGER `project_id` referencing id on projects
- ... have a NOT NULL UNSIGNED BIG INTEGER `user_id` referencing id on users
- ... have a NULL DATEIMTE `start_at` marking the start of a time period
- ... have a NULL DATEIMTE `finish_at` marking the end of a time period
- ... have a NULL MEDIUMINT `duration` marking the duration of time log in **seconds** (as the smallest accuracy of time logs)

Timelogs also have a *computed* **status** value which is:
- A Timelog with both `start_at` and `duration` set to NULL is considered **INVALID**
- A Timelog with NOT NULL `duration` is considered **FINISHED**
- A Timelog with NULL `duration` and NOT NULL `start_at` and NOT NULL `finish_at` is considered **FINISHED**
- A Timelog with NULL `duration` and NULL `finish_at` is considered **ONGOING**

## Endpoints
| Method | Endpoint             | Success Status |
| ------ | -------------------- | -------------- |
| GET    | /api/v1/projects     | 200            |
| POST   | /api/v1/projects     | 200            |
| GET    | /api/v1/projects/:id | 200            |
| PUT    | /api/v1/projects/:id | 204            |
| DELETE | /api/v1/projects/:id | 204            |
| GET    | /api/v1/timelogs     | 200            |
| POST   | /api/v1/timelogs     | 200            |
| GET    | /api/v1/timelogs/:id | 200            |
| PUT    | /api/v1/timelogs/:id | 204            |
| DELETE | /api/v1/timelogs/:id | 204            |
