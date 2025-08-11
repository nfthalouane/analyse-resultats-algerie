import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# إعداد الصفحة
st.set_page_config(
    page_title="تحليل نتائج الطور المتوسط - الجزائر",
    page_icon="📊",
    layout="wide"
)

# عنوان التطبيق
st.title("📊 تحليل نتائج الطور المتوسط")
st.markdown("تحليل شامل لنتائج الفصول الدراسية - الجزائر")

# الشريط الجانبي
with st.sidebar:
    st.markdown("## ⚙️ إعدادات التحليل")
    uploaded_file = st.file_uploader("📤 رفع ملف النتائج", type=['xlsx', 'xls'])
    
    annee_scolaire = st.selectbox("📚 السنة الدراسية", 
                                 ["أولى متوسط", "ثانية متوسط", "ثالثة متوسط", "رابعة متوسط"])
    
    semestre = st.selectbox("📅 الفصل الدراسي",
                           ["الفصل الأول", "الفصل الثاني", "الفصل الثالث", "السنة كاملة"])

# دالة لتحميل بيانات مثال
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    data = {
        'رقم التسجيل': range(1, 31),
        'الاسم': [f'طالب {i}' for i in range(1, 31)],
        'اللغة العربية': np.random.uniform(8, 20, 30),
        'الرياضيات': np.random.uniform(6, 18, 30),
        'العلوم الطبيعية': np.random.uniform(9, 19, 30)
    }
    
    for col in ['اللغة العربية', 'الرياضيات', 'العلوم الطبيعية']:
        data[col] = np.round(data[col] * 4) / 4
    
    return pd.DataFrame(data)

# دالة لقراءة الملف
def read_file(file):
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            df = pd.read_excel(file, engine='xlrd')
        return df
    except:
        try:
            df = pd.read_excel(file, engine='openpyxl')
            return df
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {str(e)}")
            return None

# دالة للحسابات الإحصائية
def calculate_statistics(df, subject_columns):
    stats_data = {}
    for subject in subject_columns:
        if subject in df.columns:
            valid_scores = df[subject].dropna()
            valid_scores = valid_scores[(valid_scores >= 0) & (valid_scores <= 20)]
            if len(valid_scores) > 0:
                stats_data[subject] = {
                    'المتوسط': round(valid_scores.mean(), 2),
                    'أعلى درجة': round(valid_scores.max(), 2),
                    'أدنى درجة': round(valid_scores.min(), 2),
                    'عدد الطلاب': len(valid_scores),
                    'النجاح (%)': round((valid_scores >= 10).sum() / len(valid_scores) * 100, 2)
                }
    return stats_data

# الرئيسية
if uploaded_file is not None:
    df = read_file(uploaded_file)
    if df is not None:
        st.success("✅ تم تحميل الملف بنجاح!")
else:
    df = load_sample_data()
    st.info("ℹ️ يتم عرض بيانات مثال.")

if df is not None:
    # تحديد أعمدة المواد
    subject_columns = [col for col in df.columns if col not in ['رقم التسجيل', 'الاسم']]
    
    # حساب الإحصائيات
    stats_data = calculate_statistics(df, subject_columns)
    
    # عرض الملخص
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 عدد الطلاب", len(df))
    
    # عرض الإحصائيات
    if stats_data:
        st.markdown("## 📈 الإحصائيات")
        stats_df = pd.DataFrame(stats_data).T
        st.dataframe(stats_df.style.format("{:.2f}"))
        
        # رسم بياني بسيط
        subjects = list(stats_data.keys())
        averages = [stats_data[subject]['المتوسط'] for subject in subjects]
        
        fig = px.bar(x=subjects, y=averages, 
                    labels={'x': 'المادة', 'y': 'المتوسط'},
                    title='متوسط الدرجات حسب المادة')
        st.plotly_chart(fig)

else:
    st.error("❌ لم يتم تحميل أي بيانات.")        background-color: var(--background-color);
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--box-shadow);
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background-color: var(--card-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--box-shadow);
        border-left: 5px solid var(--accent-color);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        background-color: var(--card-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--box-shadow);
        margin-bottom: 1.5rem;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--card-color);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
    }
    
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary-color);
        transform: scale(1.02);
    }
    
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    .success-text {
        color: var(--accent-color);
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .warning-text {
        color: #ff9800;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .danger-text {
        color: #f44336;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .stProgress > div > div > div {
        background-color: var(--accent-color);
    }
    
    .stAlert {
        border-radius: var(--border-radius);
    }
    
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
    }
    
    .stDataFrame {
        border-radius: var(--border-radius);
    }
