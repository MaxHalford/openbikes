FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py /code/
COPY cities.txt /code/
COPY .env /code/
RUN python /code/clone_data.py
