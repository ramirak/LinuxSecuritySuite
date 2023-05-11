
from main_frame import create_main_window
from json_handler import save_to_file 
import os

def check_data_folder():
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    return data_folder


def create_default_policy():
    data_folder = check_data_folder()

    policies_file = data_folder + "/policies.json"
    if not os.path.isfile(policies_file):
        policy = {"hero": [{"dir": "OUTPUT", "src": "any", "dst": "any", "dport": "any", "proto": "any", "action": "ACCEPT"}, 
                           {"dir": "INPUT", "src": "any", "dst": "any","dport": "any", "proto": "any", "action": "ACCEPT"}]}
        save_to_file(policies_file, policy)


def create_default_config():
    data_folder = check_data_folder()

    conf_file = "data/config.json"
    if not os.path.isfile(conf_file):
        config = {"active_policy":"basic"}
        save_to_file(conf_file, config)
        

def check_installed_iptables():
    bin_file = "/sbin/iptables"
    if not os.path.isfile(bin_file):
        print("Iptables is not installed!")
        exit(0)


create_default_policy()
create_default_config()
create_main_window()
