FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy backend files
COPY ./app /app/app/
COPY ./saf.json /app/creds/saf.json
ENV GOOGLE_APPLICATION_CREDENTIALS /app/creds/saf.json

# Run backend
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
