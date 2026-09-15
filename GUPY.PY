import requests
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="GUPY DETECTOR",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. CONFIGURAÇÕES & WEBHOOK
# ==========================================
# Substitua pela URL gerada no gatilho "When an HTTP request is received" do Power Automate
WEBHOOK_URL = ""

# ==========================================
# 3. ESTILIZAÇÃO CSS (DARK MODE)
# ==========================================
st.markdown(
    """
    <style>
    /* Fundo da página com degradê escuro (navy/slate) + glow sutil */
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

    /* Cabeçalho / hero */
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

    /* Chips de destaque (Diário, Sem spam, 60 dias) */
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

    /* Container do Formulário estilo Glassmorphism escuro */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.045);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 32px 30px;
        box-shadow: 0 8px 40px 0 rgba(0, 0, 0, 0.55);
    }

    /* Rótulos dos campos (Labels) */
    div[data-testid="stForm"] label p {
        color: #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 15.5px !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* Estilização das caixas de entrada de texto */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.055) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 10px !important;
        color: #F9FAFB !important;
        transition: border 0.2s ease;
        min-height: 48px !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border: 1px solid #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18) !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] div {
        color: #F9FAFB !important;
        font-size: 16px !important;
    }

    ::placeholder {
        color: #6B7280 !important;
        opacity: 1 !important;
        font-size: 16px !important;
    }

    /* Botão de envio (Cadastre-se) — texto garantido branco em qualquer estado */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] button:visited,
    div[data-testid="stFormSubmitButton"] button *,
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button span,
    div[data-testid="stFormSubmitButton"] button div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 60%, #1E3A8A 100%) !important;
        border: none !important;
        padding: 15px !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 0.5px;
        transition: all 0.25s ease;
        margin-top: 6px;
        box-shadow: 0 4px 18px rgba(37, 99, 235, 0.35);
    }

    div[data-testid="stFormSubmitButton"] button p {
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 60%, #1E40AF 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(37, 99, 235, 0.5);
    }

    div[data-testid="stFormSubmitButton"] button:active,
    div[data-testid="stFormSubmitButton"] button:focus,
    div[data-testid="stFormSubmitButton"] button:focus:not(:active) {
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 18px rgba(37, 99, 235, 0.35) !important;
    }

    /* Nota explicativa fixa (não recolhível) */
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
        font-size: 18px;
    }
    .info-card p, .info-card li {
        font-size: 15.5px;
        line-height: 1.6;
        color: #B9C0CC;
    }

    /* Mensagens de erro/sucesso do formulário */
    div[data-testid="stAlert"] p {
        font-size: 15.5px !important;
    }
    .info-card hr {
        border-color: rgba(255,255,255,0.08);
        margin: 14px 0;
    }

    /* Divider decorativo */
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

# ==========================================
# 4. CABEÇALHO / HERO
# ==========================================
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

# ==========================================
# 5. CARD DO FORMULÁRIO DE CADASTRO
# ==========================================
with st.form("form_gupy_detector", clear_on_submit=True):
    email = st.text_input("Email", placeholder="username@gmail.com")
    cargo = st.text_input("Vaga", placeholder="Engenheiro de Software")

    col1, col2 = st.columns(2)
    with col1:
        modelo = st.selectbox(
            "Modelo (Opcional)",
            ["", "remoto", "presencial", "hibrido"],
            format_func=lambda x: "presencial, remoto, hibrido" if x == "" else x,
        )
    with col2:
        cidade = st.text_input("Cidade (Opcional)", placeholder="São Paulo")

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
                    st.error(
                        "Erro ao enviar cadastro. Verifique a URL do Webhook."
                    )
            except Exception:
                st.error("Falha ao conectar com o serviço de cadastro.")

# ==========================================
# 6. NOTA EXPLICATIVA & DICAS (FIXA, SEMPRE VISÍVEL)
# ==========================================
st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-card">
        <h4>ℹ️ Como funciona o Gupy Detector</h4>
        <p>Cadastre seu e-mail e preferências para receber diariamente (às 8h) um resumo consolidado
        com novas vagas publicadas nos últimos 60 dias. Sem e-mails repetidos e sem spam!</p>
        <hr>
        <h4>📌 Dicas para um bom cadastro</h4>
        <ul>
            <li><b>Vaga (Cargo):</b> digite termos genéricos ou específicos utilizados pelas empresas
            <i>(ex: Analista de Dados, Desenvolvedor Python, Gerente de Projetos)</i>.</li>
            <li><b>Cidade / Modelo:</b> deixe o campo de cidade em branco caso seu foco seja exclusivamente
            <b>Remoto</b> ou se quiser buscar vagas em todo o Brasil.</li>
            <li><b>E-mail:</b> certifique-se de cadastrar um e-mail válido que você consulte diariamente
            <i>(confira também a caixa de Spam/Lixo Eletrônico no primeiro envio)</i>.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)