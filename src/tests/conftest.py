import pytest
import pandas as pd
import os
from pickle import FALSE

@pytest.fixture
def output_data():
    # Example data for the fixture
    temp_dir = 'C:\\Apps\\retry_trial\\retry_trial\\TechM_Problem_Solution\\temp'
    updated_data = pd.read_csv(os.path.join(temp_dir, 'updated_data.csv'))
    updated_data.reset_index(drop=True, inplace=True)
    print(updated_data)
    return updated_data