FROM python:3.8
USER root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY periodic_task.py .
RUN python3 -m pip install -U pip
RUN apt update

RUN apt install
RUN apt install squid -y
RUN apt install nginx -y
RUN apt install sarg -y
RUN rm -f /var/www/html/index.nginx-debian.html

CMD ["python3","periodic_task.py"]
