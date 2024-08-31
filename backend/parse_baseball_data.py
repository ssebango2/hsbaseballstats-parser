import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Function to parse initial raw baseball data (up to "HR" and "GS")
def parse_baseball_data(raw_data):
    rows = raw_data.strip().split("\n")
    parsed_data = []

    for row in rows:
        # Check if the user wants to quit
        if row.lower() == "quit":
            print("Quitting data entry for this team.")
            return pd.DataFrame()  # Return an empty DataFrame

        parts = row.split()
        
        # Remove trailing zeros or unnecessary parts
        while len(parts) > 14 and parts[-1] == '0':
            parts.pop()

        # Dynamic name extraction
        number = parts[0]
        name_parts = []
        for part in parts[1:]:
            name_parts.append(part)
            if part.endswith(")"):  # End of the name reached
                break
        name = ' '.join(name_parts)
        
        # Parse the rest of the statistics
        remaining_parts = parts[len(name_parts) + 1:]

        # Fill missing values with default if there are fewer than expected parts
        while len(remaining_parts) < 11:
            remaining_parts.append('0')  # Use '0' or another appropriate default

        try:
            # Parse the remaining parts with default fallback
            games = int(remaining_parts[0])
            avg = float(remaining_parts[1])
            pa = int(remaining_parts[2])
            ab = int(remaining_parts[3])
            r = int(remaining_parts[4])
            h = int(remaining_parts[5])
            rbi = int(remaining_parts[6])
            doubles = int(remaining_parts[7])
            triples = int(remaining_parts[8])
            hr = int(remaining_parts[9])
            gs = int(remaining_parts[10])

            parsed_data.append([number, name, games, avg, pa, ab, r, h, rbi, doubles, triples, hr, gs])
        except ValueError as e:
            print(f"Error: Could not parse row: {row}. Error: {e}")
            continue

    df = pd.DataFrame(parsed_data, columns=["Number", "Name", "Games", "AVG", "PA", "AB", "R", "Hits", "RBI", "Doubles", "Triples", "HR", "GS"])
    return df

# Function to parse additional data with OBP, SLG, OPS
def parse_additional_data(raw_data):
    rows = raw_data.strip().split("\n")
    parsed_data = []

    for row in rows:
        # Check if the user wants to quit
        if row.lower() == "quit":
            print("Quitting data entry for this team.")
            return pd.DataFrame()  # Return an empty DataFrame

        parts = row.split()
        
        # Remove trailing zeros or unnecessary parts
        while len(parts) > 15 and parts[-1] == '0':
            parts.pop()

        # Dynamic name extraction
        number = parts[0]
        name_parts = []
        for part in parts[1:]:
            name_parts.append(part)
            if part.endswith(")"):  # End of the name reached
                break
        name = ' '.join(name_parts)
        
        # Parse the rest of the statistics
        remaining_parts = parts[len(name_parts) + 1:]

        # Fill missing values with default if there are fewer than expected parts
        while len(remaining_parts) < 12:
            remaining_parts.append('0')  # Use '0' or another appropriate default

        try:
            # Parse the remaining parts with default fallback
            games = int(remaining_parts[0])
            sf = int(remaining_parts[1])
            sacb = int(remaining_parts[2])
            bb = int(remaining_parts[3])
            k = int(remaining_parts[4])
            hbp = int(remaining_parts[5])
            roe = int(remaining_parts[6])
            fc = int(remaining_parts[7])
            lob = int(remaining_parts[8])
            obp = float(remaining_parts[9])
            slg = float(remaining_parts[10])
            ops = float(remaining_parts[11])

            parsed_data.append([number, name, games, sf, sacb, bb, k, hbp, roe, fc, lob, obp, slg, ops])
        except ValueError as e:
            print(f"Error: Could not parse row: {row}. Error: {e}")
            continue

    df = pd.DataFrame(parsed_data, columns=["Number", "Name", "Games", "SF", "SACB", "BB", "K", "HBP", "ROE", "FC", "LOB", "OBP", "SLG", "OPS"])
    return df

