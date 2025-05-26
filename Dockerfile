FROM python:3.12-slim

WORKDIR /src

COPY . /src

RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]