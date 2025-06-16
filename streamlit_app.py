import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="แบบฟอร์มประเมินการใช้ข้อมูล",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1

if 'client_info' not in st.session_state:
    st.session_state.client_info = {}

if 'choices' not in st.session_state:
    st.session_state.choices = {}

# Define questions and options
questions = {
    1: {
        "question": "เวลาท่านต้องการใช้ข้อมูล ท่านรู้หรือไม่ว่ามีข้อมูลอะไรบ้าง และต้องขอที่ไหน / ที่ใคร",
        "options": [
            "รู้ชุดข้อมูลส่วนใหญ่อย่างละเอียด และรู้ว่าอยู่ที่หน่วยงานภายในไหน",
            "รู้ชุดข้อมูลส่วนใหญ่ แต่ไม่รู้ว่าอยู่ที่หน่วยงานภายในไหน",
            "รู้ชุดข้อมูลบางส่วน",
            "ไม่ทราบ"
        ]
    },
    2: {
        "question": "ท่านทราบหรือไม่ว่าชุดข้อมูลสำคัญขององค์กรท่านมีอะไรบ้าง",
        "options": [
            "ทราบชุดข้อมูลสำคัญ และมีการระบุชุดข้อมูลหลัก (Master Data) เรียบร้อยแล้ว",
            "ทราบชุดข้อมูลสำคัญ แต่ยังไม่มีการระบุชุดข้อมูลหลัก (Master Data) ที่ชัดเจน",
            "ทราบบางส่วนแบบพอสังเขป",
            "ไม่มีการระบุชุดข้อมูลสำคัญ",
            "ไม่ทราบ"
        ]
    },
    3: {
        "question": "ในการตัดสินใจของท่าน ท่านใช้ข้อมูลหรือประสบการณ์ในการตัดสินใจเป็นหลัก",
        "options": [
            "ส่วนใหญ่ใช้ข้อมูลในการประกอบการตัดสินใจร่วมกับประสบการณ์",
            "ใช้ประสบการณ์ร่วมกับข้อมูลบางส่วนในการประกอบการตัดสินใจเสมอ",
            "ใช้ประสบการณ์เป็นหลัก และพิจารณาข้อมูลประกอบเมื่อมีข้อมูลที่เพียงพอหรือเกี่ยวข้อง",
            "ใช้ประสบการณ์เป็นหลัก"
        ]
    },
    4: {
        "question": "เมื่อท่านต้องรับผลรายงานจากฝ่ายปฏิบัติการหรือฝ่ายอื่นๆ ท่านใช้เวลานานไหมในการได้รับข้อมูล และสามารถใช้ในการตัดสินใจได้ทันทีหรือไม่",
        "options": [
            "รวดเร็ว และพร้อมใช้",
            "รวดเร็ว อาจมีการปรับแก้เล็กน้อย",
            "ใช้เวลานานและต้องปรับแก้บ่อย",
            "ล่าช้า ใช้เวลานาน และมีอุปสรรค"
        ]
    },
    5: {
        "question": "องค์กรของท่านมีการกำหนดเป้าหมายหรือกลยุทธ์ด้านข้อมูลหรือไม่ เช่น เป็นศูนย์กลางข้อมูลด้านต่างๆของประเทศ, มุ่งเน้นนำระบบดิจิทัลมาช่วยทำงาน, มุ่งมั่นเปิดเผยข้อมูล เป็นต้น",
        "options": [
            "มีเป้าหมายชัดเจนทั้งองค์กร",
            "มีเป้าหมายแต่ยังไม่ชัดเจน",
            "กำลังอยู่ระหว่างการกำหนด",
            "ไม่มีเป้าหมายด้านข้อมูล",
            "ไม่ทราบ"
        ]
    },
    6: {
        "question": "ท่านทราบถึงจุดแข็ง จุดอ่อน ด้านข้อมูลขององค์กรท่านหรือไม่",
        "options": [
            "ทราบทั้งหมดอย่างละเอียด",
            "ทราบบางส่วนอย่างละเอียด",
            "ทราบเฉพาะที่อยู่ในขอบเขตความรับผิดชอบของตน",
            "ไม่ทราบ"
        ]
    },
    7: {
        "question": "องค์กรของท่านมีการแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูลหรือไม่",
        "options": [
            "มี และแต่งตั้งตามมาตรฐานรัฐบาลดิจิทัล",
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่",
            "กำลังดำเนินการ",
            "ไม่มีการแต่งตั้ง",
            "ไม่ทราบ"
        ]
    },
    8: {
        "question": "องค์กรของท่านมีการจัดตั้งทีมบริกรข้อมูลหรือไม่",
        "options": [
            "มี และจัดตั้งตามมาตรฐานรัฐบาลดิจิทัล",
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่",
            "กำลังดำเนินการ",
            "ไม่มีการจัดตั้ง",
            "ไม่ทราบ"
        ]
    },
    9: {
        "question": "องค์กรของท่านมีการบริหารข้อมูลผ่านระบบหรือแพลตฟอร์มกลางหรือไม่",
        "options": [
            "มีการใช้งานส่วนใหญ่ภายในองค์กร",
            "มีการใช้งานบางหน่วยงานภายในร่วมกัน",
            "กำลังดำเนินการพัฒนาระบบกลาง หรือแพลตฟอร์มกลาง",
            "ไม่มีแพลตฟอร์มกลาง",
            "ไม่ทราบ"
        ]
    },
    10: {
        "question": "องค์กรของท่านมีการใช้ข้อมูลร่วมกันระหว่างหน่วยงานภายในมากน้อยแค่ไหน",
        "options": [
            "ใช้ชุดข้อมูลร่วมกันหลายชุด และมีมาตรฐานชัดเจน",
            "ใช้ชุดข้อมูลร่วมกันหลายชุด แต่ยังไม่มีมาตรฐานชัดเจน",
            "ใช้ชุดข้อมูลร่วมกันเพียงเล็กน้อย",
            "ไม่มีการใช้ชุดข้อมูลร่วมกัน",
            "ไม่ทราบ"
        ]
    }
}

