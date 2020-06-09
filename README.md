#### Web Scrapper
Built on top of flask and flask restful python package, this is a rest api to scrape web pages to look for apartments listing.
##### How to install
* Requirements
    * Docker
    * Docker-compose

Go to the root project directory and  run
```docker-compose up```
in the terminal output you will see the url on which it's running.

##### API Endpoints
```
GET /api/apartments/<int:zipcode>
POST /api/apartments/       --data '{"zipcode": "123","bathroom": 1, "bedroom": 1}'