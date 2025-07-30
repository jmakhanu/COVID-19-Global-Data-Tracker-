# covid_tracker.py

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os # Import os module to handle file paths

# --- 1. Data Collection ---
# Goal: Obtain a reliable COVID-19 dataset.
# The recommended dataset is from Our World in Data.
# You should have already downloaded 'owid-covid-data.csv'
# and placed it in the same directory as this script.

# Define the filename for the dataset
DATA_FILENAME = 'owid-covid-data.csv'

# --- 2. Data Loading & Exploration ---
# Goal: Load the dataset and explore its structure.

print("--- Data Loading & Exploration ---")

# Construct the full path to the CSV file
# This helps ensure the script finds the file whether run from its directory
# or from a different current working directory.
script_dir = os.path.dirname(__file__) if '__file__' in locals() else os.getcwd()
data_path = os.path.join(script_dir, DATA_FILENAME)

# Load data using pandas.read_csv()
try:
    df = pd.read_csv(data_path)
    print(f"Dataset '{DATA_FILENAME}' loaded successfully from: {data_path}")
except FileNotFoundError:
    print(f"Error: '{DATA_FILENAME}' not found at {data_path}.")
    print("Please download the file from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
    print(f"and save it in the same directory as this script: {script_dir}")
    exit()
except Exception as e:
    print(f"An error occurred while loading the dataset: {e}")
    exit()

# Check columns: df.columns.
print("\nColumns in the dataset:")
print(df.columns.tolist())

# Preview rows: df.head().
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Identify missing values: df.isnull().sum().
print("\nMissing values per column (only showing columns with missing values):")
print(df.isnull().sum()[df.isnull().sum() > 0])

# --- 3. Data Cleaning ---
# Goal: Prepare data for analysis.

print("\n--- Data Cleaning ---")

# Convert 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Filter countries of interest (e.g., Kenya, USA, India)
# You can modify this list to include any countries you want to analyze.
countries_of_interest = ['Kenya', 'United States', 'India', 'Brazil', 'United Kingdom', 'World']
df_filtered = df[df['location'].isin(countries_of_interest)].copy()

# Drop rows where 'date' or 'location' are missing, as these are critical for analysis
df_filtered.dropna(subset=['date', 'location'], inplace=True)

# Handle missing numeric values with fillna(0) for cases, deaths, and vaccinations.
# For other numeric columns, we might use interpolate() if a trend is expected,
# but for cumulative counts, 0 is a safer initial fill.
# We'll focus on key columns for this project.
numeric_cols = [
    'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
    'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
    'total_boosters', 'icu_patients', 'hosp_patients', 'population' # Include population for percentage calculations
]

for col in numeric_cols:
    if col in df_filtered.columns:
        # Fill NaNs with 0 for cumulative counts, as missing means no cases/deaths/vaccinations reported
        df_filtered[col] = df_filtered[col].fillna(0)

# Sort data by location and date for proper time series analysis
df_filtered.sort_values(by=['location', 'date'], inplace=True)

print(f"\nData cleaned and filtered for countries: {countries_of_interest}")
print("Filtered data info:")
df_filtered.info()

# --- 4. Exploratory Data Analysis (EDA) ---
# Goal: Generate descriptive statistics & explore trends.

print("\n--- Exploratory Data Analysis (EDA) ---")

# Set a style for the plots
sns.set_style("whitegrid")

# Plot total cases over time for selected countries
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_filtered, x='date', y='total_cases', hue='location')
plt.title('Total COVID-19 Cases Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Cases', fontsize=12)
plt.yscale('log') # Use log scale for better visualization of exponential growth
plt.legend(title='Country', title_fontsize='13', fontsize='10')
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()

# Plot total deaths over time for selected countries
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_filtered, x='date', y='total_deaths', hue='location')
plt.title('Total COVID-19 Deaths Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Deaths', fontsize=12)
plt.yscale('log') # Use log scale
plt.legend(title='Country', title_fontsize='13', fontsize='10')
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()

# Compare daily new cases between countries (7-day smoothed for better trend visibility)
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_filtered, x='date', y='new_cases_smoothed', hue='location')
plt.title('Daily New COVID-19 Cases (7-day smoothed) Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('New Cases (Smoothed)', fontsize=12)
plt.legend(title='Country', title_fontsize='13', fontsize='10')
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()

# Calculate the death rate: total_deaths / total_cases.
# Avoid division by zero by handling cases where total_cases is 0
df_filtered['death_rate'] = df_filtered.apply(
    lambda row: (row['total_deaths'] / row['total_cases']) * 100 if row['total_cases'] > 0 else 0,
    axis=1
)

# Plot death rate over time for selected countries
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_filtered, x='date', y='death_rate', hue='location')
plt.title('COVID-19 Death Rate (%) Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Death Rate (%)', fontsize=12)
plt.legend(title='Country', title_fontsize='13', fontsize='10')
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()

# --- 5. Visualizing Vaccination Progress ---
# Goal: Analyze vaccination rollouts.

print("\n--- Visualizing Vaccination Progress ---")

