import csv


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
        with open('Configuration.csv', 'r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            domain_names = [row[1] for row in rows[1:1]]
            ip_ranges = [row[1] for row in rows[2:2]]
            ip_addresses = [row[1] for row in rows[3:3]]
            email_addresses = [row[1] for row in rows[4:4]]

        return domain_names, ip_ranges, ip_addresses, email_addresses
