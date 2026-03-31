import os
import zipfile
import sqlite3
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    """Download the European Soccer Database from Kaggle if not already present."""
    raw_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    db_path = os.path.join(raw_data_path, 'database.sqlite')
    
    if os.path.exists(db_path):
        print("Database file already exists. Skipping download.")
        return
    
    print("Initializing Kaggle API...")
    api = KaggleApi()
    api.authenticate()
    
    print("Downloading dataset from Kaggle...")
    api.dataset_download_files('hugomathien/soccer', path=raw_data_path, unzip=False)
    
    zip_file = os.path.join(raw_data_path, 'soccer.zip')
    if os.path.exists(zip_file):
        print("Extracting zip file...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(raw_data_path)
        os.remove(zip_file)  # Remove zip after extraction
        print("Extraction complete.")
    else:
        raise FileNotFoundError("Downloaded zip file not found.")

def process_data():
    """Process the SQLite database to extract and transform match data."""
    raw_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    db_path = os.path.join(raw_data_path, 'database.sqlite')
    
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    
    print("Querying and joining Match and Team tables...")
    query = """
    SELECT 
        m.match_api_id,
        m.season,
        m.date,
        ht.team_long_name AS home_team_name,
        at.team_long_name AS away_team_name,
        m.home_team_goal,
        m.away_team_goal
    FROM Match m
    JOIN Team ht ON m.home_team_api_id = ht.team_api_id
    JOIN Team at ON m.away_team_api_id = at.team_api_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print("Creating target column FTR...")
    df['FTR'] = df.apply(
        lambda row: 'H' if row['home_team_goal'] > row['away_team_goal'] 
                    else 'A' if row['away_team_goal'] > row['home_team_goal'] 
                    else 'D', axis=1
    )
    
    output_path = os.path.join(raw_data_path, 'matches.csv')
    print(f"Saving processed data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data processing complete.")

if __name__ == "__main__":
    download_dataset()
    process_data()