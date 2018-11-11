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

@app.route('/app/<service_number>')
def hello(service_number):
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\n'.format(SERVICE_NAME,
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname())))

@app.route('/app/<service_number>/view', methods=['GET'])
def redis_view(service_number):
    times = conn.get('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname()),
                                    int(times)))

@app.route('/app/<service_number>/incr', methods=['GET'])
def redis_incr(service_number):
    times = conn.incr('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname()),
                                    int(times)))


@app.route('/app/<service_number>/init', methods=['GET'])
def redis_init(service_number):
    conn.set('carats', 0)
    times = conn.get('carats')
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\napp {}times\n'.format(SERVICE_NAME,
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname()),
                                    int(times)))

if __name__ == "__main__":
    app.run()
