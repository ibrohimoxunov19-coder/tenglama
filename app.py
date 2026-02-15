import streamlit as st
from sympy import symbols, Function, Eq, dsolve, latex, sympify

# Sahifa sarlavhasi
st.set_page_config(page_title="Differensial Tenglamalar Yechuvchisi", page_icon="🧮")

st.title("🧮 Differensial Tenglamalar Yechuvchisi")
st.write("Tenglamani kiriting (Masalan: `f(x).diff(x) - 2*f(x)`) va javobni oling.")

# Foydalanuvchi kiritish qismi
equation_input = st.text_input("Tenglamani kiriting:", value="f(x).diff(x, x) + 9*f(x)")

if st.button("Yechish"):
    try:
        # Matematik o'zgaruvchilarni e'lon qilish
        x = symbols('x')
        f = Function('f')(x)
        
        # Kiritilgan matnni SymPy formatiga o'tkazish
        # Bu yerda foydalanuvchi y(x) emas, f(x) deb yozishi kerak
        expr = sympify(equation_input)
        diffeq = Eq(expr, 0)
        
        # Tenglamani yechish
        solution = dsolve(diffeq, f)
        
        # Natijani ko'rsatish
        st.success("Muvaffaqiyatli yechildi!")
        
        st.markdown("### Berilgan tenglama:")
        st.latex(latex(diffeq))
        
        st.markdown("### Umumiy yechim:")
        st.latex(latex(solution))
        
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
        st.info("Eslatma: Hosilani `f(x).diff(x)` ko'rinishida yozing. Masalan: `f(x).diff(x, x) + f(x)`")

st.divider()
st.info("Bu sayt SymPy va Streamlit yordamida yaratilgan.")