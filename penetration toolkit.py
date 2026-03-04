#!/usr/bin/env python3
import argparse
import socket
import requests
import concurrent.futures
from datetime import datetime

# Banner
BANNER = """
▓█████▄  ▒█████   ██▀███  ▓█████ ▓█████▄ 
▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌
░██   █▌▒██░  ██▒▓██ ░▄█ ▒▒███   ░██   █▌
░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌
░▒████▓ ░ ████▓▒░░██▓ ▒██▒░▒████▒░▒████▓ 
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ 
 ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒ 
 ░ ░  ░ ░ ░ ░ ▒    ░░   ░    ░    ░ ░  ░ 
   ░        ░ ░     ░        ░  ░   ░    
 ░                                  ░    
v1.0 | Aravind Dhakuri | Qualcomm-ready
"""

# Common ports for Android/embedded systems
COMMON_PORTS = [5555, 8080, 22, 80, 443, 9000, 3389]

class PenTestTool:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        print(BANNER)

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                print(f"[+] Port {port} is open")
                self.open_ports.append(port)
            sock.close()
        except Exception as e:
            pass

    def port_scan(self, ports=COMMON_PORTS, threads=50):
        print(f"\n[🚀] Scanning {self.target}...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.scan_port, ports)
        return self.open_ports

    def dir_brute(self, wordlist="common_dirs.txt", extensions=[], threads=10):
        print(f"\n[🔍] Bruteforcing directories on http://{self.target}...")
        try:
            with open(wordlist, 'r') as f:
                dirs = [line.strip() for line in f]
            
            def check_dir(d):
                for ext in [''] + extensions:
                    url = f"http://{self.target}/{d}{ext}"
                    try:
                        r = requests.get(url, timeout=3)
                        if r.status_code == 200:
                            print(f"[+] Found: {url}")
                    except:
                        pass
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(check_dir, dirs)
        except FileNotFoundError:
            print("[!] Wordlist not found. Use '-w custom_wordlist.txt'")

    def cve_lookup(self, service, version):
        print(f"\n[📚] Checking CVEs for {service} {version}...")
        # API example (replace with real CVE DB like NVD)
        url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={service}+{version}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                cves = r.json().get("result", {}).get("CVE_Items", [])
                for cve in cves[:5]:  # Show top 5
                    print(f"  - {cve['cve']['CVE_data_meta']['ID']}: {cve['cve']['description']['description_data'][0]['value']}")
            else:
                print("[!] CVE lookup failed. Check API rate limits.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PenTest Toolbox for Android/Kernel Targets")
    parser.add_argument("-t", "--target", required=True, help="Target IP/Domain")
    parser.add_argument("-p", "--ports", nargs="+", type=int, default=COMMON_PORTS, help="Ports to scan")
    parser.add_argument("-d", "--dirs", action="store_true", help="Enable directory brute-forcing")
    parser.add_argument("-w", "--wordlist", default="common_dirs.txt", help="Custom wordlist path")
    parser.add_argument("-e", "--extensions", nargs="+", default=["", ".php", ".sh"], help="File extensions for dir brute")
    parser.add_argument("-c", "--cve", nargs=2, metavar=("SERVICE", "VERSION"), help="Check CVEs (e.g., 'openssl 1.1.1')")
    args = parser.parse_args()

    tool = PenTestTool(args.target)
    
    # Port scan (always run)
    open_ports = tool.port_scan(ports=args.ports)
    
    # Optional modules
    if args.dirs:
        tool.dir_brute(wordlist=args.wordlist, extensions=args.extensions)
    if args.cve:
        tool.cve_lookup(args.cve[0], args.cve[1])
    
    print("\n[+] Scan completed at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
