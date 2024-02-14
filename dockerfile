FROM python:3.12.0

WORKDIR /PONG

COPY . /PONG

RUN pip install -r requirements.txt

CMD touch highscore.json && echo '{"highscore": 0}' > highscore.json && python main.py