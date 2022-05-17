import requests
import socket
import urllib3
import urllib3.request as request

SUBDOMAINS_PATH = r"C:\Users\vikib\Documents\מסמכים\עבודה\subdomains.txt"
PORTS = [21,22,23,25,53,80,110,115,135,143,443,445,1433,3306,3389,5632,5900]
HTTP = urllib3.PoolManager()

def sub_domain_scan(domain, sub_list):
    """This function checks all the optional subdomains for this domain
    :param:
    domain - string of the input domain
    sub_list - list of optionals subdomains from the file
    """
    discovered_subdomains = []
    for sub_d in sub_list:
        url = f"https://{sub_d}.{domain}"
        try:
            requests.get(url)
            discovered_subdomains.append(url)
        except requests.ConnectionError:
            pass
    return discovered_subdomains

def port_scanner(discovered_subdomains):
    """This function checks all the optional port that might be open for this domain
    :param:
    discovered_subdomains - a list of full subdomains
    """
    for domain in discovered_subdomains:
        open_ports = []
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        domain = domain.strip('https://')
        ip = socket.gethostbyname(domain)
        for port in PORTS:
            location = (ip, port)
            is_open_port = a_socket.connect_ex(location)
            if is_open_port == 0:
                open_ports.append(port)
        http_allowed = open_service(domain)
        if len(open_ports) != 0:
            http_port = ""
            if http_allowed == True:
                http_port = "and Port 80 is open! (http service)"
            print_open_ports = f"this ports are open: {open_ports} {http_port}"
        else:
            print_open_ports = "no ports are open"
        print(f"For the subdomain {domain}, {print_open_ports}")
        a_socket.close()

def open_service(domain):
    """This function checks if we connect to the domain by http
    :param:
    domain - string of the input domain
    """
    check_port = HTTP.request('GET', domain)
    if check_port.status == 200:
        return True
    return False

def domain_scanner(domain):
    """This function contains 2 func - the subdomains and the ports
    :param:
    domain - string of the input domain
    """
    with open(SUBDOMAINS_PATH, 'r') as file:
        sub = file.read()
        sub_list = sub.splitlines()
    discovered_subdomains = sub_domain_scan(domain, sub_list)
    port_scanner(discovered_subdomains)

if __name__ == '__main__':
    domain = input("Please enter the domain you would like to scan:")
    domain_scanner(domain)
