These instructions are for Ubuntu Linux 22.04

# Open a new issue and request to be onboarded

Open a new issue with the following:

1. Your Github account name
2. Your IP address

Jake will send you an envfile called `.env.remote.dev` on slack, which contains credentials to login to the RDS test database, and add your IP address to the AWS whitelist. Put .env.remote.dev in streetlives-api project directory (after cloning the project - see below). 

Note: In the future, we will provide seed data in the repository so that we can eliminate this step.

# Fetch all of the source code

```
mkdir -p ~/workspace/streetlives
git clone git@github.com:streetlives/yourpeer.nyc.git
git clone https://github.com/streetlives/streetlives-api
git clone git@github.com:streetlives/streetlives-web.git
```

# Setup local postgres 

## Install Postgres 

```
sudo apt install postgresql postgresql-14-postgis-3
```


## Setup postgres for local login with password authentication 

Make sure you can login to your local postgresql database using a password for authentication. Something like this:

```
local   all             streetlives                                md5
```

## Create the Streetlives user, streetlives database, and the test database 

Login to database as administrator. Here's how I do this on ubuntu:

```
sudo bash
su postgres
psql
```

By default, in ubuntu, this will allow you to login to the database without a specifying a password. 

Then, as postgres user, from psql shell:

```
create user streetlives with password 'password';
create database streetlives_prod with owner streetlives;
```

Logout and log back into the new database with user streetlives:

`psql -d streetlives_prod`

```
create extension postgis  schema public;
```

## Load a copy of the data into local Streetlives database 

As your user (not postgres user), cd in project directory streetlives-api. You will dump a copy of the test database, then restore it to your local:

```
source .env.remote.dev
./scripts/backup.sh
sed -i 's/devuser/streetlives/g' prod-`date +%F`.sql
source .env.local
./scripts/restore-from-sql.sh
```

# Run local applications 

## [streetlives-api](https://github.com/streetlives/streetlives-api): 

```
npm install
source .env.local
PORT=3001 npm start
```


Open http://localhost:8000/

## [streetlives-web](https://github.com/streetlives/streetlives-web): 

```
nvm use v16
npx yarn install
REACT_APP_API_URL=http://localhost:3001 npm start
```


Visit http://localhost:3000/find and verify that the locations load (blue pins appear on the map).


## yourpeer.nyc: 

Put this in the .env file in your root directory:

```
DB_USER_AWS=streetlives
DB_PASSWORD_AWS=password
DB_NAME_AWS=streetlives_prod
DB_HOST_AWS=localhost
DB_PORT_AWS=5432
```

Then run:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
GO_GETTA_PROD_URL=http://localhost:3001 python manage.py runserver
```

Visit http://localhost:8000/locations and verify that the locations load (yellow pins appear on the map).

# Tools 

## Squirrel SQL 

```
~/.local/squirrel-sql-4.2.0/squirrel-sql.sh
```

Connect to your local database with:

```
URL: jdbc:postgresql:streetlives_prod
Username: streetlives
Password: password
```

# Deployment

Push to `env/test` branch to deploy to https://test.yourpeer.nyc/

Push to `env/live` branch to deploy to https://yourpeer.nyc/

# Contributing

Please open a pull request. Ensure that each source file includes the correct license header template, like this: 

```
Copyright (c) 2024 Streetlives, Inc., [your name]

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
```
