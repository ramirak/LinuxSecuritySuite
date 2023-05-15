import subprocess
import socket


def set_rule(direction, s_host, d_host, s_port, d_port, protocol, action):
    ip_0 = "sudo iptables -A " + direction + " -m state --state NEW,ESTABLISHED"
    if protocol != "any":
        ip_0 += " -p " + protocol
        if protocol == "tcp" or protocol == "udp":
            if s_port != "any":
                ip_0 += " --sport " + str(s_port)
            if d_port != "any":
                ip_0 += " --dport " + str(d_port)
    if s_host != "any":
        ip_0 += " -s " + s_host
    if d_host != "any":
        ip_0 += " -d " + d_host    
    ip_0 += " -j " + action 

    direction = switch_dir(direction)

    ip_1 = "sudo iptables -A " + direction
    if action == "ACCEPT":
        ip_1 += " -m state --state RELATED,ESTABLISHED" 
    if protocol != "any":
        ip_1 += " -p " + protocol
        if protocol == "tcp" or protocol == "udp":
            if s_port != "any":
                ip_1 += " --dport " + str(s_port)
            if d_port != "any":
                ip_1 += " --sport " + str(d_port)
    if d_host != "any":
        ip_1 += " -s " + d_host
    if s_host != "any":
        ip_1 += " -d " + s_host
    ip_1 += " -j " + action 

    subprocess.Popen(ip_0.split(), stdout=subprocess.PIPE).wait()
    subprocess.Popen(ip_1.split(), stdout=subprocess.PIPE).wait()
    

def set_rule_block(chain, d_host):
    rule = "sudo iptables -A " + chain + " -m state --state NEW,ESTABLISHED,RELATED -d " + d_host + " -j DROP"
    subprocess.Popen(rule.split(), stdout=subprocess.PIPE).wait()
    

def set_rule_return(chain):
    rule = "sudo iptables -C " + chain + " -j RETURN" 
    ret = subprocess.Popen(rule.split(), stdout=subprocess.PIPE).wait()
    if ret:
        rule = "sudo iptables -A " + chain + " -j RETURN" 
        subprocess.Popen(rule.split(), stdout=subprocess.PIPE).wait()


def set_rule_log_block(chain):
    rule1 = 'sudo iptables -A ' + chain + ' -j LOG --log-level 6'
    rule2 = 'sudo iptables -A ' + chain + ' -j DROP'
    subprocess.Popen(rule1.split(), stdout=subprocess.PIPE).wait()
    subprocess.Popen(rule2.split(), stdout=subprocess.PIPE).wait()


def set_forward_to_chain(chain1, chain2): 
    rule = "sudo iptables -A " + chain1 + " -j " + chain2
    subprocess.Popen(rule.split(), stdout=subprocess.PIPE).wait()


def switch_dir(direction):
    if direction == "OUTPUT":
        return "INPUT"
    return "OUTPUT"


def clear_chains(chain):
    subprocess.Popen(("sudo iptables -F " + chain).split(), stdout=subprocess.PIPE).wait()


def show_chains():
    proc = subprocess.Popen("iptables -nL".split(), stdout=subprocess.PIPE).wait()
    print(proc.stdout.read().decode())

    
def switch_mode(action):
    c1 = "sudo iptables -P INPUT " + action
    c2 = "sudo iptables -P OUTPUT " + action
    subprocess.Popen(c1.split(), stdout=subprocess.PIPE).wait()
    subprocess.Popen(c2.split(), stdout=subprocess.PIPE).wait()


def create_chain(chain): 
    c = "sudo iptables -N " + chain
    subprocess.Popen(c.split(), stdout=subprocess.PIPE).wait()


def is_valid_ip(address):
    try:
        socket.inet_aton(address)
        return 1
    except socket.error:
        return 0


def save_all():
    c1 = "sudo iptables-save"
    c2 = "sudo tee /etc/iptables/iptables.rules"
    proc1 = subprocess.Popen(c1.split(), stdout=subprocess.PIPE)
    proc1.wait()
    subprocess.Popen(c2.split(), stdin=proc1.stdout, stdout=subprocess.PIPE).wait()


    



