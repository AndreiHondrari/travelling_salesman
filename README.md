# The travelling salesman
Sample web service determining the cheapest path when visiting N locations

----

![travelling salesman](./readme_misc/travelling_salesman.png)

----

## Jumpstart

In order to start using the service proceed with the following steps:
* Open a terminal
* Navigate to the root directory of the project
* Call `./jumpstart.sh`

This command will:
* Start all the necessary docker containers
* Perform the database migrations for the (web) Django container
* Create a superuser
* Open the intro page (http://localhost:8005) in the browser

## Architecture

### Overview
The whole ecosystem of the project consists of:
* optimisation_service - the service that does the heavy work of calculating the shortest path
* web - a Django based web application that acts as a proxy for calling the optimisation service
* db - a Postgresql container
* bugsbunny - a RabbitMQ message broker (with management included)
* celery - the web container asynchronous tasks worker
* flower - an extra management dashboard for the RabbitMQ broker

### Interaction between the web, web async tasks and the optimisation service

![interaction between main services](./readme_misc/interaction_1.png)

## Credits
Icons made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com/)
