# NE Exercise

This repository implements the exercise described below.

> Implement an application in the language of your choice that has:
> 
> 1) An HTTP endpoint that accepts a record and writes it to a local queue
> 2) A console command that processes the queue and saves the records to a SQLite database
> 
> The application code should be hosted on github and include a `README.md` with instructions for local deployment.
> Assume that the platform is already set up (e.g. npm exists), but the application dependencies are not (e.g. npm
> install).
> *** Deploy the app on AWS in an ec2 instance or an architecture of your choice ***
> 
> Include a test suite that tests the major interfaces:
> 
> * HTTP request/response
> * Queue read/write
> * Record transform
> * Writing to SQLite
> 
> Feel free to over-engineer at least one part of the application, such as:
> 
> * Using a framework for the HTTP endpoint (e.g. router, middleware, etc)
> * Using a filesystem abstraction layer for the queue
> * Using an ORM for writing to SQLLite
> 
> ### HTTP Endpoint
> 
> The endpoint should accept the following request:
> 
> ```
> POST /test-app/record
> Content-Type: application/json
> Authorization: Bearer good-token
> {
>     "timestamp": "2024-07-08T14:11:54Z", //string iso8601z
>     "value": 1.23 // float >= 0.0
> }
> ```
> 
> Authorization uses a `Bearer` token. Allow valid tokens to be configurable via a secrets file.
> 
> The data should be placed in local queue of your choice (filesystem, sqlite, etc) to be picked up by the Console
> Command.
> 
> #### Validation
> 
> * Bad tokens should return a 403
> * Negative values should return a 400
> * Invalid timestamps should return a 400
> * Include any other validations you deem appropriate (e.g. invalid content types, malformed bodies, on float values,
>   etc)
> 
> ### Console Command
> 
> The command shall:
> 
> * Fetch the record from the queue, transform it, and insert it into a SQLite table called `records`
> 
> | column  | type     | source record attribute |
> |---------|----------|-------------------------|
> | ts      | datetime | timestamp               |
> | val     | float    | value                   |
> | val_sqr | float    | value*value             |
> 
> * Accept an argument `limit` with an optional parameter `--verbose`
>     * `limit` defines how many records should be processed per invocation
>     * `--verbose` will dump the SQL used to insert the record
> 
> Wrap your entry point (language specific) in a bash script to be invoked as follows:
> 
> `$ ./test-app.sh <limit> [--verbose]`
> 
> Include a non-secret configuration option called `hard_limit` that caps the maximum records that can be processed per
> invocation. This should be alterable by configuration file.

## Set up

Get a copy of the repository
```
git clone git@github.com:yianniy/ne-exercise.git
cd ne-exercise
```

You will need to create a **.secrets** file. Each line of this file should contain an API key, which will be used as a bearer token during API authentication.

You may want to create a **.env** file. Right now, only one environmental variable is supported.

```
HARD_LIMIT=1000
```

## Running Locally

To run locally.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

## OpenApi Docs

http://127.0.0.1:8000/docs

## API Call

### Create an Queue Item

```
curl --location 'http://127.0.0.1:8000/queue' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your_token_from_.secrets>' \
--data '{
    "timestamp": "2024-07-11T15:05:36.726Z",
    "value": 1.4236833084935818
}'
```

### Read Queue
```
curl --location 'http://127.0.0.1:8000/queue' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

### Process Queue and create records

#### All Queue items
up to hard_limit

```
curl --location --request POST 'http://127.0.0.1:8000/records/' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

#### 10 Queue items

```
curl --location --request POST 'http://127.0.0.1:8000/records/10' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

#### Get SQL commands returned too

```
curl --location --request POST 'http://127.0.0.1:8000/records/10/1' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

### Read Records

```
curl --location 'http://127.0.0.1:8000/records/' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

## Unit Tests

From the project's root directory

```
pytest --disable-warnings
```

warnings are disabled, because they are all related to deprecated code within libraries being used.

## Straying from the exercise parameters.

##### A console command that processes the queue and saves the records to a SQLite database

The shell script was not created. Instead, an API call that accomplishes this result was implemented.

This is partly philosophical and partly a limit of the framework used.

- **philosophical**: I am not a fan of people logging onto production servers and doing things there. All sorts of thing can go wrong.

- **framework**: there is not easy way to run a function within fastapi without invoking the related API endpoint directly.

If one want a CLI to process records, a curl call will suffice.

```
curl --location --request POST 'http://127.0.0.1:8000/records/' \
--header 'Authorization: Bearer <your_token_from_.secrets>'
```

##### Error Handling

FastApi handles error codes returned out of the box. It is possible to overwrite the defaults, but it doesn't seem like a good idea.

- Bad tokens return a 401: Unauthorized, not 403
- Negative values return a 422: Unprocessable Entity, not 400
- Invalid timestamps return a 422: Unprocessable Entity, not 400
