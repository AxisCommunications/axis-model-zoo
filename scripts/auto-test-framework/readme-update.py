import os
import re  

tokens = ['A8_tf1_mnv2','A7_tf1_mnv2','A7_tf2_mnv2','A7_tf2_mnv3','cv25_tf1_mnv2','cv25_tf1_ens']
token_parameters = { 

    "/artpec7/mobilenet_v2_1.0_224_quant_edgetpu.tflite" : "A7_tf1_mnv2",
    "/artpec7/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite" : "A7_tf2_mnv2",
    "/artpec7/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite" : "A7_tf2_mnv3",
    "/artpec8/mobilenet_v2_1.0_224_quant.tflite" : "A8_tf1_mnv2",
    "/cv25/mobilenetv2_cavalry.bin" : "cv25_tf1_mnv2",
    "/cv25/EfficientNet-S.bin" : "cv25_tf1_ens"
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
    #extract inference time from larod output
    regex = "result: \.\/models((.*?).(tflite|bin)) (.*?) job: (.*?) ms"
    matches = re.findall(regex, larod_output, re.MULTILINE)
    # filter file name and inference time
    return {token_parameters[match[0]]: match[4] for match in matches}

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
        else:
            print("Can't find token in file: " + token)

if __name__ == '__main__':
    main() 
  
