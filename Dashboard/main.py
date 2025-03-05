import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load cleaned data
all_df = pd.read_csv("Dashboard/all_data.csv")

# Konversi kolom tanggal menjadi datetime
all_df["date"] = pd.to_datetime(all_df["date"])

st.title("Analisis Efektivitas Sistem Bike-Sharing")

# Pilihan pertanyaan di sidebar
option = st.sidebar.selectbox("Pilih Analisis:", [
    "1. Pengaruh Hari Kerja/Libur vs. Cuaca terhadap Peminjaman",
    "2. Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja",
    "3. Perbedaan pola peminjaman pengguna registered dan casual",
    "4. Hari yang paling sering digunakan untuk meminjam sepeda"
])

if option == "1. Pengaruh Hari Kerja/Libur vs. Cuaca terhadap Peminjaman":
    st.header("Pengaruh Hari Kerja/Libur vs. Cuaca terhadap Peminjaman")
    st.subheader("Perbandingan Peminjaman Sepeda: Hari Kerja vs. Libur")
    table_working_vs_holiday = all_df.groupby(['working_day'])[['total_rentals']].agg(['mean', 'median', 'std'])
    table_working_vs_holiday.columns = ['Mean Rentals', 'Median Rentals', 'Std Dev']
    table_working_vs_holiday.index = ['Libur', 'Hari Kerja']
    st.dataframe(table_working_vs_holiday)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=table_working_vs_holiday.index, y=table_working_vs_holiday['Mean Rentals'], palette=['red', 'blue'], ax=ax)
    ax.set_title('Rata-rata Peminjaman: Hari Kerja vs. Libur', fontsize=14)
    ax.set_xlabel('Kategori', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    st.pyplot(fig)
    
    st.subheader("Perbandingan Peminjaman Sepeda Berdasarkan Cuaca")
    table_weather_vs_rentals = all_df.groupby(['weather_condition'])[['total_rentals']].agg(['mean', 'median', 'std'])
    table_weather_vs_rentals.columns = ['Mean Rentals', 'Median Rentals', 'Std Dev']
    st.dataframe(table_weather_vs_rentals)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=table_weather_vs_rentals.index, y=table_weather_vs_rentals['Mean Rentals'], palette='viridis', ax=ax)
    ax.set_title('Rata-rata Peminjaman: Berdasarkan Cuaca', fontsize=14)
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    st.pyplot(fig)
    
    st.markdown(
        """
        1. Rata-rata peminjaman lebih tinggi pada hari kerja dibandingkan hari libur. Namun, cuaca juga berpengaruh signifikan terhadap jumlah peminjaman.
        2. Saat cuaca cerah, jumlah peminjaman lebih tinggi dibandingkan saat hujan atau mendung.
        3. Korelasi menunjukkan bahwa cuaca (-0.31) lebih memengaruhi peminjaman dibandingkan hari kerja/libur (0.06).
        ### Berdasarkan ketiga poin di atas, dapat disimpulkan bahwa cuaca lebih berdampak pada jumlah peminjaman dibandingkan status hari kerja/libur.
        """
    )

