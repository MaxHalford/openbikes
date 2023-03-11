FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py /bin/
COPY cities.txt /bin/
COPY .env /bin/
CMD [ "python",  "/bin/fetch_stations.py", "--commit" ]
