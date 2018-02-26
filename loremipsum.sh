#!/bin/sh
mkdir ./loremipsum/media/
cp ./images/* ./loremipsum/media/
git submodule update --init
sudo docker-compose build
sudo docker-compose down -v
sudo docker-compose rm
#sudo docker-compose run web python3 loremipsum/manage.py loaddata db.json
sudo docker-compose run web python3 loremipsum/manage.py makemigrations tickets
sudo docker-compose run web python3 loremipsum/manage.py migrate

#trap "exit" INT
sudo docker-compose up -e

echo "OKKK"
sudo docker-compose rm
sudo docker-compose run web python3 loremipsum/manage.py loaddata db.json
sudo docker-compose up