run:
	poetry run uvicorn api.main:app --reload

test:
	poetry run pytest tests/ -v

fmt:
	poetry run black engine/ api/ tests/
	poetry run ruff check engine/ api/ tests/ --fix

score:
	poetry run python -c "from engine.scorer import score_player; print('engine ok')"

push:
	git add . && git commit -m "$(m)" && git push

install:
	poetry install

claude:
	claude
