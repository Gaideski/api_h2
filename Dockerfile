FROM python:3.10

COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

WORKDIR  /app
ADD . .
COPY requeriments.txt .
COPY start.sh .
RUN chmod +x start.sh
RUN pwd && ls

RUN apt-get update && apt-get upgrade -y
RUN pip install --no-cache-dir -r requeriments.txt 

# creating ssh access to container
RUN apt-get install openssh-server supervisor -y
RUN mkdir /var/run/sshd
RUN echo 'root:pass123' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ./start.sh

EXPOSE 22
EXPOSE 5000

