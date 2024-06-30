FROM python:3.10-slim

WORKDIR /

COPY schenefelder-bote .
COPY ../db .

RUN pip install -r requirements.txt

CMD ["python", "__init__.py"]