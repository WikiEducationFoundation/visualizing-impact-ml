# visualizing-impact-ml

## Installing required packages

apt-get install -y postgresql python3-pip python3-venv

## Setting up the venv

python3 -m venv wikivi_venv

source wikivi_venv/bin/activate

pip install utils mediawiki_dump psycopg2-binary

## Setting up Postgres

sudo su postgres

psql

(The following commands will be in the postgresql shell, you can use whatever username/password you want when creating a user. I recommend using your shell username as postgresql checks for it by default)

create user username with password 'password';

create database wikivi;
grant all privileges on database wikivi to
username;

\c wikivi

grant all on schema public to username;

exit

## Creating tables inside of the wikivi database

Make sure to use "su" to go back to your original user then run the following command:

psql -d wikivi -a -f firstcommand.sql

## Creating tables inside of the wikivi database
