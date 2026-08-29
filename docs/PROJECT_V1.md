# Salt & Story — Project V1

## Project Goal

Salt & Story is a Django web application for publishing and browsing culinary recipes.

Version 1 is developed as the final project for a Python/Django course and focuses on the core functionality required by the assignment.

The project is intentionally kept small enough for the course, while being structured so that it can later evolve into a real culinary website.

---

## Course Requirements

V1 must include:

* user authentication;
* at least one Django model;
* a one-to-many relationship between User and Recipe;
* recipe creation;
* recipe editing;
* recipe deletion;
* public recipe viewing;
* one page that lists recipes alphabetically;
* one page that lists recipes by creation date;
* at least five automated tests;
* a `README.md` file;
* a `requirements.txt` file.

---

## V1 Features

Salt & Story V1 includes:

* login;
* logout;
* custom Django user model;
* recipe creation;
* recipe detail page;
* recipe editing;
* recipe deletion;
* recipe ownership;
* alphabetical recipe listing;
* latest recipe listing;
* homepage with latest recipes;
* recipe cards;
* basic responsive styling;
* automated tests;
* SQLite database;
* project documentation.

---

## Recipe Content

A recipe contains:

* title;
* description;
* ingredients;
* preparation instructions;
* cooking time;
* creation date;
* last update date;
* author.

The `ingredients` and `instructions` fields extend the minimum project requirements while keeping the model simple and making each recipe useful.

---

## User Permissions

Visitors can:

* access the homepage;
* browse recipes;
* open recipe detail pages.

Authenticated users can additionally:

* create recipes.

Recipe authors can additionally:

* edit their own recipes;
* delete their own recipes.

Users cannot edit or delete recipes created by another user.

---

## Main Pages

* `/` — homepage
* `/recipes/` — all recipes sorted alphabetically
* `/recipes/latest/` — recipes sorted by creation date
* `/recipe/add/` — add recipe
* `/recipe/<id>/` — recipe details
* `/recipe/<id>/edit/` — edit recipe
* `/recipe/<id>/delete/` — delete recipe
* `/login/` — login
* `/logout/` — logout

---

## V1 Homepage

The homepage will contain:

1. navigation bar;
2. culinary hero section;
3. latest recipes;
4. link to all recipes;
5. footer.

The homepage is separate from the two recipe listing pages required by the assignment.

---

## Out of Scope for V1

The following features are intentionally postponed until V2:

* Stories;
* recipe categories;
* comments;
* ratings;
* favorites;
* collections;
* public user profiles;
* public user registration;
* advanced search;
* recipe image uploads;
* REST API;
* PostgreSQL;
* Docker;
* CI/CD;
* production deployment;
* domain configuration;
* cloud media storage.

The domain `saltandstory.ro` is already reserved, but deployment is not part of V1.

---

## V1 Principle

> Build only what the final course project needs, while avoiding decisions that would make future development unnecessarily difficult.

Salt & Story V1 should be simple enough to understand and explain completely, but structured well enough to become the foundation of a real application after the course.

