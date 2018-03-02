# graphQL-core
This a work in progress prototype graphQL resource server used for handling social collaboration information within a larger open sourced collaboration platform model.  The graphQL-core project is based off of the [Django project](https://www.djangoproject.com/) and [GraphQL](http://graphql.org/) query language.  Once completed the graphQL resource server will be able to integrate with an OpenID Connect/Oauth Identity provider and provide access to microservices such as user profile, blogs, skills, and more.

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

Current backend for dev testing is sqlite3.  This will be migrated to MariaDB for Prod or Staging setups.

