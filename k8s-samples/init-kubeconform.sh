#!/bin/bash

TMP_KC_OPTIONS="";
if [[ "${KUBECONFORM_USE_CACHE}" == "true" ]]; then
    TMP_KC_OPTIONS="$TMP_KC_OPTIONS -cache /app/k8s-samples/ "
fi
if [[ "${KUBECONFORM_USE_TLS}" == "false" ]]; then
    TMP_KC_OPTIONS="$TMP_KC_OPTIONS -insecure-skip-tls-verify "
fi


/app/kubeconform $TMP_KC_OPTIONS /app/k8s-samples/pod.yaml
/app/kubeconform $TMP_KC_OPTIONS /app/k8s-samples/deployment.yaml
/app/kubeconform $TMP_KC_OPTIONS /app/k8s-samples/service.yaml
