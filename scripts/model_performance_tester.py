import paramiko
import os
import argparse
import re

#python3 ./model-performance-tester.py --model_path ../models/ --model mobilenet_v2_1.0_224_quant.tflite --chip A8-DLPU

#python3 ./model-performance-tester.py --model_path ../models/ --model mobilenetv2_cavalry.bin --chip CV25 --camera_ip 172.25.71.70 --camera_password pass

#4.55 ms
#python3 ./model-performance-tester.py --model_path ../models/ --model mobilenet_v2_1.0_224_quant_edgetpu.tflite --chip A7-DLPU --camera_ip 172.27.67.240 --camera_password pass

#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v1_1.0_224_ptq_edgetpu.tflite --chip A7-DLPU --camera_ip 172.27.67.240 --camera_password pass
#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite --chip A7-DLPU --camera_ip 172.27.67.240 --camera_password pass
#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite --chip A7-DLPU --camera_ip 172.27.67.240 --camera_password pass
#4.29 ms, 4.58, 4.76 ms

#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v1_1.0_224_ptq.tflite --chip A8-DLPU
#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v2_1.0_224_ptq.tflite --chip A8-DLPU
#python3 ./model-performance-tester.py --model_path ../models/ --model tf2_mobilenet_v3_edgetpu_1.0_224_ptq.tflite --chip A8-DLPU
#117.25 ms 84.64  ms (64 on cpu) 181.99 ms 

chipset = {
        "CPU": "cpu-tflite",
        "A8-DLPU": "axis-a8-dlpu-tflite",
        "A7-DLPU": "google-edge-tpu-tflite",
        "CV25": "ambarella-cvflow"
    }

def run_speed_test(CAMERA_IP, PORT, CAMERA_USERNAME, CAMERA_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP):

    #Take model name from path
    model_name = MODEL_PATH.split("/")[-1]
    
    
    camera_model_location = os.path.join("/tmp/", model_name)
    print("Testing model: ", model_name)
    print("Connecting to camera at " + CAMERA_IP + " and port "+ str(PORT))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CAMERA_IP, username=CAMERA_USERNAME, password=CAMERA_PASSWORD, port=PORT)

    print("Loading Model...")
    sftp = ssh.open_sftp()
    sftp.put(MODEL_PATH, camera_model_location)
    sftp.close()

    print("Starting Test...")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "larod-client -R "+ TEST_DURATION +" -p" +
        " -c " + chipset[CHIP] +
        " -g " + camera_model_location +
        " -i ''")
    time = -1
    print("Parsing the output...")
    try:
        out=list(filter(lambda k: 'Mean execution time for job:' in k, ssh_stdout))[0]
        print(out)
        time = re.findall(r'\d+\.\d+', out)[-1]
    except:
        print("Something went wrong:")
        print(ssh_stdout.read().decode("utf-8"))
        print(ssh_stderr.read().decode("utf-8"))


    print("Cleaning...")
    ssh.exec_command("rm "+camera_model_location)

    ssh.close()
    return time

if __name__ == "__main__":

    CAMERA_IP="172.25.71.119"
    CAMERA_USERNAME="root"
    CAMERA_PASSWORD="Pass"
    MODEL_PATH="../models/efficientdet_lite0_320_ptq.tflite"
    TEST_DURATION="1000"
    CHIP="CPU"

    parser = argparse.ArgumentParser(description='Run a speed test of a model on the camera')
    parser.add_argument('--model_path', type=str, default=MODEL_PATH, help='Model path')
    parser.add_argument('--test_duration', type=str, default=TEST_DURATION, help='Test duration')
    parser.add_argument('--chip', type=str, default=CHIP, choices=chipset.keys(), help='Chipset')
    parser.add_argument('--camera_ip', type=str, default=CAMERA_IP, help='Camera IP')
    parser.add_argument('--camera_port', type=int, default=22, help='Camera port for ssh')
    parser.add_argument('--camera_username', type=str, default=CAMERA_USERNAME, help='Camera Username')
    parser.add_argument('--camera_password', type=str, default=CAMERA_PASSWORD, help='Camera Password')

    args = parser.parse_args()


    MODEL_PATH = args.model_path
    TEST_DURATION = args.test_duration
    CHIP = args.chip
    CAMERA_IP = args.camera_ip
    CAMERA_PORT=args.camera_port
    CAMERA_USERNAME = args.camera_username
    CAMERA_PASSWORD = args.camera_password

    run_speed_test(CAMERA_IP, CAMERA_PORT, CAMERA_USERNAME, CAMERA_PASSWORD, MODEL_PATH, TEST_DURATION, CHIP)

