import paramiko
import numpy as np
import os
import argparse

CAMERA_IP="172.25.71.119"
CAMERA_USERNAME="root"
CAMERA_PASSWORD="Pass"
MODEL_NAME="efficientdet_lite0_320_ptq.tflite"
MODEL_PATH="../Models/"
TEST_DURATION="1"
CHIP="CPU"
INPUT_SIZE=[3,320,320]


camera_model_location = os.path.join("/tmp/", MODEL_NAME)

chipset = {
    "CPU": "cpu-tflite",
    "A8-DLPU": "axis-a8-dlpu-tflite",
    "A7-DLPU": "google-edge-tpu-tflite",
    "CV25": "ambarella-cvflow"
}


parser = argparse.ArgumentParser(description='Run a speed test of a model on the camera')
parser.add_argument('--model_path', type=str, default=MODEL_PATH, help='Model path')
parser.add_argument('--model', type=str, help='Model name')
parser.add_argument('--size', type=int, nargs='+', help='Input size')
parser.add_argument('--test_duration', type=str, default=TEST_DURATION, help='Test duration')
parser.add_argument('--chip', type=str, default=CHIP, choices=chipset.keys(), help='Chipset')
parser.add_argument('--camera_ip', type=str, default=CAMERA_IP, help='Camera IP')
parser.add_argument('--camera_username', type=str, default=CAMERA_USERNAME, help='Camera Username')
parser.add_argument('--camera_password', type=str, default=CAMERA_PASSWORD, help='Camera Password')
args = parser.parse_args()


MODEL_PATH = args.model_path
MODEL_NAME = args.model
INPUT_SIZE = args.size
TEST_DURATION = args.test_duration
CHIP = args.chip
CAMERA_IP = args.camera_ip
CAMERA_USERNAME = args.camera_username
CAMERA_PASSWORD = args.camera_password



def run_speed_test():
    print("Connecting to camera...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CAMERA_IP, username=CAMERA_USERNAME, password=CAMERA_PASSWORD)

    print("Loading Model...")
    sftp = ssh.open_sftp()
    sftp.put(MODEL_PATH+MODEL_NAME, camera_model_location)
    sftp.close()

    print("Starting Test...")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "larod-client -R "+ TEST_DURATION +" -p" +
        " -c " + chipset[CHIP] +
        " -g " + camera_model_location +
        " -i ''")

    print("Parsing the output...")
    try:
        out=list(filter(lambda k: 'Mean execution time for job:' in k, ssh_stdout))[0]
        print(out)
    except:
        print("Something went wrong:")
        print(ssh_stdout)
        print(ssh_stderr)

    print("Cleaning...")
    ssh.exec_command("rm rand.in rand.in.out0 "+camera_model_location)

    ssh.close()

run_speed_test()
