# Submission Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan submission akhir kelas **Belajar Analisis Data dengan Python** di Dicoding. Analisis dilakukan terhadap dataset Bike Sharing dari Capital Bikeshare System (Washington D.C.) selama periode 2011 hingga 2012.

## Identitas

- **Nama:** Muhamad Chandra Darmawan
- **Email:** muhamadchandra.d19@gmail.com
- **ID Dicoding:** m_chn9

## Pertanyaan Bisnis

1. Bagaimana pengaruh musim dan kondisi cuaca terhadap rata-rata jumlah peminjaman sepeda harian di Washington D.C. selama 2011 hingga 2012, serta kombinasi musim dan cuaca mana yang menghasilkan rata-rata peminjaman tertinggi?
2. Pada jam berapa puncak peminjaman sepeda terjadi pada hari kerja dibandingkan hari libur, dan bagaimana perbandingan pengguna casual terhadap registered pada jam puncak tersebut?

## Struktur Direktori

```
submission
├── .streamlit
│   └── config.toml
├── dashboard
│   ├── .streamlit
│   │   └── config.toml
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard Secara Lokal

### 1. Menyiapkan Virtual Environment (opsional tetapi direkomendasikan)

```bash
python -m venv venv
source venv/bin/activate   # untuk macOS atau Linux
venv\Scripts\activate       # untuk Windows
```

### 2. Menginstal Dependensi

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard Streamlit

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

## Cara Menjalankan Notebook

```bash
jupyter notebook notebook.ipynb
```

Pastikan folder `data` berada pada direktori yang sama dengan `notebook.ipynb` karena notebook memuat berkas dari path `data/day.csv` dan `data/hour.csv`. Anda juga bisa membuka notebook ini di Google Colab atau VSCode karena format `.ipynb` kompatibel di semua environment.

## Dashboard Online

Dashboard versi online dapat diakses melalui tautan yang tercantum pada berkas `url.txt`.

## Ringkasan Temuan Utama

Musim Gugur mencatat rata-rata peminjaman harian tertinggi sebesar 5.644 sepeda, sementara musim Semi hanya 2.604 sepeda. Hari dengan cuaca Cerah menghasilkan rata-rata 4.877 peminjaman, sedangkan hari dengan Hujan atau Salju Ringan hanya 1.803 peminjaman. Puncak peminjaman pada hari kerja terjadi pukul 08.00 dan 17.00 yang menunjukkan pola commuting, sedangkan hari libur memperlihatkan puncak tunggal pada siang hari. Total peminjaman tahun 2012 tumbuh 64,9 persen dibandingkan tahun 2011.

## Tools yang Digunakan

- Python 3.11
- Pandas untuk manipulasi data
- Matplotlib dan Seaborn untuk visualisasi di notebook
- Plotly untuk visualisasi interaktif di dashboard
- Streamlit untuk dashboard web
- Jupyter Notebook untuk dokumentasi analisis
