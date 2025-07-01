# 🍲 Feast Mode: A Django Recipe Blog & Community Platform 📝

<p align="center">
  <img src="Site_Grupo15/projectIWGD/recipe/static/recipe/img/hero_banner.jpg" alt="Feast Mode Project Banner" width="100%" height="230px">
</p>

<p align="center">
    <!-- Project Links -->
    <a href="https://github.com/Silvestre17/Django-Recipe-Blog-FeastMode"><img src="https://img.shields.io/badge/Project_Repo-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repo"></a>
</p>

## 📝 Description

<p align="center">
    <!-- Logo -->
    <img src="Site_Grupo15/projectIWGD/recipe/static/recipe/img/logo_site.png" alt="Feast Mode Logo" width="200px" height="200px">
</p>

**Feast Mode** is a robust and feature-rich recipe blog and community platform built entirely on the **Django** framework. The website allows users to register, share their own culinary creations, and interact with a community of food lovers by commenting and rating recipes. It is designed to be scalable, secure, and user-friendly.

<p align="center">
    <img src="https://img.shields.io/badge/Project_Type-Recipe_Blog-FF6347?style=for-the-badge" alt="Project Type">
    <img src="https://img.shields.io/badge/Framework-Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Framework">
    <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Language">
</p>


## ✨ Objective

The primary goal of this project was to model and program a complete web application to manage a user community centered around recipes. This involved:
*   Designing a structured and scalable database schema for users, recipes, and interactions.
*   Implementing full **CRUD** (Create, Read, Update, Delete) functionality for recipes.
*   Building a secure user authentication and profile management system.
*   Creating an intuitive and visually appealing user interface.

## 🎓 Project Context

This project was developed for the **Interfaces Web para A Gestão de Dados (IWAGD)** (*Web Interfaces for Data Management*) course, as part of the 3rd year of the **[Licenciatura em Ciência de Dados](https://www.iscte-iul.pt/degree/code/0322/bachelor-degree-in-data-science)** (*Bachelor Degree in Data Science*) at **ISCTE-IUL**, during the 2023/2024 academic year (1st semester).

## 🛠️ Technologies Used

The application was built on the Django framework, integrating various frontend and backend technologies to create a modern web experience.

#### Backend
<p align="center">
    <a href="https://www.djangoproject.com/">
        <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
</p>

#### Frontend
<p align="center">
    <a href="https://getbootstrap.com/">
        <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
    </a>
    <a href="https://jquery.com/">
        <img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white" alt="jQuery" />
    </a>
    <a href="https://github.com/michalsnik/aos">
        <img src="https://img.shields.io/badge/AOS-Animate_On_Scroll-2C3E50?style=for-the-badge" alt="Animate On Scroll" />
    </a>
</p>

#### Database & Assets
<p align="center">
    <a href="https://www.sqlite.org/index.html">
        <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
    </a>
    <a href="https://pillow.readthedocs.io/en/stable/">
        <img src="https://img.shields.io/badge/Pillow-9B59B6?style=for-the-badge&logo=python&logoColor=white" alt="Pillow" />
    </a>
    <a href="https://fontawesome.com/">
        <img src="https://img.shields.io/badge/Font_Awesome-528DD7?style=for-the-badge&logo=fontawesome&logoColor=white" alt="Font Awesome" />
    </a>
</p>

---

## 🚀 Key Features & Project Breakdown

### 👤 User & Authentication System
*   **Secure Registration & Login:** Users can create an account and log in securely.
*   **User Profiles:** Authenticated users have a personal profile page where they can view their submitted recipes, comments, and ratings.
*   **Profile Customization:** Users can upload/change their profile picture and add a personal description.

### 🍲 Recipe Management (CRUD)
*   **Submit & Edit Recipes:** Logged-in users can submit new recipes, including ingredients, preparation steps, and tags. They can also edit or delete their own submissions.
*   **Detailed Recipe View:** Each recipe has a dedicated page with a detailed description, user comments, and an average rating.

### 💬 Community Interaction
*   **Recipe Ratings:** Users can rate a recipe on a scale of 1-5 stars.
*   **Commenting System:** Users can leave comments on recipes to share their thoughts and feedback.

### ⚙️ Advanced Functionality & Usability
*   **Dynamic Ingredient Dosage (JavaScript):** An innovative feature that automatically calculates ingredient quantities based on the number of servings the user selects.
*   **Filtering & Pagination:** The main recipe page includes a robust filtering system (by title, category, etc.) and pagination to handle a large number of recipes efficiently.
*   **User-Friendly Forms:** Features like password preview on the registration form improve the user experience.
*   **Admin Panel:** Utilizes the built-in Django Admin interface for comprehensive site management (users, recipes, comments).
*   **Custom Error Pages:** A custom-designed `404 Not Found` page maintains visual consistency throughout the site.

## 🚀 How to Run the Project Locally

To run this application on your local machine, follow these steps:

1.  **Prerequisites:**
    *   Ensure you have **Python 3.x** and **Git** installed.

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Silvestre17/IWAGD_FeastMode_RecipesWebsite.git
    cd IWAGD_FeastMode_RecipesWebsite
    ```

3.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    *   This project uses a `requirements.txt` file to manage its dependencies.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If a `requirements.txt` file is not present, you will need to install Django and other packages like `django-bootstrap-v5` and `Pillow` manually.)*

5.  **Run Database Migrations:**
    *   This will create the SQLite database and the necessary tables.
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (for Admin Access):**
    ```bash
    python manage.py createsuperuser
    ```
    *   Follow the prompts to create an administrator account.

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    *   The website will be available at `http://127.0.0.1:8000/`. You can access the admin panel at `/admin`.

## 👥 Team Members (Group 15)

*   **André Silvestre** (Nº104532)
*   **Margarida Pereira** (Nº105877)
*   **Umeima Mahomed** (Nº99239)

## 🇵🇹 Note

This project was developed using Portuguese from Portugal 🇵🇹.