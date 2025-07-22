# Email Access List Extractor

## Overview

This repository contains scripts to help extract and organize dashboard access information from email dumps and Google Looker Studio (Data Studio) assets. The main scripts are:
- `extract_dashboard_request.py`: Extracts dashboard access requests from email CSV dumps.
- `extract_viewers.py`: Fetches the list of viewer users for active dashboards from Looker Studio using the API.

---

## Scripts

### 1. extract_dashboard_request.py

**Purpose:**
Extracts key information from an email dump CSV file, specifically targeting requests for dashboard access. Outputs a CSV with the earliest request date for each user-dashboard pair.

**Features:**
- Parses large email dump CSV files efficiently
- Extracts and organizes dashboard access requests
- Handles various date and dashboard name formats
- Outputs a user-friendly CSV for further analysis or record-keeping

**Requirements:**
- Python 3.x
- [pandas](https://pandas.pydata.org/)

Install requirements:
```bash
pip install pandas
```

**Usage:**
1. Prepare your email dump CSV file. Ensure it contains at least the columns `body` (email content) and `Date`.
2. Run the script:
   ```bash
   python extract_dashboard_request.py
   ```
   - The script will prompt you to enter the path to your email CSV file.
3. The script will generate `email_first_requested_date.csv` containing the extracted information.

**Output:**
- `email_first_requested_date.csv` with columns:
  - `Email`: Email address of the requester
  - `Dashboard`: Dashboard name requested
  - `Requested Date`: Date of the earliest request

---

### 2. extract_viewers.py

**Purpose:**
Fetches the list of viewer users for a set of active dashboards from Google Looker Studio (Data Studio) using the API, and outputs the results to a CSV file.

**Features:**
- Authenticates with Google using OAuth2
- Reads a list of active dashboards and their asset IDs from a CSV (`dashboards_url.csv`)
- Fetches viewer users for each dashboard via the Looker Studio API
- Outputs a CSV with each dashboard, its asset ID, and the list of viewer users

**Requirements:**
- Python 3.x
- [google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)
- [requests](https://pypi.org/project/requests/)
- A valid `client_secret.json` file from Google Cloud Console
- A `dashboards_url.csv` file with columns: `Dashboard`, `URL IDs`

Install requirements:
```bash
pip install google-auth-oauthlib requests
```

**Usage:**
1. Ensure you have `client_secret.json` and `dashboards_url.csv` in your project directory.
2. Run the script:
   ```bash
   python extract_viewers.py
   ```
3. The script will generate `dashboard_viewers.csv` with the results.

**Output:**
- `dashboard_viewers.csv` with columns:
  - `dashboard_name`: Name of the dashboard
  - `asset_id`: Looker Studio asset ID
  - `viewer_users`: List of viewer user emails (one per line within the cell)

---

## Example Workflow
1. Use `extract_dashboard_request.py` to identify which users have requested access to which dashboards.
2. Use `extract_viewers.py` to fetch the current list of viewers for each active dashboard.
