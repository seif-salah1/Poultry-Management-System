import streamlit as st
import pandas as pd
import numpy as np
import requests
from scipy.optimize import linprog
from datetime import datetime, timedelta

# محاولة استدعاء مكتبة التفقيط (كتابة الأرقام بالعربية)
try:
    from num2words import num2words
except ImportError:
    pass

st.set_page_config(page_title="Kholoud Management System", layout="wide")

custom_css = """
<style>
    html, body, [class*="st-"] {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, .stDataFrame {
        direction: rtl;
        text-align: right !important;
    }
    
    /* 1. تكبير عرض القائمة الجانبية لتستوعب الكلام على سطر واحد */
    section[data-testid="stSidebar"] {
        direction: rtl;
        min-width: 380px !important;
        max-width: 380px !important;
    }
    
    /* 2. إجبار الكلمات على البقاء في سطر واحد بدون التفاف */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1 {
        white-space: nowrap !important;
    }
    
    .stApp h1 {
        font-size: 26px !important;
        padding-bottom: 5px !important;
    }
    
    /* 3. إرجاع حجم الخط الكبير والشيك للعنوان */
    section[data-testid="stSidebar"] h1 {
        font-size: 24px !important;
        padding-top: 0px !important;
    }
    
    .dataframe {
        font-size: 14px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.sidebar.title("Kholoud Management System")
st.sidebar.markdown("**النظام الذكي لإدارة الإنتاج الداجني**")
st.sidebar.markdown("---") 

breed_data = {
    "Ross 308 (روس)": {"max_weight": 2250, "fcr": 1.45, "max_feed": 165},
    "Cobb 500 (كب)": {"max_weight": 2150, "fcr": 1.48, "max_feed": 155},
    "Hubbard (هابرد)": {"max_weight": 2050, "fcr": 1.52, "max_feed": 150},
    "Arbor Acres (أربور إيكرز)": {"max_weight": 2200, "fcr": 1.47, "max_feed": 160},
    "Indian River (إنديان ريفر)": {"max_weight": 2100, "fcr": 1.50, "max_feed": 152},
    "Avian 48 (إيفيان)": {"max_weight": 2180, "fcr": 1.46, "max_feed": 158}
}

selected_breed = st.sidebar.selectbox("اختاري سلالة القطيع (للحسابات):", list(breed_data.keys()))
current_breed = breed_data[selected_breed]

st.sidebar.markdown("---")
app_mode = st.sidebar.radio("القائمة الرئيسية:", 
                            ["لوحة قياس الأداء", 
                             "الحاسبة الاقتصادية", 
                             "نظام التشخيص الطبي",
                             "التحليل المناخي",
                             "تركيب العلف الاقتصادي",
                             "مصفوفة مخاطر السوق",
                             "الأجندة وبرنامج الرعاية"])

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        Developed & Designed by <br>
        <b>Eng. Kholoud & Team</b> <br>
        All Rights Reserved © 2026
    </div>
    """, 
    unsafe_allow_html=True
)

