
Spur
====

Downloading Code
----------------

    #download the code
    git clone https://github.com/JohnBerryman/Spur.git
    cd Spur/
    #create virtual environment #http://pypi.python.org/pypi/virtualenv
    virtualenv venv --distribute
    #use it
    source venv/bin/activate
    #install all requirements
    sudo pip install -r requirements.txt

Running Locally
---------------
You will need to have postgreSQL set up with *user:spurdev* *database:spurdb* and *password:spurword*. This might or might not be a pain in the butt.

    python manage.py syncdb
    python manage.py runsever
    
Accessing Database
------------------

    psql -U spurdev -d spurdb

Running in Heroku
-----------------

    #you need to heroku toolbelt https://devcenter.heroku.com/articles/django
    heroku create
    git push heroku master
    heroku run python manage.py syncdb
    heroku open



