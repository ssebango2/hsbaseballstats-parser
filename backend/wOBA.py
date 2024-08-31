import os
import pandas as pd

# Directory containing CSV files
input_directory = 'output_data'
league_data_file = os.path.join(input_directory, 'league_stats.csv')

# Function to calculate the league wOBA using league data
def calculate_league_woba(league_data, weights):
    # Calculate league totals
    singles = league_data.loc[league_data['Statistic'] == 'Hits', 'Total'].values[0] - (
        league_data.loc[league_data['Statistic'] == 'Doubles', 'Total'].values[0] +
        league_data.loc[league_data['Statistic'] == 'Triples', 'Total'].values[0] +
        league_data.loc[league_data['Statistic'] == 'HR', 'Total'].values[0]
    )
    doubles = league_data.loc[league_data['Statistic'] == 'Doubles', 'Total'].values[0]
    triples = league_data.loc[league_data['Statistic'] == 'Triples', 'Total'].values[0]
    home_runs = league_data.loc[league_data['Statistic'] == 'HR', 'Total'].values[0]
    walks = league_data.loc[league_data['Statistic'] == 'BB', 'Total'].values[0]
    hit_by_pitch = league_data.loc[league_data['Statistic'] == 'HBP', 'Total'].values[0]
    sacrifice_flies = league_data.loc[league_data['Statistic'] == 'SF', 'Total'].values[0]
    at_bats = league_data.loc[league_data['Statistic'] == 'AB', 'Total'].values[0]
    
    # Calculate numerator and denominator for league wOBA
    numerator = (
        weights['Walks'] * walks +
        weights['Hit By Pitch'] * hit_by_pitch +
        weights['Singles'] * singles +
        weights['Doubles'] * doubles +
        weights['Triples'] * triples +
        weights['Home Runs'] * home_runs
    )
    denominator = (
        at_bats +
        walks +
        hit_by_pitch +
        sacrifice_flies
    )
    
    # Avoid division by zero
    if denominator == 0:
        return 0
    
    # Calculate league wOBA
    return numerator / denominator

# Function to calculate wOBA for each player
def calculate_woba(row, weights):
    try:
        # Calculate singles
        singles = row['Hits'] - row['Doubles'] - row['Triples'] - row['HR']

        # Calculate wOBA numerator using the provided weights
        numerator = (
            weights['Walks'] * row['BB'] +
            weights['Hit By Pitch'] * row['HBP'] +
            weights['Singles'] * singles +
            weights['Doubles'] * row['Doubles'] +
            weights['Triples'] * row['Triples'] +
            weights['Home Runs'] * row['HR']
        )

        # Calculate wOBA denominator
        denominator = (
            row['AB'] +
            row['BB'] +
            row['HBP'] +
            row['SF']
        )

        # Avoid division by zero
        if denominator == 0:
            return 0

        # Calculate wOBA and round to three decimal places
        woba = numerator / denominator
        return round(woba, 3)
    except Exception as e:
        print(f"Error calculating wOBA for row: {row['Name']}. Error: {e}")
        return 0

# Function to calculate wRAA for each player
def calculate_wraa(row, league_woba, woba_scale):
    try:
        # Calculate wRAA using the formula
        woba = row['wOBA']
        pa = row['PA']
        wraa = ((woba - league_woba) / woba_scale) * pa
        return round(wraa, 2)
    except Exception as e:
        print(f"Error calculating wRAA for row: {row['Name']}. Error: {e}")
        return 0

# Define typical MLB wOBA weights
mlb_woba_weights = {
    'Singles': 0.89,
    'Doubles': 1.27,
    'Triples': 1.62,
    'Home Runs': 2.10,
    'Walks': 0.69,
    'Hit By Pitch': 0.72,
    'Sacrifice Flies': 0.50
}

# Load the league data from the CSV file
league_data = pd.read_csv(league_data_file)

# Calculate the league wOBA using the league data
calculated_league_woba = calculate_league_woba(league_data, mlb_woba_weights)
woba_scale = 1.20  # Typical wOBA scale value

print(f"Calculated League wOBA: {calculated_league_woba}")

# Check if the wOBA row exists in the league data; if not, add it
if 'wOBA' not in league_data['Statistic'].values:
    new_row = pd.DataFrame({'Statistic': ['wOBA'], 'Total': [calculated_league_woba]})
    league_data = pd.concat([league_data, new_row], ignore_index=True)
    league_data.to_csv(league_data_file, index=False)
    print("Added wOBA to league_stats.csv")

# Loop through CSV files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv') and filename != 'league_stats.csv':
        file_path = os.path.join(input_directory, filename)
        
        # Read CSV file
        df = pd.read_csv(file_path)

        # Calculate wOBA for each player using the regular MLB weights
        if 'wOBA' not in df.columns:
            df['wOBA'] = df.apply(calculate_woba, axis=1, weights=mlb_woba_weights)

        # Calculate wRAA for each player using the calculated league wOBA
        df['wRAA'] = df.apply(calculate_wraa, axis=1, league_woba=calculated_league_woba, woba_scale=woba_scale)

        # Write updated DataFrame back to CSV
        df.to_csv(file_path, index=False)
        print(f"Updated wOBA and wRAA for {filename}")

print("wOBA and wRAA calculation and update complete.")
