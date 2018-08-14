# API docs

For this test i have created a very simple API that follows the *REST CRUD* principle,
which means that each endpoint is manipulated by using HTTP GET,POST,PUT,DELETE methods.


## Data format

Each request returns JSON data (except for when internal server error occurs). The format of returned data is:


```
{
	"success": true|false,
    "data": null|any,
    "error": null|string
}
```

`success` is always present while `error` and `data` are present only when the request failed or succeeded respectfully.


## Edges

Api consists of 3 edges:
 - api/providers
 - api/areas
 - api/query



### api/providers
This edge is used to read and write providers data. The basic syntax for using it is:

- Retrieve individual provider: `GET http://174.129.166.53:8000/api/providers/<provider_id>`(provider id is returned from write op)
- Write data: `POST|PUT http://174.129.166.53:8000/api/providers?name=Named&email=provider@email.com&phone=12341234&lang=en-us&currency=bam`
- Delete data: `DELETE http://174.129.166.53:8000/api/providers/<provider_id>`

All of the above methods return the provider data in `data` field of the response object except for delete which returns null.

### api/areas
This edge is used to read and write areas data. The basic syntax for using it is:

- Retrieve individual area: `GET http://174.129.166.53:8000/api/areas/<provider_id>/<area_id>`(provider id is returned from provider write op and area_id is returned from area write op)
- Write data: `POST|PUT http://174.129.166.53:8000/api/areas/<provider_id>?name=AreaName&price=1.23&point=polygon=(0,0)_(0,50)_(50,50)_(50,0)_(0,0)`
- Delete data: `DELETE http://174.129.166.53:8000/api/areas/<provider_id>/<area_id>`

All of the above methods return the area data in `data` field of the response object except for delete which returns null.

### api/query
This edge is used to query for available providers in the area.

It has a single method: ```GET http://174.129.166.53:8000/api/query/<lat>/<lon>``` and it returns a list of area data fields.
