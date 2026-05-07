import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Nomad Whisper", page_icon="🌍")

# --- ESTILO COQUETTE & MODERN ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFF;
    }
    h1 {
        color: #FF85A1 !important;
        font-family: 'Georgia', serif;
        text-align: center;
        font-size: 42px !important;
    }
    .stText {
        color: #8E8E93;
        text-align: center;
    }
    /* Estilo para el botón de Bokeh a través del contenedor de Streamlit */
    .stBokehEvents {
        display: flex;
        justify-content: center;
    }
    .stButton>button {
        background-color: #FFD1DC !important;
        border-radius: 20px !important;
        color: #7A4A58 !important;
        border: 2px solid #FF85A1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Nomad Whisper ✨")
st.markdown("<p style='text-align: center; color: #D4778B;'>Trabaja desde cualquier rincón del mundo. Tu voz no tiene fronteras. 🕊️🐚</p>", unsafe_allow_html=True)

# Imagen con estilo
try:
    image = Image.open('descarga (12).jpg')
    st.image(image, width=350)
except:
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=400", width=400)

with st.sidebar:
    st.markdown("<h2 style='color: #FF85A1;'>✨ Concierge de Idiomas</h2>", unsafe_allow_html=True)
    st.write("Presiona el botón rosa, espera la señal y habla con confianza. ¡Yo me encargo del resto! 🎀")
    st.image("https://cdn-icons-png.flaticon.com/512/2014/2014751.png", width=100)

st.write("---")
st.markdown("### 🎙️ Toca para empezar a hablar")

# Configuración del botón de voz (Bokeh)
stt_button = Button(label="Escuchar Vibe 🎤", width=300, height=60, button_type="danger") # Rediseñado para Bokeh

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=100,
    debounce_time=0)

# Lógica después de escuchar
if result:
    if "GET_TEXT" in result:
        detected_text = result.get("GET_TEXT")
        st.markdown(f"""
            <div style='background-color: white; padding: 15px; border-radius: 15px; border-left: 5px solid #FF85A1;'>
                <b>Lo que escuché:</b><br>{detected_text}
            </div>
            """, unsafe_allow_html=True)
        
        if not os.path.exists("temp"):
            os.mkdir("temp")
            
        st.markdown("### 🪄 Configura tu Traducción")
        
        col1, col2 = st.columns(2)
        translator = Translator()
        
        with col1:
            in_lang = st.selectbox(
                "Entrada 📥",
                ("Español", "Inglés", "Bengali", "Coreano", "Mandarín", "Japonés"),
            )
        
        with col2:
            out_lang = st.selectbox(
                "Salida 📤",
                ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
            )

        lang_map = {
            "Inglés": "en", "Español": "es", "Bengali": "bn", 
            "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"
        }

        accent_options = {
            "Defecto": "com", "Español": "com.mx", "UK": "co.uk", 
            "USA": "com", "Canadá": "ca", "Australia": "com.au"
        }
        
        english_accent = st.selectbox("🐚 Selecciona el acento del audio", list(accent_options.keys()))

        def text_to_speech(input_language, output_language, text, tld):
            translation = translator.translate(text, src=input_language, dest=output_language)
            trans_text = translation.text
            tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
            my_file_name = "".join(x for x in text[0:10] if x.isalnum()) or "audio_vibe"
            tts.save(f"temp/{my_file_name}.mp3")
            return my_file_name, trans_text

        display_output = st.checkbox("Mostrar texto traducido ✨", value=True)

        if st.button("🪄 Convertir Vibe"):
            with st.spinner("Traduciendo tus sueños..."):
                res_name, out_txt = text_to_speech(
                    lang_map[in_lang], 
                    lang_map[out_lang], 
                    detected_text, 
                    accent_options[english_accent]
                )
                
                st.success("¡Traducción lista! 🥂")
                audio_file = open(f"temp/{res_name}.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")
                
                if display_output:
                    st.markdown(f"**Resultado:** `{out_txt}`")
                st.balloons()

# Limpieza de archivos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    for f in mp3_files:
        if os.stat(f).st_mtime < now - (n * 86400):
            os.remove(f)

remove_files(7)

st.markdown("---")
st.caption("Creado para Nómadas Digitales con ✨ y mucho estilo.")


        
    



        
    


