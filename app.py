import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
from sympy import symbols, simplify, sympify
from gtts import gTTS
import io
import base64

# ============================================================
# CONFIGURACIÓN Y ESTILOS MODERNOS
# ============================================================
st.set_page_config(
    page_title="🧑‍ Profe Sofía - Factorización",
    page_icon="🧑‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* HERO MODERNO */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .hero-title {
        font-size: 3rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    .hero-stats {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1rem;
        position: relative;
        z-index: 1;
    }
    .stat-card {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        min-width: 120px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        display: block;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* TARJETAS DE CONTENIDO */
    .profe-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #8e24aa;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(142, 36, 170, 0.1);
    }
    .formula-box {
        background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-family: 'Courier New', Courier, monospace;
        color: #283593;
        margin: 1rem 0;
        border: 3px dashed #5c6bc0;
        box-shadow: 0 4px 15px rgba(92, 107, 192, 0.2);
    }
    .example-box {
        background: #fff3e0;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #ff9800;
        margin: 1rem 0;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    /* CAJAS DE FEEDBACK */
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #2e7d32;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
    }
    .error-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #c62828;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(198, 40, 40, 0.1);
    }
    .hint-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #ef6c00;
        margin: 1rem 0;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(239, 108, 0, 0.1);
    }
    .answer-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #1976d2;
        margin: 1rem 0;
        font-size: 1.2rem;
        text-align: center;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 15px rgba(25, 118, 210, 0.1);
    }
    
    /* BOTONES */
    .stButton>button {
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* EJERCICIO */
    .exercise-box {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.8rem;
        color: #880e4f;
        margin: 1.5rem 0;
        border: 3px solid #f06292;
        box-shadow: 0 6px 20px rgba(240, 98, 146, 0.2);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def speak_text(text, lang="es"):
    """Genera audio con la voz de la Profe Sofía."""
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
    <audio controls autoplay style="width: 100%; max-width: 400px; margin: 1rem auto;">
        <source src="data:{format_type};base64,{audio_base64}" type="{format_type}">
        Tu navegador no soporta audio.
    </audio>
    """
    components.html(audio_html, height=100)


def validate_algebra(student_input, expected_expr_str):
    """Valida si la respuesta es matemáticamente equivalente."""
    x, y, a, b = symbols('x y a b')
    
    try:
        student_expr = sympify(student_input.replace('^', '**').replace('×', '*'))
        expected_expr = sympify(expected_expr_str.replace('^', '**').replace('×', '*'))
        difference = simplify(student_expr - expected_expr)
        return difference == 0
    except Exception:
        return False


# ============================================================
# BASE DE DATOS DE LA PROFE SOFÍA
# ============================================================
CASOS_FACTORIZACION = {
    "1. Factor Común Monomio": {
        "nivel": "🟢 Básico",
        "analogía": "Imagina que tienes 6 manzanas y 9 naranjas. ¿Qué tienen en común? Que ambas cantidades son divisibles por 3. En álgebra hacemos exactamente lo mismo: buscamos el número o letra que 'todos comparten' y lo sacamos afuera como un líder de grupo.",
        "formula": "ab + ac = a(b + c)",
        "ejemplo_paso_a_paso": "Ejemplo: 6x² + 9x\n\n1. ¿Qué número divide a 6 y a 9? El 3.\n2. ¿Qué letra se repite? La x (tomamos la de menor exponente: x).\n3. El factor común es 3x.\n4. Dividimos: 6x²/3x = 2x, y 9x/3x = 3.\n5. Resultado: 3x(2x + 3)",
        "ejercicio": "Factoriza: 4x³ + 8x²",
        "respuesta_correcta": "4*x**2*(x + 2)",
        "pistas": [
            "Pista 1: ¿Cuál es el máximo común divisor de 4 y 8? Piensa en el número más grande que divide a ambos.",
            "Pista 2: ¿Cuál es la variable con el menor exponente? Recuerda que x² es menor que x³.",
            "Pista 3: El factor común es 4x². Ahora divide cada término: 4x³/4x² = x, y 8x²/4x² = 2."
        ]
    },
    "2. Factor Común Polinomio": {
        "nivel": "🟢 Básico",
        "analogía": "A veces, el 'paquete completo' se repite. Es como si en dos familias diferentes, el apellido 'Pérez' se repitiera. En lugar de separar a las personas, sacamos el apellido 'Pérez' como un bloque entero.",
        "formula": "x(a + b) + y(a + b) = (a + b)(x + y)",
        "ejemplo_paso_a_paso": "Ejemplo: x(x+2) + 3(x+2)\n\n1. Observa que el bloque (x+2) se repite en ambos términos.\n2. Ese bloque es nuestro factor común.\n3. Lo sacamos afuera: (x+2).\n4. Lo que sobra de cada término lo metemos en otro paréntesis: (x+3).\n5. Resultado: (x+2)(x+3)",
        "ejercicio": "Factoriza: a(x-1) + b(x-1)",
        "respuesta_correcta": "(x - 1)*(a + b)",
        "pistas": [
            "Pista 1: Busca el paréntesis que se repite exactamente igual en ambos términos.",
            "Pista 2: Ese paréntesis repetido (x-1) es tu primer factor. Sácalo afuera.",
            "Pista 3: El segundo factor se forma con lo que quedó afuera de cada término: a y b, entonces (a+b)."
        ]
    },
    "3. Factorización por Agrupación": {
        "nivel": "🟢 Básico",
        "analogía": "Imagina que estás en una fiesta y no conoces a nadie. Lo que haces es agruparte con 3 personas para jugar un juego, y otras 4 para jugar otro. En álgebra, cuando hay 4 o más términos, los 'agrupamos' en parejas para encontrar factores comunes por separado.",
        "formula": "ax + ay + bx + by = a(x+y) + b(x+y) = (x+y)(a+b)",
        "ejemplo_paso_a_paso": "Ejemplo: x² + 2x + 3x + 6\n\n1. Agrupamos los dos primeros y los dos últimos: (x² + 2x) + (3x + 6).\n2. Sacamos factor común en el primer grupo: x(x+2).\n3. Sacamos factor común en el segundo grupo: 3(x+2).\n4. Ahora tenemos: x(x+2) + 3(x+2). ¡Cayó en el Caso 2!\n5. Resultado: (x+2)(x+3)",
        "ejercicio": "Factoriza: x² + 3x + 2x + 6",
        "respuesta_correcta": "(x + 3)*(x + 2)",
        "pistas": [
            "Pista 1: Agrupa así: (x² + 3x) y (2x + 6). Pon paréntesis mentalmente.",
            "Pista 2: Saca factor común de cada grupo: del primero sale x, del segundo sale 2. Queda: x(x+3) + 2(x+3).",
            "Pista 3: Ahora tienes un paréntesis repetido (x+3). Sácalo afuera y queda (x+3)(x+2)."
        ]
    }
}


# ============================================================
# INICIALIZACIÓN DE SESSION STATE
# ============================================================
if "current_case" not in st.session_state:
    st.session_state.current_case = list(CASOS_FACTORIZACION.keys())[0]
if "hint_level" not in st.session_state:
    st.session_state.hint_level = 0
if "solved" not in st.session_state:
    st.session_state.solved = False
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "student_answer" not in st.session_state:
    st.session_state.student_answer = ""
if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = ""
if "feedback_type" not in st.session_state:
    st.session_state.feedback_type = ""


# ============================================================
# HERO SECTION MODERNO
# ============================================================
st.markdown("""
<div class='hero-container'>
    <h1 class='hero-title'>🧑‍🏫 Profe Sofía</h1>
    <p class='hero-subtitle'>Tu asistente personal de Factorización Algebraica</p>
    <div class='hero-stats'>
        <div class='stat-card'>
            <span class='stat-number'>3</span>
            <span class='stat-label'>Casos Disponibles</span>
        </div>
        <div class='stat-card'>
            <span class='stat-number'></span>
            <span class='stat-label'>Ejercicios Interactivos</span>
        </div>
        <div class='stat-card'>
            <span class='stat-number'>🔊</span>
            <span class='stat-label'>Audio Explicativo</span>
        </div>
        <div class='stat-card'>
            <span class='stat-number'>💡</span>
            <span class='stat-label'>Pistas Inteligentes</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR: Selector de Casos
# ============================================================
with st.sidebar:
    st.header("📚 Temario")
    st.markdown("####  Nivel Básico")
    
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
        st.session_state.show_answer = False
        st.session_state.student_answer = ""
        st.session_state.feedback_message = ""
        st.session_state.feedback_type = ""
        st.rerun()

    st.markdown("---")
    st.info("💡 **Consejo de Sofía:** Escucha la explicación antes de intentar el ejercicio. ¡La matemática entra por los oídos!")


# ============================================================
# CONTENIDO PRINCIPAL
# ============================================================
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
    st.markdown("### 🧪 Ejemplo Resuelto Paso a Paso")
    st.markdown(f"""
    <div class='example-box'>
        {case_data['ejemplo_paso_a_paso'].replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔊 Escuchar el ejemplo", key="btn_speak_example"):
        audio = speak_text(case_data['ejemplo_paso_a_paso'].replace('\n', '. '))
        if audio:
            play_audio_html(audio)

# === TAB 2: PRACTICA ===
with tab2:
    st.subheader("✍️ ¡Tu turno! Resuelve este ejercicio")
    
    # Caja del ejercicio
    st.markdown(f"""
    <div class='exercise-box'>
        🎯 {case_data['ejercicio']}
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Formato de respuesta:** Usa `*` para multiplicar y `^` para potencias. Ejemplo: `4*x^2*(x + 2)`")

    # Campo de respuesta (con valor persistente)
    student_answer = st.text_input(
        "Escribe tu respuesta aquí:",
        value=st.session_state.student_answer,
        placeholder="Ej: 4*x^2*(x + 2)",
        key="student_input_field"
    )

    # Botones de acción
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        check_btn = st.button("✅ Verificar", type="primary", use_container_width=True)
    with col2:
        hint_btn = st.button("💡 Pista", use_container_width=True)
    with col3:
        answer_btn = st.button("👁️ Ver Respuesta", use_container_width=True)
    with col4:
        reset_btn = st.button("🔄 Reiniciar", use_container_width=True)

    # Guardar respuesta en session state
    if student_answer:
        st.session_state.student_answer = student_answer

    # Lógica de Verificación
    if check_btn and student_answer:
        is_correct = validate_algebra(student_answer, case_data['respuesta_correcta'])
        
        if is_correct:
            st.session_state.solved = True
            st.session_state.feedback_type = "success"
            st.session_state.feedback_message = "🎉 ¡Excelente trabajo! La Profe Sofía está muy orgullosa de ti. Has dominado este concepto. ¡Vamos por el siguiente caso!"
            st.balloons()
        else:
            st.session_state.feedback_type = "error"
            st.session_state.feedback_message = " Casi, pero no del todo. Revisa tus signos o tu factor común. ¡No te rindas! Pide una pista si lo necesitas."

    # Lógica de Ver Respuesta
    if answer_btn:
        st.session_state.show_answer = True
        st.session_state.feedback_type = "answer"
        st.session_state.feedback_message = f"La respuesta correcta es: {case_data['respuesta_correcta'].replace('**', '^').replace('*', '·')}"

    # Lógica de Pistas
    if hint_btn:
        if st.session_state.hint_level < len(case_data['pistas']):
            st.session_state.feedback_type = "hint"
            st.session_state.feedback_message = case_data['pistas'][st.session_state.hint_level]
            st.session_state.hint_level += 1
        else:
            st.session_state.feedback_type = "warning"
            st.session_state.feedback_message = "Ya te di todas las pistas. ¡Tú puedes resolverlo solo/a!"

    # Lógica de Reiniciar
    if reset_btn:
        st.session_state.hint_level = 0
        st.session_state.solved = False
        st.session_state.show_answer = False
        st.session_state.student_answer = ""
        st.session_state.feedback_message = ""
        st.session_state.feedback_type = ""
        st.rerun()

    # Mostrar Feedback
    if st.session_state.feedback_message:
        if st.session_state.feedback_type == "success":
            st.markdown(f"""
            <div class='success-box'>
                {st.session_state.feedback_message}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.feedback_type == "error":
            st.markdown(f"""
            <div class='error-box'>
                {st.session_state.feedback_message}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.feedback_type == "answer":
            st.markdown(f"""
            <div class='answer-box'>
                {st.session_state.feedback_message}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.feedback_type == "hint":
            st.markdown(f"""
            <div class='hint-box'>
                💡 {st.session_state.feedback_message}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.feedback_type == "warning":
            st.warning(st.session_state.feedback_message)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a1b9a; padding: 1rem;'>
    <small>🧑‍🏫 Profe Sofía | Diseño por Vibe Coding - Ing. Hernán Quiroz | Octubre 2026</small>
</div>
""", unsafe_allow_html=True)
