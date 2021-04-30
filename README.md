# Description

This is an e-commerce site, built by a 6 member team for Software Engineer
 class in National Technical University of Athens. You can buy tickets for
children events or create an event for your own.


## Deploy:

#### Local deployment of Docker / Django. Follow steps

1. [Download Docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository)  
Contains all steps until running hello-world.
2. [Download Docker Compose](https://docs.docker.com/compose/install/)
3. git pull το lorem-ipsum repo
4. sudo docker-compose up
5. In localhost:8000, django should be available


## Development

### How to run server 

`sudo docker-compose up`

### How to run manage.py commands inside docker

`sudo docker-compose run web python3 loremipsum/manage.py ...`

### How to create user for django admin

`sudo docker-compose run web python3 loremipsum/manage.py createsuperuser`


### How to apply create changes

`sudo docker-compose run web python3 loremipsum/manage.py makemigrations`


### How to apply model changes

`sudo docker-compose run web python3 loremipsum/manage.py migrate`

---

## Deployment

`sudo ./loremipsum.sh
`

 After database is populated, following users should exist:
 
 
#### ADMIN
 
 Username: admin   Password: loremipsum2018!
 
 
#### PROVIDERS
 
 Username: paliatsos   Password: provider
 
 Username: paidikixara   Password: provider
 
 Username: partyanimal   Password: provider


#### PARENTS
 
 Username: george_stathis   Password: parent
 
 Username: nikos_pappas   Password: parent
