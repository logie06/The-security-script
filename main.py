import csv
import socket
import ipaddress

from SecurityScripts.live_hostscan import StealthHostDiscovery
from SecurityScripts.portscan import PortScanner as port_scanner
from SecurityScripts.data_source import DataSourceInput
from SecurityScripts.config_server import start_http_server


def print_menu():
    print("Welcome to the Menu!")
    print("1. Perform a live host discovery and vulnerability scan on the network")
    print("2. Option 2")
    print("3. ?")
    print("4. Exit")


def host_discovery_vuln_scan():
    data = load_data_stream()
    if data is None:
        return

    domain_names, ip_ranges, ip_addresses, email_addresses = data
    ip_ranges_stream = ip_ranges
    print("Domain names:", domain_names)
    print("IP ranges:", ip_ranges_stream)
    print("IP addresses:", ip_addresses)
    print("Email addresses:", email_addresses)

    ports = [22, 80, 443, 3389]  # Specify the ports to scan

    for ip_range in ip_ranges_stream:
        scanner = StealthHostDiscovery(ip_range, ports)
        live_hosts = scanner.scan_hosts()

        output_file = f'host_scan_results_{ip_range.replace("/", "_")}.csv'
        header = ['IP Address', 'Port', 'Hostname']

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for ip, hostname, port in live_hosts:
                writer.writerow([ip, port, hostname if hostname != 'Unknown' else 'Hostname not found'])
                print(
                    f"Live Host: {ip}\tPort: {port}\tHostname: {hostname if hostname != 'Unknown' else 'Hostname not found'}")

        print(f"Scan results saved to {output_file}.")

        # Read IP addresses from host_scan_results.csv
        with open(output_file, 'r') as file:
            csv_reader = csv.reader(file)
            ip_addresses = [row[0] for row in csv_reader]

        # Scan each IP address and save the results to individual files
        for ip_address in ip_addresses:
            ports = port_scanner.get_open_ports(ip_address, port_range="1-1000")

            with open(f'{ip_address}_scan_results.txt', 'w') as file:
                for port in ports:
                    service = port_scanner.get_service_name(port)
                    file.write(f"Port {port} is open - Service: {service}\n")

                print(f"Scan results for {ip_address} saved to {ip_address}_scan_results.txt")


def option2():
    print("You chose Option 2.")
    # Add your code for Option 2 here


def http_server():
    port = 8000
    directory = "."

    start_http_server(port, directory)


def load_data_stream():
    while True:
        print("1. Generate config file")
        print("2. Load config file into script")
        print("3. Return")

        choice_data = input("Enter your choice (1-3): ")

        if choice_data == '1':
            DataSourceInput.generate_config_file()

        elif choice_data == '2':
            config_data = DataSourceInput.read_config_file()
            if len(config_data) == 5:
                domain_names, ip_ranges, ip_addresses, email_addresses, read_stat = config_data

                # Validate IP ranges
                for ip_range in ip_ranges:
                    try:
                        ipaddress.ip_network(ip_range)
                    except ValueError:
                        print(f"Invalid IP range: {ip_range}")
                        return None

                # Use the returned values as needed
                return domain_names, ip_ranges, ip_addresses, email_addresses

            else:
                print("Error reading configuration file.")

        elif choice_data == '3':
            return None

        else:
            print("Invalid choice. Please choose again.")


while True:
    print_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        host_discovery_vuln_scan()
    elif choice == "2":
        option2()
    elif choice == "3":
        load_data_stream()
    elif choice == "4":
        print("Exiting the program...")
        break
    else:
        print("Invalid choice. Please try again.")


def main():
    print_menu()


if __name__ == "__main__":
    main()
