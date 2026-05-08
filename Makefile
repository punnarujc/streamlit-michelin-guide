.PHONY: setup run clean

setup:
	uv init --app --no-workspace || true
	uv add streamlit duckdb plotly pandas numpy kagglehub

run:
	uv run streamlit run app/app.py

clean:
	rm -rf .venv
	rm -rf .uv
