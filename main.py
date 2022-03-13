import pandas as pd
from google.cloud import storage
import os
from datetime import datetime, timedelta
import joblib
import yfinance as yf
from datetime import datetime, timedelta
import re
from flask import Flask
app = Flask(__name__)


# In[2]:


#!pip install simplejson
#!pip install google.cloud
#!pip install google-cloud
#!pip install google-cloud-storage


# In[3]:


#yf.__version__
#import numpy as np
#np.__version__


# In[4]:


#=========== Set directory ==============
PROJECT_DIR = '/app/projectname/'
os.chdir(PROJECT_DIR)


# In[5]:


def upload_to_gcp(FILEPATH, UPLOAD_FILEPATH, BUCKET_NAME, CRED_PATH = '04_live/spy500/utils/sheets_api.json'):
    client = storage.Client.from_service_account_json(json_credentials_path=CRED_PATH)
    bucket = client.get_bucket(BUCKET_NAME)

    object_name_in_gcs_bucket = bucket.blob(UPLOAD_FILEPATH)
    object_name_in_gcs_bucket.upload_from_filename(FILEPATH)

def download_from_gcp(FILEPATH, GCP_FILEPATH, BUCKET_NAME, CRED_PATH = '04_live/spy500/utils/sheets_api.json'):
    client = storage.Client.from_service_account_json(json_credentials_path=CRED_PATH)
    bucket = client.get_bucket(BUCKET_NAME)

    #object_name_in_gcs_bucket = bucket.blob(UPLOAD_FILEPATH)

    blob = bucket.blob(GCP_FILEPATH)
    blob.download_to_filename(FILEPATH)
# In[6]:
def download_folder_from_gcp(LOCAL_FOLDER, GCP_FOLDER, BUCKET_NAME, CRED_PATH = '04_live/spy500/utils/sheets_api.json'):
    client = storage.Client.from_service_account_json(json_credentials_path=CRED_PATH)
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=GCP_FOLDER) # Get list of files
    print(blobs)
    for blob in blobs:
        filename = blob.name.replace('/', '_') 
        filename = re.sub(":","_",filename)
        blob.download_to_filename(LOCAL_FOLDER + filename)  # Download

def run_container():


    # Download
    #download_from_gcp(FILEPATH = fl, GCP_FILEPATH = fls_vec[fl], BUCKET_NAME = "abolfadl-sp500-live", CRED_PATH = '04_live/spy500/utils/sheets_api.json')



    # Upload
    #upload_to_gcp(MODEL_PERF_DIR+'raw_master_model.csv', 'model_performance/'+'raw_master_model.csv', 'abolfadl-sp500-live', CRED_PATH = '04_live/spy500/utils/sheets_api.json')



    # In[ ]:



@app.route('/')
def entry():
    run_container()    
    return 'Hey, we have Flask in a Docker container!'


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 8080)