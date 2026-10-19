# Google Play Store App Analytics

An exploratory data analysis of the Android app market using a dataset of roughly 10,800 apps scraped from the Google Play Store. The project uses **pandas** for cleaning and analysis and **Plotly Express** for interactive charts.

## Dataset

`apps.csv` holds app data scraped from the Google Play Store by Lavanya Gupta in 2018 ([original on Kaggle](https://www.kaggle.com/lava18/google-play-store-apps)).

- **Rows:** 10,841 apps
- **Columns:** 12

| Column | Description |
| --- | --- |
| `App` | App name |
| `Category` | Store category (e.g. `GAME`, `FAMILY`, `TOOLS`) |
| `Rating` | Average user rating (1–5); 1,474 rows are missing a value |
| `Reviews` | Number of user reviews |
| `Size_MBs` | App size in megabytes |
| `Installs` | Install bracket stored as text (e.g. `"1,000,000"`) |
| `Type` | `Free` or `Paid` |
| `Price` | Price stored as text (e.g. `"$2.99"`, or `0` for free apps) |
| `Content_Rating` | Audience rating (e.g. `Everyone`, `Teen`, `Mature 17+`) |
| `Genres` | One or more genres separated by `;` |
| `Last_Updated` | Date of the last update |
| `Android_Ver` | Minimum Android version required |

## Project structure

```
.
├── Google Play Store App Analytics (start).ipynb   # Main notebook: guided challenges
├── app.py                                          # Script version of the completed steps
├── apps.csv                                        # Dataset
└── requirements.txt                                # Python dependencies
```

## Getting started

Requires Python 3.10 or later.

```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the notebook

```bash
jupyter notebook "Google Play Store App Analytics (start).ipynb"
```

### Run the script

```bash
python app.py
```

`app.py` prints the cleaning and summary steps to the terminal and opens the Content Rating pie chart in your browser.

## Analysis steps

### Done so far

1. **Explore the data**: shape, column names and a random sample of rows.
2. **Drop unused columns**: `Last_Updated` and `Android_Ver`.
3. **Remove missing ratings**: drop rows where `Rating` is NaN, which gives `df_apps_clean`.
4. **Remove duplicates**: drop repeated rows. The Instagram app, for example, appears several times.
5. **Highest-rated apps**: find the apps with the top rating. Many of them have only a handful of reviews.
6. **Largest apps**: the 5 biggest apps by `Size_MBs`.
7. **Most-reviewed apps**: the top 50 by review count, with a check for any paid apps among them.
8. **Content ratings**: a Plotly pie chart of the `Content_Rating` distribution.

### Still to do (empty cells in the notebook)

- Convert `Installs` and `Price` to numeric types
- Find the most expensive apps, remove junk apps priced over $250, and estimate revenue (`Installs × Price`)
- Bar charts and a scatter plot of category competition versus downloads
- Split the nested `Genres` column and chart genre competition with colour scales
- Grouped bar chart of free versus paid apps per category
- Box plots of installs (free versus paid), revenue by category and paid-app pricing by category

## Notes

- `Installs` and `Price` contain commas and `$` signs. Clean them before running any numeric operations.
- `app.py` drops duplicates using `App`, `Type` and `Price` as keys. The notebook currently uses a full-row `.drop_duplicates()`, which keeps rows that differ only in fields like `Reviews`, so the two can give different row counts.
- Ratings alone are a poor measure of quality: an app with one 5-star review ranks the same as one with millions. Consider review counts alongside ratings.

## Dependencies

Listed in `requirements.txt`:

- `pandas`
- `plotly`
- `numpy`
- `notebook` (Jupyter)
