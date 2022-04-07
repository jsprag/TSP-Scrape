# TSP Share Price Scraper

Scrapes Thrift Savings Plan (TSP) fund prices from [TSP Website][tsp] for import into Quicken.

## Quicken (Windows)
Downloads TSP fund prices into a single file *tspQuicken.csv* for import into *Quicken (Windows)*.

## Quicken For Mac
*Quicken for Mac* can only import fund prices for a single Security at a time:
* Windows &rarr; Securities &rarr; (Double click a Security) &rarr; Price History &rarr; Import History From CSV File...

If running on MacOS, this script also saves results into individual *security*.csv files.

```bash
# MacOS conversion requires pandas
pip install pandas
```

# History
| Date       | Description |
| ----       | ----------- |
| 2022-06-03 | [Updated][mysteriousclam-tsp-update] for new TSP.gov website by [mysteriousclam][mysteriousclam-bogle] |
| 2020-02-03 | [Updated][jsprag-python3] to Python3 by [jsprag][jsprag-bogle] |
| 2013-01-06 | [Created][simbilis-created] by [Simbilis][simbilis-bogle] on the [Bogleheads forum][bogleheads] |

[tsp]: https://www.tsp.gov
[bogleheads]: https://bogleheads.org

[mysteriousclam-bogle]: https://www.bogleheads.org/forum/memberlist.php?mode=viewprofile&u=186009
[mysteriousclam-tsp-update]: https://www.bogleheads.org/forum/viewtopic.php?p=6708886#p6708886
[jsprag-bogle]: https://www.bogleheads.org/forum/memberlist.php?mode=viewprofile&u=127367
[jsprag-python3]: https://www.bogleheads.org/forum/viewtopic.php?p=5038932#p5038932
[simbilis-bogle]: https://www.bogleheads.org/forum/memberlist.php?mode=viewprofile&u=40770
[simbilis-created]: https://www.bogleheads.org/forum/viewtopic.php?f=1&t=108388
