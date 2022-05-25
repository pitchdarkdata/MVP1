FROM nikolaik/python-nodejs:python3.10-nodejs18

USER pn
WORKDIR /home/pn/app

COPY requirements.txt reviewer.py probotmvp1.js ./

RUN pip3 install -r requirements.txt


CMD ["node", "probotmvp1.js"]
