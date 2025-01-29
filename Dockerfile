FROM python3:13

RUN pip install poetry

COPY ./pyproject.toml ./poetry.toml /app/

WORKDIR /app

RUN poetry install

COPY ./app /app/app

ENV PYTHONPATH=/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
