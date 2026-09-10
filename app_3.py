from fastapi import FastAPI, File, UploadFile, Depends
from io import StringIO
import pandas as pd
from joblib import load

from datetime import datetime
import pytz
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session


# Configurar base de datos
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:ObRUdQorHSpJPsZucgdsxQMxSTqsOliI@metro.proxy.rlwy.net:46692/railway"
SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()
# Configurar sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health", status_code=200, include_in_schema=False)
def health_check(db=Depends(get_db)):
    """This is the health check endpoint"""
    return {"status": "ok"}
 



@app.post("/predict")
async def predict_houseprice(file: UploadFile = File(...), db: Session = Depends(get_db)):

    classifier = load("linear_regression.joblib")
    
    features_df = pd.read_csv('selected_features.csv')
    features = features_df['0'].to_list()
    
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))
    df = df[features]
    
    predictions = classifier.predict(df)

    lima_tz = pytz.timezone('America/Lima')
    now = datetime.now(lima_tz)
    
    predictions_df = pd.DataFrame({
        'file_name': file.filename,
        'prediction': predictions,
        'created_at': now
    })
    
    predictions_df.to_sql('predictions', con=engine, if_exists='append', index=False)

    return {
        "predictions": predictions.tolist()
    }
