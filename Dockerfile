FROM  python:3.10-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install requirements.txt
COPY . .
FROM python:3.1-alpine AS bare
COPY --from=base /app /app
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
