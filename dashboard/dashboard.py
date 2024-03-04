import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache(allow_output_mutation=True)
def load_data():
    return pd.read_csv('main_data.csv')

# Initialize session_state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Call load_data to get the data
data = st.session_state.data

# Convert date columns to datetime
data['dteday'] = pd.to_datetime(data['dteday'])

st.title('Visualisasi Data')

# Sidebar
st.sidebar.header('Rentang Waktu')
start_date = st.sidebar.date_input("Mulai", min_value=data['dteday'].min().date(), max_value=data['dteday'].max().date(), value=data['dteday'].min().date())
end_date = st.sidebar.date_input("Selesai", min_value=data['dteday'].min().date(), max_value=data['dteday'].max().date(), value=data['dteday'].max().date())

# Filter data
if st.sidebar.button('Lihat Hasil'):
    if 'start_date' in locals() and 'end_date' in locals():
        filtered_df = data[(data['dteday'] >= pd.Timestamp(start_date)) & (data['dteday'] <= pd.Timestamp(end_date))]
        if 'filtered_df' not in locals():
            st.warning("Silakan pilih rentang waktu yang valid.")
        else:
            st.write('**Detail Rentang Waktu yang Dipilih:**')
            st.write(f"Mulai: {start_date.strftime('%Y-%m-%d')}")
            st.write(f"Selesai: {end_date.strftime('%Y-%m-%d')}")


            # Convert input dates to datetime
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter data based on date range
            filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date)]

            # Plot waktu (jam/hari) vs jumlah total sepeda yang dipinjam
            st.subheader('Waktu vs Total Sewa Sepeda')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x='hr', y='cnt_x', data=filtered_df, estimator='sum', ci=None, ax=ax)
            ax.set_xlabel('Jam')
            ax.set_ylabel('Total Sewa Sepeda')
            st.pyplot(fig)

            # Plot pola musiman dalam penggunaan sepeda berdasarkan bulan atau musim
            st.subheader('Penggunaan Musiman')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='mnth_x', y='cnt_x', data=filtered_df, estimator='sum', ci=None, ax=ax, palette='viridis')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Jumlah Sepeda Dipinjam')
            st.pyplot(fig)

            # Plot pengaruh cuaca terhadap jumlah sepeda yang dipinjam
            st.subheader('Pengaruh Cuaca Terhadap Jumlah Sepeda yang Dipinjam')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='weathersit_x', y='cnt_x', data=filtered_df, estimator='sum', ci=None, ax=ax)
            ax.set_xlabel('Kondisi Cuaca')
            ax.set_ylabel('Jumlah Sepeda Dipinjam')

            # Check if plot has data
            if not filtered_df.empty:
                st.pyplot(fig)
            else:
                st.error("Tidak ada data yang valid untuk diplot.")
    else:
        st.warning("Silakan pilih rentang waktu terlebih dahulu.")