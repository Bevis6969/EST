import streamlit as st
import datetime

# 標題
st.markdown("<h1 style='text-align: center;'>EduSessionTracker</h1>", unsafe_allow_html=True)

# 日期選擇器
date = st.date_input("日期", value=datetime.date.today())

# 年段選擇
grade = st.selectbox("年段", ["小四數", "小五數", "小六數"])

# 時間選單生成
def generate_time_options():
    return [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in [0, 30]]

# 補課時段選擇
start_time = st.selectbox("開始時間", generate_time_options())
end_time = st.selectbox("結束時間", generate_time_options())

# 學年度與學期選擇
school_year = st.selectbox("學年度", ["110", "111", "112", "113", "114", "115"])
semester = st.selectbox("學期", ["第一學期", "第二學期"])

# 學生姓名輸入
student_name = st.text_input("學生姓名")

# 補課進度輸入
progress = st.text_area("補課進度", placeholder="例如: 完成第3章，第4章習題1-5題")

# 今日課程內容
content = st.text_area("今日內容", placeholder="例如: 講解第3章重點，分析題型")

# 指派作業
homework = st.text_area("指派作業", placeholder="例如: 完成第4章P23-30")

# 考試範圍
exam_range = st.text_input("考試範圍", placeholder="例如: 第3章到第4章")

# 考試成績
exam_score = st.text_input("考試成績", placeholder="例如: 90分")

# 學生表現
performance = st.text_area("學生表現", placeholder="例如: 理解力良好，但速度較慢")

# 備註
suggestion = st.text_area("備註", placeholder="例如: 建議每日閱讀練習30分鐘")

# 下次補課安排
next_class_date = st.date_input("下次補課日期", value=None)

# 聯絡簿
contact_book_signature = st.selectbox("聯絡簿", ["已簽名", "未簽名", "未帶"])

# 上次回家作業
homework_brought = st.selectbox("上次回家作業", ["已帶", "未帶", "未寫", "無"])

# 時間差計算（補課時數）
def calculate_hours(start_time, end_time):
    try:
        start_dt = datetime.datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.datetime.strptime(end_time, "%H:%M")
        if end_dt < start_dt:  # 如果結束時間小於開始時間，視為跨日
            end_dt += datetime.timedelta(days=1)
        duration = end_dt - start_dt
        return round(duration.total_seconds() / 3600, 2)  # 返回小數點2位的時數
    except Exception as e:
        return f"時間計算錯誤: {e}"

# 生成回報訊息
if st.button("生成回報訊息", key="generate_report"):
    hours = calculate_hours(start_time, end_time)
    weekday = date.strftime("%A")  # 英文格式
    weekday_map = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日",
    }
    weekday_chinese = weekday_map.get(weekday, weekday)
    
    # 確保 next_class_date 被處理
    if next_class_date and isinstance(next_class_date, datetime.date):  # 確認其為日期類型
        next_weekday = next_class_date.strftime("%A")
        next_weekday_chinese = weekday_map.get(next_weekday, next_weekday)
        next_class_str = f"{next_class_date} ({next_weekday_chinese})"
    else:
        next_class_str = "(備註)"
    
    report = f"""
=====狀況回報訊息=====
日期: {date} ({weekday_chinese})
學年度: {school_year}學年度 {semester}
年段: {grade}
時段: {start_time} ~ {end_time}
時數: {hours} 小時

學生姓名: {student_name}
課程進度: {progress}

今日內容:
{content}

指派作業:
{homework}

考試範圍: {exam_range if exam_range else "無"}
考試成績: {exam_score if exam_score else "無"}

學生表現:
{performance}

聯絡簿簽名: {contact_book_signature}
上次回家作業: {homework_brought}

備註:
{suggestion}

下次補課安排: {next_class_str}
    """.strip()
    
    # 顯示訊息
    st.text_area("生成的回報訊息", report, height=300)

    # 使用 HTML 和 JavaScript 來實現複製功能
    html_code = f"""
    <button onclick="navigator.clipboard.writeText(`{report.replace('`', '')}`)">
        點擊複製回報訊息
    </button>
    <p>請點擊上面按鈕複製回報訊息</p>
    """
    st.markdown(html_code, unsafe_allow_html=True)
