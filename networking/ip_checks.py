import socket, validators

VALID_PROTO = ["tcp", "udp", "icmp"]
VALID_ACTION = ["REJECT", "DROP", "ACCEPT"]
VALID_CHAIN = ["OUTPUT", "INPUT"]


def is_valid_chain(chain):
    if chain in VALID_CHAIN:
        return True
    print("Invalid chain..")
    return False


def is_valid_action(action):
    if action in VALID_ACTION:
        return True
    print("Invalid action..")
    return False


def is_valid_proto(proto):
    if proto == "any":
        return True
    if proto in VALID_PROTO:
        return True
    print("Invalid protocol..")
    return False


def is_valid_port(port):
    try:
        if port == "any":
            return True
        port = int(port)
        if port >= 0 and port <= 65535:
            return True
    except:
        pass
    print("Invalid port number..")
    return False


def is_valid_ip(addr):
    addr = addr.split("/")[0]
    try:
        if addr == "any":
            return True
        socket.inet_aton(addr)
        return True
    except socket.error:
        print("Invalid IP..")
        return False

def is_valid_ip2(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def is_valid_domain(domain):
    return validators.domain(domain)


def get_ip_addr(addr):
    if is_valid_domain(addr):
        addr = socket.gethostbyname(addr)
    if is_valid_ip(addr): 
        return addr
    return None

