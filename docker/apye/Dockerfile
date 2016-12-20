FROM debian:jessie

MAINTAINER Adrián Álvarez

#Sincronizamos el indice e instalamos dependencias
RUN apt-get update -y
RUN apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8
ENV LANG es_ES.utf8
RUN apt-get update -y &&  apt-get install -y libpq-dev python3-dev python3-pip git

#Descargamos apliccaión e instalamos requisitos con pip
RUN git clone https://github.com/adalsa91/APYE.git
WORKDIR /APYE
RUN pip3 install -r requirements.txt


#Fijamos el punto de entrada y el comando a ejecutar
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "--host" , "0.0.0.0"]
