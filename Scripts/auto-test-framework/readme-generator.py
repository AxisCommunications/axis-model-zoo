import os
import re  
from model_performance_tester import run_speed_test

#TODO: Would be better to replace this with a dict of dicts to make get_value_to_add more readable
#TODO: MOVE PASSWORD TO GITHUB SECRETS!
token_parameters = { 
    "A8_tf1_mnv2" : ["213.112.161.127", 2222, "root", "Models/", "mobilenet_v2_1.0_224_quant.tflite", "1000", "A8-DLPU"] 
    }

#read md file
def read_md_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#find token in md file
def find_token(md_file, token):
    return md_file.find(token)

#get value to add to readme
def get_value_to_add(token):
    #read password from github secrets
    superSecretPassword = os.environ['SUPERSECRETPASSWORD']
    val= run_speed_test(token_parameters[token][0], token_parameters[token][1], token_parameters[token][2], superSecretPassword,  token_parameters[token][3], token_parameters[token][4], token_parameters[token][5], token_parameters[token][6]) 
    return val
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
    tokens = ['A8_tf1_mnv2']
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