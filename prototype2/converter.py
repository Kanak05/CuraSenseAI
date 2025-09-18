import pandas as pd
import sys

def convert_to_json(input_path: str, output_path: str):
    """
    Converts an Excel or CSV file into a JSON file.

    The JSON output is a list of objects, where each object represents a row.

    Args:
        input_path (str): The file path for the input Excel or CSV file.
        output_path (str): The file path for the output JSON file.
    """
    # Validate the input file extension
    try:
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        elif input_path.endswith(('.xlsx', '.xls')):
            # The 'openpyxl' engine is required for .xlsx files
            df = pd.read_excel(input_path, engine='openpyxl')
        else:
            print("Error: Unsupported file format. Please use a '.csv' or '.xlsx' file.")
            return
            
        # Convert the DataFrame to a JSON string
        # orient='records' creates the desired list of dictionaries [{column: value}, ...]
        # indent=4 makes the JSON output human-readable
        df.to_json(output_path, orient='records', indent=4)
        
        print(f"✅ Successfully converted '{input_path}' to '{output_path}'")

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- How to use the script ---

# To run this from your terminal/command prompt:
# python your_script_name.py your_data.csv converted_data.json
# python your_script_name.py your_data.xlsx converted_data.json

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <script_name>.py <input_file_path> <output_file_path>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_to_json(input_file, output_file)