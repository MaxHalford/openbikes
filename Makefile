SHELL := bash
IMAGE  = ghcr.io/MaxHalford/openbikes:latest
ARGS   = --builder=kube --platform linux/amd64,linux/arm64 -t ${IMAGE}

login:
	. <(pass export/GITHUB_TOKEN/package-writer-docker-login)

build:
	docker buildx build ${ARGS} .

push: login
	docker buildx build --push ${ARGS} .