# Plot cumulative vaccinations over time for selected countries
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_filtered, x='date', y='total_vaccinations', hue='location')
plt.title('Total COVID-19 Vaccinations Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Vaccinations', fontsize=12)
plt.yscale('log') # Use log scale
plt.legend(title='Country', title_fontsize='13', fontsize='10')
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()

# Compare % vaccinated population for the latest date available for each country
# Get the latest data point for each location
df_latest = df_filtered.loc[df_filtered.groupby('location')['date'].idxmax()].copy()

# Calculate percentage of population vaccinated (at least one dose)
# Ensure 'population' column is available and not zero
df_latest['percent_vaccinated'] = df_latest.apply(
    lambda row: (row['people_vaccinated'] / row['population']) * 100 if row['population'] > 0 else 0,
    axis=1
)

# Calculate percentage of population fully vaccinated
df_latest['percent_fully_vaccinated'] = df_latest.apply(
    lambda row: (row['people_fully_vaccinated'] / row['population']) * 100 if row['population'] > 0 else 0,
    axis=1
)

print("\nLatest vaccination status (as of last reported date):")
print(df_latest[['location', 'date', 'total_vaccinations', 'people_vaccinated', 'percent_vaccinated', 'people_fully_vaccinated', 'percent_fully_vaccinated']].round(2))

# Bar chart for percentage of population vaccinated
plt.figure(figsize=(12, 7))
sns.barplot(data=df_latest.sort_values('percent_vaccinated', ascending=False),
            x='percent_vaccinated', y='location', palette='viridis')
plt.title('Percentage of Population Vaccinated (at least one dose, Latest Data)', fontsize=16)
plt.xlabel('Percentage Vaccinated (%)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()

# Bar chart for percentage of population fully vaccinated
plt.figure(figsize=(12, 7))
sns.barplot(data=df_latest.sort_values('percent_fully_vaccinated', ascending=False),
            x='percent_fully_vaccinated', y='location', palette='magma')
plt.title('Percentage of Population Fully Vaccinated (Latest Data)', fontsize=16)
plt.xlabel('Percentage Fully Vaccinated (%)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()


# --- 6. Optional: Build a Choropleth Map ---
# Goal: Visualize cases or vaccination rates by country on a world map.
# Requires 'iso_code' column.

print("\n--- Optional: Choropleth Map (requires Plotly) ---")

# Filter out 'World' and other non-country entities for mapping
df_map_data = df_latest[~df_latest['iso_code'].str.startswith('OWID_') & (df_latest['location'] != 'World')].copy()

# Ensure 'iso_code' is present and valid
if 'iso_code' in df_map_data.columns and not df_map_data['iso_code'].isnull().all():
    # Plot choropleth showing total cases per million for the latest date
    # Ensure total_cases_per_million is available and filled
    if 'total_cases_per_million' in df_map_data.columns:
        df_map_data['total_cases_per_million'] = df_map_data['total_cases_per_million'].fillna(0)
        fig_cases = px.choropleth(df_map_data,
                                  locations="iso_code",
                                  color="total_cases_per_million",
                                  hover_name="location",
                                  color_continuous_scale=px.colors.sequential.Plasma,
                                  title="Total COVID-19 Cases per Million (Latest Data)")
        fig_cases.show()
    else:
        print("Column 'total_cases_per_million' not found or is entirely empty for mapping.")

    # Plot choropleth showing percentage of population fully vaccinated
    if 'percent_fully_vaccinated' in df_map_data.columns:
        fig_vaccinated = px.choropleth(df_map_data,
                                       locations="iso_code",
                                       color="percent_fully_vaccinated",
                                       hover_name="location",
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       title="Percentage of Population Fully Vaccinated (Latest Data)")
        fig_vaccinated.show()
    else:
        print("Column 'percent_fully_vaccinated' not found or is entirely empty for mapping.")
else:
    print("Skipping choropleth map: 'iso_code' column is missing or empty for mapping.")
    print("Please ensure your dataset contains a valid 'iso_code' column for countries if you wish to use the map.")


# --- 7. Insights & Reporting ---
# Goal: Summarize findings.

print("\n--- Insights & Reporting ---")
print("This section is for you to write your narrative insights based on the visualizations.")
print("In a Jupyter Notebook, you would use Markdown cells for this.")
print("\nExample Insights:")
print("1. Total cases and deaths show an exponential growth pattern initially, then flatten or fluctuate, indicating waves of infection.")
print("2. The death rate varies significantly across countries, potentially due to differences in healthcare systems, testing capacities, demographics, or reporting methods.")
print("3. Vaccination rollouts show a clear progression, with some countries achieving high vaccination rates faster than others.")
print("4. You can compare the daily new cases trends to vaccination progress to infer potential impacts of vaccination on case numbers.")
print("5. Look for anomalies: Are there sudden spikes or drops in data that might indicate reporting errors or specific events?")
print("\nTo export your report:")
print("If using Jupyter Notebook, you can go to File -> Download as -> PDF via LaTeX or HTML.")
print("Alternatively, you can take screenshots of your plots and paste them into a presentation software like PowerPoint or Google Slides, adding your narrative.")

print("\n--- Project Complete! ---")
print("You have successfully performed data analysis and visualization for COVID-19 global trends.")
