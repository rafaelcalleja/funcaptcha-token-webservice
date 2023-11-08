WHISPER_IMAGE ?= onerahmet/openai-whisper-asr-webservice
WHISPER_TAG ?= latest
ASR_MODEL ?= tiny
ASR_ENGINE ?= openai_whisper

.PHONY: run
run: build
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose up -d --force-recreate

.PHONY: build
build:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose --env-file /dev/null build

.PHONY: stop
stop:
	docker compose down

destroy:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose down --rmi local -v
	docker rmi $(DOCKER_IMAGE)

.PHONY: logs
logs:
	docker compose logs -f

push:
	docker push $(DOCKER_IMAGE)

