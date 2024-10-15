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

# Nginx
```
sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
sudo ufw status
sudo systemctl status nginx
sudo nano /etc/nginx/sites-available/etender
```
```nginx
server {
    listen 80;
    server_name 209.38.43.108;

    location / {
        proxy_pass http://127.0.0.1:8040;  # Pass requests to Gunicorn
        proxy_set_header Host $host;  # Forward the original host
        proxy_set_header X-Real-IP $remote_addr;  # Forward the client's IP
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # Forward the original IP address
        proxy_set_header X-Forwarded-Proto $scheme;  # Forward the original protocol (http or https)
    }
    location /static/ {
        alias /home/Etender_back/static/;
    }

 
}
```

```
sudo nginx -t
sudo nginx -s reload
sudo systemctl restart nginx
```

# Supervisor
```
sudo apt update
sudo apt install supervisor
sudo nano /etc/supervisor/conf.d/etender.conf
```
```supervisor
[program:etender]
command=/home/Etender_back/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8040 Etender.wsgi:application
directory=/home/Etender_back
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/etender.log
stderr_logfile=/var/log/etender_err.log
```
