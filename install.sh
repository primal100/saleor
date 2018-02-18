#!/usr/bin/env bash
POSTGRES_USER=shop
POSTGRES_DB=shop
POSTGRES_PASSWORD=
APPNAME=shop
REPOSITORY_URL=https://github.com/primal100/shop
REPOSITORY_DIRNAME=shop
BRANCH_NAME=myshop

cd $HOME
sudo yum install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat96-9.6-3.noarch.rpm
sudo yum -y install postgresql96-server postgresql96-contrib nginx redis redis-server gcc wget openssl-devel git bzip2 xz fontconfig-devel
sudo yum -y install cairo-devel pango gdk-pixbuf2 libffi-devel roboto-fontface-fonts
sudo systemctl enable redis
sudo systemctl start redis
sudo /usr/pgsql-9.6/bin/postgresql96-setup initdb
sudo systemctl enable postgresql-9.6.service
sudo systemctl start postgresql-9.6.service
sudo su - postgres -c "echo '$PATH=$PATH:/usr/pgsql-9.6/bin/' >> .bash_profile"
sudo su - postgres -c "echo 'export PATH' > .bash_profile"
sudo su - postgres -c "createuser -P -S -D -R -e $POSTGRES_USER"
sudo su - postgres -c "createdb $POSTGRES_DB"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB to $POSTGRES_USER;'"
sudo su - postgres -c "psql -c \"alter user $POSTGRES_USER with encrypted password '$POSTGRES_PASSWORD';\""
sudo su - postgres -c "psql -c 'ALTER USER $POSTGRES_USER WITH SUPERUSER;'"
cp /var/lib/pgsql/9.6/data/pg_hba.conf /var/lib/pgsql/9.6/data/pg_hba.conf.default
sed -i 's/ident/md5/g' /var/lib/pgsql/9.6/data/pg_hba.conf
wget https://nodejs.org/dist/v8.9.3/node-v8.9.3-linux-x64.tar.xz
sudo tar -C /usr/local --strip-components 1 -xJf node-v8.9.3-linux.x64.tar.xz
sudo ln -s /usr/local/bin/npm /usr/bin/npm
sudo ln -s /usr/local/bin/node /usr/bin/node
sudo npm i webpack -g
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz
sudo tar xzf Python-3.5.4.tgz
cd Python-3.5.4
./configure  --with-ensurepip=upgrade
sudo make altinstall
cd ..
rm Python-3.5.4.tgz
sudo ln -s /usr/local/bin/python3.5 /usr/bin/python3
sudo ln -s /usr/local/bin/pip3.5 /usr/bin/pip3
sudo pip3 install virtualenv
cd $HOME
virtualenv $APPNAME
cd $APPNAME
source $HOME/$APPNAME/bin/activate
git clone $REPOSITORY_URL
cd $REPOSITORY_DIRNAME
git checkout $BRANCH_NAME
pip3 install -r requirements.txt
npm install
npm run build-assets
npm run build-emails


...Enter environment variables
python manage.py migrate
python manage.py collectstatic
python manage.py update_exchange_rates --all

#Setup celery daemon
sudo mkdir /var/log/celery
sudo mkdir /var/run/celery
chown nilepottery:nilepottery /var/run/celery/
sudo chown nilepottery:nilepottery /var/run/celery/
sudo chown nilepottery:nilepottery /var/log/celery/

sudo cat <<EOT >>  /etc/celery.conf:
CELERYD_NODES="w1"
CELERY_BIN="/home/nilepottery/shop/bin/celery"
CELERY_APP="saleor"
CELERYD_MULTI="multi"
CELERYD_OPTS="--time-limit=300 --concurrency=8"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"
SECRET_KEY=''
DEFAULT_FROM_EMAIL='noreply@nilepottery.com'
SENDGRID_PASSWORD=''
REDIS_URL='redis://localhost:6379/0'
REDIS_BROKER_URL='redis://localhost:6379/1'
DATABASE_URL=''
GOOGLE_ANALYTICS_TRACKING_ID=''
PAYPAL_SECRET=''
STRIPE_SECRET=''
DEBUG='False'
EOT

