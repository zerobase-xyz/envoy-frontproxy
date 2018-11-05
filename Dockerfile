FROM envoyproxy/envoy:latest

RUN apt-get update && apt-get -q install -y \
    curl

COPY  ./front-envoy.yaml /etc/front-envoy.yaml

EXPOSE 80
EXPOSE 8001

CMD /usr/local/bin/envoy -c /etc/front-envoy.yaml --service-cluster front-proxy
