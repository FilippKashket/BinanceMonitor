Server part


1. Install packages for project

$ virtualenv NEWVIRTUALENV

$ source NEWVIRTUALENV/bin/activate

$ pip install -r requirements.txt

2. For run use
To run the application you can either use the flask command or python’s -m switch with Flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:

$ export FLASK_APP=server.py 

$ flask run

Running on http://127.0.0.1:5000/

