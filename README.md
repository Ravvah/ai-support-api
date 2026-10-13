# AI Support API

To launch the api service :

```bash
uv run uvicorn app.main:app
```

To run the tests :

```bash
uv run pytest
```

To run the lint-checks and lint format :

```bash
uv run ruff check .
uv run ruff format .
```

To run type-checks :

```bash
uv run pyright
```