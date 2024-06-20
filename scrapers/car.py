import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from data import OffsetProject

PROJECT_FILE = "data/car/projects.json"
FINAL = "data/car_final.csv"


def get_page(page=1, r="111"):
    cookies = {
        "ASPSESSIONIDQWSTATAQ": "DLOFILGCJDEEEBGDBKDKAECK",
        "ASPSESSIONIDQUSTBRAR": "JBMOAIBDFJPLKKMAMNHBEDPL",
        "ASPSESSIONIDQGCRSQDA": "DBMJDFCBPEFMDCNNEKJILNFE",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://thereserve2.apx.com",
        "Connection": "keep-alive",
        "Referer": "https://thereserve2.apx.com/myModule/rpt/myrpt.asp?r=111",
        # 'Cookie': 'ASPSESSIONIDQWSTATAQ=DLOFILGCJDEEEBGDBKDKAECK; ASPSESSIONIDQUSTBRAR=JBMOAIBDFJPLKKMAMNHBEDPL; ASPSESSIONIDQGCRSQDA=DBMJDFCBPEFMDCNNEKJILNFE',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=1",
    }

    data = {
        "r": "111",
        "X999myquery": "",
        "X999tablenumber": "2",
        "X999csv": "",
        "X999sort": "",
        "X999action": "",
        "X999actionfield": "",
        "X999field": "",
        "X999paging": "On",
        "X999whichpage": str(page),
    }

    response = requests.post(
        "https://thereserve2.apx.com/myModule/rpt/myrpt.asp",
        cookies=cookies,
        headers=headers,
        data=data,
    )

    soup = BeautifulSoup(response.text, "html.parser")
    main_table = soup.select("table")[3]  # lol!

    rows = main_table.select("tr")
    table_head = rows[0]
    col_names = [c.text.strip() for c in table_head.select("td")]

    items = []

    for row in rows[1:]:
        item = {}
        cols = row.select("td")
        for c, cn in zip(cols, col_names):
            item[cn] = c.text.strip()

        try:
            item["Developer URL"] = cols[3].select_one("a").attrs.get("href")
        except Exception as e:
            item["Developer URL"] = ""
        try:
            item["Project URL"] = cols[5].select_one("a").attrs.get("href")
        except Exception as e:
            item["Project URL"] = ""
        try:
            item["Documents URL"] = cols[-3].select_one("a").attrs.get("href")
        except Exception as e:
            item["Documents URL"] = ""

        items.append(item)

    last_page = soup.select_one("#x999nextoff2")

    if last_page:
        has_next = False
    else:
        has_next = True

    return (has_next, items)


def get_all(outname=PROJECT_FILE):
    print("Getting projects from American Carbon")
    page = 1
    has_next = True
    items = []
    while has_next:
        print("page", page)
        has_next, _items = get_page(page=page)
        items += _items
        page += 1

    with open(outname, "w") as outfile:
        json.dump(items, outfile)


def get_project_description(url):
    desc = ""
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        desc = (
            soup.find(text=re.compile("project description", re.IGNORECASE))
            .parent.find_next("td")
            .text.strip()
        )
    except Exception as e:
        pass
    return desc


def get_project_descriptions():
    print("Getting project descriptions from American Carbon")

    with open(PROJECT_FILE, "r") as infile:
        projects = json.load(infile)

    for p in projects:
        url = p["Project URL"]
        if url == "":
            continue
        url = "https://thereserve2.apx.com" + url
        print(url)
        description = get_project_description(url)
        p["description"] = description

    with open(PROJECT_FILE, "w") as outfile:
        json.dump(projects, outfile)


def merge():
    with open(PROJECT_FILE, "r") as infile:
        projects = json.load(infile)

    out = []

    for p in projects:
        total = re.sub(r"\D", "", p["Total Number of Offset Credits Registered"])
        if total == "":
            total = 0.0
        else:
            total = float(total)

        registry_url = "https://thereserve2.apx.com" + p["Project URL"]
        loc = f'{p["Project Site Location"]}, {p["Project Site State"]}, {p["Project Site Country"]}'

        project = OffsetProject(
            registry_id=p["Project ID"],
            total_credits=total,
            description=p["description"],
            status=p["Status"] + "; " + p["ARB Project Status"],
            registry_url=registry_url,
            developer=p["Project Developer"],
            project_type=p["Project Type"],
            methodology="",
            location=loc,
            name=p["Project Name"],
            registry="car",
        )

        out.append(project.dict())

    out = pd.DataFrame.from_records(out)
    out.to_csv(FINAL, index=False)
    return out


def run():
    get_all()
    get_project_descriptions()
    merge()


if __name__ == "__main__":
    run()
