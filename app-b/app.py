from flask import Flask
from flask import request
import socket
import os
import sys
import requests
import redis

app = Flask(__name__)

SERVICE_NAME = os.environ['SERVICE_NAME']
REDIS_HOST = os.environ['REDIS_HOST']
conn = redis.Redis(host=REDIS_HOST, port=6379)

# hostnameと環境変数に設定したSERVICE_NAMEを返す(aとかb)
@app.route('/app/<app_number>')
def hello(app_number):
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\n'.format(SERVICE_NAME,
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname())))

# redisのincrementされた数を表示する
@app.route('/app/<app_number>/view', methods=['GET'])
def redis_view(app_number):
    times = conn.get('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                                 socket.gethostname(),
                                                 socket.gethostbyname(socket.gethostname()),
                                                 int(times)))

# redisをincrementする
@app.route('/app/<app_number>/incr', methods=['GET'])
def redis_incr(app_number):
    times = conn.incr('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                                 socket.gethostname(),
                                                 socket.gethostbyname(socket.gethostname()),
                                                 int(times)))

# redisを初期化する
@app.route('/app/<app_number>/init', methods=['GET'])
def redis_init(app_number):
    conn.set('carats', 0)
    times = conn.get('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                                 socket.gethostname(),
                                                 socket.gethostbyname(socket.gethostname()),
                                                 int(times)))

if __name__ == "__main__":
    app.run()
