# GITHUB

```
cd /home/
git clone https://github.com/Jasurbek2003/Etender_back.git 
cd Etender_back
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

# Python Version 3.12
```
sudo apt update
sudo apt install python3.12
sudo apt install python3.12-venv
```

# Postgresql
```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```
```postgresql
CREATE DATABASE etender;
CREATE USER etender WITH PASSWORD 'etender';
ALTER DATABASE etender OWNER TO etender;

```
!!! Change the password in settings.py