FROM python:alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./main.py .
CMD [ "python3", "-m" , "main.py"]

