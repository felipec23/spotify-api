# Spotify - API
This repository fetches data from the Spotify API and creates a CRUD system to manipulate it, using Flask and Sqlalchemy.

# Requirements
The dependencies needed for running this app are in the requirements.txt file of the repository. The main libraries used are:
- flask
- request
- flask_restful
- flask_sqlalchemy
- flask_marshmallow

# Usage
The main code is contained in "main.py" file. You can run the app by typing in a console: "python main.py". Next is a description of all the files in the repository:
- main.py: contains the resources used in the routes that the API has available.
- agregar_datos.py: this file is to be runned once. It can be used to fetch data from the Spotify API and store it in MySql database, using Sqlalchemy.
- argumentos_y_fields.py: it has all the arguments that each route and method will receive.
- clases.py: this file has the classes that Sqlalchemy needs in order to create the tables and to query them.
- funciones.py: contains functions needed when fetching the data from Spotify.

# Validations:
The following data validations and error handlings are applied:
- Whenever a CRUD operation is called, the API checks if the element exists or not in the database. Depending on the case, it'll return the error and the explanation.
- Date entities are checked before insertion in the database.
- All responses are serialized and with a status code.
- Code is easily reproducible (for the creation of new entities)
- When the case, the arguments in the body of the request will be reviewed, and if mandatory elements are not detected, it'll throw an error stating the argument missing.
- Nullability and uniqueness are pointed out in the tables creation.