# Function to calculate custom wOBA weights based on league-wide statistics
def calculate_woba_weights(league_totals):
    """
    Calculate custom wOBA weights based on league-wide statistics.
    
    Parameters:
    league_totals (dict): A dictionary containing league-wide totals for different stats.
    
    Returns:
    tuple: Custom weights for BB, HBP, 1B, 2B, 3B, HR.
    """
    total_pa = league_totals['PA']  # Total Plate Appearances
    total_runs = league_totals['Runs']  # Total Runs scored

    # Avoid division by zero
    if total_pa == 0:
        return 0, 0, 0, 0, 0, 0

    # Calculate weights based on league averages
    wBB = (total_runs / total_pa) * (league_totals['BB'] / total_pa)
    wHBP = (total_runs / total_pa) * (league_totals['HBP'] / total_pa)
    w1B = (total_runs / total_pa) * (league_totals['1B'] / total_pa)
    w2B = (total_runs / total_pa) * (league_totals['2B'] / total_pa)
    w3B = (total_runs / total_pa) * (league_totals['3B'] / total_pa)
    wHR = (total_runs / total_pa) * (league_totals['HR'] / total_pa)

    return wBB, wHBP, w1B, w2B, w3B, wHR

# Function to calculate wOBA for each player using custom weights
def calculate_woba(df, wBB, wHBP, w1B, w2B, w3B, wHR):
    """
    Calculate wOBA for each player in the DataFrame using custom weights.
    
    Parameters:
    df (DataFrame): DataFrame containing player stats.
    wBB (float): Weight for walks (BB).
    wHBP (float): Weight for hit-by-pitch (HBP).
    w1B (float): Weight for singles (1B).
    w2B (float): Weight for doubles (2B).
    w3B (float): Weight for triples (3B).
    wHR (float): Weight for home runs (HR).
    
    Returns:
    DataFrame: Updated DataFrame with the 'wOBA' column added.
    """
    # Calculate the number of singles (1B) for each player
    df['1B'] = df['Hits'] - df['Doubles'] - df['Triples'] - df['HR']

    # Calculate wOBA using the custom weights
    df['wOBA'] = (
        (wBB * df['BB']) +
        (wHBP * df['HBP']) +
        (w1B * df['1B']) +
        (w2B * df['Doubles']) +
        (w3B * df['Triples']) +
        (wHR * df['HR'])
    ) / (df['AB'] + df['BB'] + df['HBP'] + df['SF'])

    return df

def visualize_team_statistics(team_dataframes):
    # Check if there are any teams
    if not team_dataframes:
        print("No team data available to visualize.")
        return

    # Create a DataFrame to store aggregated team statistics
    team_stats = []

    for team, df in team_dataframes.items():
        total_runs = df['R'].sum()
        total_hr = df['HR'].sum()
        avg_batting_avg = df['AVG'].mean()

        team_stats.append({
            'Team': team,
            'Total Runs': total_runs,
            'Total Home Runs': total_hr,
            'Average Batting Average': avg_batting_avg
        })

    # Convert to DataFrame
    team_stats_df = pd.DataFrame(team_stats)

    # Set the style of the plots
    sns.set(style="whitegrid")

    # Bar plot for total runs per team
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Team', y='Total Runs', data=team_stats_df, palette='Blues_d')
    plt.title('Total Runs by Team')
    plt.ylabel('Total Runs')
    plt.xlabel('Team')
    plt.xticks(rotation=45)
    plt.show()

    # Bar plot for total home runs per team
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Team', y='Total Home Runs', data=team_stats_df, palette='Reds_d')
    plt.title('Total Home Runs by Team')
    plt.ylabel('Total Home Runs')
    plt.xlabel('Team')
    plt.xticks(rotation=45)
    plt.show()

    # Bar plot for average batting average per team
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Team', y='Average Batting Average', data=team_stats_df, palette='Greens_d')
    plt.title('Average Batting Average by Team')
    plt.ylabel('Average Batting Average')
    plt.xlabel('Team')
    plt.xticks(rotation=45)
    plt.show()

