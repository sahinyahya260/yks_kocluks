import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import numpy as np

# Uygulama ayarları
APP_TITLE = "🎓 YKS Ultra Profesyonel Koç v2.0"
SHOPIER_LINK = "https://www.shopier.com/37499480"

# Sayfa konfigürasyonu
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏆",
    layout="wide"
)

# Ana başlık
st.title(APP_TITLE)

# Session state başlatma
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if 'öğrenci_bilgisi' not in st.session_state:
    st.session_state['öğrenci_bilgisi'] = {}
if 'program_oluşturuldu' not in st.session_state:
    st.session_state['program_oluşturuldu'] = False

# Demo kullanıcılar
demo_users = pd.DataFrame({
    'username': ['demo', 'test', 'admin'],
    'password': ['123', '456', 'admin123']
})

# Bölüm teması
BÖLÜM_TEMALARI = {
    "Tıp": {"renk": "#dc3545", "icon": "🩺"},
    "Hukuk": {"renk": "#6f42c1", "icon": "⚖️"},
    "Mühendislik": {"renk": "#fd7e14", "icon": "⚙️"},
    "İşletme": {"renk": "#20c997", "icon": "💼"},
    "Öğretmenlik": {"renk": "#198754", "icon": "👩‍🏫"},
    "Diğer": {"renk": "#6c757d", "icon": "🎓"}
}

# Strateji verileri
DERECE_STRATEJİLERİ = {
    "9. Sınıf": {
        "öncelik": ["TYT Matematik Temeli", "TYT Türkçe", "Fen Temel"],
        "günlük_strateji": "Temel kavram odaklı çalışma",
        "hedef": "TYT konularında %80 hakimiyet"
    },
    "10. Sınıf": {
        "öncelik": ["TYT Matematik İleri", "AYT Giriş", "TYT Pekiştirme"],
        "günlük_strateji": "TYT pekiştirme + AYT başlangıç",
        "hedef": "TYT %85, AYT temel %60 hakimiyet"
    },
    "11. Sınıf": {
        "öncelik": ["AYT Ana Dersler", "TYT Hız", "Deneme Yoğunluğu"],
        "günlük_strateji": "AYT odaklı yoğun çalışma",
        "hedef": "TYT %90, AYT %75 hakimiyet"
    },
    "12. Sınıf": {
        "öncelik": ["AYT İleri Seviye", "Deneme Maratonu", "Zayıf Alan"],
        "günlük_strateji": "Zorlu sorular, hız ve doğruluk",
        "hedef": "TYT %95, AYT %85+ hakimiyet"
    },
    "Mezun": {
        "öncelik": ["Eksik Alan Kapatma", "Üst Seviye Problemler"],
        "günlük_strateji": "Uzman seviyesi sorular",
        "hedef": "TYT %98, AYT %90+ hakimiyet"
    }
}

def bölüm_kategorisi_belirle(hedef_bölüm):
    bölüm_lower = hedef_bölüm.lower()
    if any(word in bölüm_lower for word in ['tıp', 'diş', 'eczacılık']):
        return "Tıp"
    elif any(word in bölüm_lower for word in ['hukuk', 'adalet']):
        return "Hukuk"
    elif any(word in bölüm_lower for word in ['mühendis', 'bilgisayar', 'elektrik']):
        return "Mühendislik"
    elif any(word in bölüm_lower for word in ['işletme', 'iktisat', 'ekonomi']):
        return "İşletme"
    elif any(word in bölüm_lower for word in ['öğretmen', 'eğitim']):
        return "Öğretmenlik"
    else:
        return "Diğer"

