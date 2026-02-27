from collections import Counter
import sys

MIN_FIELDS = 6

def analyze_log(file_path):
    total = 0
    success = 0
    client_errors = 0
    server_errors = 0
    redirects = 0
    ip_counter = Counter()

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue

                parts = line.split()

                if len(parts) < MIN_FIELDS: # Not enough fields to parse, skip this line
                    continue

                ip_address = parts[0]

                try:
                    status_code = int(parts[10]) # Status code is usually the 11th field in common log format
                except ValueError: 
                    continue

                total += 1
                ip_counter[ip_address] += 1

                if 200 <= status_code < 300:
                    success += 1
                elif 300 <= status_code < 400:
                    redirects += 1  
                elif 400 <= status_code < 500:
                    client_errors += 1
                elif 500 <= status_code < 600:
                    server_errors += 1

    except FileNotFoundError:
        print(f'Error: File {file_path} not found.')
        return
    
    print(f'Total requests: {total}')
    print(f'Successful requests: {success}')
    print(f'Redirects: {redirects}')
    print(f'Client errors: {client_errors}')
    print(f'Server errors: {server_errors}')

    if ip_counter:
        most_common_ip, count = ip_counter.most_common(1)[0]
        print(f'Most common IP: {most_common_ip} ({count} requests)')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <log_file_path>")
    else:
        analyze_log(sys.argv[1])
    