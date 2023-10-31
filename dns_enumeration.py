import dns.resolver as dns
import socket
from sys import argv
import json

# Get command line arguments

try:
    domain = argv[1]
except IndexError:
    domain = ''
if domain == '' or domain is None:
    print('Usage: python3 dns_enumeration.py <domain/ip>')
    exit(0)
if domain.split('.')[0].isnumeric():
    domain = socket.gethostbyaddr(domain)[0]
record_types = ['A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'HTTPS', 'IPSECKEY', 'MX', 'NAPTR', 'NS', 'PTR', 'SPF', 'SRV', 'SSHFP', 'SVCB', 'TLSA', 'TXT']

records = []
for record_type in record_types:
    try:
        answers = dns.resolve(domain, record_type)
        for rdata in answers:
            records.append({'domain': domain, 'record_type': record_type, 'record_data': str(rdata)})
    except dns.NoAnswer:
        records.append({'domain': domain, 'record_type': record_type, 'record_data': 'No Answer'})
    except dns.NXDOMAIN:
        records.append({'domain': 'No Domain', 'record_type': 'No Answer', 'record_data': 'No Answer'})
        break
    except dns.LifetimeTimeout:
        records.append({'domain': 'Timeout', 'record_type': 'Timeout', 'record_data': 'Timeout'})
        break

response = json.dumps(records)

print(response)