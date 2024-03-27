
## Run the service
`docker-compose build`  
`docker-compose up`

## Endpoints
- `CREATE USER [POST]`  
localhost:5001/api/user/create  
Request parameters  
[first_name,
last_name,
email,
password,
phone_number,
uni_number,
user_role]


- `GET ALL USERS [GET]`  
localhost:5001/api/users  

- `USER LOGIN [POST]`   
localhost:5001/api/user/login  
Request parameters  
[email,
password]

- `USER LOGOUT [POST]`  
localhost:5001/api/user/logout  

- `CHECK IF USER EMAIL EXISTS [GET]` 
localhost:5001/api/user/\<email>/exists  
Returns  
`200 OK` { "result" : true }  
`404 NOT FOUND` { "message" : "Cannot find email" }



- `GET LOGGED IN USER DETAILS [GET]` 
localhost:5001/api/user
