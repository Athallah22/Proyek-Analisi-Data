# Proyek-Analisi-Data
# Analisis Efektivitas Sistem Bike-Sharing

Proyek ini bertujuan untuk menganalisis efektivitas sistem bike-sharing dengan berbagai faktor, seperti hari kerja vs. hari libur, kondisi cuaca, serta pola peminjaman pengguna terdaftar dan kasual.

## 📌 Persyaratan
Sebelum menjalankan kode, pastikan Anda memiliki lingkungan yang telah dikonfigurasi dengan:

- **Python 3.x**
- **pip** (package manager untuk Python)
- **Streamlit** untuk membuat dashboard interaktif
- **Pandas** untuk manipulasi data
- **Matplotlib** dan **Seaborn** untuk visualisasi data

## 📥 Instalasi
Untuk menjalankan kode, install dependensi berikut terlebih dahulu:

```bash
pip install streamlit pandas matplotlib seaborn
```

## 🚀 Menjalankan Aplikasi
1. Pastikan file `all_data.csv` sudah tersedia dalam direktori yang sama dengan skrip.
2. Jalankan perintah berikut untuk memulai aplikasi Streamlit:

```bash
streamlit run nama_file.py
```

Gantilah `nama_file.py` dengan nama file Python yang berisi kode utama.

## Cara Menjalankan Notebook di Google Colab atau Jupyter Notebook

### 1. Jupyter Notebook (Lokal)
#### a. Pastikan Jupyter Notebook Terinstal
Jika belum terinstal, jalankan:
```bash
pip install jupyter
```

#### b. Jalankan Jupyter Notebook
```bash
jupyter notebook
```
Buka file `Proyek_Analisis_Data.ipynb` di browser.

### 2. Google Colab
#### a. Upload Notebook ke Google Drive
1. Buka [Google Colab](https://colab.research.google.com/)
2. Pilih **File > Upload Notebook**
3. Pilih `Proyek_Analisis_Data.ipynb` dan mulai eksplorasi data

#### b. Upload Dataset ke Google Colab
Jika dataset tidak tersedia di repository, unggah secara manual atau gunakan kode berikut di Colab:
```python
from google.colab import files
uploaded = files.upload()
```
Buka file `Proyek_Analisis_Data.ipynb`.

## 🔍 Fitur Analisis
Aplikasi ini memiliki 4 analisis utama:

1. **Pengaruh Hari Kerja/Libur vs. Cuaca terhadap Peminjaman**
2. **Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja**
3. **Perbedaan Pola Peminjaman Pengguna Registered dan Casual**
4. **Hari yang Paling Sering Digunakan untuk Meminjam Sepeda**

Setiap analisis menampilkan tabel data, visualisasi grafik, serta kesimpulan dari hasil analisis.

## 📊 Dataset
Dataset yang digunakan adalah `all_data.csv`, yang merupakan gabungan dari dataset harian dan per jam.
