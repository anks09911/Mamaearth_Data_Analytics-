# Mamaearth Data Analytics

This project analyzes Mamaearth customer, product, and order data. Follow the sections below from the repository root and in order to rebuild the SQL reports, Python outputs and charts, and the final narrative. The same input files and processing steps are required to reproduce the figures in the project brief.

## Requirements

- MySQL 8 or a compatible MySQL server and command-line client
- Python 3.10 or later
- The project input data files used by the SQL and Python steps
- For Python steps: `pandas`, `numpy`, and `matplotlib`
- Optional, only for Gemini generation: `google-genai`

Run every command below from the repository root, the folder containing `sql/`, `analysis/`, and `narrator/`.

## 1. Create the database and run the SQL reports

Start your MySQL server, then load the schema and seed data in this order:

```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/seed_data.sql
```

Enter your MySQL password when prompted. Next, run the report queries:

```bash
mysql -u root -p < sql/reports.sql
```

The report script prints the SQL results in the terminal. Keep the database and source data unchanged when comparing results with the brief.

## 2. Clean and analyze the data, then create visualizations

Create and activate a virtual environment, install the Python packages, and run the analysis scripts in order:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install pandas numpy matplotlib
python analysis/clean_and_eda.py
python analysis/visualize.py
```

On macOS or Linux:

```bash
source .venv/bin/activate
python -m pip install pandas numpy matplotlib
python analysis/clean_and_eda.py
python analysis/visualize.py
```

The cleaning and EDA script writes the cleaned analysis outputs used by the visualization script. Run it first so `analysis/visualize.py` can read those outputs. **Task 5 of Part 2 writes `narrator/findings.json`**; the narrative step in the next section reads that file. Keep the original input data in place so the calculations use the same records.

## 3. Generate the narrative

The narrative script reads `narrator/findings.json` and saves its result to `narrator/sample_output.txt`. It uses the local offline narrative automatically when `GEMINI_API_KEY` is not set. This path needs no API key, Gemini account, network connection, or Gemini SDK:

```bash
python narrator/generate_narrative.py
```

To use Gemini, install its SDK and set the API key in the environment for your current terminal session before running the script. Do not put the key in this README or commit it to the repository.

Windows PowerShell:

```powershell
python -m pip install google-genai
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
python narrator/generate_narrative.py
```

macOS or Linux:

```bash
python -m pip install google-genai
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
python narrator/generate_narrative.py
```

The environment variable only applies to the current terminal session. To run offline again, clear it and rerun the script:

```powershell
Remove-Item Env:GEMINI_API_KEY
python narrator/generate_narrative.py
```

```bash
unset GEMINI_API_KEY
python narrator/generate_narrative.py
```

The script checks that the saved narrative contains the required figures. For reproducibility, compare the generated `narrator/findings.json`, SQL report results, Python output files, charts, and narrative with the corresponding values in the brief.
