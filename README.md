# simpleApi

## Building


## How to deploy to heroku

Heroku doesn't have support for poetry. To make possible deploying application with poetry, install buildpack first. This build pack generates files for heroku build in python support from poetry.lock. 

```
heroku buildpacks:clear -a simpleapi-evox
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git -a simpleapi-evox
heroku buildpacks:add heroku/python -a simpleapi-evox
heroku config:set PYTHON_RUNTIME_VERSION=3.9.1 -a simpleapi-evox
heroku config:set POETRY_EXPORT_DEV_REQUIREMENTS=1 -a simpleapi-evox

```
