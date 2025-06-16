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

# Define questions, options and scores
questions_with_scores = {
    1: {
        "question": "เวลาท่านต้องการใช้ข้อมูล ท่านรู้หรือไม่ว่ามีข้อมูลอะไรบ้าง และต้องขอที่ไหน / ที่ใคร",
        "options": {
            "รู้ชุดข้อมูลส่วนใหญ่อย่างละเอียด และรู้ว่าอยู่ที่หน่วยงานภายในไหน": 100,
            "รู้ชุดข้อมูลส่วนใหญ่ แต่ไม่รู้ว่าอยู่ที่หน่วยงานภายในไหน": 75,
            "รู้ชุดข้อมูลบางส่วน": 50,
            "ไม่ทราบ": 25
        }
    },
    2: {
        "question": "ท่านทราบหรือไม่ว่าชุดข้อมูลสำคัญขององค์กรท่านมีอะไรบ้าง",
        "options": {
            "ทราบชุดข้อมูลสำคัญ และมีการระบุชุดข้อมูลหลัก (Master Data) เรียบร้อยแล้ว": 100,
            "ทราบชุดข้อมูลสำคัญ แต่ยังไม่มีการระบุชุดข้อมูลหลัก (Master Data) ที่ชัดเจน": 75,
            "ทราบบางส่วนแบบพอสังเขป": 50,
            "ไม่มีการระบุชุดข้อมูลสำคัญ": 25,
            "ไม่ทราบ": 25
        }
    },
    3: {
        "question": "ในการตัดสินใจของท่าน ท่านใช้ข้อมูลหรือประสบการณ์ในการตัดสินใจเป็นหลัก",
        "options": {
            "ส่วนใหญ่ใช้ข้อมูลในการประกอบการตัดสินใจร่วมกับประสบการณ์": 100,
            "ใช้ประสบการณ์ร่วมกับข้อมูลบางส่วนในการประกอบการตัดสินใจเสมอ": 75,
            "ใช้ประสบการณ์เป็นหลัก และพิจารณาข้อมูลประกอบเมื่อมีข้อมูลที่เพียงพอหรือเกี่ยวข้อง": 50,
            "ใช้ประสบการณ์เป็นหลัก": 25
        }
    },
    4: {
        "question": "เมื่อท่านต้องรับผลรายงานจากฝ่ายปฏิบัติการหรือฝ่ายอื่นๆ ท่านใช้เวลานานไหมในการได้รับข้อมูล และสามารถใช้ในการตัดสินใจได้ทันทีหรือไม่",
        "options": {
            "รวดเร็ว และพร้อมใช้": 100,
            "รวดเร็ว อาจมีการปรับแก้เล็กน้อย": 75,
            "ใช้เวลานานและต้องปรับแก้บ่อย": 50,
            "ล่าช้า ใช้เวลานาน และมีอุปสรรค": 25
        }
    },
    5: {
        "question": "องค์กรของท่านมีการกำหนดเป้าหมายหรือกลยุทธ์ด้านข้อมูลหรือไม่ เช่น เป็นศูนย์กลางข้อมูลด้านต่างๆของประเทศ, มุ่งเน้นนำระบบดิจิทัลมาช่วยทำงาน, มุ่งมั่นเปิดเผยข้อมูล เป็นต้น",
        "options": {
            "มีเป้าหมายชัดเจนทั้งองค์กร": 100,
            "มีเป้าหมายแต่ยังไม่ชัดเจน": 75,
            "กำลังอยู่ระหว่างการกำหนด": 50,
            "ไม่มีเป้าหมายด้านข้อมูล": 25,
            "ไม่ทราบ": 25
        }
    },
    6: {
        "question": "ท่านทราบถึงจุดแข็ง จุดอ่อน ด้านข้อมูลขององค์กรท่านหรือไม่",
        "options": {
            "ทราบทั้งหมดอย่างละเอียด": 100,
            "ทราบบางส่วนอย่างละเอียด": 75,
            "ทราบเฉพาะที่อยู่ในขอบเขตความรับผิดชอบของตน": 50,
            "ไม่ทราบ": 25
        }
    },
    7: {
        "question": "องค์กรของท่านมีการแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูลหรือไม่",
        "options": {
            "มี และแต่งตั้งตามมาตรฐานรัฐบาลดิจิทัล": 100,
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่": 75,
            "กำลังดำเนินการ": 50,
            "ไม่มีการแต่งตั้ง": 25,
            "ไม่ทราบ": 25
        }
    },
    8: {
        "question": "องค์กรของท่านมีการจัดตั้งทีมบริหารข้อมูลหรือไม่",
        "options": {
            "มี และจัดตั้งตามมาตรฐานรัฐบาลดิจิทัล": 100,
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่": 75,
            "กำลังดำเนินการ": 50,
            "ไม่มีการจัดตั้ง": 25,
            "ไม่ทราบ": 25
        }
    },
    9: {
        "question": "องค์กรของท่านมีการบริหารข้อมูลผ่านระบบหรือแพลตฟอร์มกลางหรือไม่",
        "options": {
            "มีการใช้งานส่วนใหญ่ภายในองค์กร": 100,
            "มีการใช้งานบางหน่วยงานภายในร่วมกัน": 75,
            "กำลังดำเนินการพัฒนาระบบกลาง หรือแพลตฟอร์มกลาง": 50,
            "ไม่มีแพลตฟอร์มกลาง": 25,
            "ไม่ทราบ": 25
        }
    },
    10: {
        "question": "องค์กรของท่านมีการใช้ข้อมูลร่วมกันระหว่างหน่วยงานภายในมากน้อยแค่ไหน",
        "options": {
            "ใช้ชุดข้อมูลร่วมกันหลายชุด และมีมาตรฐานชัดเจน": 100,
            "ใช้ชุดข้อมูลร่วมกันหลายชุด แต่ยังไม่มีมาตรฐานชัดเจน": 75,
            "ใช้ชุดข้อมูลร่วมกันเพียงเล็กน้อย": 50,
            "ไม่มีการใช้ชุดข้อมูลร่วมกัน": 25,
            "ไม่ทราบ": 25
        }
    }
}

