\# FastAPI Practical Assessment 2



\## Overview



This repository contains the solutions for \*\*FastAPI Practical Assessment 2\*\*.



The assessment consists of two FastAPI applications using:



\* FastAPI

\* Pydantic

\* SQLModel

\* SQLite

\* Uvicorn

\* REST APIs



Both applications use SQLite databases created through SQLModel and `create\_engine()`.



\---



\# Task 1 – Campus Lost \& Found API



\## Problem Statement



The Campus Lost \& Found API allows students to report and manage lost, found, and returned items on campus.



Each item contains:



\* Title

\* Description

\* Category

\* Location

\* Reported By

\* Status



The allowed status values are:



\* Lost

\* Found

\* Returned



\## Features



\* Create a lost/found item

\* View all items

\* View an item by ID

\* Update an item

\* Delete an item

\* Filter items by status

\* Filter items by category

\* Input validation

\* Proper HTTP error handling



\## API Endpoints



| Method | Endpoint                     | Purpose            |

| ------ | ---------------------------- | ------------------ |

| POST   | `/items`                     | Create item        |

| GET    | `/items`                     | Get all items      |

| GET    | `/items/{item\_id}`           | Get item by ID     |

| PUT    | `/items/{item\_id}`           | Update item        |

| DELETE | `/items/{item\_id}`           | Delete item        |

| GET    | `/items/status/{status}`     | Filter by status   |

| GET    | `/items/category/{category}` | Filter by category |



\## Database



SQLite database:



```text

lost\_found.db

```



SQLModel is used for database models and operations.



\---



\# Task 2 – Campus Event Seat Reservation API



\## Problem Statement



The Campus Event Seat Reservation API manages college events and student seat reservations.



Each event contains:



\* Title

\* Venue

\* Capacity

\* Organizer

\* Status



The allowed event status values are:



\* Open

\* Closed



Students can reserve seats for open events.



\## Features



\* Create an event

\* View all events

\* View event by ID

\* Update an event

\* Delete an event

\* Reserve a seat

\* View event reservations

\* Cancel a reservation

\* Check seat availability

\* Prevent overbooking

\* Prevent reservations for closed events

\* Validate student information and email

\* Proper HTTP error handling



\## API Endpoints



| Method | Endpoint                          | Purpose                 |

| ------ | --------------------------------- | ----------------------- |

| POST   | `/events`                         | Create event            |

| GET    | `/events`                         | Get all events          |

| GET    | `/events/{event\_id}`              | Get event by ID         |

| PUT    | `/events/{event\_id}`              | Update event            |

| DELETE | `/events/{event\_id}`              | Delete event            |

| POST   | `/events/{event\_id}/reserve`      | Create reservation      |

| GET    | `/events/{event\_id}/reservations` | Get reservations        |

| DELETE | `/reservations/{reservation\_id}`  | Cancel reservation      |

| GET    | `/events/{event\_id}/availability` | Check seat availability |



\## Database



SQLite database:



```text

events.db

```



SQLModel is used for Event and Reservation models and database operations.



\---



\# Technologies Used



\* Python

\* FastAPI

\* Pydantic

\* SQLModel

\* SQLite

\* Uvicorn



\---



\# Project Structure



```text

FastAPI-Practical-Assessment-2/

│

├── task1\_lost\_found/

│   ├── main.py

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   └── requirements.txt

│

├── task2\_event\_reservation/

│   ├── main.py

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   └── requirements.txt

│

├── screenshots/

│   ├── task1/

│   └── task2/

│

├── README.md

└── .gitignore

```



\---



\# How to Run Task 1



Open a terminal and navigate to:



```text

task1\_lost\_found

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



Run the application:



```bash

python -m uvicorn main:app --reload

```



Open Swagger UI:



```text

http://127.0.0.1:8000/docs

```



\---



\# How to Run Task 2



Open another terminal and navigate to:



```text

task2\_event\_reservation

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



Run the application:



```bash

python -m uvicorn main:app --reload

```



Open Swagger UI:



```text

http://127.0.0.1:8000/docs

```



\---



\# Validation and Error Handling



The applications use Pydantic validation and FastAPI HTTP exceptions.



Examples include:



\* Empty required fields are rejected.

\* Invalid status values are rejected.

\* Event capacity must be greater than zero.

\* Invalid email addresses are rejected.

\* Non-existing IDs return HTTP 404.

\* Closed events cannot accept reservations.

\* Events cannot be overbooked.



\---



\# Screenshots



Screenshots of the tested API endpoints are available in:



```text

screenshots/task1/

screenshots/task2/

```



These screenshots demonstrate successful API operations and validation/error handling.



\---



\# Database Design



\## Task 1



The `Item` table stores campus lost and found records.



\## Task 2



The `Event` table stores event information.



The `Reservation` table stores student reservations and connects each reservation to an event using `event\_id`.



\---



\# Testing



The APIs were tested using \*\*FastAPI Swagger UI\*\*.



The following operations were tested:



\### Task 1



\* Create item

\* Get all items

\* Get item by ID

\* Update item

\* Delete item

\* Filter by status

\* Filter by category

\* Validation/error handling



\### Task 2



\* Create event

\* Get events

\* Create reservation

\* Get reservations

\* Check availability

\* Cancel reservation

\* Reservation business logic



\---



\# Author



B.Tech CSE – Artificial Intelligence



FastAPI Practical Assessment 2



