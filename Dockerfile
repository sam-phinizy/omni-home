ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN pip install uv
COPY pyproject.toml uv.lock /code/
RUN uv sync
COPY . /code

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","omni_home.wsgi"]
