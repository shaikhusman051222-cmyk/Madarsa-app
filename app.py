import streamlit as str
import sqlite3
import pandas as pd

# صفحے کی بنیادی سیٹنگز (خوبصورت لے آؤٹ)
str.set_page_config(page_title="جامعہ اسلامیہ دارالعلوم محمدیہ", page_icon="🕌", layout="wide")

# کسٹم CSS برائے خوبصورت ڈیزائن اور اردو فانٹ (RTL)
str.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    body, div, p, h1, h2, h3, h4, h5, h6, label {
        direction: RTL !important;
        text-align: right !important;
        font-family: 'Noto Nastaliq Urdu', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    .main-title {
        text-align: center !important;
        color: #1e4620;
        background-color: #f0f7f4;
        padding: 20px;
        border-radius: 10px;
        border-right: 10px solid #2e7d32;
        margin-bottom: 30px;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center !important;
        border-top: 4px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- ڈیٹا بیس کی تیاری ----------------
def init_db():
    conn = sqlite3.connect('madrasa_db.db')
    c = conn.cursor()
    # طلبہ کا ٹیبل
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, father_name TEXT, class TEXT, contact TEXT)''')
    # اساتذہ کا ٹیبل
    c.execute('''CREATE TABLE IF NOT EXISTS teachers 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, designation TEXT, qualification TEXT)''')
    # فارغ التحصیل طلبہ کا ٹیبل
    c.execute('''CREATE TABLE IF NOT EXISTS alumni 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, graduation_year TEXT, current_status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ---------------- مددگار فنکشنز ----------------
def run_query(query, params=(), is_select=False):
    conn = sqlite3.connect('madrasa_db.db')
    c = conn.cursor()
    c.execute(query, params)
    if is_select:
        data = c.fetchall()
        conn.close()
        return data
    conn.commit()
    conn.close()

# ---------------- ایپلی کیشن کا ہیڈر ----------------
str.markdown("<div class='main-title'><h1>🕌 جامعہ اسلامیہ دارالعلوم محمدیہ، حمایت نگر</h1><p>مکمل تعلیمی و انتظامی پورٹل</p></div>", unsafe_allow_html=True)

# سائیڈ بار مینیو (Navigation)
str.sidebar.image("https://img.icons8.com/colors/150/mosque.png", width=100)
str.sidebar.title("مینونیو")
choice = str.sidebar.radio("آپشن منتخب کریں:", ["ہوم پیج (تعارف و نصاب)", "طلبہ لاگ ان پورٹل", "نگران کنٹرول پینل (Admin)", "AI اسسٹنٹ (Darul Uloom AI)"])

# ---------------- 1. ہوم پیج (تعارف و نصاب) ----------------
if choice == "ہوم پیج (تعارف و نصاب)":
    str.subheader("✨ مدرسہ ہذا کی مکمل جانکاری")
    
    # لائیو اعداد و شمار (Live Stats Dashboard)
    total_students = len(run_query("SELECT * FROM students", is_select=True)) + 120
    total_teachers = len(run_query("SELECT * FROM teachers", is_select=True)) + 12
    total_alumni = len(run_query("SELECT * FROM alumni", is_select=True)) + 350
    
    col1, col2, col3 = str.columns(3)
    with col1:
        str.markdown(f"<div class='stat-card'><h3>👦 کل زیرِ تعلیم طلبہ</h3><h2>{total_students}</h2></div>", unsafe_allow_html=True)
    with col2:
        str.markdown(f"<div class='stat-card'><h3> 📚 کل اساتذہ کرام</h3><h2>{total_teachers}</h2></div>", unsafe_allow_html=True)
    with col3:
        str.markdown(f"<div class='stat-card'><h3>🎓 فارغ التحصیل طلبہ</h3><h2>{total_alumni}</h2></div>", unsafe_allow_html=True)
    
    str.write("---")
    
    # تعلیمی نصاب
    str.markdown("### 📖 تعلیمی نصاب (Syllabus)")
    tab1, tab2, tab3 = str.tabs(["درجہ ابتدائیہ (Primary)", "درسِ نظامی (عالم کورس)", "حفظ و تجوید"])
    
    with tab1:
        str.write("• قاعدہ بغدادی، ناظرہ قرآن کریم، بنیادی دینیات، اردو، ریاضی اور انگریزی۔")
    with tab2:
        str.write("• صرف و نحو، فقہ (ہدایہ، قدوری)، اصولِ فقہ، بلاغت، اور احادیثِ مبارکہ (صحاح ستہ)۔")
    with tab3:
        str.write("• حسنِ قرأت، تجوید کے قواعد کے ساتھ مکمل حفظِ قرآن کی تعلیم۔")

# ---------------- 2. طلبہ لاگ ان پورٹل ----------------
elif choice == "طلبہ لاگ ان پورٹل":
    str.subheader("🔐 طلبہ لاگ ان پورٹل")
    str.info("تمام طلبہ اپنے مخصوص آئی ڈی کے ذریعے لاگ ان کر کے معلومات دیکھ سکتے ہیں۔")
    
    student_id = str.text_input("اپنا اسٹوڈنٹ آئی ڈی (ID) درج کریں:")
    if student_id:
        str.success("کامیابی سے لاگ ان ہو گئے!")
        str.markdown("#### 📋 آپ کی تعلیمی معلومات:")
        str.write("• **حاضری کا ریکارڈ:** 95%")
        str.write("• **موجودہ درجہ:** عالم سالِ سوم")
        str.write("• **ماہانہ ٹیسٹ رپورٹ:** ممتاز (A+)")

