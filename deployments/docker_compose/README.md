# About
This is a docker-compose single node implementation.  It is not distributed in nature and is not meant as a scalable solution.  It is meant to get the stack up and running for demo or small scale deployments.


## Dependencies
Make sure you have the following installed:
- `docker` (Make sure the engine is running after the install)
- `docker-compose`


## Configuration File
| Key                               | Required | Description                                                                                                           | Default message                                                                                      |
| --------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| HOST_ADDRESS                      | ✔     | Watchtower:FLow's public address as would be entered in a web browser. |
| ALLOWED_HOSTS                     | ❌    | Watchtower:FLow's approved list of host names provided as an array. If not provided, will default to HOST_ADDRESS. |
| HOST_PORT_HTTPS                   | ✔     | Watchtower:FLow's public address HTTPS port; defaults to 443 |
| HOST_PORT_HTTP                    | ❌    | Watchtower:FLow's public address HTTP port; defaults to 80   |
| ADMINS                            | ✔    | Administrator accounts. Ex: `[{"username": "username", "email":"first.last@example.com", "password": "REPLACEME"}]`     | Will auto-create an admin, you need to find it in the logs docker-compose logs                       |
| BRANDING                          | ❌    | Full file path to Watchtower:FLow branding directory                                                                       | Wacthtower:Flow default branding will be used.                                                              |
| DATABASE_CONNECTION_STRING        | ❌    | Database connection string: `<db_connector>://<name>:<password>@<host>:<port>/<db_name>`                                | Will create a Postgres server in the docker-compose deployment for you.  It will not have snapshots. |
| MOUNT_FOLDER                      | ❌    | Mount folder to put artifacts, logs, etc.                                                                             | Current directory                                                                                    |
| GIT_URL                           | ❌    | Watchtower:FLow Github Repo                                                                                                | Defaults to https://github.com/mjhillyer/watchtower-flow.git                                              |
| MAILGUN_API_KEY                   | ❌    | Mailgun is used to submit an incoming email from notifications.                                                       | No default provided.                                                                                 |
| NGINX_CERT                        | ❌    | Full file path to Nginx cert.pem                                                                                      | Defaults to self signed                                                                              |
| NGINX_KEY                         | ❌    | Full file path to Nginx key.pem                                                                                       | Defaults to self signed                                                                              |
| EMAIL_DOMAIN                      | ❌    | Domain of the Email Server.                                                                                           | No default provided.                                                                                 |
| EMAIL_HOST                        | ❌    | Host of Email Server.                                                                                                 | No default provided.                                                                                 |
| EMAIL_PORT                        | ❌    | Port of Email Server.                                                                                                 | No default provided.                                                                                 |
| EMAIL_PW                          | ❌    | Password for the User for of Email Server.                                                                            | No default provided.                                                                                 |
| EMAIL_USER                        | ❌    | User for the Email Server.                                                                                            | No default provided.                                                                                 |
| GR_PDF_GENERATOR                  | ❌    | PDF generator binary name.                                                                                            | Default is to disable this feature                                                                          |
| GR_IMG_GENERATOR                  | ❌    | IMG generator binary name.                                                                                            | Default is to disable this feature                                                                         |
| PERSIST_STACK                     | ❌    | Persist stack between runs.                                                                                           | Default is False |
| PROXY_AUTHENTICATION_USER_HEADER  | ❌    | Proxy Authentication User header.                                                                                     | No default provided.                                                                                 |
| PROXY_AUTHENTICATION_EMAIL_HEADER | ❌    | Proxy Authentication Email header.                                                                                    | No default provided.                                                                                 |
| SECRET_KEY                        | ✔     | Django Secret                                                                                                         |                                                                                   |
| VERSION                           | ❌    | Watchtower:FLow version/tag                                                                                                | Defaulting to latest release                                                                         |

To build an empty configuration file use `python run.py init` at the root of the project.

## Local Docker Database

A local Docker container running PostgreSQL will automatically be added when the `configuration.json` file's `DATABASE_CONNECTION_STRING` is set to `""`.

The local database running in Docker container is persisted between deploys in a Docker Volume called `watchtower-flow_postgres-data` to preserve data.

The Docker container running the default PostgreSQL is Alpine Linux. The PostgreSQL configuration files located in the `/postgres-data` directory (e.g., `/postgres-data/postgresql.conf`).

#### Wipe Local Docker Database Volume

Remove existing docker build - then:

