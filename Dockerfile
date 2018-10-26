FROM python:3.6

RUN git clone https://github.com/agudelotmateo/forecasting.git
WORKDIR forecasting
RUN python3 -m pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:$PORT app:app
