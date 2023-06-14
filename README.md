### info
Application that can be used to validate kubernetes resources or commands
It can be extended to validate any type of input in the end.

Naming explanation of repo: a playfull way of saying vali owns you some flags
vali (short from Valentin)
dator (to own somebody somthing, you are indebted, like money for example; word in romanian)
de (of; word in romanian romanian)
flags (you may get this one)

### build & run
```
docker build -t vali-dator-de-flags:v0.1 .
docker push vali-dator-de-flags:v0.1

docker run -it --rm -p 8080:80 vali-dator-de-flags:v0.1
```

### doc

```
# you need to provide the right config in order to get the good flag as a reward

# supported operation types and subtypes
# 1.0 type: k8s_yaml_check_fields - checks if the provided string is a valid k8s yaml file
# 1.0.1 type: k8s - checks if valid yaml + valid k8s resource using kubeconform 
# 1.0.1.0 type: k8s_field - checks k8s yaml field (separated by . for dictionary, in case list prepend ~)
# 1.0.1.1 operation: equal - checks if value is equal to what is in expect

# 2.0 type: regular_expression - check if the provided string is matching the provided regexp validators
# 2.0.1 type: regex - a regular expression validator
# 2.0.1.1 pattern: 'some regex pattern' - pattern for match

```

### usage
```
# general config sample - for the doc from above
# more samples can be found in config-flags.yaml and in config-flags-verification.txt (how to validate fast the flags)

config:
  # between 0 and 1
  probability_flag_trick: 0.2
section:
 - name: vinsec-thisiswinedryinromania
   type: k8s_yaml_check_fields
   flag:
     good: FLAG-xyzwem8ahzae3Apoyie2aexaiZohK0en
     trick: FLAG-https://t.ly/Tex82
     info: FLAG-you-getting-closer-try-again
   validators:
     - type: k8s
     - type: k8s_field
       field: kind
       operation: equal
       expect: Pod
     - type: k8s_field
       field: metadata.name
       operation: equal
       expect: nginx
     - type: k8s_field
       field: metadata.annotations.can-i
       operation: equal
       expect: https://t.ly/7nhi
     - type: k8s_field
       field: spec.containers.~0.name
       operation: equal
       expect: nginx-web
     - type: k8s_field
       field: spec.restartPolicy
       operation: equal
       expect: OnFailure
     - type: k8s_field
       field: spec.containers.~0.image
       operation: equal
       expect: nginx:1.23.4
 - name: resourceseverywhere
   type: regular_expression
   flag:
     good: FLAG-xyzwozahxoa4aheeng5eeTieC3sae3Ie
     trick: FLAG-https://t.ly/Tex82
     info: FLAG-you-getting-closer-try-again
   validators:
     - type: regex
       pattern: '^kubectl\s+api-resources$'

# after you have the docker instance up and running you can check if the above config is working by
# 1.0 go to http://localhost:8095/?section=annonannot
# 1.1 provide sample
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  annotations:
    can-i: https://t.ly/7nhi
spec:
  containers:
  - name: nginx-web
    image: nginx:1.23.4
  restartPolicy: OnFailure

# 2.0 go to http://localhost:8095/?section=resourceseverywhere
# 2.1 provide sample
kubectl api-resources

```


# Extension and contribution
This platform can be easily extended for example by adding more operations or other validators.
Please submit any pull request and will review for merging.
