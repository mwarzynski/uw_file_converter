FROM python:3.6.3-alpine3.7
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
