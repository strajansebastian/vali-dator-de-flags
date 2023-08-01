FROM ghcr.io/yannh/kubeconform:latest as kubeconform

FROM ubuntu:22.04

RUN mkdir -p /app

WORKDIR /app

RUN apt update && \
    apt install -y python3-pip && \
    rm -rf /var/cache/apt

RUN mkdir -p /config

COPY --from=kubeconform /kubeconform /app/

COPY src/requirements.txt /app/

RUN pip3 install -r /app/requirements.txt
RUN pip3 install --upgrade kubernetes

COPY src /app

# cache samples for kubeconform in case internet connection is missing 
ARG KUBECONFORM_USE_CACHE=false \
    KUBECONFORM_USE_TLS=false
ENV KUBECONFORM_USE_CACHE=$KUBECONFORM_USE_CACHE \
    KUBECONFORM_USE_TLS=$KUBECONFORM_USE_TLS

COPY k8s-samples /app/k8s-samples
RUN bash /app/k8s-samples/init-kubeconform.sh
# end cache generation

ENV KUBECONFIG=/config/.kube-config \
    VALIDATOR_PATH_CONFIG_FLAGS=/config/config-flags.yaml

CMD python3 /app/app.py
