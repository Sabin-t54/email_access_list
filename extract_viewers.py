import csv
import requests

# get access token
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/datastudio.readonly']
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
creds = flow.run_local_server(port=0)

active_dashboard_list = [
    'American Express - Dashboard 2.4',
    'Ashley Home Furniture - Dashboard 2.4',
    'Care.com - Dashboard 2.4',
    'Care Test & Learn - Dashboard 2.4',
    'Cleveland Clinic UK - Dashboard 2.4',
    'Dentsu Insight - Brand',
    'Dentsu Industry Retail - Dashboard 2.4',
    'Dentsu Industry Health - Dashboard 2.4',
    'Dentsu Industry High-Tech - Dashboard 2.4',
    'Dentsu Industry Travel - Dashboard 2.4,',
    'Dentsu Industry FiServ - Dashboard 2.4',
    'Dentsu Industry Automotive - Dashboard 2.4',
    'Dentsu Industry Software Dashboard 2.4',
    'Finance SME - Dashboard 2.4',
    'Gerber Life Insurance - Dashboard 2.4',
    'L.L.Bean - Dashboard 2.4',
    'Netskope - Dashboard 2.4',
    'Sweetwater - Dashboard 2.4',
    'UPMC - Dashboard 2.4',
    'Vanguard - Dashboard 2.4',
    'WorkWise & Labor Lawn Posters - Dashboard 2.4',
    'IKEA - Dashboard 2.4',
    'Propper - Dashboard 2.4',
    'Etsy - Dashboard 2.4',
    'TravisMathew - Dashboard 2.4',
    'Vertx - Dashboard 2.4',
    'Cargurus - Dashboard 2.4',
    'Microsoft - Dashboard 2.4',
    'General Motors - Dashboard 2.4',
    'General Motors LLM - Dashboard 2.4',
    'Sono Bello - Dashboard 2.4',
    'Tiffany & Co - Dashboard 2.4',
    'Bank of America - Dashboard 2.4',
    'Sunday Natural - Dashboard 2.4',
]

active_dashboard_report_link = {}

with open('dashboards_url.csv', mode = 'r', newline = '', encoding = 'utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Dashboard'] in active_dashboard_list:
            active_dashboard_report_link[row['Dashboard']] = row['URL IDs']

# Output CSV file
output_csv = 'dashboard_viewers.csv'

def fetch_viewer_users(asset_id, access_token = creds.token):
    """Fetch only 'user:' entries under VIEWER permissions for a given asset."""
    
    url = f'https://datastudio.googleapis.com/v1/assets/{asset_id}/permissions'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        permissions = response.json().get('permissions', {})
        return [
            member.split(':', 1)[1]
            for member in permissions.get('VIEWER', {}).get('members', [])
            if member.startswith('user:')
        ]
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching {asset_id}: {e}")
        return []

# Write all results to CSV
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['dashboard_name', 'asset_id', 'viewer_users'])
    writer.writeheader()

    for dashboard_name, asset_id in active_dashboard_report_link.items():
        viewer_users = fetch_viewer_users(asset_id)
        if viewer_users:
            writer.writerow({
                'dashboard_name': dashboard_name,
                'asset_id': asset_id,
                'viewer_users': '\n'.join(viewer_users)
            })
            print(f"✓ Successfully retrieved users: {dashboard_name}")
        else:
            print(f"⚠️ No viewer users or failed: {dashboard_name}")