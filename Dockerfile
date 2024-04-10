FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000

COPY pyproject.toml poetry.lock ./

RUN apk add gcc python3-dev musl-dev linux-headers

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN chmod +x start.sh

CMD ["poetry", "run", "task", "dev"]