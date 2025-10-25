# ml_extract.py - ML-based line classification for metadata vs code

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
import os

MODEL_PATH = 'sas_classifier.pkl'

def train_ml_model(csv_path):
    """
    Train a simple TF-IDF + Logistic Regression classifier on labeled data.
    Labels: 'metadata' or 'code'
    """
    df = pd.read_csv(csv_path)
    X = df['line']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100, stop_words='english')),
        ('clf', LogisticRegression())
    ])

    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    print(f"Model accuracy: {score:.2f}")

    joblib.dump(pipeline, MODEL_PATH)
    print("Model saved.")

def load_ml_model():
    """
    Load the trained model.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train first with --train.")
    return joblib.load(MODEL_PATH)

def classify_lines_ml(lines, model):
    """
    Classify each line as 'metadata' or 'code'.
    Returns list of (line, label) tuples.
    """
    line_strs = [line.strip() for line in lines if line.strip()]  # Clean lines
    predictions = model.predict(line_strs)
    return list(zip(line_strs, predictions))
