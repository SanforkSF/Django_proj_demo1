# our base image
FROM python:3
# upgrade pip
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# tell the port number the container should expose
EXPOSE 5000
# run the application
CMD ["python", "app.py"]