```bash
docker volume rm watchtower-flow_postgres-data`
```

## Running Database on Host or Seperate Server

You can also connect a Docker-ized Watchtower:Flow instance to a persistent Postgres database running on:

1. the Host machine that is used by a Wacthtower:Flow deployment running the docker containers (e.g., Postgres not in a container)
2. a second server
3. a managed Postgres service run by you Cloud Service Provider

The following instructions are for option #1 on Ubuntu 18.04, which keeps everything on one server while reducing the chance of accidentally wiping a containerized Postgres database. (Adjust appropriately for your OS.)

For additional information see https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html.

### Step 1 - Configure postgresql.conf

Modify the Host's Postgres configuration file `/etc/postgresql/10/main/postgresql.conf` to instruct Postgres to listen on the Host machine's IP address, Host name, etc.:

```bash
listen_addresses = 'localhost, ip_address, domain_name'
```

Example:

```bash
listen_addresses = 'localhost, 10.1.0.10'
```

### Step 2 - Configure pg_hba.conf

Modify Host's Postgres configuration file `/etc/postgres/10/main/pg_hba.conf` to permit connection from the Watchtower:FLow instance running in the docker container by allowing a connection from the IP address the Host perceives for the docker container.

Watchtower:FLow's docker compose network is configured with the IP address `172.32.0.0/24`.

NOTES: If you deployed Wacthtower:Flow using Docker-Compose, the IP address will be that of the Docker-Compose network bridge. If you deployed Wacthtower:Flow using a single container, the IP address will be that of the container's IP address. If you are connecting to a database on a remote server, the IP address of the Watchtower:FLow instance is the Host machine's IP address.

Configure `pg_hba.conf` to permit connections from the perceived IP address of docker network (or container):

```bash
host all all 172.32.0.0/24 password
local all postgres peer
...
```

### Step 3 - Restart Postgres

Restart Postgres:

```
sudo service postgresql stop
sudo service postgresql start
```

### Step 4 - Configure Wacthtower:Flow Deployment configuration.json

Modify Wacthtower:Flow's docker deployment configuration file `configuration_mantech.json` to have Postgres database connection string that includes the Host IP address running the Postgres instance.

`"DATABASE_CONNECTION_STRING": "postgres://username:password@host/dbname",`

Example:

`"DATABASE_CONNECTION_STRING": "postgres://watchtower-flow:s&kerjkDKW231@10.1.0.10/watchtower_flow_db",`

### Step 5 - Restart Wacthtower:Flow container stack

Restart Wacthtower:Flow stack appropriately.


# BACKUP POSTGRES DATABASE

1. Look up password in file `/home/watchtower-flow/local/environment.json`.
1. Run: `pg_dump postres -U example_user -h localhost > <file_path>/pg_dump_<date>.sql`

## Remote Database

It is also possible to connect Docker-ized Watchtower:Flow instance to a PostgreSQL database instance running on a different machine (i.e., remote database) following the below instructions.

This configuration provides a persistent Postgres database on the Host machine that is used by a Wacthtower:Flow deployment running withing docker containers on the host machine.

## Viewing Logs

When a `Server Error (500)` appears the will almost always be written to the log file in the `watchtower-flow_app_1` container and can be accessed from the following `tail` command on the HOST machine:

```bash
tail <path_to>/watchtower-deployments/volumes/watchtower-flow/logs/gunicorn.error.log
```

This file can also be reached from the Watchtower:Flow container (watchtower-flow_app_1):

```bash
docker exec -it watchtower-flow_app_1 tail /var/log/gunicorn.error.log
```

NOTE: You may need to prefix your docker commands with `sudo` depending on the relative ownership of Docker and ownership and install directory of `watchtower-deployments` on your Host.

The STDOUT of the Watchtower:Flow as it runs can be viewed by attaching in a terminal to the Watchtower:Flow container via the command (for example):

```bash
docker attach watchtower-flow_app_1
```

## Setting up SSL via Let's Encrypt certbot

The following instructions describe the general process of using Let's Encrypt certbot to configure an SSL certificate for your instance on Ubuntu 18.04. (Adjust appropriately for your OS.)

Watchtower:Flow's NGINX is preconfigred to allow port 80 access to the path where certbot adds a file for validating the domain.

You may find it useful to read one of the many posts online regarding certbot for additional hints.

### Step 1 - Connect to NGINX instance.

First, connect to NINGX running in the Docker container.

```bash
docker exec -it watchtower-flow_nginx_1 /bin/sh
```

NOTE: The NGINX container uses the Alpine OS.

### Step 2 - Install certbot

Install certbot and it’s NINGX plugin with apt:

```bash
apk add certbot certbot-nginx
```

NOTE: The NINGX configure file is `/etc/nginx/nginx.conf `. Also, `sudo` is not installed in the Alpine NGINX container. You are root when you exec'ed into the container.

### Step 3 - Run certbot to Obtain an SSL Certificate

Now run certbot by typing the following:

```bash
certbot --nginx -d example.com
```

This runs certbot with the --nginx plugin, using -d to specify the domain names for the certificate. Be sure to use the same domain as specified Wacthtower:Flow's configuration file (e.g., "HOST_ADDRESS": "example.com").

You will be prompted to enter an email address, agree to the terms of service and other information. certbot will communicate with the Let’s Encrypt server, then run a challenge to verify that you control the domain. Watchtower:Flow's NGINX is preconfigred to allow port 80 access to the path where certbot adds a file for validating the domain. certbot's NGINX plugin will reconfiguring NGINX and reload the config whenever necessary. 

Complete any additional certbot prompts to configure your HTTPS settings.

NOTE: Firewall configurations that block access over port 80 and 443 are a common source of certbot failures. Make sure your Host firewall (and any other firewalls) are properly configured to allow port 80 and port 443 access for inbound remote requests.

### Step 4 - Access your Server

You should now be able to access your server via HTTPS and see a valid certificate.

### Step 5 - Exit the Container

You're done. Type the following to exit the NGINX container:

```bash
exit
```

### Step 6 - Routinely Renew the Certificate

Re-run certbot every ninety days to renew the certificate by typing the following:

```bash
docker exec -it low_nginx_1 /bin/sh
certbot --nginx -d example.com
```

Alternatively, allow certbot to automatically renew by typing the following:

```bash
systemctl status certbot.timer
```