sudo cat <<EOT >>  /etc/celerytest.conf:
CELERYD_NODES="w1"
CELERY_BIN="/home/nilepottery/shop/bin/celery"
CELERY_APP="saleor"
CELERYD_MULTI="multi"
CELERYD_OPTS="--time-limit=300 --concurrency=8"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="DEBUG"
SECRET_KEY=''
DEFAULT_FROM_EMAIL='noreply@nilepottery.com'
SENDGRID_PASSWORD=''
REDIS_URL='redis://localhost:6379/0'
REDIS_BROKER_URL='redis://localhost:6379/1'
DATABASE_URL=''
GOOGLE_ANALYTICS_TRACKING_ID=''
PAYPAL_SECRET=''
STRIPE_SECRET=''
DEBUG='True'
EOT

sudo cat <<EOT >> //usr/lib/systemd/system/celery.service
[Unit]
Description=Celery Service
After=network.target redis.service
[Service]
Type=forking
User=nilepottery
Group=nilepottery
EnvironmentFile=-/etc/celery.conf
WorkingDirectory=/home/nilepottery/shop/shop
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
[Install]
WantedBy=multi-user.target
EOT

sudo cat <<EOT >> /usr/lib/systemd/system/celerytest.service
[Unit]
Description=Celery Service
After=network.target redis.service
[Service]
Type=forking
User=nilepottery
Group=nilepottery
EnvironmentFile=-/etc/celerytest.conf
WorkingDirectory=/home/nilepottery/shop/shop
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
[Install]
WantedBy=multi-user.target
EOT

sudo mkdir /var/run/celery
sudo chown -R nilepottery:nilepottery /var/run/celery
sudo cat <<EOT >> /etc/tmpfiles.d/celery.conf:
d /var/run/celery 0755 nilepottery nilepottery -
d /var/log/celery 0755 nilepottery nilepottery -
EOT

sudo systemctl daemon-reload
sudo systemctl start celerytest
sudo systemctl enable celerytest


sudo cat <<EOT >>  /etc/envs.conf:
SECRET_KEY=
DEFAULT_FROM_EMAIL=noreply@nilepottery.com
SENDGRID_PASSWORD=
REDIS_URL=redis://localhost:6379/0
REDIS_BROKER_URL=redis://localhost:6379/1
DATABASE_URL=
GOOGLE_ANALYTICS_TRACKING_ID=
PAYPAL_SECRET=
STRIPE_SECRET=
DEBUG=False
EOT

sudo cat <<EOT >>  /etc/envstest.conf:
SECRET_KEY=
DEFAULT_FROM_EMAIL=noreply@nilepottery.com
SENDGRID_PASSWORD=
REDIS_URL=redis://localhost:6379/0
REDIS_BROKER_URL=redis://localhost:6379/1
DATABASE_URL=
GOOGLE_ANALYTICS_TRACKING_ID=
PAYPAL_SECRET=
STRIPE_SECRET=
DEBUG=True
EOT

cat <<EOT >>  uwsgitest.ini:
[uwsgi]

die-on-term = true
socket = /home/nilepottery/shop/shop.sock
chdir = /home/nilepottery/shop/shop
log-format = UWSGI uwsgi "%(method) %(uri) %(proto)" %(status) %(size) %(msecs)ms
[PID:%(pid):Worker-%(wid)] [RSS:%(rssM)MB]
master = true
max-requests = 100
memory-report = true
module = saleor.wsgi:application
processes = 4
static-map = /static=static
virtualenv = /home/nilepottery/shop
for-readline = /etc/envstest.conf
  env = %(_)
endfor =
EOT

