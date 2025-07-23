import csv

unique_emails = set()

with open('viewer_permissions.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        # Split the viewer_users field by newlines
        users = row['viewer_users'].split('\n')
        for email in users:
            email = email.strip()
            if email:
                unique_emails.add(email)

# Write unique emails to a new CSV
with open('unique_viewer_emails.csv', mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['email'])  # header
    for email in sorted(unique_emails):
        writer.writerow([email])