import os
import re  

token_parameters = { "<!--A8_tf1_mnv2-->" : "python3 ./model-performance-tester.py --model_path ../Models/ --model mobilenet_v2_1.0_224_quant.tflite --chip A8-DLPU --camera_ip 213.112.161.127:7777 --camera_username root --camera_password IcantRememberMyPasswordd" }

#read md file
def read_md_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#find token in md file
def find_token(md_file, token):
    return md_file.find(token)

#get value to add to readme
def get_value_to_add(token):
    return 100

#generate section from value to add
def generate_table(value_to_add, token):
    section = ''
    section += token + " "
    section += str(value_to_add) + " "
    section += "<!--end--> "
    return section

#rewrite md file
def rewrite_md_file(file_name, md_file, token, text_to_replace):
    #regex numbers, dots, "ms" and spaces
    regex = r"(\d+\.?\d*\s?ms)"

    regex = "("+token+") "+regex+" (<!--end-->)"
    print(regex)
    with open(file_name, 'w') as f:
        f.write(re.sub(regex, text_to_replace, md_file, flags=re.DOTALL))

#main function
def main():
    file_name = 'README.md'
    tokens = ['<!--A8_tf1_mnv2-->']
    md_file = read_md_file(file_name)
    for token in tokens:
        token_index = find_token(md_file, token)
        if token_index != -1:
            value_to_add = get_value_to_add(token)
            table = generate_table(value_to_add, token)
            rewrite_md_file(file_name, md_file, token, table)
        else:
            print("Can't find token in file " + token)

if __name__ == '__main__':
    main() 