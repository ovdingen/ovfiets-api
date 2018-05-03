# ovfiets-api

This is a API for the rental bike service offered by the Nederlandse Spoorwegen (Dutch national railway operator, hereafter called "NS").

It's currently in a beta state. Our testing has proven it to be functional, but it isn't yet ready for production because of a few issues that need to be solved regarding i.e. code quality.

## Available functions

`GET /v1/station/<station_code>`

Returns OV-fiets availability for a specific train station. `station_code` is a station telegraph code (i.e. AMF, SHL, ASB, UT)

`GET /v1/afgiftepunt/<afg_code>`

Returns OV-fiets availability for a specific pickup point.

`GET /v1/total`

Returns OV-fiets availability for known all pickup points.


## Setting up

(We use gunicorn and systemd in this example. It's up to you to use something else.)

1) Create a new user called (i.e.) `ovfiets-api` which will run the HTTP api and the data collector.

# `adduser --disabled-login --disabled-password --shell /bin/false --home $CLONE_DIR --no-create-home $USER_NAME`

2) Create a directory, grant permission to the newly created user and clone this project.

$ `mkdir $CLONE_DIR && chown $USER_NAME:$USER_NAME $clone_dir && sudo -u $USER_NAME git clone $CLONE_URL`

3) Copy conf/daemon.json.dist to conf/daemon.json and change any necessary settings. We recommend using [universal-pubsub](https://github.com/StichtingOpenGeo/universal) as middleware between the OpenOV ZMQ server and the OVFiets API.

4) Install requirements.

# `pip install -r requirements.txt`

5) Install gunicorn. 

# `pip install gunicorn`

6) Copy `data/db.sqlite.dist` to `data/db.sqlite`.

7) Create a unit file for the data gatherer. Here is a example:

```
[Unit]
Description=OVFiets API data gatherer daemon
After=syslog.target network.target

[Service]
User=ovfiets-api
WorkingDirectory=/opt/ovfiets-api/
ExecStart=/usr/bin/python /opt/ovfiets-api/api-daemon.py conf/daemon.json

[Install]
WantedBy=multi-user.target
```

8) Create a unit file for Gunicorn. Here is a example:

```
[Unit]
Description=OVFiets API HTTP Gunicorn application
After=syslog.target network.target

[Service]   
User=ovfiets-api
WorkingDirectory=/opt/ovfiets-api/
ExecStart=/usr/local/bin/gunicorn -b 127.0.0.1:9000 http:app

[Install]
WantedBy=multi-user.target
```

Please note that the above is just a example, and not an extensive guide.

