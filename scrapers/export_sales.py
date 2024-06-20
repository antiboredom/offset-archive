import pandas as pd
import json
import requests
import re
import zipfile
from bs4 import BeautifulSoup


def download_raw():
    soup = BeautifulSoup(requests.get(ZIP_URL_HOME).text, "html.parser")
    link = soup.find(string=re.compile("Download the raw registry files"))
    url = ZIP_URL_BASE + link.parent.attrs.get("href")
    local_name = "sales_data.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_name


def combine_data(local_name="sales_data.zip"):
    all = []
    with zipfile.ZipFile(local_name) as z:
        filenames = z.namelist()
        for f in filenames:
            _f = f.split("/")[-1]
            parser = PARSERS.get(_f)
            if parser is None:
                continue
            with z.open(f, "r") as infile:
                all.append(parser(infile))

    all = pd.concat(all)
    # headers = ["project_id", "project_name", "total", "date", "details"]
    headers = ["id", "date", "details", "total", "type"]
    all = all[headers]
    all["date"] = pd.to_datetime(all["date"], format="mixed")
    all.dropna(inplace=True)
    all.to_csv("data/all_sales.csv", index=False)

    all["date"] = all["date"].astype(str)
    values = all.values.tolist()

    with open("data/all_sales.json", "w") as outfile:
        json.dump({"headers": headers, "values": values}, outfile)


def parse_gold(fname):
    print("GOLD")
    # headers: ['Vintage', 'Credit Status', 'Quantity', 'GSID', 'Project Name', 'Project Developer', 'Country', 'Product Type', 'Project Type', 'Methodology', 'Programme of Activities', 'POA GSID', 'Issuance Date', 'Retirement Date', 'Monitoring Period Start', 'Monitoring Period End', 'Serial Number', 'Note', 'Eligible for CORSIA?', 'Retired for CORSIA?', 'CORSIA Authorisation', 'Aeroplane Operator Name']
    df = pd.read_csv(fname)
    df = df[
        [
            "GSID",
            # "Project Name",
            "Quantity",
            "Retirement Date",
            "Note",
        ]
    ]
    df = df.rename(
        columns={
            # "Project Name": "project_name",
            "Retirement Date": "date",
            "Note": "details",
            "GSID": "id",
            "Quantity": "total",
        }
    )
    df["type"] = 0
    return df


def parse_acr(fname):
    print("ACR")
    # headers: ['Status Effective', 'Account Holder', 'Quantity of Credits', 'Retirement Reason', 'Retirement Reason Details', 'Credit Serial Numbers', 'Vintage', 'Date Issued (GMT)', 'Verified Removal', 'CORSIA Eligible', 'ARB Eligible', 'Ecology Eligible', 'Sustainable Development Goal(s)', 'Project ID', 'Project Name', 'Project Site Country', 'Project Site Location', 'Project Site State', 'Project Type', 'Project Methodology/Protocol', 'Methodology/Protocol Version', 'Unnamed: 21']
    df = pd.read_csv(fname, encoding="latin_1")
    df = df[
        [
            "Project ID",
            # "Project Name",
            "Quantity of Credits",
            "Status Effective",
            "Retirement Reason Details",
        ]
    ]
    df = df.rename(
        columns={
            # "Project Name": "project_name",
            "Status Effective": "date",
            "Retirement Reason Details": "details",
            "Project ID": "id",
            "Quantity of Credits": "total",
        }
    )
    df["type"] = 2
    return df


def parse_car(fname):
    print("CAR")
    # headers: ['Vintage', 'Offset Credit Serial Numbers', 'Quantity of Offset Credits', 'Status Effective', 'Project ID', 'Project Name', 'Project Type', 'Reduction/Removal', 'Protocol Version', 'Project Site Location', 'Project Site State', 'Project Site Country', 'Additional Certification(s)', 'CORSIA Eligible', 'Corresponding Adjustment', 'Account Holder', 'Retirement Reason', 'Retirement Reason Details', 'Unnamed: 18']
    df = pd.read_csv(fname, encoding="latin_1", on_bad_lines="skip")
    df = df[
        [
            "Project ID",
            # "Project Name",
            "Quantity of Offset Credits",
            "Status Effective",
            "Retirement Reason Details",
        ]
    ]
    df = df.rename(
        columns={
            # "Project Name": "project_name",
            "Status Effective": "date",
            "Retirement Reason Details": "details",
            "Project ID": "id",
            "Quantity of Offset Credits": "total",
        }
    )
    df["type"] = 3
    return df


def parse_verra(fname):
    print("Verra")
    # headers: ['Issuance Date', 'Sustainable Development Goals', 'Vintage Start', 'Vintage End', 'ID', 'Name', 'Country/Area', 'Project Type', 'Methodology', 'Total Vintage Quantity', 'Quantity Issued', 'Serial Number', 'Additional Certifications', 'Retirement/Cancellation Date', 'Retirement Beneficiary', 'Retirement Reason', 'Retirement Details']
    df = pd.read_excel(fname)
    df = df[
        [
            "ID",
            # "Name",
            "Quantity Issued",
            "Issuance Date",
            "Retirement Details",
        ]
    ]
    df = df.rename(
        columns={
            # "Name": "project_name",
            "Issuance Date": "date",
            "Retirement Details": "details",
            "ID": "id",
            "Quantity Issued": "total",
        }
    )
    df["type"] = 1
    return df


ZIP_URL_BASE = "https://gspp.berkeley.edu"
ZIP_URL_HOME = (
    ZIP_URL_BASE
    + "/research-and-impact/centers/cepp/projects/berkeley-carbon-trading-project/offsets-database"
)

PARSERS = {
    "Gold Retirements.csv": parse_gold,
    "CAR Retirements.csv": parse_car,
    "VERRA vcus.xlsx": parse_verra,
    "ACR Retirements.csv": parse_acr,
}


if __name__ == "__main__":
    download_raw()
    combine_data()
