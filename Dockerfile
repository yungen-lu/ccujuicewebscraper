FROM python:slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./main.py .
COPY ./.env .
# CMD [ "python3", "-m" , "main.py"]

