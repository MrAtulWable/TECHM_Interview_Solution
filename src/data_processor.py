import os
import pandas as pd
import json

def read_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    csv_data = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        print(f"Reading CSV file: {file_path}")
        data = pd.read_csv(file_path)
        print(f"CSV data from {file_path}:\n{data.head()}")
        csv_data.append(data)
    return pd.concat(csv_data, ignore_index=True) if csv_data else pd.DataFrame()

def read_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    json_data = []
    for file in json_files:
        file_path = os.path.join(directory, file)
        print(f"Reading JSON file: {file_path}")
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    json_data.append(data)
            print(f"JSON data from {file_path}:\n{json_data[:5]}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading file {file_path}: {e}")
    return pd.DataFrame(json_data) if json_data else pd.DataFrame()

def merge_data(csv_data, json_data):
    # Ensure both DataFrames have the same columns
    common_columns = list(set(csv_data.columns).intersection(set(json_data.columns)))
    print(f"Common columns: {common_columns}")
    csv_data = csv_data[common_columns]
    json_data = json_data[common_columns]
    merged_data = pd.concat([csv_data, json_data], ignore_index=True)
    print(f"Merged data:\n{merged_data.head()}")
    return merged_data
def update_player_type(data):
    # Define the criteria for player types
    conditions = [
        (data['runs'] > 500) & (data['wickets'] > 50),
        (data['runs'] > 500) & (data['wickets'] <= 50),
        (data['runs'] <= 500)
    ]
    choices = ['All-Rounder', 'Batsman', 'Bowler']
    
    # Create a new column 'Player Type' with predefined categories
    data['playerType'] = pd.Categorical(pd.cut(data['runs'], bins=[-1, 500, float('inf')], labels=['Bowler', 'Batsman']))
    data['playerType'] = data['playerType'].cat.add_categories(['All-Rounder'])
    
    # Set the 'Player Type' for 'All-Rounder'
    data.loc[(data['runs'] > 500) & (data['wickets'] > 50), 'playerType'] = 'All-Rounder'
    
    # Remove players with no data for runs and wickets
    data = data.dropna(subset=['runs', 'wickets'])
    
    # Remove players with age > 50 or < 15
    data = data[(data['age'] <= 50) & (data['age'] >= 15)]
    
    # data = data[['eventType', 'playerName', 'age',  'runs' , 'wickets',   'playerType']]
    return data

# def validate_output(processed_data, processor_output):
#     # Compare the processed data with the processor's output
#     def compare_rows(row):
#         try:
#             print(processor_output)
#             print(processor_output['playerName'] == row['playerName'])
#             # processor_row = processor_output[processor_output['playerName'] == row['playerName']].iloc[0]
#             # print(processor_row)
#             # return 'PASS' if row.equals(processor_row) else 'FAIL'
#         except IndexError:
#             return 'FAIL'
#
#     processed_data['Result'] = processed_data.apply(compare_rows, axis=1)
#     return processed_data
def validate_output(processed_data, processor_output):
    print(processed_data)
    print(processor_output)
    # Merge the dataframes on 'playerName'
    merged_data = pd.merge(processed_data, processor_output, on='playerName', suffixes=('_processed', '_expected'))
    print(merged_data)
    
    # Compare relevant columns and create 'Result' column
    comparison_columns = ['eventType', 'age', 'runs', 'wickets', 'playerType']
    merged_data['Result'] = merged_data.apply(lambda row: 'PASS' if all(row[f'{col}_processed'] == row[f'{col}_expected'] for col in comparison_columns) else 'FAIL', axis=1)
    
    # Select relevant columns for the final output
    final_data = merged_data[['playerName', 'eventType_processed', 'age_processed', 'runs_processed', 'wickets_processed', 'playerType_processed', 'Result']]
    final_data.columns = ['playerName', 'eventType', 'age', 'runs', 'wickets', 'playerType', 'Result']
    
    return final_data

def main(input_dir, temp_dir, output_dir):
    csv_data = read_csv_files(input_dir)
    json_data = read_json_files(input_dir)
    merged_data = merge_data(csv_data, json_data)
    temp_file_path = os.path.join(temp_dir, 'arranged_merged_data.csv')
    merged_data.to_csv(temp_file_path, index=False)
    print(f'Data has been arranged and saved to {temp_file_path}')
    updated_data = update_player_type(merged_data)
    
    # Save the updated data to a new CSV file
    temp_file_path1 = os.path.join(temp_dir, 'updated_data.csv')
    updated_data.to_csv(temp_file_path1, index=False)
    print("Player Type updated and data cleaned successfully.")
    
    # Read the updated data from temp folder
    updated_data = pd.read_csv(os.path.join(temp_dir, 'updated_data.csv'))
    
    out_file_path = os.path.join(output_dir, 'odi.csv')
    # Read the processor's output data
    processor_output = pd.read_csv(out_file_path)
    
    # Validate the output and store the results
    validated_data = validate_output(updated_data, processor_output)
    
    # Save the results to 'test_result.csv'
    if validated_data is not None:
        validated_data.to_csv(os.path.join(temp_dir, 'test_result.csv'), index=False)
        print(f'Results have been saved to {os.path.join(temp_dir, "test_result.csv")}')
    else:
        print("Validation failed. No data to save.")

if __name__ == "__main__":
    input_dir = 'C:\\Users\\sai\\PycharmProjects\\pythonProject1\\TechM_Problem_Solution\\InputDataSet'  # Change this to your input directory path
    temp_dir = 'C:\\Users\\sai\\PycharmProjects\\pythonProject1\\TechM_Problem_Solution\\temp'  # Change this to your temp directory path
    output_dir = 'C:\\Users\\sai\\PycharmProjects\\pythonProject1\\TechM_Problem_Solution\\OutputDataSet'  # Change this to your output directory path
    main(input_dir, temp_dir,output_dir)