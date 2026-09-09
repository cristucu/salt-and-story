# Salt & Story

Salt & Story is a Django culinary recipe application developed as the final project for a Python/Django course.

The application allows authenticated users to create and manage their own recipes, while recipes remain publicly available to visitors.

## Features

- User authentication
- Custom Django user model
- Public recipe browsing
- Recipe creation
- Recipe editing
- Recipe deletion
- Recipe ownership and access control
- Alphabetical recipe sorting
- Latest recipes sorting
- Responsive user interface
- Automated test suite
- Automated CI checks with GitHub Actions

## Recipe Fields

Each recipe contains:

- Title
- Description
- Ingredients
- Instructions
- Cooking time
- Creation date
- Last update date
- Author

## Pages

- `/` — Homepage
- `/recipes/` — Recipes sorted alphabetically
- `/recipes/latest/` — Recipes sorted by creation date
- `/recipes/<id>/` — Recipe detail
- `/recipes/add/` — Create recipe
- `/recipes/<id>/edit/` — Edit recipe
- `/recipes/<id>/delete/` — Delete recipe
- `/login/` — Login
- `/logout/` — Logout

## Technologies

- Python 3.12
- Django 5.2
- SQLite
- HTML
- CSS
- Ruff
- GitHub Actions


## Installation

Clone the repository:

```bash
git clone git@github.com:cristucu/salt-and-story.git
cd salt-and-story
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```
Create a superuser for admin access:

```bash
python manage.py createsuperuser
```
Run the development server:

```bash
python manage.py runserver
``` 
Open your web browser and navigate to `http://127.0.0.1:8000/`

## Tests

Run the automated test suite:

```bash
python manage.py test
``` 
## Code Quality

Run Ruff:

```bash
ruff check .
```

Run Django system checks:

```bash
python manage.py check
```

GitHub Actions automatically runs:

- Ruff lint checks
- Django system checks
- Django tests

on pull requests targeting `main` and on pushes to `main`.

## Project Documentation

Additional project documentation is available in:

- `docs/PROJECT_V1.md`
- `docs/ARCHITECTURE_V1.md`

## Future Development

Possible V2 improvements include:

- Recipe categories
- Recipe images
- Comments
- Favorites
- Ratings
- Collections
- Stories and culinary blog content
- PostgreSQL
- Production deployment
- Custom domain integration

The domain `saltandstory.ro` has already been reserved for future deployment.


