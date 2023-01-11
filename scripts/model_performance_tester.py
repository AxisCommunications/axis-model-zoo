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
# python3 ./model-performance-tester.py --model_path <MODEL_PATH> --chip <CHIP> --camera_ip <IP> --camera_password <PASS>

import paramiko
import os
import argparse
import re

chipset = {
        'CPU': 'cpu-tflite',
        'A8-DLPU': 'axis-a8-dlpu-tflite',
        'A7-DLPU': 'google-edge-tpu-tflite',
        'CV25': 'ambarella-cvflow'
    }

def run_speed_test(CAMERA_IP, PORT, CAMERA_USERNAME, CAMERA_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP):

    # Take model name from path
    model_name = MODEL_PATH.split('/')[-1]

    camera_model_location = os.path.join('/tmp/', model_name)
    print('Testing model:', model_name)
    print('Connecting to camera at', CAMERA_IP, 'and port', PORT)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CAMERA_IP, username=CAMERA_USERNAME, password=CAMERA_PASSWORD, port=PORT)

    print('Loading Model...')
    sftp = ssh.open_sftp()
    sftp.put(MODEL_PATH, camera_model_location)
    sftp.close()

    print('Starting Test...')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        'larod-client -R ' + str(TEST_DURATION) + ' -p' +
        ' -c ' + chipset[CHIP] +
        ' -g ' + camera_model_location +
        ' -i ')
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
    ssh.exec_command('rm ' + camera_model_location)

    ssh.close()
    return time

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a speed test of a model on the camera')
    parser.add_argument('--model_path', type=str, help='Model path', default='../models/efficientdet_lite0_320_ptq.tflite')
    parser.add_argument('--test_duration', type=int, help='Test duration (iterations)', default=1000)
    parser.add_argument('--chip', type=str, choices=chipset.keys(), help='Chipset', default='CPU')
    parser.add_argument('--camera_ip', type=str, help='Camera IP')
    parser.add_argument('--camera_port', type=int, help='Camera port for ssh', default=22)
    parser.add_argument('--camera_username', type=str, help='Camera Username')
    parser.add_argument('--camera_password', type=str, help='Camera Password')

    args = parser.parse_args()

    MODEL_PATH = args.model_path
    TEST_DURATION = args.test_duration
    CHIP = args.chip
    CAMERA_IP = args.camera_ip
    CAMERA_PORT = args.camera_port
    CAMERA_USERNAME = args.camera_username
    CAMERA_PASSWORD = args.camera_password

    run_speed_test(CAMERA_IP, CAMERA_PORT, CAMERA_USERNAME, CAMERA_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP)
