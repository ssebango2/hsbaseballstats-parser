import pandas as pd
import os

# Function to calculate OPS+ for each player and add it to each CSV file
def add_ops_plus_to_files():
    output_directory = "output_data"
    league_stats_file = os.path.join(output_directory, "league_stats.csv")

    # Check if the league_stats.csv file exists
    if not os.path.exists(league_stats_file):
        print(f"The file '{league_stats_file}' does not exist. Cannot calculate OPS+ without league OPS.")
        return

    # Read the league OPS from the league_stats.csv file
    league_stats_df = pd.read_csv(league_stats_file)
    league_ops_row = league_stats_df[league_stats_df['Statistic'] == 'OPS']
    if league_ops_row.empty:
        print("OPS value not found in the league_stats.csv file.")
        return

    league_ops = league_ops_row['Average'].values[0]
    if pd.isna(league_ops) or league_ops == 0:
        print("Invalid league OPS value. Cannot calculate OPS+.")
        return

    print(f"Using league OPS of {league_ops:.3f} to calculate OPS+ for each player.")

    # Iterate over each CSV file in the directory, excluding league_stats.csv
    for filename in os.listdir(output_directory):
        if filename.endswith(".csv") and filename != "league_stats.csv":
            file_path = os.path.join(output_directory, filename)
            df = pd.read_csv(file_path)

            # Calculate OPS for each player
            df['OPS'] = df['OBP'] + df['SLG']

            # Calculate OPS+ for each player
            df['OPS+'] = (df['OPS'] / league_ops) * 100

            # Handle NaN values before rounding
            df['OPS+'] = df['OPS+'].fillna(0).replace([float('inf'), -float('inf')], 0)

            # Round OPS+ to the nearest integer
            df['OPS+'] = df['OPS+'].round().astype(int)

            # Save the updated DataFrame back to the CSV file
            df.to_csv(file_path, index=False)
            print(f"OPS+ added to file: {filename}")

# Call the function to add OPS+ to each player's CSV file
add_ops_plus_to_files()
