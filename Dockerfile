FROM python:3.10-alpine 
# Must be less than 3.11, due to telnetlib deprecation

WORKDIR /app
ADD ./requirements.txt /app/
RUN pip3 install -r requirements.txt
ADD ./telnet_client.py /app/

ENV DB_HOST "localhost"
ENV DB_PORT "27017"
ENV DB_USER "root"
ENV DB_PASS "secure"
ENV DB_NAME "cwskimmer"

ENV SKIMMER_HOST "localhost"
ENV SKIMMER_PORT "7301"
ENV SKIMMER_USER "DB2CW"
ENV SKIMMER_PASS ""

ENTRYPOINT [ "./telnet_client.py" ]