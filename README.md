# CluePoints PoC

Provides API endpoint for a homebanking system.

## Run Locally

Activate a python3.8 (or higher) virtualenv with the command `python3.8 -m venv "virtualenv"` and activate it.

Then you can install the dependencies with the command `python -m pip install -r HomeBanking\requirements.txt`.

Run the database

```
cd ./database

docker-compose up -d
```

Once everything is installed, you can run the fastapi app locally by doing :

```
cd ./HomeBanking

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be running on `localhost:8000`. The API documentation is accessible on `localhost:8000/docs`.

## Run Unit Tests

You can run the unit tests with command `pytest`.

```
cd ./HomeBanking
pytest
```


