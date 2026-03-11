import os
import pandas as pd

def save_evaluation(evaluation_result, output_folder):
    """
    Saves the evaluation result to a CSV file.
    """
    csv_path = os.path.join(output_folder, 'candidate_scores.csv')
    
    # Ensure there's no nested dictionaries or lists that pandas might choke on
    df_new = pd.DataFrame([evaluation_result])
    
    if os.path.exists(csv_path):
        try:
            # Append to existing
            df_existing = pd.read_csv(csv_path)
            # Remove empty columns if they somehow got added
            df_existing = df_existing.dropna(how='all', axis=1)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_path, index=False)
        except pd.errors.EmptyDataError:
            df_new.to_csv(csv_path, index=False)
    else:
        # Create new
        df_new.to_csv(csv_path, index=False)

def load_all_evaluations(output_folder):
    """
    Loads all evaluations from the CSV file.
    Returns a list of dictionaries.
    """
    csv_path = os.path.join(output_folder, 'candidate_scores.csv')
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df = df.fillna('')
            return df.to_dict('records')
        except pd.errors.EmptyDataError:
            return []
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []
    return []
