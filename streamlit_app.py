import streamlit as st
from datetime import datetime
import pandas as pd   # only needed for any later export you might add

# ────────────────────────────────────────────────────────────────────────────────
# Page configuration
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="แบบฟอร์มประเมินการใช้ข้อมูล",
    page_icon="📊",
    layout="wide"
)

# ────────────────────────────────────────────────────────────────────────────────
# Session-state initialisation
# ────────────────────────────────────────────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'client_info' not in st.session_state:
    st.session_state.client_info = {}
if 'choices' not in st.session_state:
    st.session_state.choices = {}
if 'assessment_type' not in st.session_state:
    st.session_state.assessment_type = None

# ────────────────────────────────────────────────────────────────────────────────
# Questions, options and scores  (unchanged)
# ────────────────────────────────────────────────────────────────────────────────
questions_with_scores = {
    1: { "question": "เวลาท่านต้องการใช้ข้อมูล ท่านรู้หรือไม่ว่ามีข้อมูลอะไรบ้าง และต้องขอที่ไหน / ที่ใคร",
        "options": {
            "ทราบชุดข้อมูลส่วนใหญ่อย่างละเอียด และรู้ว่าอยู่ที่หน่วยงานภายในไหน": 100,
            "ทราบชุดข้อมูลส่วนใหญ่ แต่ไม่รู้ว่าอยู่ที่หน่วยงานภายในไหน": 75,
            "ทราบชุดข้อมูลบางส่วน": 50,
            "ไม่ทราบ": 25 } },
    2: { "question": "ท่านทราบหรือไม่ว่าชุดข้อมูลสำคัญขององค์กรท่านมีอะไรบ้าง",
        "options": {
            "ทราบชุดข้อมูลสำคัญ และมีการระบุชุดข้อมูลหลัก (Master Data) เรียบร้อยแล้ว": 100,
            "ทราบชุดข้อมูลสำคัญ แต่ยังไม่มีการระบุชุดข้อมูลหลัก (Master Data) ที่ชัดเจน": 75,
            "ทราบบางส่วนแบบพอสังเขป": 50,
            "ไม่มีการระบุชุดข้อมูลสำคัญ": 25,
            "ไม่ทราบ": 25 } },
    3: { "question": "ในการตัดสินใจของท่าน ท่านใช้ข้อมูลหรือประสบการณ์ในการตัดสินใจเป็นหลัก",
        "options": {
            "ส่วนใหญ่ใช้ข้อมูลในการประกอบการตัดสินใจร่วมกับประสบการณ์": 100,
            "ใช้ประสบการณ์ร่วมกับข้อมูลบางส่วนในการประกอบการตัดสินใจเสมอ": 75,
            "ใช้ประสบการณ์เป็นหลัก และพิจารณาข้อมูลประกอบเมื่อมีข้อมูลที่เพียงพอหรือเกี่ยวข้อง": 50,
            "ใช้ประสบการณ์เป็นหลัก": 25 } },
    4: { "question": "เมื่อท่านต้องรับผลรายงานจากฝ่ายปฏิบัติการหรือฝ่ายอื่นๆ ท่านใช้เวลานานไหมในการได้รับข้อมูล และสามารถใช้ในการตัดสินใจได้ทันทีหรือไม่",
        "options": {
            "รวดเร็ว และพร้อมใช้": 100,
            "รวดเร็ว อาจมีการปรับแก้เล็กน้อย": 75,
            "ใช้เวลานานและต้องปรับแก้บ่อย": 50,
            "ล่าช้า ใช้เวลานาน และมีอุปสรรค": 25 } },
    5: { "question": "องค์กรของท่านมีการกำหนดเป้าหมายหรือกลยุทธ์ด้านข้อมูลหรือไม่...",
        "options": {
            "มีเป้าหมายชัดเจนทั้งองค์กร": 100,
            "มีเป้าหมายแต่ยังไม่ชัดเจน": 75,
            "กำลังอยู่ระหว่างการกำหนด": 50,
            "ไม่มีเป้าหมายด้านข้อมูล": 25,
            "ไม่ทราบ": 25 } },
    6: { "question": "ท่านทราบถึงจุดแข็ง จุดอ่อน ด้านข้อมูลขององค์กรท่านหรือไม่",
        "options": {
            "ทราบทั้งหมดอย่างละเอียด": 100,
            "ทราบบางส่วนอย่างละเอียด": 75,
            "ทราบเฉพาะที่อยู่ในขอบเขตความรับผิดชอบของตน": 50,
            "ไม่ทราบ": 25 } },
    7: { "question": "องค์กรของท่านมีการแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูลหรือไม่",
        "options": {
            "มี และแต่งตั้งตามมาตรฐานรัฐบาลดิจิทัล": 100,
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่": 75,
            "กำลังดำเนินการ": 50,
            "ไม่มีการแต่งตั้ง": 25,
            "ไม่ทราบ": 25 } },
    8: { "question": "องค์กรของท่านมีการจัดตั้งทีมบริหารข้อมูลหรือไม่",
        "options": {
            "มี และจัดตั้งตามมาตรฐานรัฐบาลดิจิทัล": 100,
            "มี แต่ไม่มั่นใจว่าถูกต้องตามมาตรฐานรัฐบาลดิจิทัลหรือไม่": 75,
            "กำลังดำเนินการ": 50,
            "ไม่มีการจัดตั้ง": 25,
            "ไม่ทราบ": 25 } },
    9: { "question": "องค์กรของท่านมีการบริหารข้อมูลผ่านระบบหรือแพลตฟอร์มกลางหรือไม่",
        "options": {
            "มีการใช้งานส่วนใหญ่ภายในองค์กร": 100,
            "มีการใช้งานบางหน่วยงานภายในร่วมกัน": 75,
            "กำลังดำเนินการพัฒนาระบบกลาง หรือแพลตฟอร์มกลาง": 50,
            "ไม่มีแพลตฟอร์มกลาง": 25,
            "ไม่ทราบ": 25 } },
    10: { "question": "องค์กรของท่านมีการใช้ข้อมูลร่วมกันระหว่างหน่วยงานภายในมากน้อยแค่ไหน",
        "options": {
            "ใช้ชุดข้อมูลร่วมกันหลายชุด และมีมาตรฐานชัดเจน": 100,
            "ใช้ชุดข้อมูลร่วมกันหลายชุด แต่ยังไม่มีมาตรฐานชัดเจน": 75,
            "ใช้ชุดข้อมูลร่วมกันเพียงเล็กน้อย": 50,
            "ไม่มีการใช้ชุดข้อมูลร่วมกัน": 25,
            "ไม่ทราบ": 25 } }
}

