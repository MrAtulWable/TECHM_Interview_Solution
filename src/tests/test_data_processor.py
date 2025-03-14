import pandas as pd
import pytest
import os

from data_processor import validate_output

# Define the expected schema
expected_schema = {
    'eventType': str,
    'playerName': str,
    'age': int,
    'runs': int,
    'wickets': int,
    'playerType': str
}

def test_schema(output_data):
    """
    Test to check if the output data has the correct schema.
    """
    for column, dtype in expected_schema.items():
        assert column in output_data.columns, f"Missing column: {column}"
        print(column)
        print(output_data[column].dtype)
        assert output_data[column].dtype == dtype, f"Incorrect dtype for column: {column}"
def test_validate_output(output_data):
    """
    Test to validate the output data.
    """
    # Example data
    processed_data = output_data
    output_dir = 'C:\\Apps\\retry_trial\\retry_trial\\TechM_Problem_Solution\\OutputDataSet'
    out_file_path = os.path.join(output_dir, 'odi.csv')
    # Read the processor's output data
    processor_output = pd.read_csv(out_file_path)
    
    output_data = validate_output(processed_data, processor_output)
    
    # Check schema
    test_schema(output_data)
    
    # Check if all results are 'PASS'
    assert all(output_data['Result'] == 'PASS'), "Validation failed for some players"


if __name__ == "__main__":
    pytest.main()