# ANA AKIŞ - LOGIN KONTROLÜ
if not st.session_state["logged_in"]:
    # LOGIN EKRANI
    st.info("Sisteme giriş yapmak için kullanıcı adı ve şifre gerekli")
    st.success("**Demo Giriş:** Kullanıcı: demo, Şifre: 123")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Kullanıcı Adı:")
            password = st.text_input("🔑 Şifre:", type="password")
            
            login_button = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
            
            if login_button:
                if username and password:
                    # Kullanıcı kontrolü
                    if ((demo_users["username"] == username) & (demo_users["password"] == password)).any():
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.success(f"Hoş geldin {username}!")
                        st.rerun()
                    else:
                        st.error("Kullanıcı adı veya şifre yanlış!")
                else:
                    st.warning("Lütfen kullanıcı adı ve şifre girin!")
    
    # Özellikler tanıtımı
    st.markdown("---")
    st.markdown("### 🌟 YKS Derece Öğrencisi Sistemi Özellikleri")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Kişisel Program**
        - Sınıfa özel plan
        - Günlük detay
        - Zaman yönetimi
        """)
    
    with col2:
        st.markdown("""
        **📈 Analiz Sistemi**
        - Deneme takibi
        - Performans grafiği
        - İlerleme raporu
        """)
    
    with col3:
        st.markdown("""
        **🎯 Derece Stratejileri**
        - Bölüm özel taktik
        - Motivasyon desteği
        - Uzman önerileri
        """)

else:
    # KULLANICI GİRİŞ YAPMIŞ - YKS PANEL
    
    # Sidebar
    with st.sidebar:
        st.success(f"Giriş yapıldı ✅ ({st.session_state['username']})")
        
        if st.button("🚪 Çıkış Yap"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["program_oluşturuldu"] = False
            st.session_state["öğrenci_bilgisi"] = {}
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.program_oluşturuldu:
            bilgi = st.session_state.öğrenci_bilgisi
            tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
            
            st.markdown(f"""
            **{tema['icon']} {bilgi['isim']}**
            - {bilgi['sınıf']} - {bilgi['alan']}
            - 🎯 {bilgi['hedef_bölüm']}
            - 🏅 Hedef: {bilgi['hedef_sıralama']}. sıra
            """)
            
            menu = st.selectbox("📋 Menü", [
                "🏠 Ana Panel",
                "📅 Günlük Program", 
                "📈 Deneme Takibi",
                "💡 Öneriler"
            ])
        else:
            menu = "🏠 Ana Panel"
    
    # ANA İÇERİK
    if not st.session_state.program_oluşturuldu:
        # ÖĞRENCİ BİLGİ FORMU
        st.markdown("## 🏆 YKS Derece Öğrencisi Sistemi")
        st.markdown("Türkiye'nin en başarılı öğrencilerinin stratejileri ile hazırlan!")
        
        with st.form("öğrenci_form"):
            st.markdown("### 📝 Kişisel Bilgiler")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                isim = st.text_input("👤 Adın Soyadın", placeholder="Örn: Ahmet Yılmaz")
                sınıf = st.selectbox("🏫 Sınıf", ["9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf", "Mezun"])
                alan = st.selectbox("📚 Alan", ["Sayısal", "Eşit Ağırlık", "Sözel"])
            
            with col2:
                hedef_bölüm = st.text_input("🎯 Hedef Bölüm", placeholder="Örn: Tıp - İstanbul Üniversitesi")
                hedef_sıralama = st.number_input("🏅 Hedef Sıralama", min_value=1, max_value=100000, value=1000)
                çalışma_saati = st.slider("⏰ Günlük Çalışma Saati", 4, 16, 10)
            
            with col3:
                seviye = st.selectbox("📊 Şu Anki Seviye", 
                                    ["Başlangıç (0-30)", "Temel (30-60)", 
                                     "Orta (60-90)", "İyi (90-120)", "Çok İyi (120+)"])
                uyku_saati = st.slider("😴 Uyku Saati", 6, 10, 8)
                motivasyon = st.slider("💪 Motivasyon", 1, 10, 8)
            
            submitted = st.form_submit_button("✅ Programı Başlat", use_container_width=True)
            
            if submitted and isim and hedef_bölüm:
                bölüm_kategori = bölüm_kategorisi_belirle(hedef_bölüm)
                
                st.session_state.öğrenci_bilgisi = {
                    'isim': isim, 'sınıf': sınıf, 'alan': alan, 'hedef_bölüm': hedef_bölüm,
                    'hedef_sıralama': hedef_sıralama, 'seviye': seviye, 'çalışma_saati': çalışma_saati,
                    'uyku_saati': uyku_saati, 'motivasyon': motivasyon,
                    'bölüm_kategori': bölüm_kategori, 'kayıt_tarihi': str(date.today())
                }
                st.session_state.program_oluşturuldu = True
                
                st.success(f"🎉 Hoş geldin {isim}! Programın hazırlandı!")
                st.rerun()
    
    else:
        # ANA PANEL - PROGRAM OLUŞTURULMUŞ
        bilgi = st.session_state.öğrenci_bilgisi
        tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
        strateji = DERECE_STRATEJİLERİ[bilgi['sınıf']]
        
        if menu == "🏠 Ana Panel":
            # Ana dashboard
            st.markdown(f"## {tema['icon']} {bilgi['isim']}'in Derece Yolculuğu")
            st.markdown(f"**Hedef:** {bilgi['hedef_bölüm']} - {bilgi['hedef_sıralama']}. sıra")
            
            # Metrikler
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 Seviye", bilgi['seviye'])
            
            with col2:
                st.metric("⏰ Günlük Saat", f"{bilgi['çalışma_saati']}h")
            
            with col3:
                st.metric("😴 Uyku", f"{bilgi['uyku_saati']}h")
            
            with col4:
                st.metric("💪 Motivasyon", f"{bilgi['motivasyon']}/10")
            
            # Strateji bilgisi
            st.markdown("### 📋 Derece Öğrencisi Stratejin")
            
            col5, col6 = st.columns(2)
            
            with col5:
                st.markdown(f"""
                **🎯 Öncelikler:**
                """)
                for i, öncelik in enumerate(strateji['öncelik'], 1):
                    st.markdown(f"{i}. {öncelik}")
            
            with col6:
                st.markdown(f"""
                **📊 Günlük Strateji:**
                {strateji['günlük_strateji']}
                
                **🏆 Hedef:**
                {strateji['hedef']}
                """)
        
        elif menu == "📅 Günlük Program":
            st.markdown("### 📅 Derece Öğrencisi Günlük Program")
            
            gün = st.selectbox("Gün Seçin", 
                             ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
            
            # Örnek program
            st.markdown("#### 🌅 Sabah Programı")
            st.markdown("""
            - **06:00-07:00:** Uyanış + Kahvaltı
            - **07:00-09:00:** TYT Matematik (Zor konular)
            - **09:00-09:15:** Mola
            - **09:15-11:15:** TYT Türkçe
            - **11:15-12:00:** TYT Fen/Sosyal
            """)
            
            st.markdown("#### ☀️ Öğle Programı")
            st.markdown("""
            - **12:00-13:00:** Öğle yemeği + Dinlenme
            - **13:00-15:00:** AYT Ana Ders
            - **15:00-15:15:** Mola
            - **15:15-17:00:** Problem Çözümü
            - **17:00-18:00:** Deneme/Test
            """)
            
            st.markdown("#### 🌙 Akşam Programı")
            st.markdown("""
            - **19:00-20:00:** Akşam yemeği
            - **20:00-21:30:** Zayıf alan çalışması
            - **21:30-22:30:** Konu tekrarı
            - **22:30-23:00:** Yarın planı + Meditasyon
            """)
        
        elif menu == "📈 Deneme Takibi":
            st.markdown("### 📈 Deneme Sonuçları Takibi")
            
            with st.expander("➕ Yeni Deneme Sonucu Ekle"):
                with st.form("deneme_form"):
                    deneme_tarihi = st.date_input("Tarih")
                    deneme_adı = st.text_input("Deneme Adı", "YKS Denemesi")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**TYT**")
                        tyt_turkce = st.number_input("Türkçe Net", 0, 40, 0)
                        tyt_mat = st.number_input("Matematik Net", 0, 40, 0)
                        tyt_fen = st.number_input("Fen Net", 0, 20, 0)
                        tyt_sosyal = st.number_input("Sosyal Net", 0, 20, 0)
                    
                    with col2:
                        st.markdown("**AYT**")
                        ayt_mat = st.number_input("AYT Mat Net", 0, 40, 0)
                        ayt_fen1 = st.number_input("Fen-1 Net", 0, 14, 0)
                        ayt_fen2 = st.number_input("Fen-2 Net", 0, 13, 0)
                    
                    if st.form_submit_button("Kaydet"):
                        tyt_toplam = tyt_turkce + tyt_mat + tyt_fen + tyt_sosyal
                        ayt_toplam = ayt_mat + ayt_fen1 + ayt_fen2
                        
                        st.success(f"TYT: {tyt_toplam} Net, AYT: {ayt_toplam} Net kaydedildi!")
            
            st.info("Deneme analiz sistemi geliştiriliyor...")
        
        elif menu == "💡 Öneriler":
            st.markdown("### 💡 Derece Öğrencisi Önerileri")
            
            # Bölüm özel öneriler
            bölüm_önerileri = {
                "Tıp": ["🩺 Biyoloji ve Kimya'ya extra odaklan", "🧠 Problem çözme hızını artır"],
                "Hukuk": ["⚖️ Türkçe ve mantık güçlendir", "📖 Hukuk felsefesi oku"],
                "Mühendislik": ["⚙️ Matematik ve Fizik'te uzmanlaş", "🔧 Pratik problem çözme"],
                "İşletme": ["💼 Matematik ve Sosyal güçlendir", "📊 Analitik düşünce geliştir"],
                "Öğretmenlik": ["👩‍🏫 Pedagoji oku", "🎯 Öğretim tekniklerini araştır"],
                "Diğer": ["🎓 Genel strateji uygula", "📚 Kapsayıcı çalışma yap"]
            }
            
            kategori = bilgi['bölüm_kategori']
            st.markdown(f"#### {tema['icon']} {kategori} Özel Öneriler")
            
            for öneri in bölüm_önerileri[kategori]:
                st.markdown(f"• {öneri}")
            
            st.markdown("#### 🏅 Genel Derece Öğrencisi Alışkanlıkları")
            alışkanlıklar = [
                "🌅 Erken kalkma (6:00)",
                "🧘 Günlük meditasyon",
                "📚 Pomodoro tekniği",
                "💧 Bol su içme",
                "🏃 Düzenli egzersiz",
                "📱 Sosyal medya detoksu",
                "😴 Kaliteli uyku"
            ]
            
            for alışkanlık in alışkanlıklar:
                st.markdown(f"• {alışkanlık}")