# ────────────────────────────────────────────────────────────────────────────────
# Maturity-group definitions
# ────────────────────────────────────────────────────────────────────────────────
maturity_groups = {
    "ความเข้าใจและความพร้อมในสินทรัพย์ข้อมูลขององค์กร": [1, 2],
    "การขับเคลื่อนองค์กรด้วยข้อมูล":               [3, 4],
    "การตั้งเป้าหมายด้านข้อมูล":                  [5, 6],
    "การจัดตั้งโครงสร้างธรรมาภิบาลข้อมูล":        [7, 8],
    "การบริหารจัดการข้อมูล":                      [9, 10]
}

# ────────────────────────────────────────────────────────────────────────────────
# Helper functions
# ────────────────────────────────────────────────────────────────────────────────
def get_maturity_level_pct(score: float):
    """Classify a 0-100 *percentage* score (overall display)."""
    if score >= 85:
        return "ดีมาก", "🟢", "#00CC00"
    elif score >= 65:
        return "ดี", "🟡", "#FFCC00"
    elif score >= 45:
        return "ปานกลาง", "🟠", "#FF9900"
    else:
        return "ต้องปรับปรุง", "🔴", "#FF3333"

def get_maturity_level_total(total: int):
    """Classify a *total* on 0-200 scale."""
    if total == 200:
        return "ดีมาก", "🟢", "#00CC00"
    elif total >= 150:
        return "ดี", "🟡", "#FFCC00"
    elif total >= 100:
        return "ปานกลาง", "🟠", "#FF9900"
    else:           # 50-99
        return "ต้องปรับปรุง", "🔴", "#FF3333"

def create_progress_bar(score: float, width: int = 20) -> str:
    filled = int((score / 100) * width)
    return "█" * filled + "░" * (width - filled)

