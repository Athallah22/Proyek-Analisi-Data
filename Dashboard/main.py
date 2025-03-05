import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load cleaned data
all_df = pd.read_csv("Dashboard/all_data.csv")

# Konversi kolom tanggal menjadi datetime
all_df["date"] = pd.to_datetime(all_df["date"])

day_mapping = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
all_df['weekday'] = all_df['weekday'].map(day_mapping)

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
    
    # Filter berdasarkan hari dan cuaca
    selected_days = st.sidebar.multiselect("Pilih Hari:", all_df['weekday'].unique(), default=all_df['weekday'].unique())
    selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca:", all_df['weather_condition'].unique(), default=all_df['weather_condition'].unique())
    
    filtered_df = all_df[(all_df['weekday'].isin(selected_days)) & (all_df['weather_condition'].isin(selected_weather))]
    
    st.subheader("Perbandingan Peminjaman Sepeda: Hari Kerja vs. Libur")
    table_working_vs_holiday = filtered_df.groupby(['working_day'])[['total_rentals']].agg(['mean', 'median', 'std'])
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
    table_weather_vs_rentals = filtered_df.groupby(['weather_condition'])[['total_rentals']].agg(['mean', 'median', 'std'])
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
        **Kesimpulan:**
        - Rata-rata peminjaman lebih tinggi pada hari kerja dibandingkan hari libur.
        - Saat cuaca cerah, jumlah peminjaman lebih tinggi dibandingkan saat hujan atau mendung.
        - Korelasi menunjukkan bahwa cuaca (-0.31) lebih memengaruhi peminjaman dibandingkan hari kerja/libur (0.06).
        - **Cuaca lebih berdampak pada jumlah peminjaman dibandingkan status hari kerja/libur.**
        """
    )

elif option == "2. Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja":
    st.header("Efektivitas Sistem Bike-Sharing pada Hari Libur vs Hari Kerja")
    
    # Filter pilihan Hari Kerja atau Hari Libur
    work_holiday_option = st.radio("Pilih kategori:", ['Semua', 'Hari Kerja', 'Hari Libur'])
    
    if work_holiday_option == 'Hari Kerja':
        filtered_df = all_df[all_df['working_day'] == 1]
    elif work_holiday_option == 'Hari Libur':
        filtered_df = all_df[all_df['working_day'] == 0]
    else:
        filtered_df = all_df
    
    st.subheader("Perbandingan Rata-rata Peminjaman pada Hari Kerja vs. Hari Libur")
    work_holiday_summary = filtered_df.groupby('working_day')['total_rentals'].agg(['mean', 'median', 'std'])
    work_holiday_summary = work_holiday_summary.rename(index={0: 'Libur', 1: 'Hari Kerja'})
    st.dataframe(work_holiday_summary)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=work_holiday_summary.index, y=work_holiday_summary['mean'], palette=['red', 'blue'], ax=ax)
    ax.set_title('Rata-rata Peminjaman Sepeda: Hari Kerja vs. Libur', fontsize=14)
    ax.set_xlabel('Kategori', fontsize=12)
    ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
    st.pyplot(fig)
    
    st.subheader("Perbandingan Peminjaman: Pengguna Terdaftar vs. Kasual")
    user_type_comparison = filtered_df.groupby(['working_day'])[['total_registered', 'total_casual']].mean()
    user_type_comparison = user_type_comparison.rename(index={0: 'Libur', 1: 'Hari Kerja'})
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

    # Mapping angka ke nama hari
    day_mapping = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
    day_mapping_reverse = {v: k for k, v in day_mapping.items()}  # Untuk mapping balik dari nama hari ke angka

    # Jika weekday dalam format string, ubah ke angka
    if all_df['weekday'].dtype == 'object':
        all_df['weekday'] = all_df['weekday'].map(day_mapping_reverse)

    # Pastikan weekday adalah integer setelah mapping
    all_df['weekday'] = all_df['weekday'].astype(int)

    # Grouping data berdasarkan weekday
    weekly_rentals = all_df.groupby('weekday')[['total_registered', 'total_casual']].mean()
    weekly_rentals.index = weekly_rentals.index.map(day_mapping)

    # **✅ Filter Data Per Hari**
    selected_day = st.selectbox("Pilih Hari:", ["Semua Hari"] + list(day_mapping.values()))

    if selected_day != "Semua Hari":
        # Filter data berdasarkan hari yang dipilih
        filtered_data = weekly_rentals.loc[[selected_day]]
    else:
        filtered_data = weekly_rentals  # Tampilkan semua data

    # Cek apakah dataframe kosong
    if filtered_data.empty or filtered_data.isnull().values.all():
        st.warning("Data tidak tersedia untuk ditampilkan.")
    else:
        st.dataframe(filtered_data)

        # Buat plot
        fig, ax = plt.subplots(figsize=(10, 5))
        filtered_data.plot(kind='bar', width=0.8, colormap='coolwarm', edgecolor='black', ax=ax)
        ax.set_xticklabels(filtered_data.index, rotation=0)
        ax.set_title('Pola Peminjaman Sepeda: Registered vs. Casual per Hari', fontsize=14)
        ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
        ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
        ax.legend(['Registered', 'Casual'], loc='upper left')

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

    # Mapping angka ke nama hari
    day_mapping = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
    day_mapping_reverse = {v: k for k, v in day_mapping.items()}  # Mapping balik nama hari ke angka

    # Jika weekday dalam format string, ubah ke angka
    if all_df['weekday'].dtype == 'object':
        all_df['weekday'] = all_df['weekday'].map(day_mapping_reverse)

    # Pastikan weekday adalah integer setelah mapping
    all_df['weekday'] = all_df['weekday'].astype(int)

    # **Hitung rata-rata peminjaman sepeda per hari**
    weekly_total_rentals = all_df.groupby('weekday')['total_rentals'].mean()
    weekly_total_rentals.index = weekly_total_rentals.index.map(day_mapping)

    # **✅ Filter Data Per Hari**
    selected_day = st.selectbox("Pilih Hari:", ["Semua Hari"] + list(day_mapping.values()))

    if selected_day != "Semua Hari":
        # Filter data berdasarkan hari yang dipilih
        filtered_data = weekly_total_rentals.loc[[selected_day]]
    else:
        filtered_data = weekly_total_rentals  # Tampilkan semua data

    # **Tampilkan Data**
    st.dataframe(filtered_data)

    # **Buat Plot**
    if not filtered_data.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=filtered_data.index, y=filtered_data.values, palette='coolwarm', edgecolor='black')
        ax.set_title('Rata-rata Peminjaman Sepeda per Hari dalam Seminggu', fontsize=14)
        ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
        ax.set_ylabel('Rata-rata Peminjaman', fontsize=12)
        ax.set_xticklabels(filtered_data.index, rotation=0)
        st.pyplot(fig)
    else:
        st.warning("Data tidak tersedia untuk ditampilkan.")

    st.markdown(
        """
        ### Berdasarkan hasil visualisasi didapatkan hari dengan peminjaman tertinggi adalah `hari Sabtu` & `hari Jumat`.
        """
    )
