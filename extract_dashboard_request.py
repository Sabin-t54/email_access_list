import pandas as pd
import re
from datetime import datetime
import sys

# Enter path to csv file containing emails
input_csv = input("Enter the path to the csv file: ")

# Strip whitespace and leading/trailing double quotes
input_csv = input_csv.strip().strip('"')

# Read csv file with exception handling
try:
    df = pd.read_csv(input_csv)
except FileNotFoundError:
    print(f"Error: The file '{input_csv}' was not found.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file '{input_csv}' is empty or not a valid CSV.")
    sys.exit(1)
except pd.errors.ParserError:
    print(f"Error: The file '{input_csv}' could not be parsed as a CSV.")
    sys.exit(1)
except PermissionError:
    print(f"Error: Permission denied when trying to read '{input_csv}'.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")
    sys.exit(1)

# Filter emails that contain "Share this report"
df_filtered = df[df['body'].str.contains('Share this report', case = False, na=False)]

def safe_split(body):
    try:
        if isinstance(body, str):
            return re.split(r'\n(?:From: |\_{5,}|\-{5,})', body.strip())
        else:
            return []
    except Exception as e:
        print(f"Error processing body: {e}\nBody: {body}")
        return []
    
# Function to extract requested date, email, and dashboard from email body
def extract_email_details(body):
    formats = [
        '%A, %B %d, %Y %I:%M %p',  # 12-hour with AM/PM
        '%A, %B %d, %Y %H:%M'      # 24-hour without AM/PM
    ]
    
    messages = safe_split(body)

    last_msg = None
    for msg in reversed(messages):
        if "Share this report" in msg:
            last_msg = msg
            break

    if last_msg is None:
        # fallback to last message if none contains "Share this report"
        last_msg = messages[-1]

    # Extract Sent date from last_msg
    sent_match = re.search(r'Sent:\s*([^\n\r]+)', last_msg)
    sent_date = sent_match.group(1).strip() if sent_match else None
    if sent_date:
        for fmt in formats:
            try:
                sent_date = datetime.strptime(sent_date, fmt).strftime("%m/%d/%Y")
                break
            except ValueError:
                continue
    else:
        sent_date = pd.NaT  # or "" if you prefer an empty string

    # Extract email after "Share this report" in last_msg
    after_share = last_msg.split("Share this report", 1)[-1]
    email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', after_share)
    email = email_match.group() if email_match else None

        # Extract dashboard name from last_msg
    dashboard_match = re.search(r'([A-Za-z0-9\s\-\.]+Dashboard\s[\d\.]+(?:\s*\[[^\]]*\])?)', last_msg)
    dashboard = dashboard_match.group(1).strip() if dashboard_match else None

    return pd.Series([sent_date, email, dashboard], index=['Requested Date', 'Email', 'Dashboard'])

# Apply function to extract requested date, email, and dashboard from email body
extracted_df = df_filtered['body'].apply(extract_email_details)

# Group by email and dashboard and get the minimum requested date (helps to avoid duplicate requests or email threads)
grouped = (
    extracted_df
    .dropna(subset=['Email', 'Dashboard'])  # optional, drop incomplete rows
    .groupby(['Email', 'Dashboard'], as_index=False)
    .agg({'Requested Date': 'min'})
)

# Save to csv
grouped.to_csv("requested_date.csv", index=False)