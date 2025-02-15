import pandas as pd
from pathlib import Path

def inspect_csv():
    # Get the file path
    base_path = Path(__file__).parent.parent.parent
    file_path = base_path / 'data' / 'raw' / 'Wpl 2023-2024.csv'
    
    # Read the CSV
    df = pd.read_csv(file_path)
    
    # Print information about the DataFrame
    print("\nDataFrame Info:")
    print("===============")
    print(df.info())
    
    print("\nColumn Names:")
    print("=============")
    for col in df.columns:
        print(f"- {col}")
    
    print("\nFirst few rows:")
    print("===============")
    print(df.head())

if __name__ == "__main__":
    inspect_csv()