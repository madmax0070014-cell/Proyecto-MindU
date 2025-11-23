import streamlit as st
import time
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="MindU", page_icon="🧘", layout="centered")

# --- 2. CONFIGURACIÓN DE LA IA (GEMINI) ---
API_KEY = "AIzaSyCgv2NUFdXsCUc7sXOpIoe--YoZT98UAYw" 

try:
    genai.configure(api_key=API_KEY)
    # Usamos el modelo que apareció en tu lista scanner
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error configurando la IA: {e}")

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        color: white;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MENÚ LATERAL ---
menu = st.sidebar.radio("Navegación", ["Inicio 🏠", "Botón SOS 🆘", "Chat con IA 🤖", "Diario 📔"])

# --- SECCIÓN: INICIO ---
if menu == "Inicio 🏠":
    st.title("Bienvenido a MindU 🌿")
    st.image("https://img.freepik.com/free-vector/organic-flat-people-meditating-illustration_23-2148906556.jpg", caption="Tu paz mental importa.")
    st.info("👋 Hola. Esta app usa Inteligencia Artificial real para escucharte.")
    col1, col2 = st.columns(2)
    col1.metric("Días en calma", "5 días", "1 día")
    col2.metric("Nivel de estrés", "Medio", "5%")

# --- SECCIÓN: BOTÓN DE PÁNICO ---
elif menu == "Botón SOS 🆘":
    st.title("Zona de Calma")
    st.write("Presiona si sientes ansiedad inmediata.")
    if st.button("🚨 ACTIVAR PÁNICO 🚨"):
        st.warning("Iniciando respiración guiada...")
        my_bar = st.progress(0, text="Inhala...")
        for percent_complete in range(100):
            time.sleep(0.1)
            if percent_complete < 40: my_bar.progress(percent_complete+1, text="Inhala... 🌬️")
            elif percent_complete < 60: my_bar.progress(percent_complete+1, text="Sostén... 😶")
            else: my_bar.progress(percent_complete+1, text="Exhala... 😮‍💨")
        st.balloons()
        st.success("Muy bien. Escucha esto:")
        st.audio("interstellar.mp3", format="audio/mp3", start_time=0) 

# --- SECCIÓN: CHAT CON IA REAL ---
elif menu == "Chat con IA 🤖":
    st.title("Compañero Virtual (IA)")
    st.write("Soy una IA entrenada para apoyo estudiantil. Pregúntame lo que sea.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe aquí (ej: Estoy un poco estresado por la universidad)..."):
        # Mostrar usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- LÓGICA DE IA REAL ---
        try:
            with st.spinner("Pensando una respuesta empática..."):
                # Configuración de personalidad
                personalidad = "Eres un consejero estudiantil empático llamado MindU. Responde de forma breve (máximo 3 frases), cálida y da consejos prácticos para universitarios."
                
                prompt_completo = f"{personalidad}\n\nEstudiante dice: {prompt}"
                
                response = model.generate_content(prompt_completo)
                respuesta_ia = response.text
                
            # Mostrar IA
            with st.chat_message("assistant"):
                st.markdown(respuesta_ia)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
            
        except Exception as e:
            # Si falla, muestra el error exacto
            st.error(f"⚠️ Error: {e}")

# --- SECCIÓN: DIARIO ---
elif menu == "Diario 📔":
    st.title("Diario de Emociones")
    animo = st.slider("Estado de ánimo (1-10)", 1, 10, 5)
    st.text_area("Desahógate aquí...")
    if st.button("Guardar"):
        st.success("Guardado. Mañana será un mejor día.")