# ---------------- 3. نگران کنٹرول پینل (Admin) ----------------
elif choice == "نگران کنٹرول پینل (Admin)":
    str.subheader("⚙️ نگران کنٹرول پینل")
    
    password = str.text_input("نگران کا خفیہ پاس ورڈ درج کریں:", type="password")
    if password == "admin123":
        str.success("خوش آمدید نگرانِ اعلیٰ! آپ کو مکمل کنٹرول حاصل ہے۔")
        
        admin_choice = str.selectbox("کیا معلومات داخل کرنا چاہتے ہیں؟", ["نیا طالب علم شامل کریں", "نیا استاد شامل کریں", "فارغ التحصیل طالب علم (Alumni) شامل کریں"])
        
        with str.form("data_entry_form", clear_on_submit=True):
            if admin_choice == "نیا طالب علم شامل کریں":
                s_name = str.text_input("طالب علم کا نام:")
                s_father = str.text_input("والد کا نام:")
                s_class = str.text_input("درجہ/کلاس:")
                s_contact = str.text_input("رابطہ نمبر:")
                submit = str.form_submit_button("ڈیٹا محفوظ کریں")
                if submit and s_name:
                    run_query("INSERT INTO students (name, father_name, class, contact) VALUES (?,?,?,?)", (s_name, s_father, s_class, s_contact))
                    str.success("طالب علم کا ڈیٹا کامیابی سے داخل کر دیا گیا!")
                    
            elif admin_choice == "نیا استاد شامل کریں":
                t_name = str.text_input("استاد محترم کا نام:")
                t_desig = str.text_input("عہدہ (مثلاً شیخ الحدیث، مدرس):")
                t_qual = str.text_input("تعلیمی قابلیت:")
                submit = str.form_submit_button("ڈیٹا محفوظ کریں")
                if submit and t_name:
                    run_query("INSERT INTO teachers (name, designation, qualification) VALUES (?,?,?)", (t_name, t_desig, t_qual))
                    str.success("استاد کا ڈیٹا کامیابی سے داخل کر دیا گیا!")
                    
            elif admin_choice == "فارغ التحصیل طالب علم (Alumni) شامل کریں":
                a_name = str.text_input("فارغ طالب علم کا نام:")
                a_year = str.text_input("فراغت کا سال (ہجری/عیسوی):")
                a_status = str.text_input("موجودہ مصروفیت (مثلاً امامت، تدریس):")
                submit = str.form_submit_button("ڈیٹا محفوظ کریں")
                if submit and a_name:
                    run_query("INSERT INTO alumni (name, graduation_year, current_status) VALUES (?,?,?)", (a_name, a_year, a_status))
                    str.success("فارغ التحصیل طالب علم کا ڈیٹا محفوظ ہو گیا!")

        str.write("---")
        str.subheader("📊 موجودہ ریکارڈ کا معائنہ")
        view_data = str.selectbox("ریکارڈ دیکھیں:", ["طلبہ کی فہرست", "اساتذہ کی فہرست", "فارغین کی فہرست"])
        
        conn = sqlite3.connect('madrasa_db.db')
        if view_data == "طلبہ کی فہرست":
            df = pd.read_sql_query("SELECT id AS 'آئی ڈی', name AS 'نام', father_name AS 'والد کا نام', class AS 'درجہ', contact AS 'رابطہ' FROM students", conn)
            str.dataframe(df, use_container_width=True)
        elif view_data == "اساتذہ کی فہرست":
            df = pd.read_sql_query("SELECT id AS 'آئی ڈی', name AS 'نام', designation AS 'عہدہ', qualification AS 'قابلیت' FROM teachers", conn)
            str.dataframe(df, use_container_width=True)
        elif view_data == "فارغین کی فہرست":
            df = pd.read_sql_query("SELECT id AS 'آئی ڈی', name AS 'نام', graduation_year AS 'سالِ فراغت', current_status AS 'موجودہ مصروفیت' FROM alumni", conn)
            str.dataframe(df, use_container_width=True)
        conn.close()

    elif password != "":
        str.error("غلط پاس ورڈ! دوبارہ کوشش کریں۔")

# ---------------- 4. AI اسسٹنٹ (Darul Uloom AI) ----------------
elif choice == "AI اسسٹنٹ (Darul Uloom AI)":
    str.subheader("🤖 دارالعلوم اے آئی (AI Assistant)")
    str.write("مدرسہ، نصاب، یا کسی بھی تعلیمی معلومات کے متعلق سوال پوچھیں:")
    
    user_question = str.text_input("آپ کا سوال:")
    if user_question:
        q = user_question.lower()
        if "نصاب" in q or "syllabus" in q:
            str.markdown("**دارالعلوم AI:** جامعہ میں حفظ، تجوید، اور درسِ نظامی (عالم کورس) کا مکمل نصاب پڑھایا جاتا ہے۔")
        elif "اساتذہ" in q or "teachers" in q:
            str.markdown("**دارالعلوم AI:** جامعہ میں 12 سے زائد مخلص اور جید اساتذہ کرام تدریسی خدمات سرانجام دے رہے ہیں۔")
        elif "فارغ" in q or "alumni" in q:
            str.markdown("**دارالعلوم AI:** الحمدللہ، اب تک جامعہ سے 350 سے زائد طلبہ کرام فارغ ہو کر دین کی خدمت کر رہے ہیں۔")
        else:
            str.markdown("**دارالعلوم AI:** آپ کے سوال کا شکریہ۔ جامعہ اسلامیہ دارالعلوم محمدیہ حمایت نگر کا یہ اسسٹڈ پورٹل جلد ہی مزید اپڈیٹس کے ساتھ آپ کی رہنمائی کرے گا۔")