if app_mode == "لوحة قياس الأداء":
    st.title(f"لوحة قياس أداء - Kholoud Management System | {selected_breed}")
    st.markdown("تتبع مؤشرات النمو والاستهلاك القياسية بناءً على كتالوج السلالة المحددة.")
    
    dates = pd.date_range(start=datetime.today().strftime('%Y-%m-%d'), periods=35)
    data = pd.DataFrame({
        'اليوم': range(1, 36),
        'الوزن التقريبي (جرام)': np.round(np.linspace(40, current_breed["max_weight"], 35) + np.random.normal(0, 10, 35), 2),
        'الاستهلاك اليومي للعلف (جرام/طائر)': np.round(np.linspace(12, current_breed["max_feed"], 35), 2)
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("منحنى نمو الأوزان القياسي")
        st.line_chart(data.set_index('اليوم')['الوزن التقريبي (جرام)'])
    with col2:
        st.subheader("منحنى استهلاك العلف اليومي")
        st.line_chart(data.set_index('اليوم')['الاستهلاك اليومي للعلف (جرام/طائر)'], color="#ffaa00")

elif app_mode == "الحاسبة الاقتصادية":
    st.title(f"دراسة الجدوى - Kholoud Management System | {selected_breed}")
    st.markdown("حساب التكاليف الإجمالية، نقطة التعادل، وهامش الربح المتوقع للدورة.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        chicks_count = st.number_input("عدد الكتاكيت", min_value=100, value=5000, step=100)
        chick_price = st.number_input("سعر الكتكوت (جنيه)", min_value=1.0, value=25.0, step=1.0)
        mortality_rate = st.number_input("نسبة النافق المتوقعة (%)", min_value=0.0, value=5.0, step=1.0)
    with col2:
        feed_price = st.number_input("سعر طن العلف (جنيه)", min_value=1000, value=25000, step=500)
        other_costs = st.number_input("نثريات للطائر (أدوية، تدفئة، عمالة)", min_value=1.0, value=15.0, step=1.0)
    with col3:
        target_w = current_breed["max_weight"] / 1000.0
        target_weight = st.number_input("الوزن المستهدف (كجم)", min_value=1.0, value=float(target_w), step=0.1)
        fcr = st.number_input("معامل التحويل (FCR)", min_value=1.0, value=float(current_breed["fcr"]), step=0.05)
        market_price = st.number_input("سعر بيع الكيلو المتوقع (لحم)", min_value=10.0, value=85.0, step=1.0)

    if st.button("تشغيل التحليل الاقتصادي"):
        surviving_birds = chicks_count * (1 - (mortality_rate / 100))
        total_meat_kg = surviving_birds * target_weight
        total_feed_kg = chicks_count * target_weight * fcr
        
        feed_cost = (total_feed_kg / 1000) * feed_price
        total_chicks_cost = chicks_count * chick_price
        total_other_costs = chicks_count * other_costs
        total_cost = feed_cost + total_chicks_cost + total_other_costs
        
        expected_revenue = total_meat_kg * market_price
        net_profit = expected_revenue - total_cost
        break_even_price = total_cost / total_meat_kg

        st.markdown("---")
        st.subheader("النتائج والتحليل المالي")
        c1, c2, c3 = st.columns(3)
        c1.metric(label="إجمالي التكاليف (ج.م)", value=f"{total_cost:,.2f}")
        c2.metric(label="إجمالي اللحم المنتج (كجم)", value=f"{total_meat_kg:,.2f}")
        c3.metric(label="نقطة التعادل (ج.م/كجم)", value=f"{break_even_price:,.2f}")

        st.markdown("---")
        if net_profit > 0:
            st.success(f"المشروع رابح. صافي الربح المتوقع بنهاية الدورة: {net_profit:,.2f} جنيه مصري.")
        else:
            st.error(f"تحذير خسارة. على السعر الحالي، ستكون الخسارة: {abs(net_profit):,.2f} جنيه مصري. يجب البيع بسعر أعلى من {break_even_price:,.2f} ج.م.")

elif app_mode == "نظام التشخيص الطبي":
    st.title("المساعد البيطري - Kholoud Management System")
    st.markdown("حددي الأعراض الظاهرية على القطيع للحصول على تشخيص مبدئي وبروتوكول التدخل السريع.")
    
    symptom = st.selectbox("العرض الظاهري الأبرز:",
                           ["-- اختر من القائمة --", 
                            "أصوات تنفسية (حشرجة/طنين) وإفرازات", 
                            "إسهال أبيض مدمم (دم في الزرق)", 
                            "خمول وتجمع الكتاكيت تحت الدفايات",
                            "إسهال أخضر مع التواء في الرقبة"])

    if symptom == "أصوات تنفسية (حشرجة/طنين) وإفرازات":
        st.error("الاشتباه: مرض تنفسي (مثل التهاب الشعب المعدي IB أو الميكوبلازما). الإجراء: مراجعة التهوية فوراً، رش مطهر هوائي خفيف، واستشارة الطبيب لوصف مضاد حيوي تنفسي مناسب.")
    elif symptom == "إسهال أبيض مدمم (دم في الزرق)":
        st.error("الاشتباه: كوكسيديا (Coccidiosis). الإجراء: فحص الفرشة والتأكد من جفافها، وإضافة مضاد كوكسيديا في ماء الشرب فوراً لتجنب تآكل جدار الأمعاء.")
    elif symptom == "خمول وتجمع الكتاكيت تحت الدفايات":
        st.warning("الاشتباه: برودة شديدة. الإجراء: رفع درجة حرارة الدفايات فوراً لتصل إلى النطاق القياسي (33-34 درجة مئوية) حسب عمر الكتكوت لمنع النفوق وتوقف النمو.")
    elif symptom == "إسهال أخضر مع التواء في الرقبة":
        st.error("الاشتباه: نيوكاسل (Newcastle Disease). الإجراء: عزل فوري للطيور المصابة، رفع مناعة القطيع، واستدعاء الطبيب البيطري لسحب عينات لتأكيد الإصابة الفيروسية.")

elif app_mode == "التحليل المناخي":
    st.title("الرصد المناخي الاستباقي (Forecast DSS)")
    st.markdown("جلب بيانات الطقس الفعلية للـ 16 يوماً القادمة وحساب متوسط الحرارة لترشيح السلالة الأنسب هندسياً وبيولوجياً.")
    
    gov_coords = {
        "القاهرة": {"lat": 30.0444, "lon": 31.2357},
        "الإسكندرية": {"lat": 31.2001, "lon": 29.9187},
        "أسوان": {"lat": 24.0889, "lon": 32.8998},
        "أسيوط": {"lat": 27.1810, "lon": 31.1837},
        "المنصورة (الدقهلية)": {"lat": 31.0364, "lon": 31.3801},
        "الإسماعيلية": {"lat": 30.5833, "lon": 32.2667},
        "الفيوم": {"lat": 29.3084, "lon": 30.8428}
    }
    
    selected_gov = st.selectbox("المحافظة التي يقع بها العنبر:", list(gov_coords.keys()))
    
    if st.button("تحليل بيانات الطقس واستخراج التوصيات"):
        lat = gov_coords[selected_gov]["lat"]
        lon = gov_coords[selected_gov]["lon"]
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=16"
            response = requests.get(url)
            data = response.json()
            
            max_temps = data["daily"]["temperature_2m_max"]
            min_temps = data["daily"]["temperature_2m_min"]
            avg_temp = (sum(max_temps) + sum(min_temps)) / (len(max_temps) * 2)
            
            highest_expected = max(max_temps)
            lowest_expected = min(min_temps)
            
            st.markdown("---")
            st.subheader(f"التوقعات المناخية في {selected_gov}")
            c1, c2, c3 = st.columns(3)
            c1.metric("متوسط حرارة الدورة", f"{avg_temp:.2f} درجة مئوية")
            c2.metric("أعلى درجة متوقعة", f"{highest_expected:.2f} درجة مئوية")
            c3.metric("أقل درجة متوقعة", f"{lowest_expected:.2f} درجة مئوية")
            
            st.markdown("---")
            st.subheader("التوصية الهندسية لاختيار السلالة:")
            
            if avg_temp > 28 or highest_expected > 35:
                st.error("التحليل: الطقس يتجه نحو الحرارة الشديدة. خطر الاحتباس الحراري.")
                st.markdown("السلالات المرشحة: هابرد (Hubbard) أو إنديان ريفر (Indian River).")
                st.markdown("الأسباب: مقاومة فسيولوجية عالية للإجهاد الحراري، ونسبة نفوق أقل.")
            elif avg_temp < 20 or lowest_expected < 12:
                st.info("التحليل: الطقس يتجه نحو البرودة. خطر ضعف الأوزان والأمراض التنفسية.")
                st.markdown("السلالات المرشحة: روس 308 (Ross) أو إيفيان 48 (Avian).")
                st.markdown("الأسباب: معدلات تحويل ممتازة في الأجواء الباردة ومناعة قوية.")
            else:
                st.success("التحليل: الطقس معتدل ومثالي للتربية.")
                st.markdown("السلالات المرشحة: كب 500 (Cobb) أو أربور إيكرز (Arbor Acres).")
                st.markdown("الأسباب: البيئة المثالية للوصول لأوزان تتخطى 2.2 كجم في وقت قياسي.")
                
        except Exception as e:
            st.warning("حدث خطأ في جلب بيانات الطقس. يرجى التأكد من الاتصال بالإنترنت.")

elif app_mode == "تركيب العلف الاقتصادي":
    st.title("المحسن الذكي لتركيبات العلف الاقتصادي")
    st.markdown("يقوم هذا النظام بحساب التوليفة الأقل تكلفة لعمل طن علف مع الالتزام بالقيود الفسيولوجية والأحماض الأمينية للطائر، لضمان أعلى جودة بأرخص سعر متاح.")
    
    st.subheader("الخطوة 1: إدخال أسعار الخامات اليوم (للطن بالجنيه)")
    col1, col2, col3 = st.columns(3)
    with col1:
        price_corn = st.number_input("سعر طن الذرة الصفراء", value=12000, step=500)
        price_soy = st.number_input("سعر طن كسب الصويا 48%", value=24000, step=500)
        price_lysine = st.number_input("سعر طن الليزين (Lysine HCl)", value=85000, step=1000)
    with col2:
        price_oil = st.number_input("سعر طن زيت الصويا", value=45000, step=1000)
        price_limestone = st.number_input("سعر طن الحجر الجيري", value=1500, step=100)
        price_methionine = st.number_input("سعر طن الميثيونين (DL-Met)", value=130000, step=1000)
    with col3:
        price_dcp = st.number_input("سعر طن الداي كالسيوم", value=18000, step=500)
        
    st.subheader("الخطوة 2: اختيار مرحلة التركيبة المطلوبة")
    stage = st.selectbox("المرحلة العمرية:", ["بادي (Starter)", "نامي (Grower)", "ناهي (Finisher)"])
    
    if st.button("تشغيل النظام لحساب التركيبة المثالية"):
        if stage == "بادي (Starter)":
            target_cp = 23.0 ; target_me = 3000 ; target_ca = 1.0 ; target_p = 0.45
            bounds = [(0, 600), (0, 400), (0, 50), (0, 15), (0, 20), (0.5, 5), (0.5, 4)]
        elif stage == "نامي (Grower)":
            target_cp = 21.0 ; target_me = 3100 ; target_ca = 0.9 ; target_p = 0.40
            bounds = [(0, 650), (0, 380), (0, 50), (0, 15), (0, 20), (0.5, 4), (0.5, 4)]
        else: # Finisher
            target_cp = 19.0 ; target_me = 3200 ; target_ca = 0.85 ; target_p = 0.35
            bounds = [(0, 680), (0, 320), (0, 60), (0, 15), (0, 18), (0.5, 4), (0.5, 3.5)]

        c = [price_corn/1000, price_soy/1000, price_oil/1000, price_limestone/1000, price_dcp/1000, price_lysine/1000, price_methionine/1000]
        A_eq = [[1, 1, 1, 1, 1, 1, 1]]
        b_eq = [990]
        
        A_ub = [
            [-0.085, -0.48, 0, 0, 0, -0.94, -0.58], 
            [-3350, -2230, -8800, 0, 0, -4000, -5000], 
            [-0.0002, -0.002, 0, -0.38, -0.22, 0, 0], 
            [-0.001, -0.002, 0, 0, -0.18, 0, 0] 
        ]
        b_ub = [
            -(target_cp / 100) * 1000,
            -target_me * 1000,
            -(target_ca / 100) * 1000,
            -(target_p / 100) * 1000
        ]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            st.success("تمت العملية بنجاح. تم استخراج التركيبة الأقل تكلفة.")
            corn_kg, soy_kg, oil_kg, lime_kg, dcp_kg, lys_kg, met_kg = res.x
            
            # تصليح الخطأ الرياضي: إضافة 1500 جنيه تقديراً لأسعار الـ 10 كيلو إضافات ثابتة بدل الضرب الخاطئ في 1000
            total_ton_cost = res.fun + 1500
            
            st.markdown(f"<h3 style='text-align: right;'>تكلفة طن العلف النهائي: <span style='color: #4CAF50;'>{total_ton_cost:,.2f}</span> جنيه مصري</h3>", unsafe_allow_html=True)
            
            try:
                # توليد النص العربي آلياً
                arabic_text = num2words(int(total_ton_cost), lang='ar')
                st.markdown(f"<p style='text-align: right; color: #888; font-size: 18px;'>(فقط {arabic_text} جنيهاً مصرياً لا غير)</p>", unsafe_allow_html=True)
            except:
                pass
            
            result_df = pd.DataFrame({
                "المكونات (لعمل 1000 كجم)": [
                    "ذرة صفراء", "كسب صويا 48%", "زيت صويا", "حجر جيري", 
                    "داي كالسيوم فوسفات", "ليزين (Lysine HCl)", "ميثيونين (DL-Met)", "ثوابت وإضافات (بريمكس وسموم)"
                ],
                "الكمية بالوزن (كجم)": [
                    f"{corn_kg:.2f}", f"{soy_kg:.2f}", f"{oil_kg:.2f}", f"{lime_kg:.2f}", 
                    f"{dcp_kg:.2f}", f"{lys_kg:.2f}", f"{met_kg:.2f}", "10.00"
                ]
            })
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            
            # تم حذف الجملة المحددة بناءً على طلبك
            st.info("ملاحظة هندسية: تم الالتزام بالحدود القصوى (الفسيولوجية) للخامات وللأحماض الأمينية الصناعية لضمان كفاءة التحويل.")
        else:
            st.error("لم يتمكن النظام من إيجاد تركيبة متوافقة مع هذه القيود والأسعار. يرجى مراجعة المدخلات.")

elif app_mode == "مصفوفة مخاطر السوق":
    st.title("تحليل الحساسية ومصفوفة المخاطر المتوقعة")
    st.markdown("محاكاة لتقلبات السوق لبيان تأثير تغير أسعار العلف واللحم على صافي الأرباح، مما يدعم اتخاذ قرارات التحوط وتقليل المخاطر.")
    
    st.subheader("مدخلات المشروع الثابتة للاختبار")
    col1, col2 = st.columns(2)
    with col1:
        chicks = st.number_input("إجمالي الطيور المنتجة (بعد خصم النافق)", value=4750)
        target_wt = st.number_input("متوسط الوزن المستهدف (كجم)", value=2.1)
    with col2:
        fcr_val = st.number_input("معامل التحويل", value=1.48)
        fixed_costs = st.number_input("تكاليف ثابتة (كتاكيت + نثريات للقطيع بالكامل)", value=200000)

    if st.button("توليد مصفوفة المخاطر"):
        feed_prices = np.arange(18000, 34000, 2000)
        meat_prices = np.arange(65, 110, 5)
        
        results = []
        for feed in feed_prices:
            row = []
            for meat in meat_prices:
                total_meat = chicks * target_wt
                feed_consumed = chicks * target_wt * fcr_val
                total_cost = (feed_consumed / 1000 * feed) + fixed_costs
                revenue = total_meat * meat
                profit = revenue - total_cost
                row.append(round(profit, 2))
            results.append(row)
            
        risk_df = pd.DataFrame(results, index=[f"{p:,.2f} ج" for p in feed_prices], columns=[f"{p:,.2f} ج" for p in meat_prices])
        
        st.markdown("### مصفوفة صافي الربح المتوقع بنهاية الدورة (بالجنيه)")
        st.markdown("الصفوف تمثل: سعر طن العلف | الأعمدة تمثل: سعر بيع كيلو اللحم")
        
        st.info("دليل قراءة المصفوفة: \n\n- اللون الأخضر: يشير إلى منطقة أمان وتحقيق أرباح. كلما زاد غمقان اللون الأخضر، زاد حجم المكسب. \n\n- اللون الأحمر: يشير إلى منطقة خطر وتحقيق خسائر. كلما زاد غمقان اللون الأحمر، زادت قيمة الخسارة المادية.")
        
        styled_risk_df = risk_df.style.background_gradient(cmap='RdYlGn', axis=None).format("{:,.2f}")
        st.dataframe(styled_risk_df, use_container_width=True)

elif app_mode == "الأجندة وبرنامج الرعاية":
    st.title("نظام التشغيل القياسي للمزرعة (SOP)")
    st.markdown("توليد جدول زمني آلي للرعاية البيطرية والهندسية لتجنب العشوائية وإدارة العنبر بشكل منضبط.")
    
    st.subheader("تحديد موعد بدء الدورة")
    start_date = st.date_input("تاريخ استلام الكتاكيت في العنبر:")
    
    if st.button("توليد خطة الرعاية الشاملة"):
        schedule_data = [
            (1, 33, "بادي 23%", "استقبال القطيع: إضافة محلول جفاف أو ماء بسكر، مع مضاد حيوي تنفسي ومعوي للوقاية المبدئية."),
            (7, 31, "بادي 23%", "التحصين الأول: إعطاء تحصينة هتشنر B1 (تقطير في العين أو رش) للوقاية من مرض النيوكاسل."),
            (14, 29, "انتقال لـ نامي 21%", "التحصين الثاني: إعطاء تحصينة جمبورو في ماء الشرب، مع البدء في خلط العلف تدريجياً."),
            (18, 27, "نامي 21%", "التحصين الثالث: إعطاء جرعة تنشيطية من تحصينة لاسوتا للنيوكاسل في ماء الشرب."),
            (21, 26, "نامي 21%", "وقاية معوية: تقديم جرعة وقائية ضد الكوكسيديا والكلوستريديا لمدة 3 أيام متتالية."),
            (28, 24, "انتقال لـ ناهي 19%", "فترة السحب: وقف جميع أنواع المضادات الحيوية تماماً لضمان خلو اللحم من المتبقيات الكيميائية."),
            (35, 22, "ناهي 19%", "نهاية الدورة: الوصول لمتوسط الوزن المستهدف والبدء في إجراءات تسويق القطيع.")
        ]
        
        df_schedule = pd.DataFrame(schedule_data, columns=["عمر القطيع (بالأيام)", "الحرارة القياسية", "المقرر العلفي", "التعليمات والإجراءات البيطرية"])
        
        df_schedule["التاريخ الفعلي للتنفيذ"] = df_schedule["عمر القطيع (بالأيام)"].apply(lambda x: (start_date + timedelta(days=x-1)).strftime("%Y-%m-%d"))
        
        df_schedule = df_schedule[["عمر القطيع (بالأيام)", "التاريخ الفعلي للتنفيذ", "الحرارة القياسية", "المقرر العلفي", "التعليمات والإجراءات البيطرية"]]
        
        st.markdown("### الجدول الزمني للقطيع")
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
