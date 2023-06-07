import socket
import subprocess
import re
import platform
import threading


class PortScanner:
    @staticmethod
    def scan(target, ports):
        open_ports = []
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"Failed to resolve hostname: {target}")
            return open_ports

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)

            sock.close()

        return open_ports

    @staticmethod
    def get_open_ports(target, port_range="1-65535"):
        try:
            start_port, end_port = map(int, port_range.split('-'))
            ports = list(range(start_port, end_port + 1))
        except ValueError:
            raise ValueError("Invalid port range.")

        open_ports = PortScanner.scan(target, ports)
        return open_ports

    @staticmethod
    def get_service_name(target, port):
        os_name = platform.system()

        if os_name == "Windows":
            command = ["nmap", "-p", str(port), "--open", target]
        elif os_name == "Linux" or os_name == "Darwin":
            command = ["nc", "-vz", "-n", "-z", "-p", str(port), target]
        else:
            return "Unknown OS"

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            match = re.search(r"open .*\r\n", output.decode())
            if match:
                service = match.group().split(' ')[1].strip()
                return service
            return "Unknown"
        except (OSError, subprocess.SubprocessError):
            return "Unknown"


def scan_ip_address(ip_address):
    ports = PortScanner.get_open_ports(ip_address, port_range="1-1000")

    with open(f'{ip_address}_scan_results.txt', 'w') as file:
        for port in ports:
            service = PortScanner.get_service_name(ip_address, port)
            file.write(f"Port {port} is open - Service: {service}\n")

    print(f"Scan results for {ip_address} saved to {ip_address}_scan_results.txt")
