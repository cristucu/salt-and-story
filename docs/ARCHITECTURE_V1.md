# Salt & Story — Architecture V1

## 1. Architecture Goals

Salt & Story V1 should be:

* simple;
* easy to understand;
* aligned with standard Django conventions;
* sufficient for the final course requirements;
* easy to extend after the course.

V1 uses Django's standard server-rendered architecture.

No separate frontend framework or REST API is required.

---

## 2. Technology Stack

* Python 3.12
* Django 5.2
* SQLite3
* HTML
* CSS
* Django Templates
* Git
* GitHub

JavaScript may be used for small interface improvements, but V1 does not depend on a JavaScript framework.

---

## 3. Project Structure

```text
salt-and-story/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── recipes/
│   ├── migrations/
│   ├── templates/
│   │   └── recipes/
│   │       ├── recipe_list.html
│   │       ├── recipe_detail.html
│   │       ├── recipe_form.html
│   │       └── recipe_confirm_delete.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   └── registration/
│       └── login.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── docs/
│   ├── PROJECT_V1.md
│   └── ARCHITECTURE_V1.md
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 4. Django Applications

### `config`

Contains the global Django project configuration.

Responsibilities:

* project settings;
* root URL configuration;
* ASGI configuration;
* WSGI configuration.

Application business logic should not be placed here.

---

### `accounts`

Responsible for users and authentication-related functionality.

Salt & Story uses a custom Django User model based on `AbstractUser`.

Conceptually:

```python
class User(AbstractUser):
    pass
```

No additional fields are required in V1.

Using a custom user model from the beginning allows future versions to add fields such as:

* avatar;
* bio;
* display name;
* website.

This avoids replacing Django's default User model after the project already contains data and migrations.

---

### `recipes`

Contains the main application functionality.

Responsibilities:

* Recipe model;
* Recipe form;
* recipe creation;
* recipe editing;
* recipe deletion;
* recipe detail;
* recipe listings;
* recipe sorting;
* recipe ownership validation.

---

## 5. High-Level Architecture

The application follows Django's standard request-response flow:

```text
Browser
   │
   ▼
URL Configuration
   │
   ▼
View
   │
   ├── Form
   │
   ▼
Model
   │
   ▼
SQLite Database
```

The response flow is:

```text
Browser request
      ↓
urls.py
      ↓
view
      ↓
model / database
      ↓
template
      ↓
HTML response
```

---

## 6. Data Model

V1 contains two main entities:

```text
User
Recipe
```

A user can create multiple recipes.

Each recipe belongs to exactly one user.

```text
User
 │
 ├── Recipe
 ├── Recipe
 └── Recipe
```

Relationship:

```text
User 1 ─────────── * Recipe
```

This provides the one-to-many relationship required by the course assignment.

---

## 7. Recipe Model

The Recipe model contains:

```text
Recipe
│
├── id
├── title
├── description
├── ingredients
├── instructions
├── cooking_time
├── created_at
├── updated_at
└── author
```

Recommended Django field types:

```text
title           CharField
description     TextField
ingredients     TextField
instructions    TextField
cooking_time    CharField
created_at      DateTimeField
updated_at      DateTimeField
author          ForeignKey(User)
```

The User relationship should use the configured Django user model.

Conceptually:

```python
author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="recipes",
)
```

---

## 8. Date Handling

Although the assignment describes the creation date as a string and mentions using `datetime` for conversion, Salt & Story stores dates as real date/time values.

Conceptually:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

This provides:

* reliable sorting;
* correct date comparisons;
* automatic creation timestamps;
* automatic update timestamps.

Dates can be formatted as strings when displayed in templates.

Example:

```text
Database:
2026-08-29 18:30:00

