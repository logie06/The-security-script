import csv
import socket

from SecurityScripts.live_hostscan import StealthHostDiscovery
from SecurityScripts.portscan import PortScanner as port_scanner
from SecurityScripts.data_source import DataSourceInput


def print_menu():
    print("Welcome to the Menu!")
    print("1. Perform a live host discovery and vulnerability scan on the network")
    print("2. Option 2")
    print("3. ?")
    print("4. Exit")


def option1():
    print("You chose Option 1.")

    print("Would you like to load data from data source?(Y/N):  ")
    choice_data = input("")

    if choice_data == "Y":
        print("1. Generate config file")
        print("2. Load config file into script")
        print("3. Return")

        choice_data = input("Enter your choice (1-3):   ")

        if choice_data == '1':
            DataSourceInput.generate_config_file()

        elif choice_data == '2':
            domain_names, ip_ranges, ip_addresses, email_addresses = DataSourceInput.read_config_file()

            # Use the returned values as needed
            print("Domain names:", domain_names)
            print("IP ranges:", ip_ranges)
            print("IP addresses:", ip_addresses)
            print("Email addresses:", email_addresses)

            print("[#]Resolving each domain name provided....")

            for domain_name in domain_names:
                try:
                    ip_address = socket.gethostbyname(domain_name)
                    ip_addresses.append(ip_address)
                    return ip_addresses
                except socket.gaierror:
                    print(f"[#]Unable to resolve domain name: {domain_name}")


        elif choice_data == '3':
            return

        else:
            print("Invalid choice please choose again")
            return

    if choice_data == "N":
        ports = [22, 80, 443, 3389]  # Specify the ports to scan
        ip_range = '192.168.0.0/24'
        # ip_range = input("Enter IP address range: ")

        scanner = StealthHostDiscovery(ip_range, ports)
        live_hosts = scanner.scan_hosts()

        output_file = 'host_scan_results.csv'
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
        with open('host_scan_results.csv', 'r') as file:
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


def option3():
    print("You chose Option 3.")
    # Add your code for Option 3 here


while True:
    print_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        option1()
    elif choice == "2":
        option2()
    elif choice == "3":
        option3()
    elif choice == "4":
        print("Exiting the program...")
        break
    else:
        print("Invalid choice. Please try again.")


def main():
    print_menu()


if __name__ == "__main__":
    main()
