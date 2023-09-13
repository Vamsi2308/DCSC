# importing packages
import sys
import pandas as pd

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python lab_1.py input_file.csv output_file.csv")
    sys.exit(1)

# Get the input and output file names from command-line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    # Read the CSV file into a DataFrame (You can modify this part as needed)
    df = pd.read_csv(input_file)

    # Do something with the data (Example: Capitalize the column names)
    df.columns = [col.upper() for col in df.columns]

    # Save the results to the output CSV file
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)