Website:
29 August 2026
```

---

## 9. URL Architecture

### Homepage

```text
/
```

Displays:

* navigation bar;
* hero section;
* latest recipes;
* link to all recipes;
* footer.

---

### Alphabetical Recipe List

```text
/recipes/
```

Displays all recipes sorted alphabetically.

Conceptually:

```python
Recipe.objects.order_by("title")
```

---

### Latest Recipes

```text
/recipes/latest/
```

Displays all recipes sorted by creation date, newest first.

Conceptually:

```python
Recipe.objects.order_by("-created_at")
```

---

### Recipe Detail

```text
/recipe/<id>/
```

Displays the complete recipe.

---

### Create Recipe

```text
/recipe/add/
```

Requires authentication.

---

### Edit Recipe

```text
/recipe/<id>/edit/
```

Requires authentication and recipe ownership.

---

### Delete Recipe

```text
/recipe/<id>/delete/
```

Requires authentication and recipe ownership.

---

### Login

```text
/login/
```

---

### Logout

```text
/logout/
```

---

## 10. Named URLs

Templates should never depend on hard-coded URLs.

Instead of:

```html
<a href="/recipe/7/edit/">
```

Django URL names should be used:

```django
{% url 'recipes:edit' recipe.id %}
```

Suggested names:

```text
recipes:list
recipes:latest
recipes:detail
recipes:add
recipes:edit
recipes:delete
```

This allows URL structures to change later without modifying every template.

---

## 11. View Architecture

Function-based Django views are sufficient for V1.

Conceptual views:

```text
home

recipe_list
recipe_latest
recipe_detail

recipe_create
recipe_update
recipe_delete
```

### `home`

Returns the homepage and a limited number of recent recipes.

Conceptually:

```python
Recipe.objects.order_by("-created_at")[:3]
```

### `recipe_list`

Returns all recipes ordered alphabetically.

### `recipe_latest`

Returns all recipes ordered by creation date.

### `recipe_detail`

Returns one Recipe based on its ID.

Invalid IDs should return a 404 response.

### `recipe_create`

Requires an authenticated user.

The logged-in user automatically becomes the Recipe author.

### `recipe_update`

Requires:

* authentication;
* current user to be the Recipe author.

### `recipe_delete`

Requires:

* authentication;
* current user to be the Recipe author.

---

## 12. Authentication

V1 provides:

```text
/login/
/logout/
```

Public registration is not required in V1.

Users needed for development and project evaluation can be created through Django administration.

---

## 13. Authorization and Ownership

Authentication answers:

> Who is the user?

Authorization answers:

> Is the user allowed to perform this action?

V1 permissions:

| Action                       | Visitor | Authenticated User | Recipe Author |
| ---------------------------- | ------: | -----------------: | ------------: |
| View homepage                |     Yes |                Yes |           Yes |
| View recipe list             |     Yes |                Yes |           Yes |
| View recipe detail           |     Yes |                Yes |           Yes |
| Create recipe                |      No |                Yes |           Yes |
| Edit another user's recipe   |      No |                 No |            No |
| Edit own recipe              |      No |                 No |           Yes |
| Delete another user's recipe |      No |                 No |            No |
| Delete own recipe            |      No |                 No |           Yes |

Permissions must be enforced in Django views.

Hiding Edit or Delete buttons in the template is not sufficient protection.

---

## 14. Recipe Cards

Recipe lists and the homepage use reusable recipe cards.

Conceptually:

```text
┌──────────────────────────────┐
│                              │
│ Spaghetti Carbonara          │
│                              │
│ 25 min                       │
│ by Cristian                  │
│                              │
│                 Edit Delete  │
└──────────────────────────────┘
```

The normal card area opens the recipe detail page.

```text
/recipe/<id>/
```

Edit and Delete remain separate actions.

These actions are visible only when:

```text
request.user == recipe.author
```

The implementation should avoid invalid nested interactive HTML.

---

## 15. Template Architecture

All pages extend a shared template:

```text
base.html
```

Conceptual structure:

```text
base.html
│
├── navbar
├── content block
└── footer
```

Child templates:

```text
home.html

recipes/
├── recipe_list.html
├── recipe_detail.html
├── recipe_form.html
└── recipe_confirm_delete.html

