# SimpleApi - Evox

## Framework
Fast api 
## API

FastApi provides a simple docs view with all endpoints, schemas and exertions. It can be accessed [here](https://simpleapi-evox.herokuapp.com/docs)

### Views

Authorizations works by appending authorization header with token Bearer to the request.  Every view that requirers authorizations, requires header.
Authorizations header scheme 
```
'Authorization: Bearer -token- ' 
```

#### [**New**](https://simpleapi-evox.herokuapp.com/docs#/default/new_message_new_post)

View is used to add new messages. Body with content of the message is required. View requires authorization header.

```
url: https://simpleapi-evox.herokuapp.com/new
```
* **Method**: Post

* **Parameters**:
    No parameters

* **Request body**:

    **Type**: application/json

    ```
    {
        "content": "string"
    }
    ```
* **Responses**:
  
    * Successful response:
  
       Code: 200
       ```
       {
        "content": "string",
        "id": int,
        "views_count": int
        } 
        ```
    * Validation Error:
  
       Code: 422
       ```
        {
        "detail": [
            {
            "loc": [
                "string"
            ],
            "msg": "string",
            "type": "string"
            }
        ]
        }
        ```
    * Bad Request:
  
       Code: 400
       ```
        {
        "detail": "string"
        }
        ```
    * Request Entity Too Large - also raised when length of message is abot 160 :
  
       Code: 413
       ```
        {
        "detail": "string"
        }
        ```
* **Example curl call**:

    ```bash
    curl -X 'POST' \
    'https://simpleapi-evox.herokuapp.com/new' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer -token- ' \
    -H 'Content-Type: application/json' \
    -d '{
    "content": "string"
    }'
    ```

#### [**View**](https://simpleapi-evox.herokuapp.com/docs#/default/view_message__message_id__get) 

Used to view a message. Parameter- path with message id is required. View dose not require authorization header.

```
url: https://simpleapi-evox.herokuapp.com/{id}
```

* **Method**: Get

* **Parameters**:
    message_id (path) - integer 

* **Request body**:
    not required
* **Responses**:
  
    * Successful response:
  
       Code: 200
       ```
       {
        "content": "string",
        "id": int,
        "views_count": int
        } 
        ```
    * Validation Error:
  
       Code: 422
       ```
        {
        "detail": [
            {
            "loc": [
                "string"
            ],
            "msg": "string",
            "type": "string"
            }
        ]
        }
        ```
    * Not Found - message of this id has not been found:
  
       Code: 404
       ```
        {
        "detail": "string"
        }
        ```
* **Example curl call**:

    ```bash
    curl -X 'GET' \
    'https://simpleapi-evox.herokuapp.com/1' \
    -H 'accept: application/json'
    ```

#### [**Edit**](https://simpleapi-evox.herokuapp.com/docs#/default/edit_message__message_id__put)

Used to edit a message. Parameter- path with message id is required. Body with new content is required. View requires authorization header.

```
url: https://simpleapi-evox.herokuapp.com/{id}
```

* **Method**: Put

* **Parameters**:
    message_id (path) - integer 

* **Request body**:
    **Type**: application/json

    ```
    {
        "content": "string"
    }
    ```
* **Responses**:
  
    * Successful response:
  
       Code: 200
       ```
       {
        "content": "string",
        "id": int,
        "views_count": int
        } 
        ```
    * Validation Error:
  
       Code: 422
       ```
        {
        "detail": [
            {
            "loc": [
                "string"
            ],
            "msg": "string",
            "type": "string"
            }
        ]
        }
        ```
    * Bad Request:
  
       Code: 400
       ```
        {
        "detail": "string"
        }
        ```
    * Request Entity Too Large - also raised when length of message is abot 160 :
  
       Code: 413
       ```
        {
        "detail": "string"
        }
        ```
    * Not Found - message of this id has not been found:
  
       Code: 404
       ```
        {
        "detail": "string"
        }
        ```
* **Example curl call**:

    ```bash
    curl -X 'PUT' \
    'https://simpleapi-evox.herokuapp.com/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer -TOKEN-' \
    -H 'Content-Type: application/json' \
    -d '{
    "content": "test2"
    }'
    ```

#### [**Delete**](https://simpleapi-evox.herokuapp.com/docs#/default/delete_message__message_id__delete)

Used to delete a message. Parameter- path with message id is required. View requires authorization header.

```
url: https://simpleapi-evox.herokuapp.com/{id}
```

* **Method**: Delete

* **Parameters**:
    not required
* **Request body**:
    **Type**: application/x-www-form-urlencoded

    * grant_type - string - pattern: password
    * username (required) - string
    * password (required) - string
    * scope (optional) -string
    * client_id (optional) -string
    * client_secret (optional) -string
* **Responses**:
  
    * Successful response:
  
       Code: 200
       ```
        {
        "access_token": "string",
        "token_type": "string"
        }
        ```
    * Validation Error:
  
       Code: 422
       ```
        {
        "detail": [
            {
            "loc": [
                "string"
            ],
            "msg": "string",
            "type": "string"
            }
        ]
        }
        ```
    * Unauthorized - authorization hasn't been successful:
  
       Code: 401
       ```
        {
        "detail": "string"
        }
        ```
* **Example curl call**:

    ```bash
    curl -X 'DELETE' \
    'https://simpleapi-evox.herokuapp.com/5' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer -token-'
    ```

#### **Authorize**

Used to authorize a user. Body with new content is required. View requires authorization header.

```
url: https://simpleapi-evox.herokuapp.com/authorize
```

* **Method**: Delete

* **Parameters**:
    message_id (path) - integer 

* **Request body**:
    not required
* **Responses**:
  
    * Successful response:
  
       Code: 200
       ```
        bool
        ```
    * Validation Error:
  
       Code: 422
       ```
        {
        "detail": [
            {
            "loc": [
                "string"
            ],
            "msg": "string",
            "type": "string"
            }
        ]
        }
        ```
    * Not Found - message of this id has not been found:
  
       Code: 404
       ```
        {
        "detail": "string"
        }
        ```
* **Example curl call**:

    ```bash
    curl -X 'POST' \
    'https://simpleapi-evox.herokuapp.com/authorize' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=password&username=username1&password=password1'
    ```

#### **Welcome**

## Building and running


## How to deploy to heroku

The app is deployed on [Heroku](https://simpleapi-evox.herokuapp.com/)

Heroku doesn't have support for poetry. To make possible deploying application with poetry, install buildpack first. This build pack generates files for heroku builtin python support from poetry.lock. 

```
heroku buildpacks:clear -a simpleapi-evox
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git -a simpleapi-evox
heroku buildpacks:add heroku/python -a simpleapi-evox
heroku config:set PYTHON_RUNTIME_VERSION=3.9.1 -a simpleapi-evox
heroku config:set POETRY_EXPORT_DEV_REQUIREMENTS=1 -a simpleapi-evox

```

Buildpack still needs a Procfile
```
web: uvicorn simpleapi:app --host=0.0.0.0 --port=${PORT:-5000} --workers 1
```

With all this app is ready to deploy. I use automatic deployment from github.

