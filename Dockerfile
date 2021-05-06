FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD ./src .

CMD [ "python", "automate.py" ]