registration/
└── login.html
```

Using a shared base template keeps common layout and navigation in one place.

---

## 16. Homepage Architecture

The homepage is separate from the two database listing pages required by the course.

V1 homepage:

```text
Navbar
   ↓
Hero
   ↓
Latest Recipes
   ↓
View All Recipes
   ↓
Footer
```

Only a small number of recent recipes are displayed on the homepage.

The complete alphabetical listing remains available at:

```text
/recipes/
```

The complete date-based listing remains available at:

```text
/recipes/latest/
```

---

## 17. Static Files

V1 uses Django static files for:

* CSS;
* hero background;
* static interface images.

Structure:

```text
static/
├── css/
│   └── style.css
└── images/
```

User-uploaded recipe images are not implemented in V1.

They belong to V2 because they introduce additional media storage considerations.

---

## 18. Database

V1 uses:

```text
SQLite3
```

SQLite is sufficient for:

* local development;
* course evaluation;
* automated testing.

Database schema changes are tracked through Django migrations.

Migration to PostgreSQL belongs to V2.

---

## 19. Testing Strategy

The course requires at least five automated tests.

Salt & Story targets approximately 8–12 meaningful tests.

### Authentication

* valid user can log in;
* anonymous user cannot access recipe creation.

### Recipe Creation

* authenticated user can create a recipe;
* the logged-in user becomes the recipe author.

### Recipe Editing

* author can edit own recipe;
* another user cannot edit it.

### Recipe Deletion

* author can delete own recipe;
* another user cannot delete it.

### Sorting

* alphabetical listing returns recipes in alphabetical order;
* latest listing returns recipes ordered by creation date.

### Public Access

* anonymous visitors can access recipe lists;
* anonymous visitors can access recipe details.

Tests should verify behaviour and project requirements rather than being added only to increase the test count.

---

## 20. GitHub Workflow

Development should not happen directly on `main`.

Workflow:

```text
GitHub Issue
      ↓
Branch
      ↓
Implementation
      ↓
Tests
      ↓
Commit
      ↓
Push
      ↓
Pull Request
      ↓
Review
      ↓
Squash and Merge
      ↓
main
```

Feature branches:

```text
feature/<issue-number>-<description>
```

Documentation branches:

```text
docs/<issue-number>-<description>
```

Bug fix branches:

```text
fix/<issue-number>-<description>
```

Examples:

```text
feature/4-recipe-model
feature/5-homepage
docs/3-v1-architecture
```

---

## 21. V1 Boundary

V1 deliberately contains only the architecture needed for the course project.

```text
              Salt & Story V1

                   User
                    │
                    │ 1
                    │
                    │ *
                  Recipe
                    │
          ┌─────────┼─────────┐
          │         │         │
        CRUD      Sorting    Detail
          │
      Permissions

                Django
                  │
               SQLite
```

The following are intentionally not part of V1:

* Stories;
* categories;
* comments;
* favorites;
* ratings;
* image uploads;
* public user profiles;
* PostgreSQL;
* Docker;
* CI/CD;
* production deployment.

---

## 22. Future Development

After V1 is completed and submitted, Salt & Story can evolve into V2.

V2 will receive a separate architecture document:

```text
ARCHITECTURE_V2.md
```

Possible future functionality:

```text
Recipe
├── Categories
├── Images
├── Comments
└── Favorites

User
├── Profile
├── Favorites
└── Comments

Story
└── Editorial content
```

The future public version may also introduce different user roles:

```text
Normal User
→ interacts with content

Author / Editor
→ publishes recipes

Admin
→ manages the website
```

This allows Salt & Story to remain a curated culinary website rather than an uncontrolled user-generated recipe platform.

---

## 23. Architecture Principle

Salt & Story V1 is designed to demonstrate the core Django concepts required by the course:

* authentication;
* models;
* database relationships;
* CRUD;
* forms;
* permissions;
* sorting;
* templates;
* tests;
* Git workflow.

The project should remain small enough that every architectural decision can be understood and explained.

At the same time, V1 should provide a clean foundation for the future development of `saltandstory.ro`.