elif option == "2. Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja":
    st.header("Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja")
    st.subheader("Perbandingan Rata-rata Peminjaman pada Hari Kerja vs. Hari Libur")
    work_holiday_summary = all_df.groupby('working_day')['total_rentals'].agg(['mean', 'median', 'std'])
    work_holiday_summary.index = ['Libur', 'Hari Kerja']
    st.dataframe(work_holiday_summary)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=work_holiday_summary.index, y=work_holiday_summary['mean'], palette=['red', 'blue'], ax=ax)
    ax.set_title('Rata-rata Peminjaman Sepeda: Hari Kerja vs. Libur', fontsize=14)
    ax.set_xlabel('Kategori', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    st.pyplot(fig)
    
    st.subheader("Perbandingan Peminjaman: Pengguna Terdaftar vs. Kasual")
    user_type_comparison = all_df.groupby(['working_day'])[['total_registered', 'total_casual']].mean()
    user_type_comparison.index = ['Libur', 'Hari Kerja']
    st.dataframe(user_type_comparison)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    user_type_comparison.plot(kind='bar', colormap='coolwarm', edgecolor='black', ax=ax)
    ax.set_title('Peminjaman: Pengguna Terdaftar vs. Kasual', fontsize=14)
    ax.set_xlabel('Kategori', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    ax.legend(['Terdaftar', 'Kasual'])
    st.pyplot(fig)
    
    st.markdown(
        """
        1. Hari kerja memiliki jumlah peminjaman lebih tinggi dibandingkan hari libur.
        2. Sistem lebih efektif digunakan di hari kerja, yang menunjukkan bahwa layanan ini lebih sering dimanfaatkan oleh pekerja atau mahasiswa untuk transportasi harian.
        3. Hari libur tetap memiliki peminjaman yang signifikan, tetapi lebih rendah dibanding hari kerja.
        ### Berdasarkan tiga poin di atas didapatkan hasil bahwa sistem bike-sharing lebih efektif untuk pengguna harian di hari kerja dibandingkan rekreasi di hari libur.
        """
    )

elif option == "3. Perbedaan pola peminjaman pengguna registered dan casual":
    st.header("Perbedaan pola peminjaman pengguna registered dan casual")
    st.subheader("Pola Peminjaman Pengguna Registered vs. Casual Sepanjang Minggu")
    weekly_rentals = all_df.groupby('weekday')[['total_registered', 'total_casual']].mean()
    day_mapping = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
    weekly_rentals.index = weekly_rentals.index.map(day_mapping)
    st.dataframe(weekly_rentals)

    fig, ax = plt.subplots(figsize=(10, 5))
    weekly_rentals.plot(kind='bar', width=0.8, colormap='coolwarm', edgecolor='black', ax=ax)
    ax.set_xticklabels(weekly_rentals.index, rotation=0)
    ax.set_title('Pola Peminjaman Sepeda: Registered vs. Casual per Hari', fontsize=14)
    st.pyplot(fig)

    st.markdown(
        """
        1. Pengguna Registered (Terdaftar)
            - Peminjaman sepeda meningkat dari Senin hingga Jumat, dengan puncak pada Kamis dan Jumat (sekitar 4000-an).
            - Pada akhir pekan (Sabtu & Minggu), peminjaman turun secara signifikan.
            - Data ini menunjukkan bahwa pengguna registered menggunakan sepeda sebagai alat transportasi utama selama hari kerja (misalnya untuk ke kantor atau kampus).

        2. Pengguna Casual (Tidak Terdaftar)
            - Peminjaman sepeda justru menurun drastis selama hari kerja, terutama pada Selasa hingga Jumat di bawah 600-an.
            - Jumlah peminjaman naik kembali pada Sabtu & Minggu, dengan puncak pada Minggu (sekitar 1500-an).
            - Data ini menunjukkan bahwa pengguna casual lebih sering menggunakan sepeda untuk rekreasi atau aktivitas santai di akhir pekan.
  
        ### Registered Users lebih aktif pada hari kerja, kemungkinan besar untuk transportasi sehari-hari, dan Casual Users lebih aktif di akhir pekan, kemungkinan besar untuk rekreasi atau perjalanan santai.
        """
    )
elif option == "4. Hari yang paling sering digunakan untuk meminjam sepeda":
    st.header("Hari yang paling sering digunakan untuk meminjam sepeda")
    st.subheader("Rata-rata Total Peminjaman Sepeda per Hari dalam Seminggu")
    weekly_total_rentals = all_df.groupby('weekday')['total_rentals'].mean()
    day_mapping = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
    weekly_total_rentals.index = weekly_total_rentals.index.map(day_mapping)
    st.dataframe(weekly_total_rentals)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=weekly_total_rentals.index, y=weekly_total_rentals.values, palette='coolwarm', edgecolor='black')
    ax.set_title('Rata-rata Peminjaman Sepeda per Hari dalam Seminggu', fontsize=14)
    ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    ax.set_xticklabels(weekly_total_rentals.index, rotation=0)
    st.pyplot(fig)

    st.markdown(
        """
        ### Berdasarkan hasil visualisasi didapatkan hari dengan peminjaman tertinggi adalah `hari Sabtu` & `hari Jumat`.
        """
    )