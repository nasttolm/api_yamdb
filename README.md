# API YaMDb

Yandex educational project. Python Developer course (backend).

### Description
The YaMDb project collects user reviews on titles. The titles are divided into categories: "Books", "Films", "Music". The list of categories can be expanded by the administrator.

The works themselves are not stored in YaMDb, you cannot watch a movie or listen to music here. In each category there are works: books, movies or music.

A work can be assigned a genre from the preset list. Only the administrator can create new genres.

Grateful or outraged users leave text reviews for the works and give the work a rating in the range from one to ten; an average rating of the work is formed from user ratings — a rating. The user can leave only one review for one work.
A service for collecting user reviews of various works, the ability to read reviews related to a specific work, as well as write and read comments on a separate review.

### Technologies 
- Python 3.9
- Django 3.2
- DRF 3.12.4

### Running a project
- Clone the repository and go to it on the command line:

```git clone git@github.com:nasttolm/api_yamdb_.git```

- Install and activate the virtual environment

Windows
```python -m venv venv```
```source venv/Scripts/activate```

Linux
```python3 -m venv env```
```source env/bin/activate```

- Install dependencies from requirements.txt file:

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```

- Run migrations:

```python manage.py migrate```

- In the folder with the manage.py file, run the command:

```python manage.py runserver```


### Request examples
```
User registration and token issuance
Registering a new user
POST: /api/v1/auth/signup/
Request text:
{
    "email": "user@example.com",
    "username": "string"
}
Response text:
{
    "email": "string",
    "username": "string"
}

Getting a JWT token
/api/v1/auth/token/
Request text:
{
    "username": "string",
    "confirmation_code": "string"
}
Response text:
{
    "token": "string"
}

```
### Authors
- Anastasia Tolmacheva
- Alexander Bodnar
- Said Amirov
