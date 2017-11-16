#!/usr/bin/env bash



function configure_nginx {
    nginx_config="
server {
    listen 80;
    server_name $1;
    access_log  /var/log/nginx/example.log;

    location /static/ {
        root $2;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$server_name;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
  }
"
    nginx_config=${nginx_config//server_placeholer/$1}
    nginx_config=${nginx_config//root_placeholer/$2}
    filepath=/etc/nginx/sites-available/default
    echo -e "$nginx_config" > $filepath
    sudo ln -s $filepath /etc/nginx/sites-enabled
    sudo service nginx restart
}


function configure_supervisor {
    echo $1
    supervisor_config="
[program:start_server]
command=/bin/bash $1/start_server
user=$2
numprocs=1
autostart=true
autorestart=true
startsecs=10
stopwaitsecs = 600
startretries=10
killasgroup=true
priority=997"
    echo -e "$supervisor_config" > /etc/supervisor/conf.d/start_server.conf
    supervisorctl reread
    supervisorctl update
    supervisorctl status start_server
    supervisorctl restart start_server
}


function install_packages {
    sudo apt-get update
    sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx
    sudo apt-get install python3
    sudo apt-get install python3-setuptools
    apt-get install supervisor
    sudo easy_install3 pip
    pip3 install virtualenv
}


function clone {
    git clone $1
    cd $(basename $1 .git)
    filepath=$(git rev-parse --show-toplevel)
    echo $filepath
    cd ../
}



function create_db {
    sudo -u postgres psql -c "CREATE DATABASE $1;"
    sudo -u postgres psql -c "CREATE USER $2 WITH PASSWORD '$3';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $1 TO $2;"
}

username=toerting
project_dir=$(git rev-parse --show-toplevel)
cd /opt/
echo Domain URL:
read domain
echo $project_dir
echo Want continue?
read continue

install_packages
virtualenv venv
source venv/bin/activate
cd $project_dir
ls $project_dir
pip3 install -r requirements.txt
echo Want continue?
read continue
cd /etc/nginx/sites-available/
configure_nginx $domain $project_dir
configure_supervisor $project_dir $username
echo Want continue?
read continue
create_db ege_db admin admin1703
