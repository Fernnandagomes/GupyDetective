import requests
import streamlit as st
import os 

st.set_page_config(
    page_title="GUPY DETECTOR",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 19px !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(37, 99, 235, 0.18), transparent 40%),
            radial-gradient(circle at 85% 90%, rgba(37, 99, 235, 0.12), transparent 45%),
            linear-gradient(135deg, #050810 0%, #0B1120 50%, #111827 100%);
        color: #E5E7EB;
        font-size: 19px;
    }

    .hero-wrap {
        text-align: center;
        margin-bottom: 22px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.35);
        color: #93C5FD;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 14px;
        text-transform: uppercase;
    }
    .title-text {
        text-align: center;
        color: #F9FAFB;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        font-size: 40px;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
        text-shadow: 0px 2px 10px rgba(37, 99, 235, 0.35);
    }
    .subtitle-text {
        text-align: center;
        color: #9CA3AF;
        font-size: 19px;
        font-weight: 400;
        margin-bottom: 4px;
    }

    .chip-row {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin: 18px 0 26px 0;
    }
    .chip {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #D1D5DB;
        font-size: 16px;
        padding: 8px 16px;
        border-radius: 10px;
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.045);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 32px 30px;
        box-shadow: 0 8px 40px 0 rgba(0, 0, 0, 0.55);
    }

    div[data-testid="stForm"] label p {
        color: #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* Borda e fundo das caixas de texto e seleções */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #1F2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        min-height: 50px !important;
    }

    /* Cor do cursor (piscante) e do texto digitado */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #FFFFFF !important;
        font-size: 18px !important;
    }

    /* Cor do texto do Selectbox e da Seta */
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Opções do Menu Dropdown */
    ul[role="listbox"],
    div[data-baseweb="menu"] {
        background-color: #1F2937 !important;
    }

    li[role="option"],
    div[role="option"] {
        color: #FFFFFF !important;
        background-color: #1F2937 !important;
    }

    li[role="option"]:hover,
    div[role="option"]:hover {
        background-color: #374151 !important;
    }

    /* Preenchimento automático do navegador */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
        -webkit-text-fill-color: #FFFFFF !important;
        -webkit-box-shadow: 0 0 0px 1000px #1F2937 inset !important;
        caret-color: #FFFFFF !important;
    }

    /* Botão de Envio */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 60%, #1E3A8A 100%) !important;
        border: none !important;
        padding: 16px !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        letter-spacing: 0.5px;
        margin-top: 6px;
        box-shadow: 0 4px 18px rgba(37, 99, 235, 0.35);
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 60%, #1E40AF 100%) !important;
        transform: translateY(-2px);
    }

    .info-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-left: 3px solid #3B82F6;
        border-radius: 14px;
        padding: 22px 24px;
        margin-top: 26px;
        color: #D1D5DB;
    }
    .info-card h4 {
        color: #F9FAFB;
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 21px;
    }
    .info-card p, .info-card li {
        font-size: 17.5px;
        line-height: 1.6;
        color: #B9C0CC;
    }

    .divider-glow {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.5), transparent);
        margin: 30px 0 6px 0;
    }

    footer, #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-wrap">
        <span class="hero-badge">🔍 Monitoramento automático de vagas</span>
        <div class="title-text">GUPY DETECTOR</div>
        <div class="subtitle-text">Cadastre-se e receba as vagas certas, direto na sua caixa de entrada.</div>
    </div>
    <div class="chip-row">
        <span class="chip">🕗 Resumo diário às 8h</span>
        <span class="chip">📅 Vagas dos últimos 60 dias</span>
        <span class="chip">🚫 Sem duplicados e sem spam</span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("form_gupy_detector", clear_on_submit=True):
    email = st.text_input("Email")
    cargo = st.text_input("Vaga")

    col1, col2 = st.columns(2)
    with col1:
        modelo_opcao = st.selectbox(
            "Modelo (Opcional)",
            ["Selecione...", "remoto", "presencial", "hibrido"],
            index=0,
        )
        modelo = "" if modelo_opcao == "Selecione..." else modelo_opcao

    with col2:
        cidade = st.text_input("Cidade (Opcional)")

    submitted = st.form_submit_button("Cadastre-se 🚀")

    if submitted:
        if not email or not cargo:
            st.error("Por favor, preencha pelo menos o Email e a Vaga.")
        else:
            payload = {
                "Email": email.strip(),
                "Cargo": cargo.strip(),
                "Modelo": modelo,
                "Cidade": cidade.strip(),
            }

            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                if response.status_code in [200, 202]:
                    st.success("Cadastro realizado com sucesso!")
                else:
                    st.error("Erro ao enviar cadastro. Verifique a URL do Webhook.")
            except Exception:
                st.error("Falha ao conectar com o serviço de cadastro.")

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-card">
        <h4>ℹ️ Como funciona o Gupy Detector</h4>
        <p>Cadastre seu e-mail e preferências para receber diariamente (às 8h) um resumo consolidado
        com novas vagas publicadas nos últimos 60 dias. Sem e-mails repetidos e sem spam!</p>
        <hr style="border-color: rgba(255,255,255,0.08); margin: 14px 0;">
        <h4>📌 Dicas para um bom cadastro</h4>
        <ul>
            <li><b>Vaga (Cargo):</b> digite termos genéricos ou específicos utilizados pelas empresas.</li>
            <li><b>Cidade / Modelo:</b> deixe o campo em branco caso seu foco seja exclusivamente
            <b>Remoto</b> ou se quiser buscar vagas em todo o Brasil.</li>
            <li><b>E-mail:</b> certifique-se de cadastrar um e-mail válido que você consulte diariamente.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)