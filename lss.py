
from gui.main_frame import create_main_window
from tools.json_handler import save_to_file
from tools.utils import *
import os
from policy.policy import PolicyKeys

def print_logo():
    logo = '''
    .-.    .----. .----.    .---.  .----. .-. .-. .----. .----. .-.   .----.
    | |   { {__  { {__     /  ___}/  {}  \\|  `| |{ {__  /  {}  \\| |   | {_  
    | `--..-._} }.-._} }   \     }\\      /| |\\  |.-._} }\\      /| `--.| {__ 
    `----'`----' `----'     `---'  `----' `-' `-'`----'  `----' `----'`----'
    '''
    print(logo)


def check_data_folder():
    data_folder = get_data_dir()
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    
    policy_folder = data_folder + "/Policies"
    if not os.path.exists(policy_folder):
        os.mkdir(policy_folder)

    lists_folder = data_folder + "/Blocklists"
    if not os.path.exists(policy_folder):
        os.mkdir(policy_folder)


def create_default_policy():
    check_data_folder()

    policies_file = get_data_dir() + "/Policies/Accept_all.policy"
    if not os.path.isfile(policies_file):
        keys = [key.name for key in PolicyKeys]
        values1 = ["OUTPUT", "any", "any", "any", "any", "any", "ACCEPT"]
        values2 = ["INPUT", "any", "any", "any", "any", "any", "ACCEPT"]
        policy = [dict(zip(keys,values1)), dict(zip(keys,values2))]
        save_to_file(policies_file, policy)

        
def check_installed_iptables():
    bin_file = "/sbin/iptables"
    if not os.path.isfile(bin_file):
        print("Iptables is not installed!")
        exit(0)


def check_installed_syslog():
    bin_file = "/sbin/syslog-ng"
    if not os.path.isfile(bin_file):
        print("Please install syslog-ng in order to see firewall logs.")


create_default_policy()
check_installed_iptables()
check_installed_syslog()
create_main_window()


