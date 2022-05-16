# Flask-RESTful API Challenge: User service 

This project shows one of the possible ways to implement RESTful API server for Challenge: User service.

There are implemented three models: User , PhoneNumber and Email.

Main libraries used:

1. Flask-RESTful - restful API library.

2. Flask-SQLAlchemy - adds support for SQLAlchemy ORM.

Project structure:
```
.
├── README.md
├── app.py
├── requirements.txt
└── test.py
```


* app.py - flask application initialization.
* test.py - unittest for the Flask application
## Running 

1. Clone repository.
2. pip install -r requirements.txt
4. Start server by running python app.py runserver

## Usage
### Users endpoint
POST http://127.0.0.1:5000/users

REQUEST
```json
{
	"firstName": "batman" , 
    "lastName": "Robin"
}
```
RESPONSE
```json
    {
    "id": 1, 
    "lastName": "Robin", 
    "firstName": "batman", 
    "emails": [], 
    "phoneNumbers": []
    }
```
PUT http://127.0.0.1:5000/users/1

REQUEST
```json
{
	"firstName": "change_firstname"
}
```
RESPONSE
```json
{
    "id": 1, "lastName": "Robin",
     "firstName": "change_firstname",
     "emails": [], 
    "phoneNumbers": []
}
```

GET http://127.0.0.1:5000/users

RESPONSE
```json
{"count": 2, "users": [{"id": 1, "lastName": "Robin", "firstName": "change_firstname", "emails": [{"id": 1, "email": "change@email.id"}], "phoneNumbers": [{"id": 1, "number": "6554455"}]}, {"id": 2, "lastName": "Robin", "firstName": "batman", "emails": [], "phoneNumbers": []}]}
```
GET http://127.0.0.1:5000/api/users/2
```json
{"id": 2, "lastName": "Robin", "firstName": "batman", "emails": [], "phoneNumbers": []}]}
```



Email and PhoneNumber endpoint is similar to Users endpoint.


run test.py for unitest of the endpoints