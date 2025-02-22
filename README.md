# FitnessTracker

Django installation/overview


General Documentation:


https://docs.djangoproject.com/en/5.1/ 
Recommended: Take a look at First Steps > (“from Scratch” and “tutorial”)



Installation
https://docs.djangoproject.com/en/5.1/intro/install/ 
Make sure to have python installed (latest version or 3.10+ should be fine)

python -m pip install Django 

check its installed: python -m django --version


Backend
Data base https://docs.djangoproject.com/en/5.1/intro/tutorial02/ 
Note: It comes with SQLite, we could also use a more scalable database like postgreSQL or MySQL

Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

Change your models (in models.py).

Run python manage.py makemigrations to create migrations for those changes

Run python manage.py migrate to apply those changes to the database.

Creating an admin user¶

First we’ll need to create a user who can login to the admin site. Run the following command:

$ python manage.py createsuperuser

Enter your desired username and press enter.

Username: admin

You will then be prompted for your desired email address:

Email address: admin@example.com

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.

Our password: fitness

Password: **********

Password (again): *********

Superuser created successfully.

Front End 

Creating URLs: https://docs.djangoproject.com/en/5.1/intro/tutorial03/ 
