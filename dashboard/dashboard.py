"""
Dashboard Bike Sharing Analysis
Dibuat oleh: Muhamad Chandra Darmawan
Email: muhamadchandra.d19@gmail.com
ID Dicoding: m_chn9
"""

# Mengimpor pathlib untuk pengelolaan path file yang portable antar OS dan deployment
from pathlib import Path
# Mengimpor pandas untuk manipulasi dan agregasi data
import pandas as pd
# Mengimpor plotly express untuk membuat chart interaktif
import plotly.express as px
# Mengimpor plotly graph objects untuk chart yang butuh kustomisasi lebih dalam
import plotly.graph_objects as go
# Mengimpor streamlit sebagai framework utama dashboard
import streamlit as st

# Menentukan direktori tempat script berada agar path data selalu benar
# (penting untuk deployment Streamlit Cloud dimana CWD = repo root, bukan folder script)
BASE_DIR = Path(__file__).parent

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# CUSTOM CSS - DARK MINIMAL MODERN (TEMA SEPERTI VERCEL/LINEAR)
# =====================================================================
st.markdown("""
<style>
    /* Mengimpor font Geist Mono dan Inter dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Mendefinisikan design token sebagai variabel CSS agar konsisten */
    :root {
        --bg: #0A0A0B;
        --surface: #111113;
        --surface-2: #161618;
        --border: #1F1F22;
        --border-strong: #2A2A2E;
        --text: #FAFAFA;
        --text-2: #A1A1AA;
        --text-3: #52525B;
        --accent: #10B981;
        --accent-2: #34D399;
    }

    /* Menata font dan background global */
    html, body, [class*="css"], .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg) !important;
        color: var(--text);
    }

    /* Menata container utama dengan max-width terkontrol */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }

    /* Menata header halaman dengan gaya minimal (bukan gradient besar) */
    .page-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding-bottom: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    .page-header .meta-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 11px;
        color: var(--text-2);
        font-weight: 500;
        letter-spacing: 0.02em;
        margin-bottom: 0.9rem;
    }
    .page-header .meta-badge .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    }
    .page-header h1 {
        color: var(--text);
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    .page-header .subtitle {
        color: var(--text-2);
        font-size: 0.92rem;
        margin: 0.35rem 0 0 0;
        font-weight: 400;
        max-width: 560px;
    }
    .page-header .right-meta {
        text-align: right;
        font-size: 0.78rem;
        color: var(--text-3);
        font-family: 'JetBrains Mono', monospace;
        padding-top: 0.5rem;
    }

    /* Menata KPI card dengan gaya yang bersih dan monokromatik */
    .metric {
        background: var(--surface);
        padding: 1.25rem 1.3rem;
        border-radius: 10px;
        border: 1px solid var(--border);
        transition: border-color 0.15s ease;
        height: 100%;
    }
    .metric:hover {
        border-color: var(--border-strong);
    }
    .metric-label {
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--text-3);
        font-size: 0.72rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.7rem;
    }
    .metric-label::before {
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--text-3);
    }
    .metric-label.pos::before { background: var(--accent); }
    .metric-label.amber::before { background: #F59E0B; }
    .metric-label.rose::before { background: #F43F5E; }
    .metric-value {
        color: var(--text);
        font-size: 1.75rem;
        font-weight: 600;
        line-height: 1;
        letter-spacing: -0.02em;
        font-variant-numeric: tabular-nums;
    }
    .metric-sub {
        color: var(--text-3);
        font-size: 0.78rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    .metric-sub .delta {
        color: var(--accent);
        font-weight: 500;
    }

    /* Menata section header dengan tipografi, bukan dekorasi */
    .section {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin: 2.2rem 0 1rem 0;
    }
    .section h3 {
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .section .caption {
        color: var(--text-3);
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Menata insight block yang halus */
    .note {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 2px solid var(--accent);
        padding: 0.9rem 1.1rem;
        border-radius: 8px;
        margin-top: 0.8rem;
    }
    .note-label {
        color: var(--accent);
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }
    .note-text {
        color: var(--text-2);
        font-size: 0.88rem;
        line-height: 1.55;
        margin: 0;
    }
    .note-text strong {
        color: var(--text);
        font-weight: 600;
    }

    /* Menata footer yang minimalis */
    .footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: var(--text-3);
        font-size: 0.78rem;
    }
    .footer code {
        background: var(--surface);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-2);
        font-size: 0.72rem;
    }

    /* Menata sidebar seperti panel kiri aplikasi modern */
    [data-testid="stSidebar"] {
        background: var(--bg) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] h3 {
        color: var(--text);
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-3);
        font-size: 0.8rem;
    }
    [data-testid="stSidebar"] label {
        color: var(--text-2) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500 !important;
    }

    /* Menata tab seperti underline tab Vercel */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid var(--border);
        padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-3);
        padding: 0.7rem 1rem;
        font-weight: 500;
        font-size: 0.85rem;
        border: none;
        border-bottom: 2px solid transparent;
        margin-bottom: -1px;
        border-radius: 0;
        transition: color 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-2);
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--text) !important;
        border-bottom: 2px solid var(--text) !important;
        font-weight: 600;
    }

    /* Menata input, select, dan multiselect agar konsisten dark */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="tag"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--border-strong) !important;
        color: var(--text) !important;
        border-radius: 6px !important;
    }

    /* Menata dataframe agar menyatu */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border);
    }

    /* Menyembunyikan menu hamburger dan footer bawaan Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Menata radio button agar lebih rapi */
    [role="radiogroup"] label {
        color: var(--text-2) !important;
        font-size: 0.85rem !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# FUNGSI MEMUAT DATA
# =====================================================================
@st.cache_data
def load_data():
    # Membangun path absolut ke main_data.csv relatif terhadap lokasi script
    data_path = BASE_DIR / 'main_data.csv'
    # Membaca main_data.csv yang sudah diperkaya dengan kolom label dan denormalisasi
    df = pd.read_csv(data_path)
    # Mengonversi kolom dteday ke datetime agar filter tanggal bekerja dengan benar
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df


# Memuat data satu kali dan menyimpan ke cache
day_df = load_data()

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    # Menampilkan brand minimal di bagian atas sidebar
    st.markdown("""
    <div style="padding:0.3rem 0 1.5rem 0; border-bottom:1px solid #1F1F22; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:24px; height:24px; background:linear-gradient(135deg, #10B981, #34D399);
                        border-radius:6px; display:flex; align-items:center; justify-content:center;
                        color:#0A0A0B; font-weight:700; font-size:14px;">⬢</div>
            <div style="color:#FAFAFA; font-weight:600; font-size:0.95rem;">Bike Analytics</div>
        </div>
        <div style="color:#52525B; font-size:0.72rem; margin-top:0.4rem; font-family:'JetBrains Mono', monospace;">
            v1.0 · dicoding submission
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Menampilkan header filter
    st.markdown("### Filters")

    # Menyiapkan rentang tanggal minimum dan maksimum dari dataset
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()

    # Membuat kontrol date picker dengan default seluruh rentang
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Memastikan dua tanggal terisi walau user baru pilih satu
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    # Membuat kontrol multiselect musim
    season_options = st.multiselect(
        "Season",
        options=['Semi', 'Panas', 'Gugur', 'Dingin'],
        default=['Semi', 'Panas', 'Gugur', 'Dingin']
    )

    # Membuat kontrol multiselect kondisi cuaca
    weather_options = st.multiselect(
        "Weather",
        options=['Cerah', 'Berawan/Berkabut', 'Hujan/Salju Ringan'],
        default=['Cerah', 'Berawan/Berkabut', 'Hujan/Salju Ringan']
    )

    # Membuat kontrol radio tipe hari
    workingday_filter = st.radio(
        "Day Type",
        options=['Semua', 'Hari Kerja', 'Hari Libur/Akhir Pekan'],
        index=0
    )

    st.markdown("<br>", unsafe_allow_html=True)
    # Menampilkan info pembuat dengan gaya minimal
    st.markdown("""
    <div style="padding-top:1.5rem; border-top:1px solid #1F1F22;">
        <div style="color:#52525B; font-size:0.7rem; text-transform:uppercase;
                    letter-spacing:0.08em; margin-bottom:0.4rem; font-weight:500;">Author</div>
        <div style="color:#FAFAFA; font-size:0.85rem; font-weight:500;">Muhamad Chandra Darmawan</div>
        <div style="color:#52525B; font-size:0.72rem; margin-top:0.2rem; font-family:'JetBrains Mono', monospace;">
            @m_chn9
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# FILTERING DATA SESUAI PILIHAN SIDEBAR
# =====================================================================
# Membangun mask gabungan berdasarkan seluruh filter
mask = (
    (day_df['dteday'] >= pd.to_datetime(start_date))
    & (day_df['dteday'] <= pd.to_datetime(end_date))
    & (day_df['season_label'].isin(season_options))
    & (day_df['weather_label'].isin(weather_options))
)
# Menerapkan mask tambahan untuk tipe hari bila user memilih spesifik
if workingday_filter == 'Hari Kerja':
    mask &= (day_df['workingday'] == 1)
elif workingday_filter == 'Hari Libur/Akhir Pekan':
    mask &= (day_df['workingday'] == 0)

# Menyimpan dataframe yang sudah difilter
filtered_df = day_df.loc[mask].copy()

# =====================================================================
# HEADER HALAMAN
# =====================================================================
st.markdown(f"""
<div class="page-header">
    <div>
        <div class="meta-badge">
            <span class="dot"></span>
            <span>Capital Bikeshare · Washington D.C.</span>
        </div>
        <h1>Bike Sharing Analytics</h1>
        <p class="subtitle">Analisis tren peminjaman sepeda berdasarkan musim, cuaca, dan pola waktu pengguna selama periode 2011 hingga 2012.</p>
    </div>
    <div class="right-meta">
        {len(filtered_df)} days<br>
        {filtered_df['dteday'].min().strftime('%Y-%m-%d') if not filtered_df.empty else '—'} → {filtered_df['dteday'].max().strftime('%Y-%m-%d') if not filtered_df.empty else '—'}
    </div>
</div>
""", unsafe_allow_html=True)

# Menampilkan peringatan ketika hasil filter kosong agar tidak error di chart
if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter. Silakan longgarkan filter di sidebar.")
    st.stop()

# =====================================================================
# KPI CARDS
# =====================================================================
# Menghitung metrik utama dari dataframe yang sudah difilter
total_rentals = int(filtered_df['cnt'].sum())
avg_daily = int(filtered_df['cnt'].mean())
casual_total = int(filtered_df['casual'].sum())
registered_total = int(filtered_df['registered'].sum())
casual_pct = round(casual_total / (casual_total + registered_total) * 100, 1) if (casual_total + registered_total) else 0
registered_pct = round(100 - casual_pct, 1)
peak_day = filtered_df.loc[filtered_df['cnt'].idxmax()] if not filtered_df.empty else None

# Mendefinisikan empat kolom untuk KPI card
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Menulis KPI card pertama untuk total peminjaman
kpi1.markdown(f"""
<div class="metric">
    <div class="metric-label pos">Total Rentals</div>
    <div class="metric-value">{total_rentals:,}</div>
    <div class="metric-sub">across {len(filtered_df)} observation days</div>
</div>
""", unsafe_allow_html=True)

# Menulis KPI card kedua untuk rata-rata harian
kpi2.markdown(f"""
<div class="metric">
    <div class="metric-label">Daily Average</div>
    <div class="metric-value">{avg_daily:,}</div>
    <div class="metric-sub">rentals per day</div>
</div>
""", unsafe_allow_html=True)

# Menulis KPI card ketiga untuk pengguna casual
kpi3.markdown(f"""
<div class="metric">
    <div class="metric-label amber">Casual Users</div>
    <div class="metric-value">{casual_total:,}</div>
    <div class="metric-sub">{casual_pct}% of total rentals</div>
</div>
""", unsafe_allow_html=True)

# Menulis KPI card keempat untuk pengguna registered
kpi4.markdown(f"""
<div class="metric">
    <div class="metric-label rose">Registered Users</div>
    <div class="metric-value">{registered_total:,}</div>
    <div class="metric-sub">{registered_pct}% of total rentals</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# TABS UTAMA
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Trends",
    "User Profile",
    "Temperature"
])

