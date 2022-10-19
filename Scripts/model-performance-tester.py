import paramiko
import numpy as np
import os


CAMERA_IP="172.25.71.119"
CAMERA_USERNAME="root"
CAMERA_PASSWORD="Pass"
MODEL_NAME="movenet_single_pose_lightning_ptq.tflite"
MODEL_PATH="../Models/"
TEST_DURATION="1000"
CHIP="CPU"
INPUT_SIZE=[3,192,192]


camera_model_location = os.path.join("/tmp/", MODEL_NAME)

chipset = {
    "CPU": "cpu-tflite",
    "A8-DLPU": "axis-a8-dlpu-tflite",
    "A7-DLPU": "google-edge-tpu-tflite",
    "CV25": "ambarella-cvflow"
}

print("Connecting to camera...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(CAMERA_IP, username=CAMERA_USERNAME, password=CAMERA_PASSWORD)

print("Loading Model...")
sftp = ssh.open_sftp()
sftp.put(MODEL_PATH+MODEL_NAME, camera_model_location)
sftp.close()

print("Generating input...")
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
	"dd if=/dev/urandom of=rand.in "+
	"bs="+ str(np.prod(INPUT_SIZE)) +" count=1")

print("Starting Test...")
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
    "larod-client -R "+ TEST_DURATION +" -p" +
    " -c " + chipset[CHIP] +
    " -g " + camera_model_location +
    " -i rand.in")

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
