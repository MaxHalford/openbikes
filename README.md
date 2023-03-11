# OpenBikes

Collecting and publishing bike sharing data.

## Development

### Setup

```sh
pyenv install -v 3.10
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create an `.env` file:

```sh
GITHUB_TOKEN=
JCDECAUX_API_KEY=
```

### Test the Docker image locally

```sh
docker build . -t openbikes && docker run --env-file .env openbikes python /code/fetch_stations.py
```

### Running the API locally

```sh
uvicorn api:app --reload
```

## Process for adding a city

1. Add to `cities.txt`
2. Add to `fetch_stations.py`
3. Add to `fetch_weather.py`
4. Add to `adapters.py`

## Deployment

```sh
docker buildx build --platform linux/amd64,linux/arm64 --push -t ghcr.io/maxhalford/openbikes:latest .

export RAW_GITHUB_TOKEN=
export RAW_JCDECAUX_API_KEY=
export GITHUB_TOKEN=`echo -n $RAW_GITHUB_TOKEN | base64`
export JCDECAUX_API_KEY=`echo -n $RAW_JCDECAUX_API_KEY | base64`
cat cronjob.yaml | envsubst | kubectl apply -f -

k9s
```
