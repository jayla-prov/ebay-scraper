import re
import argparse
import json
import time
import requests
import csv

from bs4 import BeautifulSoup

def get_text(item, selector):
    element = item.select_one(selector)
    if element is None:
        return None
    return element.get_text(strip=True)


def get_cents(text):
    if text is None:
        return None

    match = re.search(r"(\d[\d,]*)(?:\.(\d{1,2}))?", text)
    if match is None:
        return None

    dollars = int(match.group(1).replace(",", ""))
    decimal = match.group(2)

    cents = 0
    if decimal is not None:
        cents = int(decimal.ljust(2, "0"))

    return dollars * 100 + cents


def extract_items(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for item in soup.select(".s-item"):
        name = get_text(item, ".s-item__title")
        price = get_cents(get_text(item, ".s-item__price"))
        status = get_text(item, ".SECONDARY_INFO")

        shipping_text = get_text(item, ".s-item__shipping")
        shipping = None
        if shipping_text is not None:
            if "free" in shipping_text.lower():
                shipping = 0
            else:
                shipping = get_cents(shipping_text)

        returns_text = get_text(item, ".s-item__free-returns")
        free_returns = None
        if returns_text is not None:
            free_returns = "free returns" in returns_text.lower()

        sold_text = get_text(item, ".s-item__hotness")
        items_sold = None
        if sold_text is not None:
            number = sold_text.split()[0]
            items_sold = int(number.replace(",", "").replace("+", ""))

        items.append({
            "name": name,
            "price": price,
            "status": status,
            "shipping": shipping,
            "free_returns": free_returns,
            "items_sold": items_sold,
        })

    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", required=True)
    parser.add_argument("--pages-dir")
    parser.add_argument("--csv", action="store_true")
    args = parser.parse_args()

    all_items = []

    for page in range(1, 11):
        if args.pages_dir is not None:
            filename = f"{args.pages_dir}/page-{page}.html"
            with open(filename, encoding="utf-8") as file:
                html = file.read()
        else:
            if page > 1:
                time.sleep(1)

            response = requests.get(
                "https://www.ebay.com/sch/i.html",
                params={"_nkw": args.search, "_pgn": page},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            print("HTTP status:", response.status_code)
            response.raise_for_status()
            html = response.text

            if "robot check" in html.lower() or "pardon our interruption" in html.lower():
                print("eBay blocked the request. Use --pages-dir practice-pages.")
                return

        items = extract_items(html)

        if not items:
            print("No listings found. Stop and check the HTML or use practice pages.")
            return

        all_items.extend(items)
        print(f"Page {page}: {len(items)} listings")

    if args.csv:
        filename = args.search + ".csv"
        with open(filename, "w", newline="", encoding="utf-8") as file:
            fields = [
                "name", "price", "status",
                "shipping", "free_returns", "items_sold"
            ]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_items)
    else:
        filename = args.search + ".json"
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(all_items, file, indent=4)

    print(f"Saved {len(all_items)} listings to {filename}")


if __name__ == "__main__":
    main()