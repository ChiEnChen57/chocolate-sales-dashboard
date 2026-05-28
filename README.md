# Chocolate Sales Analytics Dashboard

An interactive data dashboard built with Python Dash, analyzing global chocolate sales performance across six countries from 2022 to 2024.

## Dashboard Preview

The dashboard includes:
- **KPI Cards** — Total Revenue, Boxes Shipped, Best Product, Top Market
- **Sales Trend Line Chart** — Top 5 / Top 10 / All products toggle, ranked by cumulative revenue
- **Sales by Country Bar Chart** — Year-filtered horizontal bar chart
- **Top 10 Sales People Bar Chart** — Click any bar to see that person's product breakdown as a donut chart
- **Product Performance Bubble Chart** — Revenue vs. shipment volume, bubble size = pricing efficiency (revenue per box)

## Data Source

Kaggle: [Chocolate Sales Dataset 2023–2024](https://www.kaggle.com/datasets/ssssws/chocolate-sales-dataset-2023-2024)

The dataset contains chocolate sales transactions across 6 countries (Australia, Canada, India, New Zealand, UK, USA) with the following fields:

| Column | Description |
|---|---|
| Sales Person | Name of the salesperson |
| Country | Market country |
| Product | Chocolate product name |
| Date | Transaction date |
| Amount | Transaction revenue (USD) |
| Boxes Shipped | Number of boxes shipped |

## Project Structure

```
├── chocolate_dashboard.py     # Main Dash application
├── Chocolate Sales.csv        # Dataset
├── writeup.pdf                # Project write-up (3 pages)
├── requirements.txt           # Python dependencies
└── README.md
```

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## How to Run

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure `Chocolate Sales.csv` is in the same directory as `chocolate_dashboard.py`

4. Run the app:
```bash
# Mac/Linux
python3 chocolate_dashboard_final.py

# Windows
python chocolate_dashboard_final.py
```

5. Open your browser and go to:
```
http://127.0.0.1:8050
```

## Features

| Feature | Description |
|---|---|
| Country Filter | Multi-select dropdown to filter by market |
| Product Filter | Optional product filter (blank = all) |
| Year Slider | Switch between 2022, 2023, 2024 |
| Line Chart Toggle | Switch between Top 5 / Top 10 / All products |
| Click Interaction | Click a salesperson bar to view their product breakdown |
| Country Flags | Flag icons update dynamically based on selected countries |

## Tools Used

- [Plotly Dash](https://dash.plotly.com/) — Dashboard framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — Visualizations
- [Pandas](https://pandas.pydata.org/) — Data processing