</style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown("""
<div class="header">
    <h1>📊 تطبيق تحليل نتائج الطور المتوسط</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">تحليل شامل لنتائج الفصول الدراسية والشهادات - وزارة التربية والتعليم - الجزائر</p>
</div>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("## ⚙️ إعدادات التحليل")
    
    # رفع الملف
    uploaded_file = st.file_uploader(
        "📤 رفع ملف النتائج (XLS)",
        type=['xls'],
        help="يرجى رفع ملف XLS الصادر من الرقمنة"
    )
    
    # تحديد السنة الدراسية
    annee_scolaire = st.selectbox(
        "📚 السنة الدراسية",
        ["أولى متوسط", "ثانية متوسط", "ثالثة متوسط", "رابعة متوسط"],
        index=0
    )
    
    # تحديد الفصل الدراسي
    semestre = st.selectbox(
        "📅 الفصل الدراسي",
        ["الفصل الأول", "الفصل الثاني", "الفصل الثالث", "السنة كاملة"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("## 📊 خيارات التحليل")
    
    show_basic_stats = st.checkbox("📈 الإحصائيات الأساسية", value=True)
    show_charts = st.checkbox("📊 الرسوم البيانية", value=True)
    show_detailed_analysis = st.checkbox("🔍 التحليل التفصيلي", value=True)
    show_recommendations = st.checkbox("💡 التوصيات", value=True)

# دالة لتحميل بيانات مثال
@st.cache_data
def load_sample_data():
    """تحميل بيانات مثال للاختبار"""
    np.random.seed(42)  # للحصول على نتائج ثابتة
    data = {
        'رقم التسجيل': range(1, 101),
        'الاسم': [f'طالب {i}' for i in range(1, 101)],
        'اللقب': [f'اللقب {i}' for i in range(1, 101)],
        'القسم': ['1AM' + str(i%4+1) for i in range(100)],
        'اللغة العربية': np.random.uniform(8, 20, 100),
        'اللغة الفرنسية': np.random.uniform(7, 19, 100),
        'الرياضيات': np.random.uniform(6, 18, 100),
        'العلوم الطبيعية': np.random.uniform(9, 19, 100),
        'التاريخ والجغرافيا': np.random.uniform(8, 18, 100),
        'التربية الإسلامية': np.random.uniform(10, 20, 100),
        'التربية المدنية': np.random.uniform(9, 19, 100),
        'الفيزياء والكيمياء': np.random.uniform(7, 17, 100),
        'اللغة الإنجليزية': np.random.uniform(6, 16, 100),
        'التكنولوجيا': np.random.uniform(8, 18, 100),
        'التربية البدنية': np.random.uniform(12, 20, 100)
    }
    
    # تقريب الدرجات إلى أقرب 0.25
    for col in data.keys():
        if col not in ['رقم التسجيل', 'الاسم', 'اللقب', 'القسم']:
            data[col] = np.round(data[col] * 4) / 4
    
    return pd.DataFrame(data)

# دالة لقراءة ملف XLS
def read_xls_file(file):
    """قراءة ملف XLS"""
    try:
        # تحويل الملف إلى DataFrame
        df = pd.read_excel(file, engine='xlrd')
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {str(e)}")
        return None

# دالة للحسابات الإحصائية
def calculate_statistics(df, subject_columns):
    """حساب الإحصائيات للنتائج"""
    stats_data = {}
    
    for subject in subject_columns:
        if subject in df.columns:
            # تصفية القيم الصالحة
            valid_scores = df[subject].dropna()
            valid_scores = valid_scores[(valid_scores >= 0) & (valid_scores <= 20)]
            
            if len(valid_scores) > 0:
                stats_data[subject] = {
                    'المتوسط': round(valid_scores.mean(), 2),
                    'الانحراف المعياري': round(valid_scores.std(), 2),
                    'أعلى درجة': round(valid_scores.max(), 2),
                    'أدنى درجة': round(valid_scores.min(), 2),
                    'الوسيط': round(valid_scores.median(), 2),
                    'عدد الطلاب': len(valid_scores),
                    'النجاح (%)': round((valid_scores >= 10).sum() / len(valid_scores) * 100, 2)
                }
            else:
                stats_data[subject] = {
                    'المتوسط': 0, 'الانحراف المعياري': 0, 'أعلى درجة': 0,
                    'أدنى درجة': 0, 'الوسيط': 0, 'عدد الطلاب': 0, 'النجاح (%)': 0
                }
    
    return stats_data

# دالة للرسم البياني
def create_subject_chart(stats_data):
    """إنشاء رسم بياني للمواد"""
    subjects = list(stats_data.keys())
    averages = [stats_data[subject]['المتوسط'] for subject in subjects]
    success_rates = [stats_data[subject]['النجاح (%)'] for subject in subjects]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('متوسط الدرجات حسب المادة', 'معدل النجاح حسب المادة'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # رسم متوسط الدرجات
    fig.add_trace(
        go.Bar(x=subjects, y=averages, name='المتوسط', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # رسم معدل النجاح
    fig.add_trace(
        go.Bar(x=subjects, y=success_rates, name='معدل النجاح %', marker_color='#2ca02c'),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_text="تحليل النتائج حسب المواد",
        title_x=0.5,
        font=dict(size=12)
    )
    
    fig.update_xaxes(tickangle=45)
    return fig

# دالة لتحليل الأداء العام
def analyze_overall_performance(df, subject_columns):
    """تحليل الأداء العام للطلاب"""
    # حساب المعدل العام لكل طالب
    student_averages = []
    for index, row in df.iterrows():
        scores = []
        for subject in subject_columns:
            if subject in df.columns and pd.notna(row[subject]):
                score = row[subject]
                if 0 <= score <= 20:
                    scores.append(score)
        if scores:
            student_averages.append(np.mean(scores))
        else:
            student_averages.append(0)
    
    df['المعدل العام'] = student_averages
    
    # تصنيف الأداء
    df['تصنيف الأداء'] = pd.cut(df['المعدل العام'], 
                               bins=[0, 10, 14, 16, 20], 
                               labels=['ضعيف', 'مقبول', 'جيد', 'ممتاز'])
    
    return df

# دالة لإنشاء توصيات
def generate_recommendations(stats_data, df):
    """توليد التوصيات التحليلية"""
    recommendations = []
    
    # تحليل المواد الضعيفة
    weak_subjects = [subject for subject, stats in stats_data.items() 
                    if stats['المتوسط'] < 10]
    
    if weak_subjects:
        recommendations.append(f"⚠️ المواد التي تحتاج إلى تحسين: {', '.join(weak_subjects[:3])}")
    
    # تحليل معدل النجاح العام
    overall_success = df['المعدل العام'].apply(lambda x: x >= 10).mean() * 100
    if overall_success < 70:
        recommendations.append(f"📉 معدل النجاح العام ({overall_success:.1f}%) يحتاج إلى تحسين")
    elif overall_success > 90:
        recommendations.append(f"🏆 معدل النجاح العام ({overall_success:.1f}%) ممتاز")
    
    # تحليل التباين
    avg_std = np.mean([stats['الانحراف المعياري'] for stats in stats_data.values()])
    if avg_std > 4:
        recommendations.append("📊 هناك تباين كبير في النتائج، مما يشير إلى اختلاف مستوى الطلاب")
    
    return recommendations

# الرئيسية
if uploaded_file is not None:
    # قراءة الملف
    df = read_xls_file(uploaded_file)
    if df is not None:
        st.success("✅ تم تحميل الملف بنجاح!")
else:
    # استخدام بيانات المثال
    df = load_sample_data()
    st.info("ℹ️ يتم عرض بيانات مثال. يرجى رفع ملف XLS لتحليل البيانات الحقيقية.")

if df is not None:
    # تحديد أعمدة المواد
    subject_columns = [col for col in df.columns if col not in 
                      ['رقم التسجيل', 'الاسم', 'اللقب', 'القسم']]
    
    # حساب الإحصائيات
    stats_data = calculate_statistics(df, subject_columns)
    
    # تحليل الأداء العام
    df = analyze_overall_performance(df, subject_columns)
    
    # عرض الملخص العام
    st.markdown("## 📊 الملخص العام")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 عدد الطلاب</h3>
            <p class="success-text">{len(df)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_performance = df['المعدل العام'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 المتوسط العام</h3>
            <p class="{'success-text' if avg_performance >= 10 else 'danger-text'}">
                {avg_performance:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        success_rate = (df['المعدل العام'] >= 10).mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ معدل النجاح</h3>
            <p class="{'success-text' if success_rate >= 70 else 'warning-text'}">
                {success_rate:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if stats_data:
            best_subject = max(stats_data.keys(), key=lambda x: stats_data[x]['المتوسط'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 أفضل مادة</h3>
                <p>{best_subject}<br/>{stats_data[best_subject]['المتوسط']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # عرض الإحصائيات الأساسية
    if show_basic_stats:
        st.markdown("## 📈 الإحصائيات التفصيلية")
        
        # عرض جدول الإحصائيات
        if stats_data:
            stats_df = pd.DataFrame(stats_data).T
            st.dataframe(stats_df.style.format("{:.2f}").background_gradient(cmap='Blues'))
    
    # عرض الرسوم البيانية
    if show_charts and stats_data:
        st.markdown("## 📊 التحليل البياني")
        
        # الرسم البياني للمواد
        fig = create_subject_chart(stats_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # توزيع المعدلات
        fig2 = px.histogram(df, x='المعدل العام', nbins=20, 
                           title='توزيع المعدلات العامة للطلاب',
                           labels={'المعدل العام': 'المعدل العام', 'count': 'عدد الطلاب'})
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # توزيع الأداء
        performance_counts = df['تصنيف الأداء'].value_counts()
        fig3 = px.pie(values=performance_counts.values, 
                     names=performance_counts.index,
                     title='توزيع تصنيف الأداء العام')
        st.plotly_chart(fig3, use_container_width=True)
    
    # التحليل التفصيلي
    if show_detailed_analysis:
        st.markdown("## 🔍 التحليل التفصيلي")
        
        # تحليل حسب الأقسام
        if 'القسم' in df.columns:
            section_analysis = df.groupby('القسم')['المعدل العام'].agg(['mean', 'std', 'count']).round(2)
            section_analysis.columns = ['المتوسط', 'الانحراف المعياري', 'عدد الطلاب']
            st.subheader("📊 تحليل حسب الأقسام")
            st.dataframe(section_analysis.style.background_gradient(cmap='Greens'))
        
        # الطلاب المتفوقون
        top_students = df.nlargest(10, 'المعدل العام')[['الاسم', 'اللقب', 'المعدل العام', 'تصنيف الأداء']]
        st.subheader("🏆 أفضل 10 طلاب")
        st.dataframe(top_students.style.format({'المعدل العام': '{:.2f}'}).background_gradient(cmap='Blues'))
    
    # التوصيات
    if show_recommendations and stats_data:
        st.markdown("## 💡 التوصيات والاقتراحات")
        recommendations = generate_recommendations(stats_data, df)
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #ff9800;">
                <p>{rec}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # توصيات محددة للمواد
        st.markdown("### 📚 توصيات حسب المواد")
        for subject, stats in stats_data.items():
            if stats['المتوسط'] < 10:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #f44336;">
                    <h4>{subject}</h4>
                    <p>المتوسط: {stats['المتوسط']:.2f} - يُوصى بتحسين طرق التدريس</p>
                </div>
                """, unsafe_allow_html=True)
    
    # خيارات التصدير
    st.markdown("## 📤 تصدير التقارير")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 تحميل التقرير (Excel)"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='البيانات', index=False)
                if 'stats_df' in locals():
                    stats_df.to_excel(writer, sheet_name='الإحصائيات')
            output.seek(0)
            st.download_button(
                label="حفظ التقرير",
                data=output,
                file_name="تقرير_النتائج.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        if st.button("📄 تحميل التقرير (PDF)"):
            st.warning("ميزة تصدير PDF ستكون متاحة في النسخة القادمة")

else:
    st.error("❌ لم يتم تحميل أي بيانات. يرجى رفع ملف XLS أو استخدام بيانات المثال.")

# معلومات إضافية
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>📊 تطبيق تحليل نتائج الطور المتوسط - وزارة التربية والتعليم - الجزائر</p>
    <p>© 2024 - جميع الحقوق محفوظة</p>
</div>

""", unsafe_allow_html=True)
