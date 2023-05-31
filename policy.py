
import subprocess, socket
import iptable_tools
from iptable_tools import *
from json_handler import *
from ip_checks import *
from utils import *

def load_policy(policy):
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
        for proto in rule['proto'].split():
            direction = rule['dir']
            src = get_ip_addr(rule['src'])
            dst = get_ip_addr(rule['dst'])
            sport = rule['sport']
            dport = rule['dport']
            action = rule['action']
            if is_valid_chain(direction) and src != None and dst != None and is_valid_port(sport) and is_valid_port(dport) and is_valid_proto(proto) and is_valid_action(action):
                set_rule(direction, src, dst, sport, dport, proto, action)
    print("Forwarding other packets to LOG_AND_DROP..")
    set_forward_to_chain("INPUT", "LOG_AND_DROP")
    set_forward_to_chain("OUTPUT", "LOG_AND_DROP")
   
    set_rule_return("BLOCKLIST")
    print("Saving rulebase to /etc/iptables..")
    save_all()
    print("Done!\n---------------------------------")


def apply_current_policy():
    my_policy_name = retrieve_from_file(get_data_dir() + "/config.json")["active_policy"]
    policy = retrieve_from_file(get_data_dir() + "/policies.json")[my_policy_name]
    load_policy(policy)


def apply_blocklist():
    print("Creating blocklist chain if it does not exists already..")
    create_chain("BLOCKLIST")
    print("Clearing previous rules if any..")
    clear_chains("BLOCKLIST")
    ip_list = []
    with open(get_data_dir() + "/addresses.list") as file:
        for line in file:
            ip_list.append(line.rstrip())
    for addr in ip_list:
        print("Checking " + addr + "..")
        addr = get_ip_addr(addr)
        if addr is not None:
            print("Blocking " + addr)
            set_rule_block("BLOCKLIST", addr)
            continue
        print("Invalid IP or Domain..")
    set_rule_return("BLOCKLIST")
    print("Saving rulebase to /etc/iptables..")
    save_all()
    print("Done!")