cat <<EOT >>  uwsgi.ini:
[uwsgi]
die-on-term = true
socket = /home/nilepottery/shop/shop.sock
chdir = /home/nilepottery/shop/shop
log-format = UWSGI uwsgi "%(method) %(uri) %(proto)" %(status) %(size) %(msecs)ms
[PID:%(pid):Worker-%(wid)] [RSS:%(rssM)MB]
master = true
max-requests = 100
memory-report = true
module = saleor.wsgi:application
processes = 4
static-map = /static=static
virtualenv = /home/nilepottery/shop
for-readline = /etc/envs.conf
  env = %(_)
endfor =
EOT

deactivate
sudo pip3 install uwsgi
sudo mkdir -p /etc/uwsgi/vassals
sudo ln -s /home/nilepottery/shop/shop/saleor/wsgi/uwsgitest.ini /etc/uwsgi/vassals/

sudo cat <<EOT >> /etc/uwsgi/emperor.ini
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = nilepottery
gid = nilepottery
EOT

sudo cat <<EOT >> /usr/lib/systemd/system/uwsgi.service
[Unit]
Description=uWSGI Emperor
After=syslog.target postgresql-9.6.service redis.service

[Service]
ExecStart=uwsgi --ini /etc/uwsgi/emperor.ini
# Requires systemd version 211 or newer
RuntimeDirectory=/usr/local/bin/uwsgi
Restart=always
KillSignal=SIGTERM
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOT

sudo systemctl start uwsgi
sudo systemctl enable uwsgi

sudo cat <<EOT >> /home/nilepottery/shop/shop/nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    server unix:///home/nilepottery/shop/shop.sock;
    # server 127.0.0.1:8000;
}
# configuration of the server
# nginx.conf
# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}
# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name .nilepottery.com; # substitute your machine's IP address or FQDN
    charset     utf-8;
    # max upload size
    client_max_body_size 75M;   # adjust to taste
    # Django media
    location /media  {
        alias /home/nilepottery/shop/shop/media;  # your Django project's media files - amend as required
    }
    location /static {
        alias /home/nilepottery/shop/shop/static; # your Django project's static files - amend as required
    }
    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
}
EOT

sudo mkdir /etc/nginx/sites-enabled
sudo ln -s /home/nilepottery/shop/shop/nginx.conf /etc/nginx/sites-enabled/
sudo chown -R nginx:nginx sites-enabled/

#Add the following lines to http section of /etc/nginx.conf
include /etc/nginx/sites-enabled/*.conf;
server_names_hash_bucket_size 64;

#Also change user to nilepottery in the same file

sudo usermod -a -G nginx nilepottery
sudo chown -R nilepottery:nginx /var/lib/nginx
sudo chmod -R 770 /var/log/nginx/
sudo chmod -R 770 /var/lib/nginx/

sudo systemctl restart nginx
sudo systemctl enable nginx

sudo yum install certbot-nginx
sudo certbot --nginx -d nilepottery.com

cd $HOME/shop
mkdir backups
cd backups
su - shop -c "/usr/pgsql-9.6/bin/pg_dump shop" > backup170217

cronjob > db backups, update exchange rates

#Change to Static IP:
#https://console.cloud.google.com/networking/addresses/list?project=nile-pottery
#Setup DNS:
#https://cloud.google.com/dns/quickstart
#Verify domain name
#Set instance cloud API access control full access
#Storage: set service account as Storage Admin, set allUsers as Viewer
#Fix favicon: 1500x1500 < 1mb

#Google storage paramaters, if required:

GS_PROJECT_ID='nile-pottery'
GS_STATIC_BUCKET_NAME='static.nilepottery.com'
GS_MEDIA_BUCKET_NAME='media.nilepottery.com'
GS_STATIC_URL='https://static.nilepottery.com'
GS_MEDIA_URL='https://media.nilepottery.com'

#Save file with sudo:

#:w !sudo tee % > /dev/null
