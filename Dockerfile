FROM arm64v8/python:3.9-alpine
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8100
CMD ["python3", "./main.py"]