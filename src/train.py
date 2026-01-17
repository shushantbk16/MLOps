import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train():
    # Load Data
    
    df = pd.DataFrame({'text': ["I love this", "This is bad", "Amazing product", "Horrible"], 'label': [1, 0, 1, 0]})
    df.to_csv('data/sentiment.csv', index=False)dvc init
    df = pd.read_csv('data/sentiment.csv')
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.25)

    # Enable MLflow
    mlflow.set_experiment("Sentiment_Baseline")

    with mlflow.start_run():
        # Define Model
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        
        # Train
        model.fit(X_train, y_train)
        
        # Evaluate
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        # Log Metrics & Model
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Model trained with accuracy: {acc}")
        
        # Save locally for the API
        joblib.dump(model, "models/sentiment_model.pkl")

if __name__ == "__main__":
    train()