# ────────────────────────────────────────────────────────────────────────────────
# Page 1  –  Client information
# ────────────────────────────────────────────────────────────────────────────────
def page_client_info():
    st.title("📝 แบบฟอร์มประเมินการใช้ข้อมูล")
    st.subheader("ข้อมูลผู้กรอกแบบฟอร์ม")

    with st.form("client_form"):
        c1, c2 = st.columns(2)
        with c1:
            org_name = st.text_input("ชื่อองค์กร",  value=st.session_state.client_info.get("org_name", ""))
            phone    = st.text_input("เบอร์โทรศัพท์", value=st.session_state.client_info.get("phone",    ""))
        with c2:
            full_name = st.text_input("ชื่อ",   value=st.session_state.client_info.get("full_name", ""))
            email     = st.text_input("อีเมล", value=st.session_state.client_info.get("email",     ""))

        submitted = st.form_submit_button("Next ➡️", use_container_width=True)
        if submitted:
            if all([org_name, phone, full_name, email]):
                st.session_state.client_info = {
                    "org_name":  org_name,
                    "phone":     phone,
                    "full_name": full_name,
                    "email":     email
                }
                st.session_state.page = 2
                st.rerun()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบทุกช่อง")

# ────────────────────────────────────────────────────────────────────────────────
# Page 2 – choose assessment type
# ────────────────────────────────────────────────────────────────────────────────
def page_assessment_selection():
    st.title("📊 เลือกประเภทการประเมิน")
    st.markdown("### เลือกการประเมินองค์กรของท่าน")
    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📈 ประเมินความพร้อมองค์กรด้านยุทธศาสตร์ข้อมูล",
                     type="primary", use_container_width=True):
            st.session_state.assessment_type = "strategy"
            st.session_state.page = 3
            st.rerun()
    with c2:
        if st.button("🏛️ ประเมินระดับความพร้อมธรรมาภิบาลข้อมูล",
                     type="secondary", use_container_width=True):
            js = ("window.open("
                  "'https://www.jotform.com/build/251632288260052?"
                  "iak=6553c26b661da8b9792faf1ab086afea-f68803ebbd499c6c',"
                  "'_blank');")
            st.components.v1.html(f"<script>{js}</script>", height=0)
            st.info("กำลังเปิดแบบประเมินธรรมาภิบาลข้อมูลในหน้าต่างใหม่...")

    st.markdown("---")
    if st.button("⬅️ กลับ", use_container_width=True):
        st.session_state.page = 1
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────────
# Page 3 – questions
# ────────────────────────────────────────────────────────────────────────────────
def page_questions():
    st.title("📊 แบบประเมินการใช้ข้อมูลในองค์กร")
    progress = len(st.session_state.choices) / len(questions_with_scores)
    st.progress(progress)
    st.caption(f"ความคืบหน้า: {len(st.session_state.choices)} / {len(questions_with_scores)} คำถาม")

    with st.form("questions_form"):
        for q_num, q_data in questions_with_scores.items():
            st.markdown(f"### คำถามที่ {q_num}")
            st.markdown(q_data["question"])

            default_idx = 0
            saved = st.session_state.choices.get(f"q{q_num}")
            if saved:
                try:
                    default_idx = list(q_data["options"]).index(saved)
                except ValueError:
                    default_idx = 0

            answer = st.radio("เลือกคำตอบ:",
                              list(q_data["options"]),
                              index=default_idx,
                              key=f"q{q_num}")
            st.markdown("---")

        c1, c2 = st.columns(2)
        back_btn  = c1.form_submit_button("⬅️ กลับ",              use_container_width=True)
        send_btn  = c2.form_submit_button("ส่งแบบฟอร์ม ✅", type="primary", use_container_width=True)

        if back_btn:
            st.session_state.page = 1
            st.rerun()
        if send_btn:
            for q in questions_with_scores:
                st.session_state.choices[f"q{q}"] = st.session_state[f"q{q}"]
            st.session_state.page = 4
            st.rerun()

