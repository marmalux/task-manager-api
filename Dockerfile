FROM python:3.13.1-slim-bookworm

RUN apt-get update && \
    apt-get install -y libaio1 wget unzip && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://download.oracle.com/otn_software/linux/instantclient/2326000/instantclient-basic-linux.x64-23.26.0.0.0.zip && \
    unzip instantclient-basic-linux.x64-23.26.0.0.0.zip -d /opt/oracle && \
    rm instantclient-basic-linux.x64-23.26.0.0.0.zip

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_23_26

WORKDIR /app 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn","main:app","--host", "0.0.0.0", "--port", "8000"]
