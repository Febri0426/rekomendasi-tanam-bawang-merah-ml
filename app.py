import streamlit as st
import joblib
import pandas as pd

# Memuat model
@st.cache_resource
def load_model():
    return joblib.load('model_bawang_sukomoro.pkl')

model = load_model()

# ==========================================
# KAMUS TIPS PERAWATAN BERDASARKAN KONDISI
# ==========================================
def dapatkan_tips(hujan, suhu_max, kelembapan):
    tips = []
    
    # Tips berdasarkan curah hujan
    if hujan > 50:
        tips.append("🌧️ **Curah hujan tinggi!** Segera periksa saluran drainase agar tidak tergenang.")
        tips.append("⚠️ Waspadai penyakit **busuk umbi** dan **busuk daun**.")
    elif hujan > 20:
        tips.append("🌦️ Hujan sedang. Kurangi penyiraman manual.")
        tips.append("🔍 Periksa daun secara rutin untuk deteksi dini jamur.")
    else:
        tips.append("☀️ Cuaca cerah. Lakukan penyiraman pagi hari (pukul 06.00-08.00).")
        tips.append("💧 Pastikan tanah tetap lembap tapi tidak becek.")
    
    # Tips berdasarkan suhu
    if suhu_max > 33:
        tips.append("🌡️ **Suhu sangat panas!** Pertimbangkan mulsa jerami untuk menjaga kelembapan tanah.")
    elif suhu_max < 27:
        tips.append("🌡️ Suhu cukup dingin. Pertumbuhan mungkin melambat, bersabar.")
    
    # Tips berdasarkan kelembapan
    if kelembapan > 85:
        tips.append("💦 Kelembapan tinggi. Waspadai serangan **Thrips** dan **Ulat Grayak**.")
        tips.append("🧴 Pertimbangkan penyemprotan fungisida preventif.")
    elif kelembapan < 60:
        tips.append("🏜️ Udara kering. Tingkatkan frekuensi penyiraman.")
    
    # Tips umum
    tips.append("📅 **Umur tanaman 0-30 hari:** Fokus pada pertumbuhan daun.")
    tips.append(" **Umur tanaman 30-60 hari:** Mulai pembentukan umbi, kurangi nitrogen.")
    
    return tips

# ==========================================
# TAMPILAN APLIKASI
# ==========================================
st.set_page_config(page_title="Rekomendasi Tanam Bawang", page_icon="🧅", layout="wide")
st.title("🧅 Sistem Rekomendasi Tanam Bawang Merah")
st.subheader("📍 Lokasi: Sukomoro, Nganjuk |  Powered by Machine Learning")
st.markdown("---")

# Input dalam 2 kolom
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌦️ Data Cuaca Hari Ini")
    hujan = st.number_input("Curah Hujan (mm/hari):", min_value=0.0, max_value=200.0, value=10.0, step=1.0)
    suhu_max = st.number_input("🌡️ Suhu Maksimum (°C):", min_value=15.0, max_value=40.0, value=31.0, step=0.5)

with col2:
    suhu_min = st.number_input("️ Suhu Minimum (°C):", min_value=10.0, max_value=30.0, value=23.0, step=0.5)
    kelembapan = st.number_input("💧 Kelembapan (%):", min_value=0.0, max_value=100.0, value=75.0, step=1.0)

st.markdown("---")

# Tombol Prediksi
if st.button("🔍 Analisis & Dapatkan Rekomendasi", use_container_width=True, type="primary"):
    with st.spinner('Sistem AI sedang menganalisis...'):
        data_input = pd.DataFrame([[hujan, suhu_max, suhu_min, kelembapan]], 
                                  columns=['Curah_Hujan_mm', 'Suhu_Max_C', 'Suhu_Min_C', 'RH2M'])
        prediksi = model.predict(data_input)[0]
        
        # Tampilkan Hasil Prediksi
        st.markdown("## 📊 Hasil Analisis")
        
        col_rekomendasi, col_tips = st.columns([1, 2])
        
        with col_rekomendasi:
            st.markdown("### Rekomendasi:")
            if prediksi == 'Sukses':
                st.success("✅ **SILAKAN TANAM!**\n\nKondisi cuaca sangat ideal untuk pertumbuhan umbi.")
            elif prediksi == 'Cukup':
                st.warning("⚠️ **BISA TANAM, TAPI WASPADA!**\n\nPastikan drainase lahan sangat baik.")
            else:
                st.error("❌ **TUNDA PENANAMAN!**\n\nRisiko umbi busuk terlalu tinggi.")
        
        with col_tips:
            st.markdown("### 💡 Tips Perawatan Hari Ini:")
            tips = dapatkan_tips(hujan, suhu_max, kelembapan)
            for tip in tips:
                st.markdown(f"- {tip}")

# Footer
st.markdown("---")
st.caption("Dibuat dengan ❤️ untuk Petani Sukomoro, Nganjuk | Data Cuaca: NASA POWER")
