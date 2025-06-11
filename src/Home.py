import streamlit as st
from streamlit_lottie import st_lottie
import requests
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Stadistics Criminality | Advanced Crime Analysis",
    page_icon="./assets/Logo-removebg.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)



def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache_data
def generate_sample_data():
    districts = ['Mission', 'SOMA', 'Tenderloin', 'Castro', 'Richmond', 'Sunset']
    crimes = ['Theft', 'Assault', 'Burglary', 'Vandalism', 'Drug Offense']
    
    monthly_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Crimes': [1250, 1180, 1320, 1450, 1380, 1290],
        'Arrests': [340, 320, 380, 420, 390, 360]
    })
    
    district_data = pd.DataFrame({
        'District': districts,
        'Total_Crimes': np.random.randint(800, 2000, len(districts)),
        'Crime_Rate': np.random.uniform(15.2, 45.8, len(districts)),
        'Safety_Score': np.random.uniform(3.2, 8.7, len(districts))
    })
    
    return monthly_data, district_data

monthly_data, district_data = generate_sample_data()

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&display=swap');
        
        :root {
            --crimson: #DC143C;
            --dark-red: #8B0000;
            --orange: #FF4500;
            --coral: #FF6347;
            --dark-bg: #0A0A0A;
            --darker-bg: #000000;
            --card-bg: #1A1A1A;
            --text-primary: #FFFFFF;
            --text-secondary: #CCCCCC;
            --text-muted: #888888;
            --border: #333333;
            --accent: #FFD700;
        }

        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--dark-bg);
            color: var(--text-primary);
        }
        
        .main, .stApp {
            background: linear-gradient(135deg, #0A0A0A 0%, #1A0A0A 50%, #0A0A0A 100%);
        }

        .nav-header {
            background: rgba(26, 26, 26, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid var(--crimson);
            padding: 1rem 0;
            margin-bottom: 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--crimson);
            text-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
        }

        .nav-stats {
            display: flex;
            gap: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            color: var(--orange);
            font-weight: 700;
            font-size: 1.2rem;
        }

        .stat-label {
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 2rem;
            margin: 3rem 0;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
            padding: 0 2rem;
        }

        .feature-module {
            background: linear-gradient(145deg, var(--card-bg) 0%, #2A1A1A 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
            min-height: 320px;
        }

        .feature-module::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);
        }

        .feature-module:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(220, 20, 60, 0.2);
            border-color: var(--crimson);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }

        .feature-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1rem;
        }

        .feature-description {
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }

        .feature-button {
            background: linear-gradient(135deg, var(--crimson) 0%, var(--orange) 100%);
            color: white;
            padding: 0.8rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Space Grotesk', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9rem;
        }

        .feature-button:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(220, 20, 60, 0.4);
        }

        .hero-section {
            display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 60vh; /* Puedes ajustar a 100vh si quieres full pantalla */
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
        }

        .hero-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--crimson) 0%, var(--orange) 50%, var(--accent) 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(220, 20, 60, 0.3);
        }

        .hero-subtitle {
            font-size: clamp(1.1rem, 2vw, 1.4rem);
            color: var(--text-secondary);
            margin-bottom: 2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .preview-section {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
            border: 1px solid var(--border);
        }

        .preview-title {
            font-family: 'JetBrains Mono', monospace;
            color: var(--orange);
            font-size: 0.9rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        @media (max-width: 1024px) {
            .features-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .nav-container {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-stats {
                gap: 1rem;
            }
        }

        @media (max-width: 768px) {
            .nav-stats {
                display: none;
            }
            
            .hero-section {
                padding: 2rem 1rem;
            }
        }

        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--dark-bg);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--crimson), var(--orange));
            border-radius: 4px;
        }

        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }

        .status-high { background: var(--crimson); }
        .status-medium { background: var(--orange); }
        .status-low { background: var(--accent); }

    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="nav-header">
        <div class="nav-container">
            <div class="logo-section">
                <div class="logo-text">Stadistics Criminality</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">v1.0.0</div>
            </div>
            <div class="nav-stats">
                <div class="stat-item">
                    <div class="stat-value">884,261</div>
                    <div class="stat-label">CASES ANALYZED</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">95.7%</div>
                    <div class="stat-label">GEMINI AI ACCURACY</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">LIVE</div>
                    <div class="stat-label">SYSTEM STATUS</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Stadistics Criminality</h1>
        <p class="hero-subtitle">
            Advanced crime analysis system for San Francisco. Real-time processing 
            of geospatial data, predictive analysis and territorial comparison using 
            machine learning algorithms specialized in urban security.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="features-grid">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-module">
            <span class="feature-icon">📊</span>
            <h3 class="feature-title">ANALYTICS_ENGINE</h3>
            <p class="feature-description">
                Advanced statistical analysis engine with interactive visualizations. 
                Processes temporal patterns, crime trends and multivariate 
                correlations in real time.
            </p>
            <div class="preview-section">
                <div class="preview-title">PREVIEW_DATA</div>
    """, unsafe_allow_html=True)
    
    fig_mini = go.Figure()
    fig_mini.add_trace(go.Scatter(
        x=monthly_data['Month'], 
        y=monthly_data['Crimes'],
        mode='lines+markers',
        line=dict(color='#DC143C', width=3),
        marker=dict(color='#FF4500', size=8)
    ))
    fig_mini.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_mini, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("""
            </div>
    <a href="/Chart" target="_self">
        <button class="feature-button">ACCESS ANALYTICS</button>
    </a>        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-module">
            <span class="feature-icon">🗺️</span>
            <h3 class="feature-title">GEOSPATIAL_MAP</h3>
            <p class="feature-description">
                Intelligent geospatial mapping with heat layers, dynamic clustering 
                and crime density analysis. 3D visualization of hotspots 
                and optimized patrol routes.
            </p>
            <div class="preview-section">
                <div class="preview-title">HEATMAP_PREVIEW</div>
    """, unsafe_allow_html=True)
    
    fig_map = go.Figure()
    np.random.seed(42)
    fig_map.add_trace(go.Scatter(
        x=np.random.uniform(-122.5, -122.3, 50),
        y=np.random.uniform(37.7, 37.8, 50),
        mode='markers',
        marker=dict(
            size=np.random.uniform(5, 15, 50),
            color=np.random.uniform(0, 1, 50),
            colorscale=[[0, '#FFD700'], [0.5, '#FF4500'], [1, '#DC143C']],
            opacity=0.7
        )
    ))
    fig_map.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("""
            </div>
            <a href="/Map" target="_self">
            <button  class="feature-button">OPEN MAP</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-module">
            <span class="feature-icon">⚖️</span>
            <h3 class="feature-title">ZONE_COMPARATOR</h3>
            <p class="feature-description">
                Advanced zone comparator with security metrics, risk indices 
                and differential analysis. Territorial benchmarking 
                and strategic recommendations based on AI.
            </p>
            <div class="preview-section">
                <div class="preview-title">COMPARISON_MATRIX</div>
    """, unsafe_allow_html=True)
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=district_data['District'][:4],
        y=district_data['Safety_Score'][:4],
        marker_color=['#DC143C', '#FF4500', '#FF6347', '#FFD700']
    ))
    fig_comp.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("""
            </div>
            <a href="/Zone_Comparator" target="_self">
            <button  class="feature-button">COMPARE ZONES</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="background: var(--card-bg); border-radius: 16px; padding: 2rem; margin: 3rem auto; max-width: 1400px; border: 1px solid var(--border);">
        <h2 style="font-family: 'JetBrains Mono', monospace; color: var(--crimson); margin-bottom: 2rem; text-align: center;">
            SYSTEM_STATUS_DASHBOARD
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
            <div style="text-align: center;">
                <div style="color: var(--orange); font-size: 2rem; font-weight: 700;">15.2%</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">CRIME REDUCTION</div>
                <div><span class="status-indicator status-low"></span>POSITIVE TREND</div>
            </div>
            <div style="text-align: center;">
                <div style="color: var(--orange); font-size: 2rem; font-weight: 700;">847</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">ACTIVE CASES</div>
                <div><span class="status-indicator status-medium"></span>ACTIVE MONITORING</div>
            </div>
            <div style="text-align: center;">
                <div style="color: var(--orange); font-size: 2rem; font-weight: 700;">23</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">CRITICAL ZONES</div>
                <div><span class="status-indicator status-high"></span>MAXIMUM ALERT</div>
            </div>
            <div style="text-align: center;">
                <div style="color: var(--orange); font-size: 2rem; font-weight: 700;">99.1%</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">SYSTEM UPTIME</div>
                <div><span class="status-indicator status-low"></span>OPERATIONAL</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 3rem 0; border-top: 1px solid var(--border); margin-top: 4rem;">
        <div style="font-family: 'JetBrains Mono', monospace; color: var(--crimson); font-size: 1.2rem; margin-bottom: 0.5rem;">
            Stadistics Criminality
        </div>
        <div style="color: var(--text-muted); font-size: 0.9rem;">
            Advanced Crime Analysis System | San Francisco 
        </div>
        <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 1rem;">
            Powered by Los matemonda | © 2025
        </div>
    </div>
""", unsafe_allow_html=True)