import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import json
from typing import Dict, List
import numpy as np
import calendar

# Uygulama ayarları
APP_TITLE = "🎓 YKS Ultra Profesyonel Koç v2.0"
SHOPIER_LINK = "https://www.shopier.com/37499480"

# Sayfa konfigürasyonu
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ana başlık
st.title(APP_TITLE)

# Session state başlatma
def initialize_session_state():
    defaults = {
        "logged_in": False,
        "username": "",
        'öğrenci_bilgisi': {},
        'program_oluşturuldu': False,
        'deneme_sonuçları': [],
        'konu_durumu': {},
        'günlük_çalışma_kayıtları': {},
        'motivasyon_puanı': 100,
        'hedef_sıralama': 1000
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Kullanıcı doğrulama fonksiyonu
def kullanici_dogrula():
    try:
        users = pd.read_csv("users.csv")
        return users
    except FileNotFoundError:
        st.error("⛔ users.csv dosyası bulunamadı! Lütfen kullanıcı listesini ekleyin.")
        return None

# LOGIN EKRANI
def login_screen():
    st.info("Bu sisteme giriş için **kullanıcı adı ve şifre** gereklidir. Şifreyi Shopier ödeme sonrası alabilirsiniz.")
    
    # Kullanıcıları yükle
    users = kullanici_dogrula()
    if users is None:
        st.stop()
    
    # Login formu
    with st.form("login_form"):
        username = st.text_input("👤 Kullanıcı Adı:")
        password = st.text_input("🔑 Şifre:", type="password")
        
        login_button = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
        
        if login_button:
            if username and password:
                # Kullanıcı doğrulaması
                if ((users["username"] == username) & (users["password"] == password)).any():
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success(f"✅ Hoş geldin {username}!")
                    st.rerun()
                else:
                    st.error("⛔ Kullanıcı adı veya şifre yanlış!")
                    st.markdown(f"[💳 Şifre almak için ödeme yap]({SHOPIER_LINK})")
            else:
                st.warning("⚠️ Lütfen kullanıcı adı ve şifre girin!")
    
    # Ek bilgilendirme
    st.markdown("---")
    st.markdown("### 🌟 YKS Derece Öğrencisi Sistemi Özellikleri")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Kişisel Çalışma Programı**
        - Sınıfa özel program
        - Günlük detaylı plan
        - Akıllı zaman yönetimi
        """)
    
    with col2:
        st.markdown("""
        **📈 Gelişmiş Analiz**
        - Deneme analizi
        - Konu mastery takibi
        - Performans grafikleri
        """)
    
    with col3:
        st.markdown("""
        **🎯 Derece Stratejileri**
        - Bölüm özel taktikler
        - Motivasyon sistemi
        - Uzman önerileri
        """)

# Bölüm bazlı tema renkleri ve arka planları
BÖLÜM_TEMALARI = {
    "Tıp": {
        "renk": "#dc3545",
        "arka_plan": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "icon": "🩺",
        "background_image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    },
    "Hukuk": {
        "renk": "#6f42c1",
        "arka_plan": "linear-gradient(135deg, #2c3e50 0%, #34495e 100%)",
        "icon": "⚖️",
        "background_image": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    },
    "Mühendislik": {
        "renk": "#fd7e14",
        "arka_plan": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "icon": "⚙️",
        "background_image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    },
    "İşletme": {
        "renk": "#20c997",
        "arka_plan": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "icon": "💼",
        "background_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    },
    "Öğretmenlik": {
        "renk": "#198754",
        "arka_plan": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "icon": "👩‍🏫",
        "background_image": "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    },
    "Diğer": {
        "renk": "#6c757d",
        "arka_plan": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "icon": "🎓",
        "background_image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
    }
}

# Derece öğrencisi stratejileri
DERECE_STRATEJİLERİ = {
    "9. Sınıf": {
        "öncelik": ["TYT Matematik Temeli", "TYT Türkçe", "Fen Temel", "Sosyal Temel"],
        "haftalık_dağılım": {
            "TYT Matematik": 6, "TYT Türkçe": 4, "TYT Fen": 3, "TYT Sosyal": 2, 
            "AYT": 0, "Deneme": 1, "Tekrar": 4
        },
        "günlük_strateji": "Temel kavram odaklı çalışma, bol tekrar",
        "hedef": "TYT konularında %80 hakimiyet"
    },
    "10. Sınıf": {
        "öncelik": ["TYT Matematik İleri", "AYT Giriş", "TYT Pekiştirme"],
        "haftalık_dağılım": {
            "TYT Matematik": 5, "TYT Türkçe": 3, "TYT Fen": 3, "TYT Sosyal": 2,
            "AYT": 3, "Deneme": 2, "Tekrar": 2
        },
        "günlük_strateji": "TYT pekiştirme + AYT temel başlangıç",
        "hedef": "TYT %85, AYT temel konularda %60 hakimiyet"
    },
    "11. Sınıf": {
        "öncelik": ["AYT Ana Dersler", "TYT Hız", "Deneme Yoğunluğu"],
        "haftalık_dağılım": {
            "TYT Matematik": 3, "TYT Türkçe": 2, "TYT Fen": 2, "TYT Sosyal": 1,
            "AYT": 8, "Deneme": 3, "Tekrar": 1
        },
        "günlük_strateji": "AYT odaklı yoğun çalışma, TYT hız çalışması",
        "hedef": "TYT %90, AYT %75 hakimiyet"
    },
    "12. Sınıf": {
        "öncelik": ["AYT İleri Seviye", "Deneme Maratonu", "Zayıf Alan Kapatma"],
        "haftalık_dağılım": {
            "TYT Matematik": 2, "TYT Türkçe": 2, "TYT Fen": 1, "TYT Sosyal": 1,
            "AYT": 8, "Deneme": 5, "Tekrar": 1
        },
        "günlük_strateji": "Zorlu sorular, hız ve doğruluk, psikolojik hazırlık",
        "hedef": "TYT %95, AYT %85+ hakimiyet"
    },
    "Mezun": {
        "öncelik": ["Eksik Alan Kapatma", "Üst Seviye Problemler", "Mental Hazırlık"],
        "haftalık_dağılım": {
            "TYT Matematik": 2, "TYT Türkçe": 1, "TYT Fen": 1, "TYT Sosyal": 1,
            "AYT": 10, "Deneme": 4, "Tekrar": 1
        },
        "günlük_strateji": "Uzman seviyesi sorular, tam hakimiyet",
        "hedef": "TYT %98, AYT %90+ hakimiyet"
    }
}

def tema_css_oluştur(bölüm_kategori):
    tema = BÖLÜM_TEMALARI[bölüm_kategori]
    
    return f"""
    <style>
        .main-container {{
            background: {tema['arka_plan']};
            min-height: 100vh;
        }}
        
        .hero-section {{
            background: url('{tema['background_image']}') center/cover;
            background-blend-mode: overlay;
            background-color: rgba(0,0,0,0.3);
            padding: 3rem 0;
            border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            color: white;
        }}
        
        .main-header {{
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            margin-bottom: 1rem;
        }}
        
        .section-header {{
            font-size: 1.8rem;
            font-weight: bold;
            color: {tema['renk']};
            margin: 2rem 0 1rem 0;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border-left: 5px solid {tema['renk']};
        }}
        
        .info-card {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
            margin: 1rem 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        .success-card {{
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        .warning-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            color: white;
        }}
        
        .metric-card {{
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(15px);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .program-item {{
            background: rgba(255,255,255,0.1);
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border-left: 4px solid {tema['renk']};
            backdrop-filter: blur(5px);
        }}
    </style>
    """

def bölüm_kategorisi_belirle(hedef_bölüm):
    bölüm_lower = hedef_bölüm.lower()
    if any(word in bölüm_lower for word in ['tıp', 'diş', 'eczacılık', 'veteriner']):
        return "Tıp"
    elif any(word in bölüm_lower for word in ['hukuk', 'adalet']):
        return "Hukuk"
    elif any(word in bölüm_lower for word in ['mühendis', 'bilgisayar', 'elektrik', 'makine', 'inşaat']):
        return "Mühendislik"
    elif any(word in bölüm_lower for word in ['işletme', 'iktisat', 'maliye', 'ekonomi']):
        return "İşletme"
    elif any(word in bölüm_lower for word in ['öğretmen', 'eğitim', 'pdrs']):
        return "Öğretmenlik"
    else:
        return "Diğer"

def öğrenci_bilgi_formu():
    st.markdown("""
    <div class="hero-section">
        <div class="main-header">🏆 YKS Derece Öğrencisi Sistemi</div>
        <p style="font-size: 1.2rem;">Türkiye'nin En Başarılı Öğrencilerinin Stratejileri ile Hazırlan!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("öğrenci_bilgi_form", clear_on_submit=False):
        st.markdown('<div class="section-header">📝 Kişisel Bilgiler</div>', unsafe_allow_html=True)
        
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
                                ["Başlangıç (Net: 0-30)", "Temel (Net: 30-60)", 
                                 "Orta (Net: 60-90)", "İyi (Net: 90-120)", "Çok İyi (Net: 120+)"])
            uyku_saati = st.slider("😴 Günlük Uyku Saati", 6, 10, 8)
            beslenme_kalitesi = st.selectbox("🍎 Beslenme Kalitesi", ["Düzenli", "Orta", "Düzensiz"])
        
        # Gelişmiş motivasyon faktörleri
        st.markdown("### 💪 Motivasyon Profili")
        col4, col5 = st.columns(2)
        
        with col4:
            çalışma_ortamı = st.selectbox("🏠 Çalışma Ortamı", ["Sessiz Oda", "Kütüphane", "Kafe", "Karışık"])
            çalışma_tarzı = st.selectbox("📖 Çalışma Tarzı", ["Yalnız", "Grup", "Karma"])
        
        with col5:
            hedef_motivasyonu = st.slider("🎯 Hedef Motivasyon Seviyesi", 1, 10, 8)
            stres_yönetimi = st.selectbox("😌 Stres Yönetimi", ["Çok İyi", "İyi", "Orta", "Zayıf"])
        
        submitted = st.form_submit_button("✅ Derece Öğrencisi Programını Başlat", use_container_width=True)
        
        if submitted and isim and hedef_bölüm:
            bölüm_kategori = bölüm_kategorisi_belirle(hedef_bölüm)
            
            st.session_state.öğrenci_bilgisi = {
                'isim': isim, 'sınıf': sınıf, 'alan': alan, 'hedef_bölüm': hedef_bölüm,
                'hedef_sıralama': hedef_sıralama, 'seviye': seviye, 'çalışma_saati': çalışma_saati,
                'uyku_saati': uyku_saati, 'beslenme_kalitesi': beslenme_kalitesi,
                'çalışma_ortamı': çalışma_ortamı, 'çalışma_tarzı': çalışma_tarzı,
                'hedef_motivasyonu': hedef_motivasyonu, 'stres_yönetimi': stres_yönetimi,
                'bölüm_kategori': bölüm_kategori, 'kayıt_tarihi': str(datetime.now().date())
            }
            st.session_state.program_oluşturuldu = True
            
            # Tema CSS'ini uygula
            tema_css = tema_css_oluştur(bölüm_kategori)
            st.markdown(tema_css, unsafe_allow_html=True)
            
            st.success(f"🎉 Hoş geldin {isim}! {bölüm_kategori} temalı derece öğrencisi programın hazırlandı!")
            st.rerun()

def derece_günlük_program():
    bilgi = st.session_state.öğrenci_bilgisi
    strateji = DERECE_STRATEJİLERİ[bilgi['sınıf']]
    tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
    
    st.markdown(f'<div class="section-header">{tema["icon"]} Derece Öğrencisi Günlük Program</div>', 
                unsafe_allow_html=True)
    
    # Basit günlük program gösterimi
    st.markdown("### 📅 Örnek Günlük Program")
    st.markdown(f"**Sınıf:** {bilgi['sınıf']}")
    st.markdown(f"**Günlük Strateji:** {strateji['günlük_strateji']}")
    st.markdown(f"**Hedef:** {strateji['hedef']}")
    
    # Öncelik listesi
    st.markdown("### 🎯 Bu Haftanın Öncelikleri:")
    for i, öncelik in enumerate(strateji['öncelik'], 1):
        st.markdown(f"{i}. {öncelik}")
    
    # Haftalık dağılım
    st.markdown("### 📊 Haftalık Saat Dağılımı:")
    col1, col2 = st.columns(2)
    
    with col1:
        for ders, saat in list(strateji['haftalık_dağılım'].items())[:4]:
            st.markdown(f"**{ders}:** {saat} saat")
    
    with col2:
        for ders, saat in list(strateji['haftalık_dağılım'].items())[4:]:
            st.markdown(f"**{ders}:** {saat} saat")

def ana_dashboard():
    bilgi = st.session_state.öğrenci_bilgisi
    tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
    
    st.markdown(f'''
    <div class="hero-section">
        <div class="main-header">{tema['icon']} {bilgi['isim']}'in Derece Yolculuğu</div>
        <p style="font-size: 1.3rem;">"{bilgi['hedef_bölüm']}" hedefine giden yolda!</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Performans kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        konu_sayısı = len(st.session_state.konu_durumu)
        st.markdown(f'''
        <div class="metric-card">
            <h3>📚 Toplam Konu</h3>
            <h2 style="color: {tema['renk']};">{konu_sayısı}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        deneme_sayısı = len(st.session_state.deneme_sonuçları)
        st.markdown(f'''
        <div class="metric-card">
            <h3>📝 Toplam Deneme</h3>
            <h2 style="color: {tema['renk']};">{deneme_sayısı}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        çalışma_günü = len(st.session_state.günlük_çalışma_kayıtları)
        st.markdown(f'''
        <div class="metric-card">
            <h3>📅 Çalışma Günü</h3>
            <h2 style="color: {tema['renk']};">{çalışma_günü}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        motivasyon = st.session_state.motivasyon_puanı
        st.markdown(f'''
        <div class="metric-card">
            <h3>💪 Motivasyon</h3>
            <h2 style="color: {tema['renk']};">{motivasyon}%</h2>
        </div>
        ''', unsafe_allow_html=True)

def yks_coach_panel():
    """YKS Koçluk paneli - sadece giriş yapmış kullanıcılar için"""
    
    # Tema CSS'ini uygula
    if st.session_state.program_oluşturuldu:
        bölüm_kategori = st.session_state.öğrenci_bilgisi['bölüm_kategori']
        tema_css = tema_css_oluştur(bölüm_kategori)
        st.markdown(tema_css, unsafe_allow_html=True)
    
    # Sidebar - Kullanıcı bilgileri
    with st.sidebar:
        st.success(f"Giriş yaptınız ✅ ({st.session_state['username']})")
        
        if st.button("🚪 Çıkış Yap"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["program_oluşturuldu"] = False
            st.session_state["öğrenci_bilgisi"] = {}
            st.rerun()
        
        if st.session_state.program_oluşturuldu:
            bilgi = st.session_state.öğrenci_bilgisi
            tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
            
            st.markdown(f'''
            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 1rem;">
                <h2>{tema['icon']} Derece Sistemi</h2>
                <p><strong>{bilgi['isim']}</strong></p>
                <p>{bilgi['sınıf']} - {bilgi['alan']}</p>
                <p>🎯 {bilgi['hedef_bölüm']}</p>
                <p>🏅 Hedef: {bilgi['hedef_sıralama']}. sıra</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Menü
            menu = st.selectbox("📋 Derece Menüsü", [
                "🏠 Ana Dashboard",
                "📅 Günlük Program", 
                "🎯 Konu Masterysi",
                "📈 Deneme Analizi",
                "💡 Derece Önerileri",
                "📊 Performans İstatistikleri"
            ])
        else:
            menu = "🏠 Ana Dashboard"
    
    # Ana içerik
    if not st.session_state.program_oluşturuldu:
        öğrenci_bilgi_formu()
    else:
        if menu == "🏠 Ana Dashboard":
            ana_dashboard()
        elif menu == "📅 Günlük Program":
            derece_günlük_program()
        elif menu == "🎯 Konu Masterysi":
            st.markdown("### 🎯 Konu Mastery Sistemi")
            st.info("Konu mastery sistemi geliştiriliyor...")
        elif menu == "📈 Deneme Analizi":
            st.markdown("### 📈 Deneme Analiz Sistemi")
            st.info("Deneme analiz sistemi geliştiriliyor...")
        elif menu == "💡 Derece Önerileri":
            st.markdown("### 💡 Derece Önerileri")
            bilgi = st.session_state.öğrenci_bilgisi
            tema = BÖLÜM_TEMALARI[bilgi['bölüm_kategori']]
            strateji = DERECE_STRATEJİLERİ[bilgi['sınıf']]
            
            st.markdown(f'''
            <div class="success-card">
                <h3>{tema['icon']} {bilgi['bölüm_kategori']} Özel Stratejileri</h3>
                <p><strong>Hedef Bölüm:</strong> {bilgi['hedef_bölüm']}</p>
                <p><strong>Günlük Strateji:</strong> {strateji['günlük_strateji']}</p>
                <p><strong>Ana Hedef:</strong> {strateji['hedef']}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        