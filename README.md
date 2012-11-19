Spur
====


git clone https://github.com/JohnBerryman/Spur.git
cd Spur/
virtualenv venv --distribute
source venv/bin/activate
sudo pip install -r requirements.txt
heroku create
git push heroku master
heroku open
heroku run python manage.py syncdb


