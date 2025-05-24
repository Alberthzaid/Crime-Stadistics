import streamlit as st

st.set_page_config(page_title="Team", page_icon="./assets/Logo-removebg.png")


st.title("👨‍💻 Conoce nuestro equipo de desarrollo")


st.markdown(
    """
    <style>
        @keyframes scroll {
            0% { transform: translateY(100%); }
            100% { transform: translateY(-100%); }
        }

        .credit-container {
            height: 400px; 
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: transparent;
            color: white;
            font-size: 24px;
            font-weight: bold;
            position: relative;
        }

        .credit-text {
            display: block;
            position: absolute;
            animation: scroll 20s linear infinite;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="credit-container">
        <div class="credit-text">
            👨‍💻 Zaid Pantoja - administrador del modelo <br><br>
            🖥️ Miguel - implementacion de charts <br><br>
            📊 Angel Ortega - despliegue del proyecto y mapa <br><br>
            📜 Andres Aviles - diagrama ploting  <br><br><br><br><br>
            ⚡ Derechos reservados - Los Matemonda 2025
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