# Page 1: Client Information
def page_client_info():
    st.title("📝 แบบฟอร์มประเมินการใช้ข้อมูล")
    st.subheader("ข้อมูลผู้กรอกแบบฟอร์ม")
    
    with st.form("client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            org_name = st.text_input("ชื่อองค์กร", value=st.session_state.client_info.get('org_name', ''))
            phone = st.text_input("เบอร์โทรศัพท์", value=st.session_state.client_info.get('phone', ''))
        
        with col2:
            full_name = st.text_input("ชื่อ-นามสกุล", value=st.session_state.client_info.get('full_name', ''))
            email = st.text_input("อีเมล", value=st.session_state.client_info.get('email', ''))
        
        submitted = st.form_submit_button("Next ➡️", use_container_width=True)
        
        if submitted:
            if all([org_name, full_name, phone, email]):
                st.session_state.client_info = {
                    'org_name': org_name,
                    'full_name': full_name,
                    'phone': phone,
                    'email': email
                }
                st.session_state.page = 2
                st.rerun()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบทุกช่อง")

# Page 2: Questions
def page_questions():
    st.title("📊 แบบประเมินการใช้ข้อมูลในองค์กร")
    
    # Progress bar
    progress = len(st.session_state.choices) / len(questions)
    st.progress(progress)
    st.caption(f"ความคืบหน้า: {len(st.session_state.choices)} / {len(questions)} คำถาม")
    
    with st.form("questions_form"):
        for q_num, q_data in questions.items():
            st.markdown(f"### คำถามที่ {q_num}")
            st.markdown(q_data["question"])
            
            # Get saved answer if exists
            saved_answer = st.session_state.choices.get(f"q{q_num}", None)
            default_index = 0
            if saved_answer:
                try:
                    default_index = q_data["options"].index(saved_answer)
                except ValueError:
                    default_index = 0
            
            answer = st.radio(
                f"เลือกคำตอบ:",
                q_data["options"],
                key=f"q{q_num}",
                index=default_index
            )
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("⬅️ กลับ", use_container_width=True)
        with col2:
            submit_button = st.form_submit_button("ส่งแบบฟอร์ม ✅", use_container_width=True, type="primary")
        
        if back_button:
            st.session_state.page = 1
            st.rerun()
            
        if submit_button:
            # Save all answers
            for q_num in questions.keys():
                st.session_state.choices[f"q{q_num}"] = st.session_state[f"q{q_num}"]
            st.session_state.page = 3
            st.rerun()

# Page 3: Results
def page_results():
    st.title("✅ สรุปผลการประเมิน")
    st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")
    
    # Display client information
    st.subheader("📋 ข้อมูลผู้กรอกแบบฟอร์ม")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**ชื่อองค์กร:** {st.session_state.client_info.get('org_name', '')}")
        st.write(f"**เบอร์โทรศัพท์:** {st.session_state.client_info.get('phone', '')}")
    with col2:
        st.write(f"**ชื่อ-นามสกุล:** {st.session_state.client_info.get('full_name', '')}")
        st.write(f"**อีเมล:** {st.session_state.client_info.get('email', '')}")
    
    st.markdown("---")
    
    # Display answers summary
    st.subheader("📊 สรุปคำตอบ")
    
    results_data = []
    for q_num, q_data in questions.items():
        answer = st.session_state.choices.get(f"q{q_num}", "ไม่ได้ตอบ")
        results_data.append({
            "คำถามที่": q_num,
            "คำถาม": q_data["question"][:50] + "...",
            "คำตอบ": answer
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export options
    st.markdown("---")
    st.subheader("📥 ส่งออกข้อมูล")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Create CSV
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="💾 ดาวน์โหลด CSV",
            data=csv_data,
            file_name=f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Print button
        if st.button("🖨️ พิมพ์", use_container_width=True):
            st.info("กรุณาใช้ฟังก์ชัน Print ของเบราว์เซอร์ (Ctrl+P หรือ Cmd+P)")
    
    with col3:
        # New assessment button
        if st.button("📝 ทำแบบประเมินใหม่", use_container_width=True):
            # Reset session state
            st.session_state.page = 1
            st.session_state.client_info = {}
            st.session_state.choices = {}
            st.rerun()
    
    # Display score or analysis (optional)
    st.markdown("---")
    st.subheader("📈 การวิเคราะห์เบื้องต้น")
    
    # Simple scoring based on first option being the best
    score = 0
    for q_num in questions.keys():
        answer = st.session_state.choices.get(f"q{q_num}", "")
        if answer and answer in questions[q_num]["options"]:
            # Give score based on position (first option = highest score)
            position = questions[q_num]["options"].index(answer)
            score += (len(questions[q_num]["options"]) - position)
    
    max_score = sum(len(q["options"]) for q in questions.values())
    percentage = (score / max_score) * 100
    
    st.metric("คะแนนรวม", f"{score}/{max_score}", f"{percentage:.1f}%")
    
    if percentage >= 75:
        st.success("🎉 องค์กรของท่านมีการบริหารจัดการข้อมูลในระดับดีมาก")
    elif percentage >= 50:
        st.warning("📊 องค์กรของท่านมีการบริหารจัดการข้อมูลในระดับปานกลาง มีโอกาสพัฒนาได้อีก")
    else:
        st.error("⚠️ องค์กรของท่านควรปรับปรุงการบริหารจัดการข้อมูลอย่างเร่งด่วน")

# Main app logic
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .stButton > button {
        height: 3rem;
        font-size: 1.1rem;
    }
    .stRadio > div {
        padding-left: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.page == 1:
        page_client_info()
    elif st.session_state.page == 2:
        page_questions()
    elif st.session_state.page == 3:
        page_results()

if __name__ == "__main__":
    main()