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
        margin-bottom: 5px !important;
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

    /* Texto pequeño en gris más oscuro debajo de los retos */
    .sub-text {{
        color: #606060;
        font-size: 0.75rem;
        font-weight: normal;
        margin-top: 8px;
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

AYUDAS = [
    "Tómate una foto en el espejo del baño, o una foto debajo de la mesa para que se vea que no traes nada 😈",
    "Puede ser que él te tome la foto o te tomas una foto tú y yo te creo que él te vio  📸",
    "Que se vea que estás desnuda o que sus manos estén debajo de tu ropa ! 🖐️",
    "Puede ser selfie o que te la tomé el conductor en un alto 🚗",
    "¡Puede ser selfie o que él te grabe, si es en la parte de atrás del coche mejor! 🔥",
    "Puedes ir al espejo del baño o un espejo en la casa donde se vea que estás desnudita! 🎉",
    "Todas las que puedas, en la cama, frente al espejo, en el jacuzzi o bailando en el tubo 🏨",
    "Puede ser chupando las dos pingas o que estes en cuatro, para que no se vean ellos, y si salen no me molesta 🔞",
    "En selfie y entre más espeso mejor jijiji si te escurre por los labios aún más rico 💦"
]

TEMP_DIR = "temp_uploads"
if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)

if 'board' not in st.session_state:
    st.session_state.board = [
        {"id": i, "challenge": RETOS[i], "ayuda": AYUDAS[i], "completed": False, "file_path": None} 
        for i in range(9)
    ]
if 'lines_notified' not in st.session_state: st.session_state.lines_notified = set()

def check_bingo():
    b = st.session_state.board
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for i, line in enumerate(lines):
        if i not in st.session_state.lines_notified and all(b[x]["completed"] for x in line):
            st.session_state.lines_notified.add(i)
            st.balloons()
            # Notificamos el bingo (sin archivos ya que se borran al subir)
            send_email_with_attachments("jimvillarene@gmail.com", f"¡BINGO! Línea {i+1} completada", "Se ha completado una línea del bingo.", [])

# --- UI ---
st.markdown("<div class='title-box'><h1>😈 BINGO DE RETOS 😈</h1></div>", unsafe_allow_html=True)

# Bloque de instrucciones
st.markdown("""
    <div style='background-color: #fce4ec; padding: 15px; border-radius: 10px; border-left: 5px solid #E6B0E0; margin-bottom: 25px;'>
        <p style='margin: 0; color: #4B4059; font-size: 0.95rem;'>
            <strong>¿Cómo jugar?</strong><br>
            ¿Así que saliste de fiesta solita? Pues aún puedes hacer muy feliz a tu marido, cumple los retos de abajo y sube una foto que demuestre que lo hiciste. Si haces una línea te toca un regalo, si llenas todas y subes un video !Puedes pedir lo que quieras! 😈
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
                    <div class="sub-text">{card['ayuda']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Sistema para resetear el cargador de archivos después de cada subida
            if f"up_key_{idx}" not in st.session_state:
                st.session_state[f"up_key_{idx}"] = 0
            
            # Subida de múltiples archivos con clave dinámica para evitar loops
            up = st.file_uploader("Evidencia", key=f"up_{idx}_{st.session_state[f'up_key_{idx}']}", label_visibility="collapsed", accept_multiple_files=True)
            if up:
                paths = []
                for uploaded_file in up:
                    path = os.path.join(TEMP_DIR, f"ev_{idx}_{uploaded_file.name}")
                    with open(path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    paths.append(path)
                
                # Marcamos como completado
                st.session_state.board[idx]["completed"] = True
                
                # Envío inmediato de todas las fotos de este lote
                send_email_with_attachments("jimvillarene@gmail.com", f"Evidencia: {card['challenge']}", "Se han recibido nuevas evidencias.", paths)
                
                # Verificar Bingo
                check_bingo()
                
                # Limpieza inmediata de archivos físicos
                for path in paths:
                    if os.path.exists(path):
                        os.remove(path)
                
                # Incrementamos la clave para limpiar el widget de Streamlit y evitar el loop
                st.session_state[f"up_key_{idx}"] += 1
                st.rerun()
            
            if card["completed"]:
                st.success("¡Reto cumplido!")

st.divider()

# Botón de reinicio centrado
col_reset1, col_reset2, col_reset3 = st.columns([1, 1, 1])
with col_reset2:
    if st.button("🗑️ Reiniciar Todo"):
        st.session_state.board = [
            {"id": i, "challenge": RETOS[i], "ayuda": AYUDAS[i], "completed": False, "file_path": None} 
            for i in range(9)
        ]
        st.session_state.lines_notified = set()
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            os.makedirs(TEMP_DIR)
        st.rerun()

# Disclaimer al final
st.markdown("""
    <div style='margin-top: 50px; text-align: center; border-top: 1px solid #eee; padding-top: 20px;'>
        <p style='color: #A1A1A6; font-size: 0.8rem; font-style: italic;'>
            <strong>Aviso:</strong> Este juego es de uso estrictamente personal. 
            Las fotos y videos subidos se envían directamente al correo del creador 
            y no están disponibles para el público en general. 
            Al jugar, aceptas este flujo de datos.
        </p>
    </div>
""", unsafe_allow_html=True)
