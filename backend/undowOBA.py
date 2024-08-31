import pandas as pd
import os

# Function to undo wOBA and remove the 1B column from all CSV files
def undo_woba_and_1b():
    output_directory = "output_data"

    # Check if the output directory exists
    if not os.path.exists(output_directory):
        print(f"The directory '{output_directory}' does not exist. No files to undo.")
        return

    # Iterate over each CSV file in the directory
    for filename in os.listdir(output_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(output_directory, filename)
            df = pd.read_csv(file_path)
            
            # List of columns to remove
            columns_to_remove = []
            if 'wOBA' in df.columns:
                columns_to_remove.append('wOBA')
            if '1B' in df.columns:
                columns_to_remove.append('1B')
            
            # Remove the columns if they exist
            if columns_to_remove:
                df = df.drop(columns=columns_to_remove)
                df.to_csv(file_path, index=False)  # Save the updated DataFrame back to the CSV file
                print(f"Columns {', '.join(columns_to_remove)} removed from file: {filename}")
            else:
                print(f"No wOBA or 1B column found in file: {filename}")

# Call the function to undo wOBA and remove the 1B column
undo_woba_and_1b()
