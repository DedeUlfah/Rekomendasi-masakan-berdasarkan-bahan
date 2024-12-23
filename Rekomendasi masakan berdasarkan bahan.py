# -*- coding: utf-8 -*-
"""LlmGPT2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1X_zbFw0UUdMJ_Itbh8GfOC71_2fjdXsn
"""

pip install transformers pandas torch

import pandas as pd
from transformers import pipeline

# Membaca 5 file dataset .csv
df1 = pd.read_csv('dataset-ayam.csv')
df2 = pd.read_csv('dataset-ikan.csv')
df3 = pd.read_csv('dataset-kambing.csv')
df4 = pd.read_csv('dataset-sapi.csv')
df5 = pd.read_csv('dataset-tahu.csv')
df6 = pd.read_csv('dataset-telur.csv')
df7 = pd.read_csv('dataset-tempe.csv')
df8 = pd.read_csv('dataset-udang.csv')

# Menggabungkan semua dataset menjadi satu dataframe
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], ignore_index=True)

# Mengisi nilai NaN dengan string kosong agar tidak menyebabkan error saat filtering
df['Ingredients'].fillna('', inplace=True)

# Inisialisasi pipeline untuk text generation menggunakan model LLM pre-trained
llm_model = pipeline('text-generation', model='gpt2')

# Fungsi untuk merekomendasikan resep berdasarkan input bahan
def rekomendasi_resep(bahan):
    # Filter dataframe berdasarkan bahan yang terkandung di kolom 'ingredients'
    resep_terkait = df[df['Ingredients'].str.contains(bahan, case=False)]

    if not resep_terkait.empty:
        # Mengambil beberapa resep dari dataset
        resep_list = resep_terkait[['Title', 'Ingredients', 'Steps']].drop_duplicates().head()
        hasil = "Resep yang bisa dibuat dari bahan {}:\n".format(bahan)
        for index, row in resep_list.iterrows():
            hasil += f"\nJudul: {row['Title']}\nBahan: {row['Ingredients']}\nLangkah: {row['Steps']}\n"
        return hasil
    else:
        # Jika bahan tidak ditemukan di dataset, gunakan LLM untuk generate jawaban
        prompt = f"Saya ingin makan {bahan}, apa resep yang bisa saya buat?"
        llm_response = llm_model(prompt, max_length=50, num_return_sequences=1)
        return llm_response[0]['generated_text']

# Input dari pengguna
input_teks = input("Masukkan bahan makanan yang ingin Anda makan: ").lower()

# Mendapatkan bahan dari input pengguna
bahan = input_teks.split()[-1]  # Mengambil kata terakhir sebagai bahan (misalnya 'beras' dari 'saya ingin makan beras')

# Mendapatkan rekomendasi resep
rekomendasi = rekomendasi_resep(bahan)
print(rekomendasi)