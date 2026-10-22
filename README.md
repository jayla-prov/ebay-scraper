# eBay Scraper

ebay-dl.py collects listings from the first 10 pages of an eBay search and saves them as JSON. Each listing includes its name, price, condition, shipping cost, free-return status, and number sold. Prices and shipping costs are stored as integer cents and missing fields are saved as null.

## Saved searches

eBay returned HTTP 403 when I attempted a live search. All three JSON files use the supplied practice data. They contain the same practice listings despite having different search names.


```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "golf clubs" --pages-dir practice-pages
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages
```

[Project instructions](https://csci40.rtealwitter.com/projects/02_webscraping/project.html)

## CSV output

Add --csv to save CSV instead of JSON. These commands generate the 3 CSV files using practice data.

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
python ebay-dl.py --search "golf clubs" --pages-dir practice-pages --csv
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages --csv
```