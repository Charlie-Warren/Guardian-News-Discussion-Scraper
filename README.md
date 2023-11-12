# Guardian-News-Discussion-Scraper
Scrapes comments from Guardian news articles. Creates dataframes for use with MAXQDA, a qualitiative analysis software.

## Installation
To install required imports:

1. Open command line.
2. Run the command:
```
python -m pip install pandas requests
```

## Usage
Put any number of guardian website urls into [urls.txt](urls.txt), with each url separated with a new line.
Each url will be read and the comments will be saved in individual diorectories within [data](data).
Comments are saved in both json and csv format.