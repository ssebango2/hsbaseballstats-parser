import pandas as pd
import os

# Function to calculate league totals, averages, and ratio stats, and save them to a CSV file
def calculate_league_averages_with_ratios():
    output_directory = "output_data"
    league_totals = {
        'Games': 0, 'PA': 0, 'AB': 0, 'R': 0, 'Hits': 0, 'RBI': 0, 
        'Doubles': 0, 'Triples': 0, 'HR': 0, 'BB': 0, 'K': 0, 'HBP': 0, 
        'SF': 0, 'SACB': 0, 'ROE': 0, 'FC': 0, 'LOB': 0
    }

    # Counter for the number of players to calculate averages
    total_players = 0

    # Check if the output directory exists
    if not os.path.exists(output_directory):
        print(f"The directory '{output_directory}' does not exist. No files to process.")
        return

    # Iterate over each CSV file in the directory
    for filename in os.listdir(output_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(output_directory, filename)
            df = pd.read_csv(file_path)
            
            # Aggregate totals for each statistic
            league_totals['Games'] += df['Games'].sum()
            league_totals['PA'] += df['PA'].sum()
            league_totals['AB'] += df['AB'].sum()
            league_totals['R'] += df['R'].sum()
            league_totals['Hits'] += df['Hits'].sum()
            league_totals['RBI'] += df['RBI'].sum()
            league_totals['Doubles'] += df['Doubles'].sum()
            league_totals['Triples'] += df['Triples'].sum()
            league_totals['HR'] += df['HR'].sum()
            league_totals['BB'] += df['BB'].sum()
            league_totals['K'] += df['K'].sum()
            league_totals['HBP'] += df['HBP'].sum()
            league_totals['SF'] += df['SF'].sum()
            league_totals['SACB'] += df['SACB'].sum()
            league_totals['ROE'] += df['ROE'].sum()
            league_totals['FC'] += df['FC'].sum()
            league_totals['LOB'] += df['LOB'].sum()
            
            total_players += len(df)

    # Calculate league averages
    league_averages = {stat: (total / total_players if total_players > 0 else 0) 
                       for stat, total in league_totals.items()}
    
    # Calculate ratio stats for the league
    total_hits = league_totals['Hits']
    total_at_bats = league_totals['AB']
    total_pa = league_totals['PA']
    total_bb = league_totals['BB']
    total_hbp = league_totals['HBP']
    total_sf = league_totals['SF']
    total_doubles = league_totals['Doubles']
    total_triples = league_totals['Triples']
    total_hr = league_totals['HR']
    
    # Calculate total bases
    total_bases = (total_hits - total_doubles - total_triples - total_hr) + (2 * total_doubles) + (3 * total_triples) + (4 * total_hr)
    
    # Calculate BA, OBP, SLG, and OPS
    league_ba = total_hits / total_at_bats if total_at_bats > 0 else 0
    league_obp = (total_hits + total_bb + total_hbp) / (total_pa - total_sf) if (total_pa - total_sf) > 0 else 0
    league_slg = total_bases / total_at_bats if total_at_bats > 0 else 0
    league_ops = league_obp + league_slg

    # Save results to a CSV file
    league_data = {
        'Statistic': list(league_totals.keys()) + ['BA', 'OBP', 'SLG', 'OPS'],
        'Total': list(league_totals.values()) + [None, None, None, None],
        'Average': list(league_averages.values()) + [league_ba, league_obp, league_slg, league_ops]
    }

    league_df = pd.DataFrame(league_data)
    output_file = os.path.join(output_directory, "league_averages.csv")
    league_df.to_csv(output_file, index=False)
    
    print(f"League averages and totals have been saved to '{output_file}'.")

# Call the function to calculate league averages, ratio stats, and save to CSV
calculate_league_averages_with_ratios()
