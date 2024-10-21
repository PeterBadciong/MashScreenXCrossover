import pandas as pd
import argparse

def extract_first_two_words(description):
    """Extracts the first two words of a description."""
    return ' '.join(description.split()[:2])

def filter_mash_distances(input_csv, output_csv, mash_distance_threshold):
    # Read the CSV file into a DataFrame (comma-separated)
    try:
        df = pd.read_csv(input_csv, sep=',')
        print(f"File read successfully with shape: {df.shape}")
        print(df.head())  # Print the first few rows to inspect the input
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    
    # Check if the input has the expected columns
    expected_columns = ['Accession1', 'Description1', 'Accession2', 'Description2', 
                        'Mash_Distance', 'P-value', 'Shared_Hashes']
    
    if list(df.columns) != expected_columns:
        print(f"Error: Expected columns {expected_columns}, but got {list(df.columns)}")
        return

    # Extract the first two words from Description1 and Description2
    df['Desc1_Two_Words'] = df['Description1'].apply(extract_first_two_words)
    df['Desc2_Two_Words'] = df['Description2'].apply(extract_first_two_words)

    # Convert Mash_Distance column to float for comparison
    df['Mash_Distance'] = pd.to_numeric(df['Mash_Distance'], errors='coerce')

    # Filter rows where the first two words do not match and Mash_Distance is less than the threshold
    filtered_df = df[(df['Desc1_Two_Words'] != df['Desc2_Two_Words']) & 
                     (df['Mash_Distance'] < mash_distance_threshold)]

    # Write the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Filter CSV rows based on Mash Distance and description comparison.")
    
    # Add arguments
    parser.add_argument('input_csv', type=str, help="Path to the input CSV file.")
    parser.add_argument('output_csv', type=str, help="Path to the output CSV file.")
    parser.add_argument('mash_distance_threshold', type=float, help="Threshold for Mash Distance filtering.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the filter function with parsed arguments
    filter_mash_distances(args.input_csv, args.output_csv, args.mash_distance_threshold)

if __name__ == "__main__":
    main()
