# Akira_Project
Akira Project is an Course Management System

## To make me live you need to follow the below instructions,
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

## API Documentation
* Display all courses
  * GET - ``` http://127.0.0.1:8000/api/courses/ ```
* Delete all courses
  * DELETE - ``` http://127.0.0.1:8000/api/courses/ ```
* Delete a course by id
   * DELETE - ``` http://127.0.0.1:8000/api/courses/<course_id>/ ```
* Create a course 
  * POST - ``` http://127.0.0.1:8000/api/courses/ ```
      ### Headers
         * Name: Content-Type
         * Value: application/json
      ### Body
      ```JSON
      {
         "name": "Technical Skilling",
         "code": "19CS1234",
         "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
      }
      ```
* Retrieve a single course by id
   * GET - ``` http://127.0.0.1:8000/api/courses/<course_id>/ ```
* Update a course by id
   * PUT - ``` http://127.0.0.1:8000/api/courses/<course_id>/ ```
      ### Headers
         * Name: Content-Type
         * Value: application/json
      ### Body
      ```JSON
      {
         "name": "Technical Skilling-2",
         "code": "19CS4321",
         "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
      }
      ```
* Bulk upload faculty 
  * POST - ``` http://127.0.0.1:8000/api/bulk_upload_faculty/ ```
      ### Headers
         * Name: Content-Type
         * Value: multipart/form-data
      ### Body
      ```Form [Name - Value]
      faculty_file - <Upload file>
      ```
      ![Upload the task submission to a course](https://raw.githubusercontent.com/4akhilkumar/course_management_system_api/main/API%20Documentation%20files/bulk_upload.jpg?token=GHSAT0AAAAAABTDLBARJD645AS3QBPSKDZYYSPXWZA)

* Bulk upload students 
  * POST - ``` http://127.0.0.1:8000/api/bulk_upload_students/ ```
      ### Headers
         * Name: Content-Type
         * Value: multipart/form-data
      ### Body
      ```Form [Name - Value]
      student_file - <Upload file>
      ```
      ![Upload the task submission to a course](https://raw.githubusercontent.com/4akhilkumar/course_management_system_api/main/API%20Documentation%20files/bulk_upload(2).jpg?token=GHSAT0AAAAAABTDLBARH2HYG43C7S5XTZGOYSPX2AQ)

* Upload the task submission to a course
   * POST - ``` http://127.0.0.1:8000/api/course_task_submission/ ```
      ### Headers
         * Name: Content-Type
         * Value: multipart/form-data
      ### Body
      ```Form [Name - Value]
      task - <TASK_ID>
      * task - bc6cd7b0-9ce9-4fb5-bd4c-e38444b502ec
      file - <Upload file>
      user_student - <USER_STUDENT_ID>
      * user_student - 4 
      ```
      ![Upload the task submission to a course](https://raw.githubusercontent.com/4akhilkumar/course_management_system_api/main/API%20Documentation%20files/Upload%20the%20task%20submission%20to%20a%20course.jpg?token=GHSAT0AAAAAABTDLBAQ323QCLN46J4ONLVOYSPWQWA)

* Grade the task submission to a course
   * POST - ``` http://127.0.0.1:8000/api/evaluate_submission/ ```
      ### Headers
         * Name: Content-Type
         * Value: application/json
      ### Body
      ```
      {
         "task_submission_id": "f94bd04a-cca6-4195-b884-c1dfab7fca17",
         "user_faculty": 3,
         "score": 100,
         "feedback": "Good work"
      }
      ```

## Sample data in JSON format

```JSON
[
   {
      "id": "43f8de73-d9da-4ad1-ac93-cc4804d83646",
      "name": "Technical Skilling",
      "code": "19CS1234",
      "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
   },
   {
      "id": "29b3ceb2-ac20-4369-a6ed-9054d14f3645",
      "name": "Enterprise Programming",
      "code": "19CS5678",
      "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
   },
   {
      "id": "c9f9f8f3-d9da-4ad1-ac93-cc4804d83646",
      "name": "Data Science",
      "code": "19CS9876",
      "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
   },
   {
      "id": "c9f9f8f3-d9da-4ad1-ac93-cc4804d83646",
      "name": "Cloud Computing",
      "code": "19CS9876",
      "description": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content."
   }
]
```
