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
uvicorn app:app --reload
```

## Adding more cities

### Refreshing GBFS APIs

More and more APIs support the (wonderful) [GBFS](https://mobilitydata.org/gbfs-and-shared-mobility-data-policy-in-europe/) [standard](https://gbfs.mobilitydata.org/). Running the `discover_gbfs_apis.py` script will refresh that list.

### Manually adding a city

1. Edit `cities.txt`
2. Edit `fetch_stations.py`
3. Edit `fetch_weather.py`
4. Edit `adapters.py`
5. Edit `app.py`

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
