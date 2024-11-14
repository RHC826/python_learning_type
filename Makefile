uncommited:
	@NR=$$(git status -s | awk '{print $$2}' | wc -l); \
	FILES=$$(git status -s | awk '{print $$2}') ;\
	if [ "$$NR" -gt 0 ]; then \
		echo $${FILES};\
	fi

format:
	@uv run ruff format ./src/*py

version:
	@python -V
test:
	@cd src; \
	python -m unittest discover
