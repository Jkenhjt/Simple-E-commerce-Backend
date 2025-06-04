ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /fastapi

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY ./app /fastapi
COPY ./alembic /fastapi

# Copy aioredis fix for python 3.12
COPY ./fix_aioredis_python3.12/exceptions.py /usr/local/lib/python3.12/site-packages/aioredis/.

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--workers=4"]