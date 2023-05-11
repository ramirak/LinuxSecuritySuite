
import subprocess
import iptable_tools
from iptable_tools import *
from json_handler import *

def load_policy(policy):
    # Default drop all
    switch_mode("DROP")
    # Clear any existing rule
    clear_chains()
    # Load all rules in this policy
    for rule in policy:
        for proto in rule['proto']:
            set_rule(rule['dir'], rule['src'], rule['dst'], rule['dport'], proto, rule['action'])


def apply_current_policy():
    my_policy_name = retrieve_from_file("data/config.json")["active_policy"]
    policy = retrieve_from_file("data/policies.json")[my_policy_name]
    load_policy(policy)



