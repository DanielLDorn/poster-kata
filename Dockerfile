# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1

# set WORKDIR
WORKDIR /code

# Install requirements
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD [ "python", "src/main.py" ]
CMD [ "python", "src/tests.py" ]