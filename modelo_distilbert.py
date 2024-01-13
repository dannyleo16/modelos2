# -*- coding: utf-8 -*-
"""modelo_distilbert.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16JJe-2K--9Defs2y8ItH07vUGMTQfL3m
"""

import time
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification
import requests

# Carga el modelo y el tokenizador
tokenizer = AutoTokenizer.from_pretrained("dccuchile/distilbert-base-spanish-uncased-finetuned-ner")
model = AutoModelForTokenClassification.from_pretrained("dccuchile/distilbert-base-spanish-uncased-finetuned-ner")

# Define una función de consulta
API_URL = "https://api-inference.huggingface.co/models/dccuchile/distilbert-base-spanish-uncased-finetuned-ner"
headers = {"Authorization": "Bearer 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"}
start_time= time.time()
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Carga el archivo csv
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ecuPrueba_40.csv')

# Itera sobre cada fila del dataframe
for index, row in df.iterrows():
    # Realiza la consulta
    output = query({"inputs": row['ATA_TEXTO']})

    # Imprime el ID de la llamada una vez
    print(f"ID LLAMADA: {row['TRA_ID']}")

    # Procesa la salida
    for entity in output:
        # Filtra por tipo 'LABEL_0'
        if entity['entity_group'] != 'LABEL_0':
            print(f"Entidad: {entity['word']}, Tipo: {entity['entity_group']}, Confianza: {entity['score']}")
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")