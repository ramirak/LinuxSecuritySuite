
import subprocess
import iptable_tools
from iptable_tools import *
from json_handler import *

def load_policy(policy):
    print("Creating blocklist chain if not exists already..")
    create_chain("BLOCKLIST")
    # Default drop all
    switch_mode("DROP")
    # Clear any existing rule
    print("Clearing old chains..")
    clear_chains("INPUT")
    clear_chains("OUTPUT")
    # Load all rules in this policy
    print("Setting policy..")
    for rule in policy:
        for proto in rule['proto'].split():
            set_rule(rule['dir'], rule['src'], rule['dst'], rule['sport'], rule['dport'], proto, rule['action'])
    print("Forwarding other packets to BLOCKLIST..")
    set_forward_to_chain("INPUT", "BLOCKLIST")
    set_forward_to_chain("OUTPUT", "BLOCKLIST")
    print("Done!\n---------------------------------")


def apply_current_policy():
    my_policy_name = retrieve_from_file("data/config.json")["active_policy"]
    policy = retrieve_from_file("data/policies.json")[my_policy_name]
    load_policy(policy)


def apply_blocklist():
    print("Creating blocklist chain if not exists already..")
    create_chain("BLOCKLIST")
    ip_list = []
    with open("data/addresses.list") as file:
        for line in file:
            ip_list.append(line.rstrip())
    for addr in ip_list:
        print("Blocking " + addr)
        set_rule_block("BLOCKLIST", addr)
    print("Done!")
