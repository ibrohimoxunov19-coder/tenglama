import streamlit as st
import re
from sympy import symbols, Function, Eq, dsolve, latex, sympify

st.set_page_config(page_title="Aqlli Matematik", page_icon="🎓")

def smart_parse(user_input):
    # 1. Tozalash
    clean = user_input.replace('"', '').replace("'", "").strip()
    
    # 2. Hosilalarni standartlashtirish
    clean = clean.replace("y''", "f(x).diff(x,x)").replace("y'", "f(x).diff(x)")
    clean = clean.replace("d2y/dx2", "f(x).diff(x,x)").replace("dy/dx", "f(x).diff(x)")
    
    # 3. Ko'paytirish belgilarini qo'shish (masalan: 4y -> 4*f(x))
    # Avval y ni f(x) ga aylantiramiz, keyin raqam va f(x) orasiga * qo'yamiz
    clean = re.sub(r'(?<![a-zA-Z0-9])y(?![a-zA-Z0-9\(])', 'f(x)', clean)
    clean = re.sub(r'(\d)([a-fA-F])', r'\1*\2', clean) 
    
    # 4. Darajalar
    clean = clean.replace('^', '**')
    
    return clean

st.title("🎓 Aqlli Differensial Yechuvchi")
st.info("Misolni kiriting (Masalan: y'' + 4y = 0 yoki y' = 2y)")

user_raw = st.text_input("Misolni kiriting:", value="y' + 4*y = 0")

if st.button("Yechish"):
    if not user_raw:
        st.warning("Iltimos, tenglamani kiriting!")
    else:
        try:
            x = symbols('x')
            f = Function('f')(x)
            
            # Tenglamani parse qilish
            if '=' in user_raw:
                parts = user_raw.split('=')
                lhs_str = smart_parse(parts[0])
                rhs_str = smart_parse(parts[1])
            else:
                lhs_str = smart_parse(user_raw)
                rhs_str = "0"

            # Sympy obyektlariga aylantirish
            # locals yordamida f va x ni aniq tanitamiz
            lhs = sympify(lhs_str, locals={'f': f, 'x': x})
            rhs = sympify(rhs_str, locals={'f': f, 'x': x})
            
            diffeq = Eq(lhs, rhs)
            
            # Yechish
            with st.spinner('Yechilmoqda...'):
                solution = dsolve(diffeq, f)
            
            st.success("Muvaffaqiyatli yechildi!")
            
            # Natijani chiroyli ko'rsatish
            # f(x) ni y ga qayta almashtiramiz ko'rinish uchun
            res_latex = latex(solution).replace('f{\\left(x \\right)}', 'y')
            st.latex(res_latex)
            
        except Exception as e:
            st.error(f"Xatolik yuz berdi. Iltimos, formatni tekshiring.")
            with st.expander("Texnik tafsilotlar"):
                st.write(f"Original xato: {e}")
                st.write(f"Dastur tushungan ko'rinish: {lhs_str} = {rhs_str}")
