from tools.table import *
from tools.utils import *
import glob
from networking.iptable_tools import *
from networking.ip_checks import *

class BlocklistTable(Table):

    @staticmethod
    def clear_all():
        clear_chains("BLOCKLIST")
        set_rule_return("BLOCKLIST")
        save_all()

    @staticmethod
    def apply_blocklist(list_name):      
        print("Creating blocklist chain if it does not exists already..")
        create_chain("BLOCKLIST")
        print("Clearing previous rules if any..")
        clear_chains("BLOCKLIST")
        ip_list = []
        with open(get_data_dir() + "/Blocklists/" + list_name) as file:
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


    @staticmethod
    def get_all_lists():
        all_lists = []
        path = get_data_dir() + "/Blocklists"
        file_list = glob.glob(path + "/*.list")  
        for path in file_list:
            all_lists.append([os.path.basename(path),get_num_lines(path)])
        return all_lists



