import ipaddress
import socket
import sys
import threading
from queue import Queue


class StealthHostDiscovery:
    @staticmethod
    def expand_cidr(cidr):
        ip_network = ipaddress.ip_network(cidr)
        ip_range = [str(ip) for ip in ip_network.hosts()]
        return ip_range

    def __init__(self, ip_range, ports=None):
        self.ip_range = self.expand_cidr(ip_range)
        self.live_hosts = []
        self.queue = Queue()
        self.num_threads = 10  # Number of threads for concurrent scanning
        self.ports = ports if ports else [80, 443] # Default ports to scan

    def scan_host(self, ip):
        for port in self.ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Timeout for connection attempt
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        try:
                            hostname = socket.gethostbyaddr(ip)[0]
                        except socket.herror:
                            hostname = 'Unknown'
                        self.live_hosts.append((ip, hostname, port))
            except ConnectionRefusedError:
                pass  # Connection refused by the target host
            except socket.timeout:
                pass  # Connection attempt timed out
            except Exception as e:
                print(f"An error occurred while scanning host {ip} on port {port}: {str(e)}")

    @staticmethod
    def get_ping_command(ip):
        if sys.platform.startswith('win'):
            return f"ping -n 1 -w 1000 {ip}"
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return f"ping -c 1 -W 1 {ip}"
        else:
            raise OSError(f"Unsupported operating system: {sys.platform}")

    def worker(self):
        while True:
            ip = self.queue.get()
            self.scan_host(ip)
            self.queue.task_done()

    def scan_hosts(self):
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        for ip in self.ip_range:
            self.queue.put(ip)

        self.queue.join()
        return self.live_hosts
