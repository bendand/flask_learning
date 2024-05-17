Instructions too set up environment for running app.py file...

Anaconda Download Instructions
If Anaconda is already installed, skip this first part.

Go to this link and download the Anaconda version made specifically for your operating system.
https://www.anaconda.com/download/


(Assuming anaconda is downloaded)
To create the environment with the appropriate python version:

$ conda create -n myenv python=3.6.13

When asked: Proceed ([y]/n)? -- type 'y'


Environment activation is required next.

$ conda activate myenv


You'll then need to install all the extensions in the requirements.txt file located under the flask_large_project directory. To do this, make sure you're in the flask_large_project directory, click on requirements.txt, download the raw file, and then use your terminal to route into your downloads folder. Then, do the following.

$ pip install -r requirements.txt

If all downloads properly, open and interactive shell and run...

>>> import flask

If that command returns no ModuleNotFoundError, then you have successfully installed flask.

To run app.py script..

$ python app.py


#### NOTES ABOUT FILE STRUCTURE ####

- you need __init__.py files in each sub-directory to let the computer know the directories are modules that are able to be imported


##### NOTES ABOUT DATABASES #####

$ flask db init 

this initializes the database as well as creates a migrations file in the directory where the database is initialized

And then run:

$ flask db migrate -m "<note about migration>"

Then:

$ flask db upgrade

If you aren't able to execute these commands error-free, something is likely wrong either with your models.py or __init__.py scripts

