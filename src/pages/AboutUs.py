import streamlit as st
from PIL import Image
import os
from io import BytesIO
import base64
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="About Us | Criminality Statistics",
    page_icon="./assets/Logo-removebg.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
        return Image.new('RGB', (120, 120), color='#1c1f26')

team = [
    {
        "name": "Zaid Pantoja Manosalva",
        "role": "UI Designer – Creator of Home and Team Pages",
        "bio": "Data enthusiast focused on predictive analysis and advanced visualization. Responsible for building and training the machine learning model for the system.",
        "image": "Zaid.png",
        "github": "https://github.com/Alberthzaid",
        "linkedin": "https://www.linkedin.com/in/alberth-zaid-a42aa8222/",
        "whatsapp": "https://wa.me/573185182953",
        "gmail": "alberthzaid2003@gmail.com"
    },
    {
        "name": "Andres Aviles de la Rosa",
        "role": "Backend Developer – Zone Comparator Designer",
        "bio": "Backend developer with experience in Java, Spring Boot and RESTful APIs. Responsible for implementing the zone comparator for geographical analysis in the system.",
        "image": "Broko.png",
        "github": "https://github.com/andresavilesdev",
        "linkedin": "https://www.linkedin.com/in/andresavilesdev/",
        "whatsapp": "https://wa.me/573137374995",
        "gmail": "andresaviles0721@gmail.com"
    },
    {
        "name": "Angel Gabriel Ortega Corzo",
        "role": "Backend Developer – Interactive Map Designer",
        "bio": "Designer focused on intuitive and accessible REST API experiences. Responsible for developing the interactive map functionality for geospatial visualization.",
        "image": "Angelo.png",
        "github": "https://github.com/Angel-ISO",
        "linkedin": "https://www.linkedin.com/in/angel-gabriel-ortega/",
        "whatsapp": "https://wa.me/573222946366",
        "gmail": "angelgabrielorteg@gmail.com"
    },
    {
        "name": "Miguel Rojas Quintero",
        "role": "Backend Developer – Interactive Charts Designer",
        "bio": "Backend developer with experience in Java, Spring Boot and RESTful APIs. Responsible for implementing the interactive charts functionality for data visualization.",
        "image": "Miguelo.jpg",
        "github": "https://github.com/jmrq-43",
        "linkedin": "http://www.linkedin.com/in/miguel-rojas-quintero",
        "whatsapp": "https://wa.me/573122603042",
        "gmail": "rojasquinteroj26@gmail.com"
    }
]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
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

    .hero-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 60vh; 
        padding: 4rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
        position: relative;
        padding: 6rem 2rem;
        text-align: center;
        overflow: hidden;
        margin-bottom: 4rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.8) 0%, rgba(10, 10, 10, 0.9) 100%);
        border: 1px solid var(--border);
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);
    }

    .hero-section::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--crimson) 50%, transparent 100%);
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

    .about-section {
        max-width: 1200px;
        margin: 0 auto 4rem auto;
        padding: 2rem;
        background: rgba(26, 26, 26, 0.5);
        border-radius: 16px;
        border: 1px solid var(--border);
        position: relative;
    }

    .about-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);
    }

    .section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--crimson);
        margin-bottom: 1.5rem;
        position: relative;
        display: inline-block;
    }

    .section-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 60%;
        height: 3px;
        background: linear-gradient(90deg, var(--crimson) 0%, transparent 100%);
    }

    .about-text {
        color: var(--text-secondary);
        line-height: 1.8;
        font-size: 1.05rem;
    }

    .about-text strong {
        color: var(--orange);
        font-weight: 600;
    }

    .about-text em {
        color: var(--accent);
        font-style: normal;
    }

    .team-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        padding: 2rem;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    .team-card {
        background-color: #1c1f26;
        border-radius: 15px;
        padding: 1.5rem;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        margin-bottom: 2rem;
    }

    .team-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(220, 20, 60, 0.2);
        border: 1px solid var(--crimson);
    }

    .profile-pic {
        width: 120px;
        height: 120px;
        object-fit: cover;
        border-radius: 50%;
        margin: 0 auto 1rem;
        border: 3px solid var(--crimson);
        display: block;
    }

    .member-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.2rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.3rem;
    }

    .member-role {
        font-size: 0.95rem;
        color: var(--orange);
        margin-bottom: 0.7rem;
        font-weight: 600;
    }

    .member-bio {
        font-size: 0.85rem;
        color: #bbb;
        margin-bottom: 1.2rem;
        line-height: 1.4;
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 15px;
    }

    .social-links a {
        color: var(--crimson);
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }

    .social-links a:hover {
        color: #fff;
        transform: scale(1.1);
    }

    .stats-section {
        max-width: 1200px;
        margin: 0 auto 4rem auto;
        padding: 3rem 2rem;
        background: rgba(26, 26, 26, 0.5);
        border-radius: 16px;
        border: 1px solid var(--border);
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
    }

    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .stat-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(220, 20, 60, 0.15);
        border-color: var(--crimson);
    }

    .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--orange);
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .footer {
        text-align: center;
        padding: 3rem 0;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
    }

    .footer-logo {
        font-family: 'JetBrains Mono', monospace;
        color: var(--crimson);
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .footer-text {
        color: var(--text-muted);
        font-size: 0.9rem;
    }

    .footer-copyright {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 1rem;
    }

    @media (max-width: 768px) {
        .team-card {
            width: 100%;
            max-width: 300px;
        }
        
        .stats-grid {
            grid-template-columns: 1fr 1fr;
        }
        
        .hero-section {
            padding: 4rem 1rem;
        }
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stApp {
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav-header">
    <div class="nav-container">
        <div class="logo-section">
            <div class="logo-text">Criminality Statistics</div>
            <div style="color: var(--text-muted); font-size: 0.9rem;">v1.0.0</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">OUR TEAM</h1>
    <p class="hero-subtitle">
        Meet the developers behind Criminality Statistics, a team of software engineers
        committed to innovation and technical excellence.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-section">
    <h2 class="section-title">ABOUT_US</h2>
    <div class="about-text">
        We are a passionate team of Software Engineering students from <strong>Jala University</strong>, currently immersed in the world of <em>Commercial Software Engineering</em>.
        Our academic training is preparing us as well-rounded professionals, skilled not only in programming and design principles, but also in real-world practices like <strong>Quality Assurance (QA)</strong>, <strong>networking fundamentals</strong> and <strong>software lifecycle methodologies</strong>.
        <br><br>
        Through our projects, we have worked with modern technologies like <strong>Python, React, FastAPI, PostgreSQL, Streamlit, Git</strong>, and explored tools like <strong>Docker</strong>, <strong>Jira</strong> and <strong>Figma</strong>.
        We are also gaining hands-on experience in collaborative development, CI/CD practices and agile methodologies, all under the mentorship of industry professionals and Jala instructors.
        <br><br>
        Our goal is not just to write code, but to create meaningful solutions that solve real problems. This team reflects creativity, discipline and a shared vision of growing as future leaders in the tech ecosystem.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h2 class="section-title" style="text-align: center; margin-bottom: 2rem;">TEAM_MEMBERS</h2>', unsafe_allow_html=True)

team_container = st.container()

with team_container:
    cols = st.columns([1, 2, 2, 1])  
    
    with cols[1]:
        for member in team[:2]:  
            image_path = os.path.join("assets", "team", member["image"])
            img = load_image(image_path)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="team-card">
                <img class="profile-pic" src="data:image/jpeg;base64,{img_str}" alt="{member['name']}">
                <div class="member-name">{member['name']}</div>
                <div class="member-role">{member['role']}</div>
                <div class="member-bio">{member['bio']}</div>
                <div class="social-links">
                    <a href="{member['github']}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    <a href="{member['linkedin']}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="{member['whatsapp']}" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    <a href="mailto:{member['gmail']}" target="_blank" title="Email"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with cols[2]:
        for member in team[2:]:  
            image_path = os.path.join("assets", "team", member["image"])
            img = load_image(image_path)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="team-card">
                <img class="profile-pic" src="data:image/jpeg;base64,{img_str}" alt="{member['name']}">
                <div class="member-name">{member['name']}</div>
                <div class="member-role">{member['role']}</div>
                <div class="member-bio">{member['bio']}</div>
                <div class="social-links">
                    <a href="{member['github']}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    <a href="{member['linkedin']}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="{member['whatsapp']}" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    <a href="mailto:{member['gmail']}" target="_blank" title="Email"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class="stats-section">
    <h2 class="section-title">TEAM_STATS</h2>
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-value">4+</div>
            <div class="stat-label">YEARS OF EXPERIENCE</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">12+</div>
            <div class="stat-label">COMPLETED PROJECTS</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">8+</div>
            <div class="stat-label">MASTERED TECHNOLOGIES</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">100%</div>
            <div class="stat-label">COMMITMENT</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-section">
    <h2 class="section-title">TECH_STACK</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 2rem;">
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">Python</span>
                <span style="color: var(--orange);">95%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 95%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">Machine Learning</span>
                <span style="color: var(--orange);">90%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 90%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">Streamlit</span>
                <span style="color: var(--orange);">85%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 85%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">FastAPI</span>
                <span style="color: var(--orange);">80%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 80%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">React</span>
                <span style="color: var(--orange);">75%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 75%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary);">PostgreSQL</span>
                <span style="color: var(--orange);">85%</span>
            </div>
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: 85%; height: 100%; background: linear-gradient(90deg, var(--crimson) 0%, var(--orange) 100%);"></div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-logo">Criminality Statistics</div>
    <div class="footer-text">Advanced Crime Analysis System | San Francisco</div>
    <div class="footer-copyright">Powered by Los matemonda | © 2025</div>
</div>
""", unsafe_allow_html=True)