# Define maturity groups
maturity_groups = {
    "ความเข้าใจและความพร้อมในสินทรัพย์ข้อมูลขององค์กร": [1, 2],
    "การขับเคลื่อนองค์กรด้วยข้อมูล": [3, 4],
    "การตั้งเป้าหมายด้านข้อมูล": [5, 6],
    "การจัดตั้งโครงสร้างธรรมาภิบาลข้อมูล": [7, 8],
    "การบริหารจัดการข้อมูล": [9, 10]
}

def get_maturity_level(score):
    """Determine maturity level, emoji and color based on score"""
    if score >= 85:
        return "ดีมาก", "🟢", "#00CC00"  # Green
    elif score >= 65:
        return "ดี", "🟡", "#FFCC00"  # Yellow
    elif score >= 45:
        return "ปานกลาง", "🟠", "#FF9900"  # Orange
    else:
        return "ต้องปรับปรุง", "🔴", "#FF3333"  # Red

def create_progress_bar(score, width=20):
    """Create a text-based progress bar"""
    filled = int((score / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty

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
    progress = len(st.session_state.choices) / len(questions_with_scores)
    st.progress(progress)
    st.caption(f"ความคืบหน้า: {len(st.session_state.choices)} / {len(questions_with_scores)} คำถาม")
    
    with st.form("questions_form"):
        for q_num, q_data in questions_with_scores.items():
            st.markdown(f"### คำถามที่ {q_num}")
            st.markdown(q_data["question"])
            
            # Get saved answer if exists
            saved_answer = st.session_state.choices.get(f"q{q_num}", None)
            options_list = list(q_data["options"].keys())
            default_index = 0
            if saved_answer:
                try:
                    default_index = options_list.index(saved_answer)
                except ValueError:
                    default_index = 0
            
            answer = st.radio(
                f"เลือกคำตอบ:",
                options_list,
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
            for q_num in questions_with_scores.keys():
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
    
    # Calculate scores for each group
    group_scores = {}
    detailed_scores = {}
    
    for group_name, question_ids in maturity_groups.items():
        scores = []
        for q_id in question_ids:
            answer = st.session_state.choices.get(f"q{q_id}", "")
            if answer and answer in questions_with_scores[q_id]["options"]:
                score = questions_with_scores[q_id]["options"][answer]
                scores.append(score)
                detailed_scores[q_id] = {
                    "question": questions_with_scores[q_id]["question"],
                    "answer": answer,
                    "score": score
                }
        
        if scores:
            group_scores[group_name] = sum(scores) / len(scores)
    
    # Calculate overall score
    total_score = sum(group_scores.values()) / len(group_scores) if group_scores else 0
    
    # Display overall score
    st.subheader("📈 คะแนนรวม")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("คะแนนเฉลี่ย", f"{total_score:.1f}/100")
    with col2:
        st.metric("เปอร์เซ็นต์", f"{total_score:.1f}%")
    with col3:
        level, emoji, color = get_maturity_level(total_score)
        st.markdown(f"### {emoji} ระดับ: {level}")
    
    # Overall progress bar
    st.markdown("**ความก้าวหน้าโดยรวม:**")
    progress_bar = create_progress_bar(total_score, 30)
    st.markdown(f"`{progress_bar}` {total_score:.1f}%")
    
    st.markdown("---")
    
    # Display maturity assessment by group with emoji visualization
    st.subheader("📊 ผลการประเมินตามด้าน (Maturity Assessment)")
    
    # Create a visual representation using emojis and text
    for group_name, score in group_scores.items():
        level, emoji, color = get_maturity_level(score)
        
        # Create a container for each group
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {emoji} {group_name}")
                progress_bar = create_progress_bar(score)
                st.markdown(f"`{progress_bar}` **{score:.1f}%** - {level}")
            
            with col2:
                # Display score in large text with color
                st.markdown(f"<h2 style='text-align: center; color: {color};'>{score:.0f}</h2>", 
                          unsafe_allow_html=True)
        
        st.markdown("")  # Add spacing
    
    # Legend
    st.markdown("---")
    st.markdown("### 📋 เกณฑ์การประเมิน:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🟢 **ดีมาก** (85-100%)")
    with col2:
        st.markdown("🟡 **ดี** (65-84%)")
    with col3:
        st.markdown("🟠 **ปานกลาง** (45-64%)")
    with col4:
        st.markdown("🔴 **ต้องปรับปรุง** (0-44%)")
    
    st.markdown("---")
    
    # Display detailed scores by group
    st.subheader("📋 รายละเอียดคะแนนแต่ละด้าน")
    
    for group_name, question_ids in maturity_groups.items():
        with st.expander(f"{group_name} - {group_scores[group_name]:.1f}%"):
            for q_id in question_ids:
                if q_id in detailed_scores:
                    detail = detailed_scores[q_id]
                    st.write(f"**คำถามที่ {q_id}:** {detail['question'][:50]}...")
                    st.write(f"คำตอบ: {detail['answer']}")
                    st.write(f"คะแนน: {detail['score']}/100")
                    st.markdown("---")
    
    # Export options
    st.markdown("---")
    st.subheader("📥 ส่งออกข้อมูล")
    
    # Prepare data for export
    export_data = []
    for q_id, detail in detailed_scores.items():
        export_data.append({
            "คำถามที่": q_id,
            "คำถาม": detail["question"],
            "คำตอบ": detail["answer"],
            "คะแนน": detail["score"]
        })
    
    # Add group scores
    for group_name, score in group_scores.items():
        export_data.append({
            "คำถามที่": f"กลุ่ม: {group_name}",
            "คำถาม": "",
            "คำตอบ": "",
            "คะแนน": f"{score:.1f}"
        })
    
    export_data.append({
        "คำถามที่": "คะแนนรวม",
        "คำถาม": "",
        "คำตอบ": "",
        "คะแนน": f"{total_score:.1f}"
    })
    
    df_export = pd.DataFrame(export_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Create CSV
        csv_data = df_export.to_csv(index=False, encoding='utf-8-sig')
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
    
    # Recommendations based on scores
    st.markdown("---")
    st.subheader("💡 ข้อเสนอแนะ")
    
    # Find areas that need improvement
    weak_areas = [(group, score) for group, score in group_scores.items() if score < 65]
    
    if weak_areas:
        st.warning("**ด้านที่ควรพัฒนาเป็นลำดับแรก:**")
        for area, score in sorted(weak_areas, key=lambda x: x[1]):
            st.write(f"- {area} (คะแนน: {score:.1f}%)")
    else:
        st.success("องค์กรของท่านมีการบริหารจัดการข้อมูลในระดับดีทุกด้าน!")

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