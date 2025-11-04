#!/usr/bin/env python3

#Nathaniel Hartley
#11/3/25

import re
import sys
from collections import defaultdict
from geoip import geolite2
from datetime import datetime

#Initializing constant of the path to the provided syslog file
LOG_FILE_PATH = '/home/student/syslog.log'

#Regular expression used to match failed login attempts to identify potential suspicious ip addresses
FAILED_LOGIN_PATTERN = r'Failed password for.* from (\S+)'

#Function that reads and scans through the log file looking for matches to the above regular expression
#if a line in the log file matches the regular expression, the associated ip address is saved 
#that failed login attempt is then incremented in the int dictionary using its associated IP address as the key
def scan_log_file(log_file_path):
    failed_login_attempts = defaultdict(int)
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            match = re.search(FAILED_LOGIN_PATTERN, line)
            if match:
                ip_address = match.group(1)
                failed_login_attempts[ip_address] += 1
    return failed_login_attempts

#Function gets the country associated with a certain IP address by using the geolite2 module lookup function
#if there is a match and that match has an associated country, the country is returned.
#If there is not country match, 'unknown' is returned
def get_country(ip_address):
    match = geolite2.lookup(ip_address)
    if match and match.country:
        return match.country
    return 'Unknown'

#Function generates report with proper formatting and date and iterates through the failed_login_attempts dictionary to get the IP address and number of logins for each address
#It then uses the get_country_from_ip function to match the country to the ip address (if it exists)
def report(failed_login_attempts):

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_with_high_attempts = {ip: count for ip, count in failed_login_attempts.items() if count >= 10}
    print(f"ATTACK REPORT - {report_date}\n")
    print(f"{'IP Address':<20} {'Failed Attempts':<20} {'Country'}")
    print("-" * 60)

    for ip, count in ip_with_high_attempts.items():
        country = get_country(ip)
        print(f"{ip:<20} {count:<20} {country}")
 
def main():
    print("Generating attack report...\n")
    failed_login_attempts = scan_log_file(LOG_FILE_PATH)
    report(failed_login_attempts)

if __name__ == '__main__':
    main()