# ────────────────────────────────────────────────────────────────────────────────
# Page 4 – results
# ────────────────────────────────────────────────────────────────────────────────
def page_results():
    st.title("✅ สรุปผลการประเมิน")
    st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")

    # ── 1. compute 0-200 totals for each group
    group_totals  = {}
    group_display = {}
    for g_name, q_ids in maturity_groups.items():
        total = sum(
            questions_with_scores[q]["options"]
            .get(st.session_state.choices.get(f"q{q}", ""), 0)
            for q in q_ids
        )                            # min 50, max 200
        group_totals[g_name]  = total
        group_display[g_name] = total / 2    # scale to 0-100 for UI

    # ── 2. overall score (0-100) for display
    overall_total   = sum(group_totals.values())     # 0-1000
    overall_display = overall_total / 10             # 0-100

    # ── 3. headline box
    st.subheader("📈 คะแนนรวม")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("คะแนนเฉลี่ย", f"{overall_display:.1f}/100")
    with c2:
        st.metric("เปอร์เซ็นต์", f"{overall_display:.1f}%")
    with c3:
        level, emoji, colour = get_maturity_level_pct(overall_display)
        st.markdown(f"### {emoji} ระดับ: {level}")

    st.markdown("**ความก้าวหน้าโดยรวม:**")
    st.markdown(f"`{create_progress_bar(overall_display,30)}` {overall_display:.1f}%")
    st.markdown("---")

    # ── 4. per-group display
    st.subheader("📊 ผลการประเมินตามด้าน (Maturity Assessment)")
    for g_name in maturity_groups:
        total   = group_totals[g_name]      # 0-200
        display = group_display[g_name]     # 0-100
        level, emoji, colour = get_maturity_level_total(total)

        with st.container():
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {emoji} {g_name}")
                st.markdown(f"`{create_progress_bar(display)}` **{display:.1f}%** - {level}")
            with c2:
                st.markdown(
                    f"<h2 style='text-align:center;color:{colour};'>{display:.0f}</h2>",
                    unsafe_allow_html=True
                )
        st.markdown("")

    # ── 5. Legend
    st.markdown("---")
    st.markdown("### 📋 เกณฑ์การประเมิน:")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("🟢 **ดีมาก** (85-100%)")
    with c2: st.markdown("🟡 **ดี** (65-84%)")
    with c3: st.markdown("🟠 **ปานกลาง** (45-64%)")
    with c4: st.markdown("🔴 **ต้องปรับปรุง** (0-44%)")
    st.markdown("---")

    # ── 6. recommendations
    st.subheader("💡 ข้อเสนอแนะ")
    weak = [(g, sc) for g, sc in group_display.items() if sc < 65]
    if weak:
        st.warning("**ด้านที่ควรพัฒนาเป็นลำดับแรก:**")
        for g, sc in sorted(weak, key=lambda x: x[1]):
            st.write(f"- {g} (คะแนน: {sc:.1f}%)")
    else:
        st.success("องค์กรของท่านมีการบริหารจัดการข้อมูลในระดับดีทุกด้าน!")

    # ── 7. client info
    st.markdown("---")
    st.subheader("📋 ข้อมูลผู้กรอกแบบฟอร์ม")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**ชื่อองค์กร:** {st.session_state.client_info.get('org_name','')}")
        st.write(f"**เบอร์โทรศัพท์:** {st.session_state.client_info.get('phone','')}")
    with c2:
        st.write(f"**ชื่อ-นามสกุล:** {st.session_state.client_info.get('full_name','')}")
        st.write(f"**อีเมล:** {st.session_state.client_info.get('email','')}")

    # ── 8. new assessment button
    st.markdown("---")
    st.subheader("📝 ทำแบบประเมิน")
    if st.button("📝 ทำแบบประเมินใหม่", type="primary", use_container_width=True):
        st.session_state.page            = 2
        st.session_state.choices         = {}
        st.session_state.assessment_type = None
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────────
# Main router
# ────────────────────────────────────────────────────────────────────────────────
def main():
    # minimal CSS tweak for better buttons
    st.markdown("""
    <style>
    .stButton > button { height:3rem; font-size:1.1rem; }
    .stRadio > div    { padding-left:1rem; }
    </style>
    """, unsafe_allow_html=True)

    if   st.session_state.page == 1: page_client_info()
    elif st.session_state.page == 2: page_assessment_selection()
    elif st.session_state.page == 3: page_questions()
    elif st.session_state.page == 4: page_results()

if __name__ == "__main__":
    main()
