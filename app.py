import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
from sympy import symbols, simplify, sympify, Eq
from gtts import gTTS
import io
import base64

# ============================================================
# CONFIGURACIÓN Y ESTILOS (VIBE CODING)
# ============================================================
st.set_page_config(
    page_title="🧑‍🏫 Profe Sofía - Factorización",
    page_icon="🧑‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #6a1b9a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .profe-card {
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #8e24aa;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .formula-box {
        background-color: #e8eaf6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Courier New', Courier, monospace;
        color: #283593;
        margin: 1rem 0;
        border: 2px dashed #5c6bc0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #c62828;
        margin: 1rem 0;
    }
    .hint-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ef6c00;
        margin: 1rem 0;
    }
    .stButton>button {
        font-size: 1.1rem;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def speak_text(text, lang="es"):
    """Genera y reproduce audio con la voz de la Profe Sofía."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        return None

def play_audio_html(audio_bytes, format_type="audio/mp3"):
    """Reproductor HTML5 para autoplay."""
    if not audio_bytes:
        return
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio controls autoplay style="width: 100%; max-width: 400px;">
        <source src="data:{format_type};base64,{audio_base64}" type="{format_type}">
    </audio>
    """
    components.html(audio_html, height=80)

def validate_algebra(student_input, expected_expr_str):
    """
    Valida si la respuesta del estudiante es matemáticamente equivalente.
    Usa sympy para evitar errores de formato de texto.
    """
    x, y, a, b = symbols('x y a b')
    
    try:
        # Convertir strings a expresiones simbólicas
        student_expr = sympify(student_input.replace('^', '**'))
        expected_expr = sympify(expected_expr_str.replace('^', '**'))
        
        # Simplificar la diferencia. Si es 0, son equivalentes.
        difference = simplify(student_expr - expected_expr)
        
        return difference == 0
    except Exception:
        return False

# ============================================================
# BASE DE DATOS DE LA PROFE SOFÍA (Nivel Básico)
# ============================================================
# Aquí estructuramos el conocimiento. En la Fase 2 agregaremos los 12 casos.
CASOS_FACTORIZACION = {
    "1. Factor Común Monomio": {
        "nivel": "🟢 Básico",
        "analogía": "Imagina que tienes 6 manzanas y 9 naranjas. ¿Qué tienen en común? Que ambas cantidades son divisibles por 3. En álgebra hacemos exactamente lo mismo: buscamos el número o letra que 'todos comparten' y lo sacamos afuera como un líder de grupo.",
        "formula": "ab + ac = a(b + c)",
        "ejemplo_paso_a_paso": "Ejemplo: 6x² + 9x\n1. ¿Qué número divide a 6 y a 9? El 3.\n2. ¿Qué letra se repite? La x (tomamos la de menor exponente: x).\n3. El factor común es 3x.\n4. Dividimos: 6x²/3x = 2x, y 9x/3x = 3.\n5. Resultado: 3x(2x + 3)",
        "ejercicio": "Factoriza: 4x³ + 8x²",
        "respuesta_correcta": "4*x**2*(x + 2)", # Formatos aceptados por sympy
        "pistas": [
            "Pista 1: ¿Cuál es el máximo común divisor de 4 y 8?",
            "Pista 2: ¿Cuál es la variable con el menor exponente?",
            "Pista 3: El factor común es 4x². ¿Qué queda al dividir?"
        ]
    },
    "2. Factor Común Polinomio": {
        "nivel": "🟢 Básico",
        "analogía": "A veces, el 'paquete completo' se repite. Es como si en dos familias diferentes, el apellido 'Pérez' se repitiera. En lugar de separar a las personas, sacamos el apellido 'Pérez' como un bloque entero.",
        "formula": "x(a + b) + y(a + b) = (a + b)(x + y)",
        "ejemplo_paso_a_paso": "Ejemplo: x(x+2) + 3(x+2)\n1. Observa que el bloque (x+2) se repite en ambos términos.\n2. Ese bloque es nuestro factor común.\n3. Lo sacamos afuera: (x+2).\n4. Lo que sobra de cada término lo metemos en otro paréntesis: (x+3).\n5. Resultado: (x+2)(x+3)",
        "ejercicio": "Factoriza: a(x-1) + b(x-1)",
        "respuesta_correcta": "(x - 1)*(a + b)",
        "pistas": [
            "Pista 1: Busca el paréntesis que se repite exactamente igual.",
            "Pista 2: Ese paréntesis repetido es tu primer factor.",
            "Pista 3: El segundo factor se forma con lo que quedó afuera: a y b."
        ]
    },
    "3. Factorización por Agrupación": {
        "nivel": "🟢 Básico",
        "analogía": "Imagina que estás en una fiesta y no conoces a nadie. Lo que haces es agruparte con 3 personas para jugar un juego, y otras 4 para jugar otro. En álgebra, cuando hay 4 o más términos, los 'agrupamos' en parejas para encontrar factores comunes por separado.",
        "formula": "ax + ay + bx + by = a(x+y) + b(x+y) = (x+y)(a+b)",
        "ejemplo_paso_a_paso": "Ejemplo: x² + 2x + 3x + 6\n1. Agrupamos los dos primeros y los dos últimos: (x² + 2x) + (3x + 6).\n2. Sacamos factor común en el primer grupo: x(x+2).\n3. Sacamos factor común en el segundo grupo: 3(x+2).\n4. Ahora tenemos: x(x+2) + 3(x+2). ¡Cayó en el Caso 2!\n5. Resultado: (x+2)(x+3)",
        "ejercicio": "Factoriza: x² + 3x + 2x + 6",
        "respuesta_correcta": "(x + 3)*(x + 2)",
        "pistas": [
            "Pista 1: Agrupa así: (x² + 3x) y (2x + 6).",
            "Pista 2: Saca factor común de cada grupo: x(...) + 2(...).",
            "Pista 3: Debería quedarte un paréntesis repetido al final."
        ]
    }
}

# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================
st.markdown('<p class="main-header">‍🏫 Profe Sofía: Asistente de Factorización</p>', unsafe_allow_html=True)
st.markdown("### *Aprende álgebra con paciencia, analogías y práctica interactiva.*")

# Inicializar Session State
if "current_case" not in st.session_state:
    st.session_state.current_case = list(CASOS_FACTORIZACION.keys())[0]
if "hint_level" not in st.session_state:
    st.session_state.hint_level = 0
if "solved" not in st.session_state:
    st.session_state.solved = False

# --- SIDEBAR: Selector de Casos ---
with st.sidebar:
    st.header("📚 Temario")
    st.markdown("#### 🟢 Nivel Básico")
    selected_case = st.radio(
        "Selecciona un caso:",
        list(CASOS_FACTORIZACION.keys()),
        label_visibility="collapsed",
        index=list(CASOS_FACTORIZACION.keys()).index(st.session_state.current_case)
    )

    if selected_case != st.session_state.current_case:
        st.session_state.current_case = selected_case
        st.session_state.hint_level = 0
        st.session_state.solved = False
        st.rerun()

    st.markdown("---")
    st.info("💡 **Consejo de Sofía:** Escucha la explicación antes de intentar el ejercicio. ¡La matemática entra por los oídos!")

# --- CONTENIDO PRINCIPAL ---
case_data = CASOS_FACTORIZACION[st.session_state.current_case]

tab1, tab2 = st.tabs(["📖 1. Aprende con Sofía", "✍️ 2. Practica y Resuelve"])

# === TAB 1: APRENDE ===
with tab1:
    st.subheader(f"📘 {st.session_state.current_case}")
    st.caption(f"Nivel: {case_data['nivel']}")

    # Analogía
    st.markdown("###  La Analogía de Sofía")
    st.markdown(f"""
    <div class='profe-card'>
        👩‍🏫 <strong>Profe Sofía dice:</strong><br><br>
        {case_data['analogía']}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        pass # Espacio
    with col2:
        if st.button("🔊 Escuchar explicación", key="btn_speak_analogy"):
            audio = speak_text(f"Hola, soy la Profe Sofía. {case_data['analogía']}")
            if audio:
                play_audio_html(audio)

    # Fórmula
    st.markdown("### 📐 La Fórmula Mágica")
    st.markdown(f"""
    <div class='formula-box'>
        {case_data['formula']}
    </div>
    """, unsafe_allow_html=True)

    # Ejemplo
    st.markdown("###  Ejemplo Resuelto Paso a Paso")
    st.info(case_data['ejemplo_paso_a_paso'])
    
    if st.button(" Escuchar el ejemplo", key="btn_speak_example"):
        audio = speak_text(case_data['ejemplo_paso_a_paso'].replace('\n', '. '))
        if audio:
            play_audio_html(audio)

# === TAB 2: PRACTICA ===
with tab2:
    st.subheader(f"✍️ ¡Tu turno! Resuelve este ejercicio")
    st.markdown(f"### 🎯 {case_data['ejercicio']}")

    student_answer = st.text_input(
        "Escribe tu respuesta aquí (usa * para multiplicar y ^ para potencias):",
        placeholder="Ej: 3*x*(x + 2)",
        key="student_input"
    )

    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_btn = st.button("✅ Verificar Respuesta", type="primary", use_container_width=True)
    with col2:
        hint_btn = st.button("💡 Dame una Pista", use_container_width=True)
    with col3:
        reset_btn = st.button("🔄 Reiniciar Ejercicio", use_container_width=True)

    if reset_btn:
        st.session_state.hint_level = 0
        st.session_state.solved = False
        st.rerun()

    # Lógica de Verificación
    if check_btn and student_answer:
        is_correct = validate_algebra(student_answer, case_data['respuesta_correcta'])
        
        if is_correct:
            st.session_state.solved = True
            st.markdown("""
            <div class='success-box'>
                🎉 <strong>¡Excelente trabajo!</strong> La Profe Sofía está muy orgullosa de ti. 
                Has dominado este concepto. ¡Vamos por el siguiente caso!
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class='error-box'>
                🤔 <strong>Casi, pero no del todo.</strong> Revisa tus signos o tu factor común. 
                ¡No te rindas! Pide una pista si lo necesitas.
            </div>
            """, unsafe_allow_html=True)

    # Lógica de Pistas
    if hint_btn:
        if st.session_state.hint_level < len(case_data['pistas']):
            st.markdown(f"""
            <div class='hint-box'>
                 <strong>Pista {st.session_state.hint_level + 1}:</strong> {case_data['pistas'][st.session_state.hint_level]}
            </div>
            """, unsafe_allow_html=True)
            st.session_state.hint_level += 1
        else:
            st.warning("Ya te di todas las pistas. ¡Tú puedes resolverlo solo/a!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a1b9a;'>
    <small>🧑‍ Profe Sofía | Diseño por Vibe Coding - Ing. Hernán Quiroz | Octubre 2026</small>
</div>
""", unsafe_allow_html=True)
