# arangodb-expore

## Preparation

Python version used: 3.9

Install requirements with ```pip install -r requirements.txt```

Create a file ".env" in the project root directory with the following content:
```commandline
ARANGO_URL="localhost"
ARANGO_PORT="8529"
ARANGO_HOST="http://${ARANGO_URL}:${ARANGO_PORT}"
ARANGO_USERNAME="root"
ARANGO_PASSWORD="example"
```

Run the docker service with ```docker-compose up -d```