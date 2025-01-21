# Copyright (C) 2023 Axis Communications AB, Lund, Sweden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# USAGE:
# python3 ./model_performance_tester.py -m <MODEL_PATH> -c <CHIP> -i <IP> -u <USER> <PASS>

import paramiko
import os
import argparse
import re

chipset = {
        'CPU': 'cpu-tflite',
        'A9-DLPU': 'a9-dlpu-tflite',
        'A8-DLPU': 'axis-a8-dlpu-tflite',
        'A7-GPU': 'axis-a7-gpu-tflite',
        'A7-TPU': 'google-edge-tpu-tflite',
        'CV25': 'ambarella-cvflow'
    }

def run_speed_test(DEVICE_IP, PORT, DEVICE_USERNAME, DEVICE_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP):

    # Take model name from path
    model_name = MODEL_PATH.split('/')[-1]

    device_model_location = os.path.join('/tmp/', model_name)
    print('Testing model:', model_name)
    print('Connecting to device at', DEVICE_IP, 'and port', PORT)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(DEVICE_IP, username=DEVICE_USERNAME, password=DEVICE_PASSWORD, port=PORT)

    print('Loading Model...')
    sftp = ssh.open_sftp()
    sftp.put(MODEL_PATH, device_model_location)
    sftp.close()

    print('Starting Test...')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'larod-client -R ' + str(TEST_DURATION) + ' -p' +
        ' -c ' + chipset[CHIP] +
        ' -g ' + device_model_location +
        ' -i "" ')
    time = -1
    print('Parsing the output...')
    try:
        out = list(filter(lambda k: 'Mean execution time for job:' in k, ssh_stdout))[0]
        print(out)
        time = re.findall(r'\d+\.\d+', out)[-1]
    except:
        print('Something went wrong:')
        print(ssh_stdout.read().decode('utf-8'))
        print(ssh_stderr.read().decode('utf-8'))


    print('Cleaning...')
    ssh.exec_command('rm ' + device_model_location)
    ssh.exec_command('rm *out[0-9]')
    ssh.close()

    return time

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a speed test of a model on the device')
    parser.add_argument('-m', '--model_path', type=str, help='Model path', required=True)
    parser.add_argument('-d', '--test_duration', type=int, help='Test duration (iterations)', default=100)
    parser.add_argument('-c', '--chip', type=str, choices=chipset.keys(), help='Chipset', required=True)
    parser.add_argument('-i', '--device_ip', type=str, help='Device IP', required=True)
    parser.add_argument('-p', '--device_port', type=int, help='Device port for ssh', default=22)
    parser.add_argument('-u', '--device_credentials', nargs=2, type=str, help='Device username and password divided by space', required=True)


    args = parser.parse_args()

    MODEL_PATH = args.model_path
    TEST_DURATION = args.test_duration
    CHIP = args.chip
    DEVICE_IP = args.device_ip
    DEVICE_PORT = args.device_port
    DEVICE_USERNAME = args.device_credentials[0]
    DEVICE_PASSWORD = args.device_credentials[1]

    run_speed_test(DEVICE_IP, DEVICE_PORT, DEVICE_USERNAME, DEVICE_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP)
