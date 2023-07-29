from enum import Enum
import subprocess, socket
from networking.iptable_tools import *
from tools.json_handler import *
from networking.ip_checks import *
from tools.utils import *
from tools.table import *
import glob

class PolicyTable(Table):
   
    def load_policy(self):
        policy = self.data
        print("Creating blocklist chain if it does not exists already..")
        create_chain("BLOCKLIST")
        print("Creating log chain if it does not exists already")
        create_chain("LOG_AND_DROP")
        clear_chains("LOG_AND_DROP")
        set_rule_log_block("LOG_AND_DROP")

        # Default drop all
        switch_mode("DROP")
        # Clear any existing rule
        print("Clearing old chains..")
        clear_chains("INPUT")
        clear_chains("OUTPUT")

        print("Forwarding to BLOCKLIST before checking main chains..")
        set_forward_to_chain("INPUT", "BLOCKLIST")
        set_forward_to_chain("OUTPUT", "BLOCKLIST") 

        # Load all rules in this policy
        print("Setting policy..")
        for rule in policy:
            for proto in rule[PolicyKeys.PROTOCOL.name].split():
                direction = rule[PolicyKeys.DIRECTION.name]
                src = get_ip_addr(rule[PolicyKeys.SOURCE.name])
                dst = get_ip_addr(rule[PolicyKeys.DESTINATION.name])
                sport = rule[PolicyKeys.S_PORT.name]
                dport = rule[PolicyKeys.D_PORT.name]
                action = rule[PolicyKeys.ACTION.name]
                if is_valid_chain(direction) and src != None and dst != None and is_valid_port(sport) and is_valid_port(dport) and is_valid_proto(proto) and is_valid_action(action):
                    set_rule(direction, src, dst, sport, dport, proto, action)
        print("Forwarding other packets to LOG_AND_DROP..")
        set_forward_to_chain("INPUT", "LOG_AND_DROP")
        set_forward_to_chain("OUTPUT", "LOG_AND_DROP")
       
        set_rule_return("BLOCKLIST")
        print("Saving rulebase to /etc/iptables..")
        save_all()
        print("Done!\n---------------------------------")
 

    @staticmethod
    def get_all_policies():
        all_policies = {}
        path = get_data_dir() + "/Policies"
        file_list = glob.glob(path + "/*.policy")  
        for policy_path in file_list:
            table = PolicyTable(policy_path)
            all_policies[table.get_name()] = table
            table.reload_data()
        return all_policies


class PolicyOperation(Enum):
    ADD = 0
    EDIT = 1
    DELETE = 2
    SAVE = 3
    APPLY = 4

class PolicyKeys(Enum):
    DIRECTION = 0
    SOURCE = 1
    DESTINATION = 2
    S_PORT = 3
    D_PORT = 4
    PROTOCOL = 5
    ACTION = 6

