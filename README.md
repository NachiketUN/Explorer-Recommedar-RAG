# Explorer-Recommendar-RAG
Ensemble Retrieval and RAG Application with integrated Recommender System. We make use of Google Local Data (2021).

## Prerequisites
* OPENAI Key needs to be stored on your local machine https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
* Two pickle files 1) restaurent_docs_1.pickle and 2) recommendation_1.pickle
* Vector Store Folder "chroma_db_res2/"
* Pickle files and Chroma DB folder can be downloaded from this Google Drive link https://drive.google.com/drive/folders/1LbOJrTIqOuxl8esmMtbVSq8hNb8RVtuZ?usp=sharing


## Getting Started
* Install the python packages from requirements.txt
* Install Node 12
* To start the backend server run ``` python app.py```
* To run React, cd into ISRFrontend Folder and run ``` npm start ```
