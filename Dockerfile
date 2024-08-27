FROM python:3.10
WORKDIR /app
COPY requirements.txt req.txt
RUN pip3 install -r req.txt 
COPY . . 
EXPOSE 8080
CMD ["python3", "app.py"]