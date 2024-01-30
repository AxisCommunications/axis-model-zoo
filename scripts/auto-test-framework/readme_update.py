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

import os
import re

tokens = \
    ['A8_tf1_mnv2', 'A8_P_tf1_mnv2', 'A7_tf1_mnv2','A7_tf2_mnv2','A7_tf2_mnv3','cv25_tf1_mnv2','cv25_tf1_ens', \
    'A7_tf1_ssd_mnv2', 'A8_P_tf1_ssd_mnv2', 'A8_Q_tf1_ssd_mnv2', 'A8_P_tf1_ssd_md', 'A8_Q_tf1_ssd_md', 'A8_P_yolov5n', 'A8_Q_yolov5n', 'A8_Q_yolov5s', 'A8_Q_yolov5m' \
    ]

token_parameters = {
    ("/artpec7/mobilenet_v2_1.0_224_quant_edgetpu.tflite","Q1615 Mk III") : "A7_tf1_mnv2",
    ("/artpec7/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite","Q1615 Mk III") : "A7_tf2_mnv2",
    ("/artpec7/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite","Q1615 Mk III") : "A7_tf2_mnv3",
    ("/artpec8/mobilenet_v2_1.0_224_quant.tflite","Q1656-LE") : "A8_tf1_mnv2",
    ("/artpec8/mobilenet_v2_1.0_224_quant.tflite","P1465-LE") : "A8_P_tf1_mnv2",
    ("/cv25/mobilenetv2_cavalry.bin","M3085-V") : "cv25_tf1_mnv2",
    ("/cv25/EfficientNet-lite0.bin","M3085-V") : "cv25_tf1_ens",
    ("/artpec7/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite","Q1615 Mk III") : "A7_tf1_ssd_mnv2",
    ("/artpec8/ssd_mobilenet_v2_coco_quant_postprocess.tflite","P1465-LE") : "A8_P_tf1_ssd_mnv2",
    ("/artpec8/ssd_mobilenet_v2_coco_quant_postprocess.tflite","Q1656-LE") : "A8_Q_tf1_ssd_mnv2",
    ("/artpec8/ssdlite_mobiledet_coco_qat_postprocess","P1465-LE") : "A8_P_tf1_ssd_md",
    ("/artpec8/ssdlite_mobiledet_coco_qat_postprocess","Q1656-LE") : "A8_Q_tf1_ssd_md",
    ("/artpec8/yolov5n.bin","P1465-LE") : "A8_P_yolov5n",
    ("/artpec8/yolov5n.bin","Q1656-LE") : "A8_Q_yolov5n",
    ("/artpec8/yolov5s.bin","Q1656-LE") : "A8_Q_yolov5s",
    ("/artpec8/yolov5m.bin","Q1656-LE") : "A8_Q_yolov5m"
    }

#read md file
def read_md_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#find token in md file
def find_token(md_file, token):
    return md_file.find(token)


def read_larod_output(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def extract_inference_time(larod_output):
    #extract model name from larod output
    regex_model = "Model name:(.*?)\."
    model = re.findall(regex_model, larod_output, re.MULTILINE)[0]

    #extract inference time from larod output
    regex = "result: \.\/models((.*?).(tflite|bin)) (.*?) job: (.*?) ms"
    matches = re.findall(regex, larod_output, re.MULTILINE)
    # filter file name and inference time
    return {token_parameters[(match[0],model)]: match[4] for match in matches}

#generate section from value to add
def generate_table(value_to_add, token):
    section = ''
    section += "<!--" + token + "--> "
    section += str(value_to_add) + " ms "
    section += "<!--end_"+token+"-->"
    return section

#rewrite md file
def rewrite_md_file(file_name, md_file, token, text_to_replace):
    regex = "<!--" + token + "-->(.*?)<!--end_"+token+"-->"
    with open(file_name, 'w') as f:
        f.write(re.sub(regex, text_to_replace, md_file, flags=re.DOTALL))

#main function
def main():
    file_name = 'README.md'

    md_file = read_md_file(file_name)
    larod_output = read_larod_output("/tmp/larod_out.txt")
    inference_times = extract_inference_time(larod_output)
    for token in tokens:
        token_index = find_token(md_file, token)
        if token_index != -1 and token in inference_times:
            print("Found token in file: " + token)
            value_to_add = inference_times[token]
            table = generate_table(value_to_add, token)
            rewrite_md_file(file_name, md_file, token, table)
            md_file = read_md_file(file_name)
        else:
            print("Can't find token in file: " + token)

if __name__ == '__main__':
    main()
