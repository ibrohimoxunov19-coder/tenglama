import streamlit as st
import re
from sympy import symbols, Function, Eq, dsolve, latex, sympify

st.set_page_config(page_title="Aqlli Matematik", page_icon="🎓")

def smart_parse(user_input):
    # 1. Keraksiz belgilarni tozalash (qo'shtirnoq va bo'sh joylar)
    clean = user_input.replace('"', '').replace("'", "").strip()
    
    # 2. dy/dx ko'rinishlarini y' ga o'tkazish
    clean = clean.replace("d2y/dx2", "y''").replace("dy/dx", "y'")
    
    # 3. y'' va y' larni SymPy tushunadigan f(x) formatiga o'tkazish
    clean = clean.replace("y''", "f(x).diff(x,x)")
    clean = clean.replace("y'", "f(x).diff(x)")
    
    # 4. "4y" ni "4*y" ga aylantirish (Raqamdan keyin harf kelsa ko'paytirish qo'yish)
    clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean)
    
    # 5. Yolg'iz 'y' harfini 'f(x)' ga aylantirish
    clean = re.sub(r'(?<![a-zA-Z0-9])y(?![a-zA-Z0-9\(])', 'f(x)', clean)
    
    # 6. Daraja belgisini to'g'irlash (^ ni ** ga)
    clean = clean.replace('^', '**')
    
    return clean

st.title("🎓 Aqlli Differensial Yechuvchi")
st.write("Xohlagancha yozing: `y''+4y=0`, `y' = 2y`, `dy/dx + y = x` va h.k.")

user_raw = st.text_input("Misolni kiriting:", value="y'' + 4y = 0")

if st.button("Yechish"):
    try:
        x = symbols('x')
        f = Function('f')(x)
        
        # Tenglamani '=' belgisi bo'yicha bo'lish
        if '=' in user_raw:
            left_part, right_part = user_raw.split('=')
        else:
            left_part, right_part = user_raw, "0"
            
        # Ikkala tomonni ham aqlli tozalash
        lhs = sympify(smart_parse(left_part), locals={'f': f, 'x': x})
        rhs = sympify(smart_parse(right_part), locals={'f': f, 'x': x})
        
        diffeq = Eq(lhs, rhs)
        solution = dsolve(diffeq, f)
        
        st.success("Mana yechim:")
        st.latex(latex(solution).replace('f{\\left(x \\right)}', 'y'))
        
    except Exception as e:
        st.error(f"Xatolik: Kirish formatini tekshiring. Masalan: y'' + 4y = 0")
