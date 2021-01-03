FROM python:3.8

WORKDIR /rest_api.py
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["rest_api.py"]