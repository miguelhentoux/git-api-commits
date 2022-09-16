.PHONY: local/run
local/run:
	poetry run uvicorn api.main:app --reload --port=8000

.PHONY: local/jupyter
local/jupyter:
	poetry run jupyter notebook