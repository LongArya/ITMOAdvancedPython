FROM python:3.10

WORKDIR /root

RUN apt-get update && apt-get install -y texlive \
                    texlive-latex-base \
                    texlive-fonts-recommended \
                    texlive-fonts-extra \
                    texlive-latex-extra 


COPY ./task2_requirements.txt /root/
RUN pip3.10 install -r /root/task2_requirements.txt

COPY . /root/

CMD python3.10 task1.py