# Function to manage user input and create new DataFrames
def manage_dataframes():
    team_dataframes = {}  # Dictionary to store each team's DataFrame
    output_directory = "output_data"  # Directory to save CSV files

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    while True:
        user_input = input("Do you want to add player data? (yes/no): ").strip().lower()
        if user_input == 'yes':
            team_name = input("Enter the team name: ").strip()
            
            if team_name in team_dataframes:
                existing_df = team_dataframes[team_name]
                print(f"Existing data found for team '{team_name}'.")
            else:
                existing_df = None
                print(f"No existing data found for team '{team_name}'. Starting new entry.")
                
            if existing_df is None:
                print("Enter initial player data (up to HR and GS). Type 'done' on a new line to finish:")
            else:
                print("Enter additional player data (with OBP, SLG, OPS). Type 'done' on a new line to finish:")
            
            while True:
                new_raw_data = ""
                while True:
                    line = input()
                    if line.lower() == 'done':
                        break
                    new_raw_data += line + "\n"

                if existing_df is None:
                    new_df = parse_baseball_data(new_raw_data)
                    if not new_df.empty:
                        team_dataframes[team_name] = new_df
                        break
                    else:
                        print("No valid rows were entered. Please try again.")
                else:
                    new_df = parse_additional_data(new_raw_data)
                    if not new_df.empty:
                        existing_df = pd.merge(existing_df, new_df, on=["Number", "Name", "Games"], how='outer')
                        
                        # Calculate and add the ISOP column (SLG - AVG) and round to 3 decimal places
                        existing_df["ISOP"] = (existing_df["SLG"] - existing_df["AVG"]).round(3)

                        # Calculate and add the BABIP column and round to 3 decimal places
                        # BABIP = (H - HR) / (AB - K - HR + SF)
                        existing_df["BABIP"] = (
                            (existing_df["Hits"] - existing_df["HR"]) /
                            (existing_df["AB"] - existing_df["K"] - existing_df["HR"] + existing_df["SF"])
                        ).fillna(0).round(3)  # Fill NaN values with 0 if the denominator is zero or if there are missing values
                        
                        team_dataframes[team_name] = existing_df
                        break
                    else:
                        print("No valid rows were entered. Please try again.")
            
            print(f"New DataFrame updated successfully for team '{team_name}'!")
            print(team_dataframes[team_name])

            # Save the team's DataFrame to a CSV file
            output_path = os.path.join(output_directory, f"{team_name}_stats.csv")
            team_dataframes[team_name].to_csv(output_path, index=False)
            print(f"Data for team '{team_name}' saved to {output_path}")

        elif user_input == 'no':
            print("No more data to add. Calculating league-wide statistics for wOBA...")
            league_totals = {
                'BB': 0, 'HBP': 0, '1B': 0, '2B': 0, '3B': 0, 'HR': 0, 'SF': 0, 'PA': 0, 'Runs': 0
            }
            # Aggregate league-wide statistics
            for df in team_dataframes.values():
                league_totals['BB'] += df['BB'].sum()
                league_totals['HBP'] += df['HBP'].sum()
                league_totals['1B'] += (df['Hits'] - df['Doubles'] - df['Triples'] - df['HR']).sum()
                league_totals['2B'] += df['Doubles'].sum()
                league_totals['3B'] += df['Triples'].sum()
                league_totals['HR'] += df['HR'].sum()
                league_totals['SF'] += df['SF'].sum()
                league_totals['PA'] += df['PA'].sum()
                league_totals['Runs'] += df['R'].sum()

            # Calculate custom wOBA weights based on the league-wide statistics
            wBB, wHBP, w1B, w2B, w3B, wHR = calculate_woba_weights(league_totals)

            print("Custom wOBA Weights Calculated:")
            print(f"wBB: {wBB}, wHBP: {wHBP}, w1B: {w1B}, w2B: {w2B}, w3B: {w3B}, wHR: {wHR}")

            # Calculate wOBA for each player in every team
            for team, df in team_dataframes.items():
                team_dataframes[team] = calculate_woba(df, wBB, wHBP, w1B, w2B, w3B, wHR)
                print(f"\nUpdated DataFrame with wOBA for team '{team}':")
                print(team_dataframes[team])

            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    return team_dataframes

# Call the function to manage multiple DataFrames
team_dataframes = manage_dataframes()
