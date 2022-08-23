FROM hwan001/pluto:0.2
MAINTAINER hwan001 "woghks7209@gmail.com"

RUN apt-get update
RUN apt-get install -y vim net-tools
RUN apt-get install -y python3-dev build-essential python3 python3-pip python3-venv
RUN apt-get install -y libmariadb-dev libmariadbclient-dev

COPY . /API-Server
WORKDIR /API-Server

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["run.py"]
