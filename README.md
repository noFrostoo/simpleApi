# SimpleApi - Evox

## API

FastApi provides a simple docs view with all endpoints, schemas and exertions. It can be accessed [here](https://simpleapi-evox.herokuapp.com/docs)

### Views

Autothications scheme 
```

```

#### [**New**](https://simpleapi-evox.herokuapp.com/new)

View is used to add new messages. Body with content of the message is required. View requires authorization header.

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

#### **View** 

#### **Edit**

#### **Delete**

#### **Authorize**

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

