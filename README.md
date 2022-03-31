# Akira_Project
 Akira Project is an Course Management System

### To make me live you need to follow the below instructions,
1. [Install Stabled Python](https://www.python.org/downloads/windows/)
2. Install the virtualenv package <code> pip install virtualenv </code>
3. Create the virtual environment <code> virtualenv venv </code>
4. Activate the virtual environment <code> venv\Scripts\activate </code>
> From now on, If you install any python packages that will be installed in this virtual environment only (On activate).
> To deactive the virtual environemnt use can type the below command or else you can continue with the next instruction [5].
> Deactivate the virtual environment <code> deactivate </code>
5. Now install Django (stabled version) on your machine <code> python -m pip install Django </code>
5. My requirements <code> python -m pip install -r requirements.txt </code>
6. For packaging up your model changes into individual migration files <code> python manage.py makemigrations </code>
7. For applying those to your satabase <code> py manage.py migrate </code>
8. To start my server <code> python manage.py runserver </code>
9. To view on browser http://127.0.0.1:8000/ [Local Host Address]

### API
1. Login: http://127.0.0.1:8000/api/login/
2. Register: http://127.0.0.1:8000/api/register/
3. Get all courses: http://127.0.0.1:8000/api/allCourses/ [GET]
4. Create a course: http://127.0.0.1:8000/api/createCourse/ [POST]
5. View each course by ID (UUID): http://127.0.0.1:8000/api/viewCourse/<INSERT_COURSE_UUID>/ [GET]
   > E.g: http://127.0.0.1:8000/api/viewCourse/16b273b8-4cad-4508-8159-d880ce52c7c2/
6. Update a course: http://127.0.0.1:8000/api/updateCourse/<INSERT_COURSE_UUID>/ [POST]
7. Delete a course: http://127.0.0.1:8000/api/deleteCourse/<INSERT_COURSE_UUID>/ [GET]