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

```sh
docker build . -t openbikes && docker run openbikes
```

### Running the API locally

```sh
uvicorn api:app --reload
```

### Process for adding a city

1. Add to `cities.txt`
2. Add to `fetch_stations.py`
3. Add to `fetch_weather.py`
4. Add to `adapters.py`

## Deployment

```sh
make login
make build
make push
```

```sh
k9s
```
