# graphQL-core
This a work in progress prototype graphQL resource server used for handling social collaboration information within a larger open sourced collaboration platform model.  The graphQL-core project is based off of the [Django project](https://www.djangoproject.com/) and [GraphQL](http://graphql.org/) query language.  The GraphQL resource server is now able to receive an OpenID Connect access token from an application and verify it's validity through custom scopes with the OpenID Connect provider.  A regular DRF token protected graphQL API endpoint is also available to run high level mutations from triggers created within other management applications.  For instance when a new user registers for an account on the OpenID Connect provider a trigger can be launched to send a graphQL mutation to this protected endpoint to create and pre-populate a users profile information (OpenID unique identifier, name, email address).

## Branches
- Master branch will have a dockerized version of the graphql-core for easy spin up.
- Development branch will not contain a dockerized version and will be used for local development within a python virtual environment.

## Docker Image
Make sure [Docker](https://www.docker.com/) is installed. Then run the following command within the repository:

    docker-compose up

Then create a superuser account using:
    docker-compose exec web python manage.py createsuperuser

Now login with your new (superuser) account on http://localhost:8080/admin for Django Admin panel.
GraphQL enpoints are:
    GraphiQL endpoint at http://localhost:8080/graphiql and query away!
    API endpoint for use with applicaitons can be found at http://localhost:8080/graphqlcore

DB in docker image uses postgreSQL and is persistent on volume db_volume in the repo once the docker image is run.

## Setup development (through python virtual env)
Ensure [Python](https://www.python.org/downloads/) version 3 or greater is installed.  Create your python virtual environment and launch it using the normiclature for your specific OS (ex. phython3.6 -m venv venv / source venv/bin/activate) and then run the following commands from within the repository:

    ex. python3.6 -m venv venv
    ex. source venv/bin/activate
    cd name_of_cloned_repo
    pip install -r requirements.txt
    cd graphql-core
    python3.6 manage.py migrate
    python3.6 manage.py createsuperuser
    python3.6 manage.py runserver localhost:8000    
  
Log into the django admin at http://localhost:8000/admin using the newly created superuser

Create your Profiles, Addreses, and OrgTiers

Access the GraphiQL endpoint at http://localhost:8000/graphiql and query away!

API endpoint for use with applicaitons can be found at http://localhost:8000/graphqlcore

Protected endpoint for management applications is at http://localhost:8000/protected

In order for an application to access the protected endpoint an account will need to be created through Django Admin.  The corresponding token will then need to be sent in each request to the endpoint in the form of:"Authorization: Token {token}"

Current backend for dev testing is sqlite3.  This will be migrated to MariaDB for Prod or Staging setups.

