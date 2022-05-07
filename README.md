# Test task bewise.ai | Instructions for setting up and launching
## Сlone the git repository and change to the project directory
```
git clone https://github.com/Cripson23/bewise.ai.git & cd bewise.ai
```
## Building containers images
```
docker-compose build
```
## Running containers
```
docker-compose up -d
```
## Execute only after the first launch of containers
### Go to the command line for the flask-app container
```
docker exec -it flask-app bash
```
### Creating a migration repository
```
flask db init
```
### Generating an initial migration
```
flask db migrate -m "Initial migration."
```
### Applying the migration to the database
```
flask db upgrade
```
```
exit
```
## API Info
### Request URL: http://127.0.0.1:8000/questions [Method: POST]
### JSON Params: questions_num (required) [type: integer; min value = 1; max_value = 100]
### Example
JSON data example:
```
{
    "questions_num": 100
}
```
Response data example:
```
{
    "answer": "mistletoe",
    "created_at": "Sat, 07 May 2022 17:32:49 GMT",
    "question": "Before we kissed under it, ancient Europeans believed this plant held magic powers to bestow life & fertility"
}
```
