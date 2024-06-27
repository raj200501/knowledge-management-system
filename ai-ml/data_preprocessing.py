import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['label'] = df['label'].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Example usage
X_train, X_test, y_train, y_test = preprocess_data('data.csv')
