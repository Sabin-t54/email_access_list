import csv

unique_emails = set()
omit_keywords = ['gtempaccount', 'seo']
client_domains = {
    'Dentsu': ['dentsu'],
    'Merkle': ['merkleinc', 'merkle'],
    'Ashley Furniture': ['ashleyfurniture'],
    'BofA': ['bofa'],
    'Carat': ['carat'],
    'Care': ['care'],
    'Cernobbio Group': ['cernobbiogroup'],
    'Etsy': ['etsy'],
    'Flying Cross': ['flyingcross'],
    'Granular Marketing': ['granularmarketing'],
    'GrowByData': ['growbydata'],
    'IKEA': ['ikea'],
    'IProspect': ['iprospect'],
    'NetSkope': ['netskope'],
    'Propper': ['propper'],
    'Sunday': ['sunday'],
    'Sweetwater': ['sweetwater'],
    'TravisMathew': ['travismathew'],
    'Upbott': ['upbott'],
    'UPMC': ['upmc'],
    'Vanguard': ['vanguard'],
    'WorkWise Compliance': ['workwisecompliance']
}

def find_client_name(domain_full, client_domains):
    # Split domain into parts, e.g., ['ingka', 'ikea', 'com']
    parts = domain_full.split('.')
    # Ignore TLDs
    for part in reversed(parts[:-1]):  # skip the last part (TLD)
        for client_name, domains in client_domains.items():
            if part in domains:
                return client_name
    return None

with open('dashboard_viewers.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        users = row['viewer_users'].split('\n')
        for email in users:
            email = email.strip()
            if not email:
                continue
            if '@' in email:
                domain_full = email.split('@')[1].lower()
            else:
                continue
            if any(keyword.lower() in email.lower() for keyword in omit_keywords):
                continue
            if domain_full == 'gmail.com':
                continue
            client_name = find_client_name(domain_full, client_domains)
            if client_name:
                unique_emails.add((email, client_name))

with open('unique_viewer_emails.csv', mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['email', 'client_name'])  # header
    for email, client_name in sorted(unique_emails):
        writer.writerow([email, client_name])