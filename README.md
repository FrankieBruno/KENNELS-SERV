# Kennel Server

## Prerequisites

Before you begin, make sure you have the following installed on your system:

* Python (version 3.9 or later)
* pip (Python package manager)

## Setup

The first thing to do is to clone the repository:

```sh
    git https://github.com/FrankieBruno/kennel-server.git
    cd kennel-server
```

Create a virtual environment:

```sh
    python3 -m venv venv
```

Activate the virtual environment:

* For Windows:
```sh
    venv\Scripts\activate
```
* For macOS/Linux:
```sh
    source venv/bin/activate
```

Then install the dependencies:
```sh
    pip install -r requirements.txt
```

Perform database migrations:
```sh
    python3 manage.py migrate
```

## Configuration

Create a new file named .env in the project directory.
Open the .env file and add the following configuration variables:
```sh
    SECRET_KEY=<your-secret-key>
    DEBUG=<True-or-False>
    DATABASE_URL=<your-database-url>
```
** Replace <your-secret-key> with a secure secret key, <True-or-False> with either True or False depending on whether you want to run the server in debug mode, and <your-database-url> with the URL of your database.

** If you don't know something, keep it empty


## Installing SQL or SQLite files

Place your SQL or SQLite file in a directory within your Django project. You can create a directory called fixtures in your app directory and put the file there.
* For example: 'kennel-server/fixtures/kennel.sql' or 'kennel-server/fixtures/kennelsqlite3'.

Run the following command to load the data from the fixture file:
```sh
    python manage.py loaddata kennel
```

## Start the Server

To start the Django server, run the following command:
```sh
    python3 manage.py runserver
```
** The server should now be running locally at http://localhost:8000/. You can access it using your web browser.

## Additional Notes

If you need to create a superuser account for administrative access, use the following command:
```sh
    python3 manage.py createsuperuser
```
Follow the prompts to enter the necessary details.
** Remember to keep your secret key and sensitive information secure. Do not commit them to version control.