# Mendefinisikan palet warna sophisticated untuk chart (monokromatik + accent)
PALETTE = {
    'accent': '#10B981',
    'accent_dim': '#059669',
    'amber': '#F59E0B',
    'rose': '#F43F5E',
    'sky': '#0EA5E9',
    'violet': '#A78BFA',
    'text': '#FAFAFA',
    'text_2': '#A1A1AA',
    'text_3': '#52525B',
    'grid': '#1F1F22',
    'surface': '#111113'
}

# Mendefinisikan template plotly dengan konsisten dark minimal
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color=PALETTE['text_2'], size=11),
        xaxis=dict(
            gridcolor=PALETTE['grid'],
            zerolinecolor=PALETTE['grid'],
            linecolor=PALETTE['grid'],
            tickfont=dict(color=PALETTE['text_2'], size=10),
            title_font=dict(color=PALETTE['text_3'], size=11)
        ),
        yaxis=dict(
            gridcolor=PALETTE['grid'],
            zerolinecolor=PALETTE['grid'],
            linecolor=PALETTE['grid'],
            tickfont=dict(color=PALETTE['text_2'], size=10),
            title_font=dict(color=PALETTE['text_3'], size=11)
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        hoverlabel=dict(
            bgcolor=PALETTE['surface'],
            font=dict(family='Inter', size=11, color=PALETTE['text']),
            bordercolor=PALETTE['grid']
        ),
        title_font=dict(size=12, color=PALETTE['text'], family='Inter'),
    )
)

