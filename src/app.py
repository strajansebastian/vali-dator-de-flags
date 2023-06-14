from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException

import ctf_k8s_questions

app = Flask(__name__)

# Create a Kubernetes API client
api = client.ApiClient()

@app.route('/', methods=['GET', 'POST'])
def index():
    section = request.args.get('section')

    if request.method == 'POST':
        yaml_text = request.form['yaml_text']
        result_msg = ctf_k8s_questions.all_questions(section, yaml_text)

        return jsonify(result_msg)

    else:
        # Render the index.html template for the GET request
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
