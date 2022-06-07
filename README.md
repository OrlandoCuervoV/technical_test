# Tech test

## Local environment for developers

### Prerequisites

  * Install Python3

### Create a virtual environment to isolate our package dependencies locally

_On Linux:_

  * Create env: ``` python3 -m venv env ```
  * Active env: ``` source env/bin/activate ```

_On Windows:_

  * Create env: ``` python -m venv env ```
  * Active env: ``` cd {env_directory}  .\Scripts\activate ```

### Install Django and Django REST framework into the virtual environment
  
  ``` 
    pip install django

    pip install djangorestframework 
  ```

### Installing dependencies

  ``` 
    cd {project_location}/src/config/
  
    pip install -r requirements.pip 
  ```

### Data base
* Install Postgres
* Create Database

### ENV

  ``` 
    You must set the values of the database variables in the .env file
  ```


### Migrate
  
  ```
    cd {project_location}/src/

    python manage.py migrate
  ```


### Running the fixtures

  ``` 
    cd {project_location}/src/

    python manage.py loaddata fixtures/users.json
  ```
  
### Running the local server
  
  ```
    cd {project_location}/src/

    python manage.py runserver
  ```
  
### Running unit tests
  
  ```
    cd {project_location}/src/

    python manage.py test
  ```

# ENDPOINTS

### LOGIN

```
    POST http://127.0.0.1:8000/rest-auth/login/
    
    Body:
    {
    "email": "admin@example.com",
    "password": "Admin/1234"
    }

  ```


### GET CATEGORIES
 
 ```
    Headers: Authorization Bearer {{token}}
    GET http://127.0.0.1:8000/api/categories/
    GET http://127.0.0.1:8000/api/categories/1/

  ```
  
 ### POST CATEGORY
 
 ```
    Headers: Authorization Bearer {{token}}
    POST http://127.0.0.1:8000/api/categories/
    
    Body:
    {
        "code": "Fru",
        "title": "Fruits",
        "description": "The best fruits in the world",
        "parent": "http://127.0.0.1:8000/api/categories/1/"   <= Optional
    }    

  ```
  
 ### PUT CATEGORY
 
 ```
    Headers: Authorization Bearer {{token}}
    PUT http://127.0.0.1:8000/api/categories/1/
    
    Body:
    {
        "code": "Fru",
        "title": "Fruits",
        "description": "The best fruits in the world",
        "parent": "http://127.0.0.1:8000/api/categories/1/"   <= Optional
    }    

  ```
  
 ### PATCH / logical deletion CATEGORY
 
 ```
    Headers: Authorization Bearer {{token}}
    PATCH http://127.0.0.1:8000/api/categories/1/
    
    Body:
    {
        "status": "inactive" 
    }    

  ```
  
   ### DELETE CATEGORY
 
 ```
    Headers: Authorization Bearer {{token}}
    DELETE http://127.0.0.1:8000/api/categories/1/
     

  ```
 
