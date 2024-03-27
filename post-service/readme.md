## Run the service
`docker-compose build`  
`docker-compose up`

## Endpoints
`Initial-post`  
localhost:5002/api/initial-post  

`Initial-comment`  
localhost:5002/api/initial-comment  

- `GET ALL POSTS [GET]`    
localhost:5002/api/posts  

- `GET POST BY ID [GET]`  
localhost:5002/api/post_id 

- `GET ALL COMMENTS [GET]`
localhost:5002/api/comments

- `GET POST COMMENTS [GET]`
localhost:5002/api/post_id/comment_id

- `CREATE POST [POST]`  
localhost:5002/api/new-post
Request parameters  
[
title,
category,
content]

- `DELETE POST [POST]`
localhost:5002/api/post_id/delete  

- `DELETE COMMENT [POST]`  
localhost:5002/api/post_id/comment_id/delete