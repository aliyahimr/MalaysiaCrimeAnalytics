# Malaysia Crime Analytics

A small data analytics project using Malaysian crime data from OpenDOSM.

I made this project mainly to **learn and practise data analytics** using a real-world Malaysian dataset. This is a personal learning project, not a formal research project. Basically, I wanted to see what I could actually find from the data instead of just staring at tutorials forever.

## 📊 Dataset

The dataset comes from **OpenDOSM**, under the Department of Statistics Malaysia.

**Dataset:** Crimes by District & Crime Type
**Source:** OpenDOSM
**Data period:** 2016–2023
**Frequency:** Annual
**Geographical level:** Police district
**Data source:** Royal Malaysia Police and Department of Statistics Malaysia

🔗 Dataset: https://open.dosm.gov.my/data-catalogue/crime_district

The dataset contains information such as:

* State
* Police district
* Crime category
* Crime type
* Number of crimes
* Year

The dataset contains **thousands of crime records** covering Malaysia from 2016 to 2023.

> Note: `district` refers to a **police district**, not an administrative district.

The dataset represents actual crimes where a conviction was secured, rather than simply all reported cases. Unreported crimes are also not included.

## 🔎 What I Did

I used Python to go through the data analytics process:

1. Data collection
2. Data understanding
3. Data cleaning
4. Exploratory Data Analysis (EDA)
5. Statistical analysis
6. Pattern analysis
7. Clustering
8. Data visualization

The analysis looks at crime patterns across:

* Years
* States
* Police districts
* Crime categories
* Crime types

I also used **K-Means clustering** to group police districts based on similar crime characteristics.

## 📈 Analysis Coverage

The analysis covers Malaysian crime data from:

**2016 → 2023**

This means the project looks at crime patterns across **8 years of annual data**.

The analysis produces tables and visualisations for things such as:

* Crime trends by year
* Total crime by state
* Crime by category
* Crime by crime type
* Top police districts by recorded crimes
* State and category patterns
* Crime trends over time
* Statistical distributions
* Police district clusters
* Cluster characteristics

## 🛠️ Tools Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Fastparquet
* Git & GitHub

## 📁 Project Structure

```text
MalaysiaCrimeAnalytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── data_collection.py
│   ├── data_understanding.py
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── statistics.py
│   ├── pattern_analysis.py
│   ├── clustering.py
│   └── visualization.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── run_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ▶️ Run the Analysis

After installing the required packages:

```bash
python run_analysis.py
```

The analysis runs all stages automatically from data collection until visualisation.

## 🎯 Why I Made This

This project was mainly made for **learning and practice**.

I wanted to:

* Practise working with real-world data
* Learn how to clean and prepare datasets
* Understand exploratory data analysis
* Practise statistical analysis
* Learn how to identify patterns in data
* Try clustering on a real dataset
* Improve my Python and data analytics skills
* Build something using Malaysian public data

There is no huge research agenda behind this project. I basically wanted to **learn by actually doing a complete data analytics project** instead of collecting another 47 tutorials that I will never finish.

## ⚠️ Data Notes

The dataset has some limitations:

* The available data covers 2016–2023.
* Data is provided at annual frequency.
* Police districts are not the same as administrative districts.
* The dataset does not represent all crimes because unreported crimes are excluded.
* The number of crimes should not automatically be interpreted as the crime risk or safety level of an area.
* The analysis shows patterns in the available dataset and does not establish causal relationships.

## 📚 Data Source

OpenDOSM – Department of Statistics Malaysia

https://open.dosm.gov.my/data-catalogue/crime_district

Dataset licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

---

**Project:** Malaysia Crime Analytics
**Field:** Data Analytics
**Purpose:** Personal learning & practice
**Data:** Malaysian crime data
**Period:** 2016–2023