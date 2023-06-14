FROM ghcr.io/yannh/kubeconform:latest as kubeconform

FROM ubuntu:22.04

RUN mkdir -p /app

WORKDIR /app

RUN apt update && \
    apt install -y python3-pip && \
    rm -rf /var/cache/apt

RUN mkdir -p /config

COPY config-flags.yaml /config
COPY --from=kubeconform /kubeconform /app/

COPY src/requirements.txt /app/

RUN pip3 install -r /app/requirements.txt
RUN pip3 install --upgrade kubernetes

COPY src /app

ENV KUBECONFIG=/config/.kube-config

CMD python3 /app/app.py
