# OpenBikes

Collecting and publishing bike sharing data.

## Development

```sh
pyenv install -v 3.10
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Deployment

```sh
make login
make build
make push
```

```sh
k9s
```
