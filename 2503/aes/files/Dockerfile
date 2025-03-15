FROM python:3.9
RUN apt update && apt install -y openssl socat && \
	rm -rf /var/lib/apt/lists/*

COPY /make_certs.sh ./start_task.sh /app/

WORKDIR /app/

RUN bash ./make_certs.sh

RUN pip3 install pycrypto

RUN chmod +x start_task.sh

COPY ./server.py /app/

RUN echo "$(cat /dev/urandom | head -c 64 | md5sum -b | head -c 32)$(cat /dev/urandom | head -c 64 | md5sum -b | head -c 26)" > /app/flag.txt

CMD socat OPENSSL-LISTEN:30001,reuseaddr,fork,cert=/app/server.pem,cafile=/app/client.crt,verify=0 EXEC:./start_task.sh