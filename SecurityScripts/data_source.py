import csv
import os
from SecurityScripts.config_server import start_http_server


class DataSourceInput:
    @staticmethod
    def generate_config_file():
        output_file = 'Configuration.csv'
        header = ['User Questions', 'User answers']
        questions = [
            'Is there any known domain names? List as www.google.com, www.youtube.com, etc.',
            'Any known IP ranges? e.g., 192.168.0.0/24',
            'Any known single IP addresses?',
            'Company email addresses? e.g., l.dunbar@hacking.com'
        ]

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for question in questions:
                writer.writerow([question, ''])

        print("[#]Generated Configuration.csv")

    @staticmethod
    def read_config_file():
        config_dir = os.path.dirname(os.path.dirname(__file__))
        file_name = 'Configuration.csv'

        file_path = os.path.join(config_dir, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)
                domain_names = [row[1] for row in rows[1:2]]
                ip_ranges = [row[1] for row in rows[2:3]]
                ip_addresses = [row[1] for row in rows[3:4]]
                email_addresses = [row[1] for row in rows[4:5]]
            read_stat = '[#]Success!'
            return domain_names, ip_ranges, ip_addresses, email_addresses, read_stat
        else:
            read_stat = '[#]Failed'
            return read_stat



