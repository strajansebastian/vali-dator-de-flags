import datetime
import yaml
import random
import re
import secrets
import subprocess
import string


def all_questions(section, data_input):
    result_msg = { 'message': 'NO flag for you here! https://t.ly/Tex82 . You need to have a valid challange link!' }

    flags_config_file = '/config/config-flags.yaml'

    flags_config = None
    with open(flags_config_file, 'r') as file:
        flags_config = yaml.safe_load(file)

    for fc_sec in flags_config['section']:
        if fc_sec['name'] != section:
            continue

        if fc_sec['type'] == 'k8s_yaml_check_fields':
            valid_all = True
            for validator in fc_sec['validators']:
                if validator['type'] == 'k8s':
                    k8s_validation = validate_k8s_config(section, data_input)
                    result_msg['message'] = k8s_validation['message']

                    if k8s_validation['valid'] == False:
                        valid_all = False
                        break

                elif validator['type'] == "k8s_field":
                    valid_k8s_filed = check_k8s_field(
                        k8s_validation['k8s_config'],
                        validator['field'],
                        validator['operation'],
                        validator['expect']
                    )

                    if valid_k8s_filed == False:
                        valid_all = False

            if valid_all == False:
                if random.random() < int(flags_config['config']['probability_flag_trick']):
                    result_msg['message'] += fc_sec['flag']['trick']
                else:
                    result_msg['message'] += fc_sec['flag']['info']
            else:
                result_msg['message'] += fc_sec['flag']['good']
        elif fc_sec['type'] == 'regular_expression':
            valid_all = True
            for validator in fc_sec['validators']:
                if validator['type'] == 'regex':
                    match = re.match(validator['pattern'], data_input)

                    if not match:
                        valid_all = False

            if valid_all == False:
                if random.random() < int(flags_config['config']['probability_flag_trick']):
                    result_msg['message'] += fc_sec['flag']['trick']
                else:
                    result_msg['message'] += fc_sec['flag']['info']
            else:
                result_msg['message'] += fc_sec['flag']['good']

    return result_msg

        
def check_k8s_field(k8s_config, field, operation, expect):
    try:
        result = k8s_config
        for item in field.split('.'):
            match = re.match(r'^~(\d+)', item)

            if match:
                number = int(match.group(1))
                result = result[number]
            else:
                result = result[item]

        if operation == 'equal':
            if result == expect:
                return True
        else:
            return Flase

    except:
        return False

    return False


def validate_k8s_config(section, yaml_text):
    result_msg = { 'message': 'res: ', 'valid': False, 'yaml_config': None, 'k8s_config': None, 'section': section}

    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))

    file_name = f"/tmp/k8s_val_config_{date_time}-{random_string}.yaml"
    write_data_to_file(file_name, yaml_text)

    if valid_yaml(file_name):
        result_msg['message'] += "YAML valid; "
        result_msg['yaml_config'] = yaml.safe_load(yaml_text)
    else:
        result_msg['message'] += "YAML invalid; "

    if valid_kubeconform(section, file_name):
        result_msg['message'] += "k8s valid; "
        result_msg['valid'] = True
        result_msg['k8s_config'] = result_msg['yaml_config']
    else:
        result_msg['message'] += "k8s invalid; "

    return result_msg


def write_data_to_file(file_name, data):
    with open(file_name, "w") as file:
        file.write(data)


def valid_kubeconform(section, file_name):
    command = f'/app/kubeconform -insecure-skip-tls-verify {file_name}'
    
    # Run the command and get the return code
    process = subprocess.run(command, shell=True)
    return_code = process.returncode
    
    # Check the return code and print the appropriate message
    if return_code == 0:
        print(f"Section: {section}; Command succeeded for file {file_name}!")
        return True
    else:
        print(f"Section: {section}; Command failed with return code: {return_code} for file: {file_name}")
        return False


def valid_yaml(file_name):
    try:
        with open(file_name, 'r') as f:
            yaml.safe_load(f)
    except yaml.YAMLError:
        return False

    return True

