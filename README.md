# Email Access List Extractor

## Overview

This Python script extracts key information from an email dump CSV file, specifically targeting requests for dashboard access. It is designed to help teams quickly identify and organize:

- **Email Address** of the user requesting dashboard access
- **Dashboard Name** being requested
- **Requested Data** or details associated with the request

The script processes the raw email dump and outputs a clean, structured CSV file containing only the relevant information.

---

## Features

- Parses large email dump CSV files efficiently
- Extracts and organizes dashboard access requests
- Outputs a user-friendly CSV for further analysis or record-keeping

---

## Requirements

- Python 3.x
- [pandas](https://pandas.pydata.org/) library

You can install the required package using:

```bash
pip install pandas
```

---

## Usage

1. **Prepare your email dump CSV file.**
   - Ensure the file contains the necessary columns (e.g., email content, sender, etc.).

2. **Run the script:**

   ```bash
   python extract_dashboard_request.py <output_extracted.csv>
   ```

   - Replace `<output_extracted.csv>` with the desired output file name.

3. **Check the output.**
   - The script will generate a CSV file containing the extracted email addresses, dashboard names, and requested data.

---

## Example

```bash
python extract_dashboard_request.py dashboard_requests.csv
```

---

## Output

The output CSV will contain the following columns:

- `Email Address`
- `Dashboard Name`
- `Requested Data`

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss your ideas or report bugs. 
