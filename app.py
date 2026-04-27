import streamlit as st
import os
import shutil
from email_utils import send_email_with_attachments

# Configuración de la página
st.set_page_config(page_title="Bingo Sexy", layout="centered")

# --- CSS MEJORADO PARA RESPONSIVE Y ESTILO DE LA IMAGEN ---
st.markdown(f"""
    <style>
    /* Fondo BLANCO de la app */
    .stApp {{
        background-color: #FFFFFF !important;
        color: #4B4059 !important;
    }}
    
    /* Título */
    .title-box {{
        text-align: center;
        margin-bottom: 20px;
    }}
    .title-box h1 {{
        color: #4B4059;
        font-size: 2.5rem;
    }}

    /* Contenedor de la tarjeta (estilo post-it rosa) */
    .bingo-card {{
        background-color: #E6B0E0 !important; /* Rosa de la imagen */
        border-radius: 20px !important;       /* Bordes redondeados */
        padding: 20px !important;
        margin-bottom: 15px !important;
        min-height: 220px !important;        /* Forzar mismo tamaño */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        color: #4B4059 !important;           /* Texto oscuro */
        font-weight: bold !important;
        border: 4px solid #D49ACD !important;
        position: relative;
    }}

    /* Icono del diablito arriba */
    .emoji-header {{
        font-size: 30px;
        margin-bottom: 10px;
    }}

    /* Botones de Streamlit dentro de las tarjetas */
    div.stButton > button {{
        width: 100% !important;
        background-color: rgba(255,255,255,0.3) !important;
        border: 2px solid #4B4059 !important;
        color: #4B4059 !important;
        border-radius: 10px !important;
    }}
    
    /* Forzar que en móviles las columnas se apilen (Responsive) */
    @media (max-width: 640px) {{
        [data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE CONTENIDO ---
RETOS = [
    "Estar sin calzones en Público", 
    "Flashear una bubi o puchi", 
    "Que alguien te manosee",
    "Estar encuerada o en calzones en el coche", 
    "Sexo o chupada en el coche", 
    "Terminar desnuda en una fiesta",
    "Ida al hotel", 
    "Un trío", 
    "Que alguien se venga en tu boca o bubis"
]

TEMP_DIR = "temp_uploads"
if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)

if 'board' not in st.session_state:
    st.session_state.board = [{"id": i, "challenge": RETOS[i], "completed": False, "file_path": None} for i in range(9)]
if 'lines_notified' not in st.session_state: st.session_state.lines_notified = set()

def check_bingo():
    b = st.session_state.board
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for i, line in enumerate(lines):
        if i not in st.session_state.lines_notified and all(b[x]["completed"] for x in line):
            st.session_state.lines_notified.add(i)
            st.balloons()
            files = [b[x]["file_path"] for x in line if b[x]["file_path"]]
            send_email_with_attachments("jimvillarene@gmail.com", f"¡BINGO! Línea {i+1} completada", "Se ha completado una línea.", files)

# --- UI ---
st.markdown("<div class='title-box'><h1>😈 BINGO DE RETOS 😈</h1></div>", unsafe_allow_html=True)

# Bloque de instrucciones
st.markdown("""
    <div style='background-color: #fce4ec; padding: 15px; border-radius: 10px; border-left: 5px solid #E6B0E0; margin-bottom: 25px;'>
        <p style='margin: 0; color: #4B4059; font-size: 0.95rem;'>
            <strong>¿Cómo jugar?</strong><br>
            ¿Así que saliste de fiesta solita? Pues aún puedes hacer muy feliz a tu marido, cumple los retos de abajo y sube una foto que demuestre que lo hiciste. Si haces una línea te toca un regalo, si llenas todas !Puedes pedir lo que quieras! 😈
        </p>
    </div>
""", unsafe_allow_html=True)
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        card = st.session_state.board[idx]
        
        with cols[col]:
            check_mark = "✅" if card["completed"] else "😈"
            
            st.markdown(f"""
                <div class="bingo-card">
                    <div class="emoji-header">{check_mark}</div>
                    {card['challenge']}
                </div>
            """, unsafe_allow_html=True)
            
            if not card["completed"]:
                up = st.file_uploader("Sube evidencia", key=f"up{idx}", label_visibility="collapsed")
                if up:
                    path = os.path.join(TEMP_DIR, f"ev_{idx}_{up.name}")
                    with open(path, "wb") as f: f.write(up.getbuffer())
                    
                    st.session_state.board[idx]["completed"] = True
                    st.session_state.board[idx]["file_path"] = path
                    
                    # Envío inmediato
                    send_email_with_attachments("jimvillarene@gmail.com", f"Evidencia: {card['challenge']}", "Nueva evidencia recibida.", [path])
                    
                    # Verificar Bingo
                    check_bingo()
                    
                    # Limpieza (borrar después de enviar)
                    if os.path.exists(path): os.remove(path)
                    st.rerun()
            else:
                st.success("¡Completado!")

st.divider()

# Botón de reinicio centrado
if st.button("🗑️ Reiniciar Todo"):
    st.session_state.board = [{"id": i, "challenge": RETOS[i], "completed": False, "file_path": None} for i in range(9)]
    st.session_state.lines_notified = set()
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
    st.rerun()
