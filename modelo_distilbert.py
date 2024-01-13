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
start_time = time.time()

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        # Manejar la situación en la que la API no devuelve una respuesta exitosa
        print(f"Error en la API: {response.status_code}")
        return []

# Carga el archivo csv
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/ecuPrueba_40.csv')

# Variable para contar el total de entidades nombradas
total_entidades_nombradas = 0

# Itera sobre cada fila del dataframe
for index, row in df.iterrows():
    # Realiza la consulta
    output = query({"inputs": row['ATA_TEXTO']})

    # Verifica que 'output' sea una lista antes de continuar
    if isinstance(output, list):
        # Filtra los resultados para excluir entidades con 'LABEL_0'
        filtered_output = [entity for entity in output if entity['entity_group'] != 'LABEL_0']

        # Imprime el ID de la llamada y las entidades nombradas que no tienen 'LABEL_0'
        print(f"ID LLAMADA: {row['TRA_ID']}")
        for entity in filtered_output:
            print(f"entidad: {entity['word']}, tipo: {entity['entity_group']}, score: {entity['score']}")

        # Imprime el número de entidades encontradas
        print(f"Entidades encontradas: {len(filtered_output)}")

        # Suma al total de entidades nombradas
        total_entidades_nombradas += len(filtered_output)
    else:
        print(f"La respuesta no es una lista: {output}")

# Imprime el total de entidades nombradas al final del bucle
print(f"Total de entidades nombradas: {total_entidades_nombradas}")

end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")