# =====================================================================
# TAB 1: OVERVIEW (PERTANYAAN 1 - MUSIM & CUACA)
# =====================================================================
with tab1:
    # Menampilkan section title untuk Pertanyaan 1
    st.markdown("""
    <div class="section">
        <h3>Pertanyaan 1 — Pengaruh Musim dan Cuaca</h3>
        <span class="caption">avg daily rentals</span>
    </div>
    """, unsafe_allow_html=True)

    # Membuat dua kolom untuk chart musim dan cuaca
    col_a, col_b = st.columns(2)

    with col_a:
        # Menghitung rata-rata peminjaman per musim
        season_order = ['Semi', 'Panas', 'Gugur', 'Dingin']
        season_avg = (
            filtered_df.groupby('season_label')['cnt']
            .mean()
            .reindex([s for s in season_order if s in filtered_df['season_label'].unique()])
            .reset_index()
        )
        # Menentukan warna muted sophisticated per musim
        season_colors = {
            'Semi': '#34D399',
            'Panas': '#FBBF24',
            'Gugur': '#FB7185',
            'Dingin': '#60A5FA'
        }
        # Membangun bar chart interaktif dengan plotly express
        fig_season = px.bar(
            season_avg,
            x='season_label', y='cnt',
            color='season_label',
            color_discrete_map=season_colors,
            text=season_avg['cnt'].apply(lambda v: f'{int(v):,}'),
            labels={'cnt': 'Avg Rentals', 'season_label': ''}
        )
        # Menyesuaikan tampilan text label di atas bar
        fig_season.update_traces(
            textposition='outside',
            textfont=dict(size=11, color=PALETTE['text'], family='Inter'),
            marker_line_width=0,
            width=0.55
        )
        # Menerapkan template minimal
        fig_season.update_layout(**PLOTLY_TEMPLATE['layout'], showlegend=False, height=320,
                                 title='Rentals by Season')
        # Menampilkan chart pada halaman
        st.plotly_chart(fig_season, use_container_width=True)

    with col_b:
        # Menghitung rata-rata peminjaman per kondisi cuaca
        weather_order = ['Cerah', 'Berawan/Berkabut', 'Hujan/Salju Ringan']
        weather_avg = (
            filtered_df.groupby('weather_label')['cnt']
            .mean()
            .reindex([w for w in weather_order if w in filtered_df['weather_label'].unique()])
            .reset_index()
        )
        # Menentukan warna gradasi dari terang ke redup
        weather_colors = {
            'Cerah': '#FBBF24',
            'Berawan/Berkabut': '#71717A',
            'Hujan/Salju Ringan': '#60A5FA'
        }
        # Membangun bar chart cuaca
        fig_weather = px.bar(
            weather_avg,
            x='weather_label', y='cnt',
            color='weather_label',
            color_discrete_map=weather_colors,
            text=weather_avg['cnt'].apply(lambda v: f'{int(v):,}'),
            labels={'cnt': 'Avg Rentals', 'weather_label': ''}
        )
        # Menyesuaikan tampilan text label di atas bar
        fig_weather.update_traces(
            textposition='outside',
            textfont=dict(size=11, color=PALETTE['text'], family='Inter'),
            marker_line_width=0,
            width=0.55
        )
        # Menerapkan template minimal
        fig_weather.update_layout(**PLOTLY_TEMPLATE['layout'], showlegend=False, height=320,
                                  title='Rentals by Weather')
        # Menampilkan chart
        st.plotly_chart(fig_weather, use_container_width=True)

    # Menyusun heatmap kombinasi musim dan cuaca
    st.markdown("""
    <div class="section">
        <h3>Season × Weather Matrix</h3>
        <span class="caption">heatmap · avg rentals</span>
    </div>
    """, unsafe_allow_html=True)

    # Membangun pivot table rata-rata peminjaman
    pivot_df = filtered_df.pivot_table(
        values='cnt', index='season_label', columns='weather_label', aggfunc='mean'
    )
    # Mengurutkan baris dan kolom sesuai urutan logis
    pivot_df = pivot_df.reindex([s for s in season_order if s in pivot_df.index])
    pivot_df = pivot_df[[w for w in weather_order if w in pivot_df.columns]]
    # Membangun heatmap interaktif dengan skala warna emerald
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale=[[0, '#0F1A17'], [0.4, '#0F5940'], [0.7, '#10B981'], [1, '#6EE7B7']],
        text=[[f'{int(v):,}' if pd.notna(v) else '—' for v in row] for row in pivot_df.values],
        texttemplate='%{text}',
        textfont=dict(size=13, color='#FAFAFA', family='Inter'),
        colorbar=dict(
            title=dict(text='avg', font=dict(color=PALETTE['text_3'], size=10)),
            tickfont=dict(color=PALETTE['text_2'], size=10),
            thickness=12,
            outlinewidth=0
        ),
        hoverongaps=False
    ))
    # Menerapkan template minimal pada heatmap
    fig_heatmap.update_layout(**PLOTLY_TEMPLATE['layout'], height=300,
                              xaxis_title='', yaxis_title='')
    # Menampilkan heatmap
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Menampilkan insight utama pertanyaan 1
    st.markdown("""
    <div class="note">
        <div class="note-label">Key Insight</div>
        <p class="note-text">
        Musim <strong>Gugur</strong> dengan cuaca <strong>Cerah</strong> menjadi kombinasi dengan permintaan tertinggi
        (rata-rata di atas 5.900 sepeda per hari). Sebaliknya, musim Semi dengan Hujan atau Salju Ringan
        mencatat permintaan paling rendah.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# TAB 2: TRENDS
# =====================================================================
with tab2:
    # Menampilkan section title tren harian
    st.markdown("""
    <div class="section">
        <h3>Daily Rental Trend</h3>
        <span class="caption">time series · 2011-2012</span>
    </div>
    """, unsafe_allow_html=True)

    # Membangun area chart tren harian
    fig_trend = go.Figure()
    # Menambahkan trace area untuk total peminjaman
    fig_trend.add_trace(go.Scatter(
        x=filtered_df['dteday'], y=filtered_df['cnt'],
        mode='lines',
        line=dict(color=PALETTE['accent'], width=1.5, shape='spline', smoothing=0.3),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.08)',
        name='Rentals',
        hovertemplate='<b>%{x|%d %b %Y}</b><br>Rentals: %{y:,}<extra></extra>'
    ))
    # Menerapkan template minimal pada tren
    fig_trend.update_layout(**PLOTLY_TEMPLATE['layout'], height=340,
                            xaxis_title='', yaxis_title='Rentals')
    # Menampilkan chart tren
    st.plotly_chart(fig_trend, use_container_width=True)

    # Membuat dua kolom untuk chart bulanan dan hari dalam minggu
    col_c, col_d = st.columns(2)

    with col_c:
        # Menghitung rata-rata peminjaman per bulan dengan urutan bulan asli
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
        monthly_avg = (
            filtered_df.groupby('month_label')['cnt']
            .mean()
            .reindex(month_order)
            .reset_index()
        )
        # Membangun bar chart peminjaman per bulan
        fig_month = px.bar(
            monthly_avg, x='month_label', y='cnt',
            labels={'cnt': 'Avg Rentals', 'month_label': ''}
        )
        # Memberi warna accent emerald yang konsisten
        fig_month.update_traces(
            marker_color=PALETTE['accent'],
            marker_line_width=0,
            width=0.6
        )
        # Menerapkan template minimal
        fig_month.update_layout(**PLOTLY_TEMPLATE['layout'], height=320, showlegend=False,
                                title='Rentals by Month')
        # Menampilkan chart bulanan
        st.plotly_chart(fig_month, use_container_width=True)

    with col_d:
        # Menghitung rata-rata peminjaman per hari dalam seminggu
        weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        weekday_avg = (
            filtered_df.groupby('weekday_label')['cnt']
            .mean()
            .reindex([d for d in weekday_order if d in filtered_df['weekday_label'].unique()])
            .reset_index()
        )
        # Membangun bar chart per hari
        fig_weekday = px.bar(
            weekday_avg, x='weekday_label', y='cnt',
            labels={'cnt': 'Avg Rentals', 'weekday_label': ''}
        )
        # Memberi warna sky yang menyegarkan
        fig_weekday.update_traces(
            marker_color=PALETTE['sky'],
            marker_line_width=0,
            width=0.6
        )
        # Menerapkan template minimal
        fig_weekday.update_layout(**PLOTLY_TEMPLATE['layout'], height=320, showlegend=False,
                                  title='Rentals by Weekday')
        # Menampilkan chart per hari
        st.plotly_chart(fig_weekday, use_container_width=True)

# =====================================================================
# TAB 3: USER PROFILE (PERTANYAAN 2)
# =====================================================================
with tab3:
    # Menampilkan section title komposisi pengguna
    st.markdown("""
    <div class="section">
        <h3>Pertanyaan 2 — Komposisi Pengguna Casual vs Registered</h3>
        <span class="caption">distribution · monthly trend</span>
    </div>
    """, unsafe_allow_html=True)

    # Membuat dua kolom untuk donut chart dan tren
    col_e, col_f = st.columns([1, 1.5])

    with col_e:
        # Membangun donut chart proporsi pengguna
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Casual', 'Registered'],
            values=[casual_total, registered_total],
            hole=0.72,
            marker=dict(
                colors=[PALETTE['amber'], PALETTE['rose']],
                line=dict(color='#0A0A0B', width=3)
            ),
            textinfo='percent',
            textfont=dict(size=13, color='#0A0A0B', family='Inter'),
            hovertemplate='<b>%{label}</b><br>%{value:,} rentals<br>%{percent}<extra></extra>'
        )])
        # Menambahkan annotation besar di tengah donut
        fig_donut.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            height=340,
            annotations=[
                dict(text=f'<b style="font-size:20px;color:#FAFAFA">{total_rentals / 1_000_000:.2f}M</b>',
                     x=0.5, y=0.55, showarrow=False),
                dict(text='<span style="font-size:10px;color:#52525B;letter-spacing:0.08em">TOTAL RENTALS</span>',
                     x=0.5, y=0.42, showarrow=False)
            ],
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5,
                        font=dict(size=11, color=PALETTE['text_2']))
        )
        # Menampilkan donut chart
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_f:
        # Menghitung agregasi casual vs registered per bulan untuk tren
        monthly_user = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M')).agg({
            'casual': 'sum', 'registered': 'sum'
        }).reset_index()
        monthly_user['dteday'] = monthly_user['dteday'].astype(str)
        # Membangun stacked bar chart tren bulanan casual vs registered
        fig_user_trend = go.Figure()
        # Menambahkan bar untuk pengguna registered dengan warna rose
        fig_user_trend.add_trace(go.Bar(
            x=monthly_user['dteday'], y=monthly_user['registered'],
            name='Registered', marker_color=PALETTE['rose'], marker_line_width=0
        ))
        # Menambahkan bar untuk pengguna casual di atas registered dengan warna amber
        fig_user_trend.add_trace(go.Bar(
            x=monthly_user['dteday'], y=monthly_user['casual'],
            name='Casual', marker_color=PALETTE['amber'], marker_line_width=0
        ))
        # Mengatur mode stacking agar terlihat kontribusi masing-masing
        fig_user_trend.update_layout(
            **PLOTLY_TEMPLATE['layout'], height=340,
            title='Monthly Casual vs Registered',
            barmode='stack',
            xaxis_title='', yaxis_title='Rentals',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(size=11, color=PALETTE['text_2']))
        )
        # Menampilkan chart tren pengguna
        st.plotly_chart(fig_user_trend, use_container_width=True)

    # Menyajikan tabel ringkasan pengguna per musim
    st.markdown("""
    <div class="section">
        <h3>Season Breakdown</h3>
        <span class="caption">per season totals</span>
    </div>
    """, unsafe_allow_html=True)

    # Membangun tabel agregasi per musim
    season_user_summary = filtered_df.groupby('season_label').agg(
        Total_Peminjaman=('cnt', 'sum'),
        Rata_rata_Harian=('cnt', 'mean'),
        Pengguna_Casual=('casual', 'sum'),
        Pengguna_Registered=('registered', 'sum')
    ).round(0).astype(int).reset_index()
    # Mengganti nama kolom agar lebih rapi
    season_user_summary.columns = ['Season', 'Total Rentals', 'Daily Avg', 'Casual', 'Registered']
    # Menampilkan tabel dengan lebar penuh
    st.dataframe(season_user_summary, use_container_width=True, hide_index=True)

# =====================================================================
# TAB 4: TEMPERATURE (ANALISIS LANJUTAN)
# =====================================================================
with tab4:
    # Menampilkan section title segmentasi suhu
    st.markdown("""
    <div class="section">
        <h3>Analisis Lanjutan — Segmentasi Kategori Suhu</h3>
        <span class="caption">manual clustering · binning</span>
    </div>
    """, unsafe_allow_html=True)

    # Menghitung agregasi berdasarkan kategori suhu
    temp_analysis = (
        filtered_df.groupby('temp_category', observed=True)['cnt']
        .agg(['mean', 'sum', 'count'])
        .reset_index()
    )
    # Mengganti nama kolom hasil agregasi
    temp_analysis.columns = ['Category', 'Average', 'Total', 'Days']
    # Mengurutkan kategori suhu secara logis
    temp_order = ['Dingin (0-10°C)', 'Sejuk (10-20°C)', 'Hangat (20-30°C)', 'Panas (30°C+)']
    temp_analysis['Category'] = pd.Categorical(temp_analysis['Category'],
                                                 categories=temp_order, ordered=True)
    temp_analysis = temp_analysis.sort_values('Category')

    # Membuat kolom chart dan tabel
    col_g, col_h = st.columns([1.5, 1])

    with col_g:
        # Mendefinisikan warna gradasi dari dingin ke panas yang muted
        temp_colors = ['#60A5FA', '#34D399', '#FBBF24', '#F43F5E']
        # Membangun bar chart segmentasi suhu
        fig_temp = px.bar(
            temp_analysis, x='Category', y='Average',
            text=temp_analysis['Average'].apply(lambda v: f'{int(v):,}'),
            color='Category', color_discrete_sequence=temp_colors
        )
        # Mengatur posisi text label di atas bar
        fig_temp.update_traces(
            textposition='outside',
            textfont=dict(size=11, color=PALETTE['text'], family='Inter'),
            marker_line_width=0,
            width=0.55
        )
        # Menerapkan template minimal
        fig_temp.update_layout(**PLOTLY_TEMPLATE['layout'], height=340, showlegend=False,
                               title='Rentals by Temperature Category',
                               xaxis_title='', yaxis_title='Avg Rentals')
        # Menampilkan chart segmentasi suhu
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_h:
        # Menyiapkan tabel tampilan dengan format angka yang rapi
        display_table = temp_analysis.copy()
        display_table['Average'] = display_table['Average'].apply(lambda v: f'{int(v):,}')
        display_table['Total'] = display_table['Total'].apply(lambda v: f'{int(v):,}')
        # Menampilkan tabel ringkasan
        st.dataframe(display_table, use_container_width=True, hide_index=True)

        # Menampilkan insight kunci dengan box halus
        st.markdown("""
        <div class="note">
            <div class="note-label">Observation</div>
            <p class="note-text">
            Kategori <strong>Hangat (20-30°C)</strong> adalah kondisi paling optimal dengan rata-rata
            peminjaman tertinggi. Kategori Dingin mencatat permintaan paling rendah.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("""
<div class="footer">
    <div>
        <code>bike-sharing</code> · Capital Bikeshare System, Washington D.C. 2011-2012
    </div>
    <div>
        Built by Muhamad Chandra Darmawan · Submission Proyek Analisis Data Dicoding
    </div>
</div>
""", unsafe_allow_html=True)
