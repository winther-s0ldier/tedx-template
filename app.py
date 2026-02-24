import streamlit as st
from datetime import date, datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TEDx GGSIPU EDC | Invitation Generator",
    page_icon="🔴",
    layout="centered"
)

def get_date_suffix(day: int) -> str:
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def format_ordinal_date(selected_date):
    dt = datetime.combine(selected_date, datetime.min.time())
    day = dt.day
    suffix = get_date_suffix(day)
    return dt.strftime(f"{day}{suffix} %B, %Y")

def generate_html(speaker_name, why_you, reply_date):
    with open("template.html", "r", encoding="utf-8") as f:
        template_content = f.read()

    formatted_date = format_ordinal_date(reply_date)

    final_html = template_content.replace("{{SpeakerName}}", speaker_name)
    final_html = final_html.replace("{{WhyYouContent}}", why_you)
    final_html = final_html.replace("{{ReplyDate}}", formatted_date)

    return final_html

st.image(
    "https://res.cloudinary.com/dtizjcnzm/image/upload/v1740243074/yrxsqk33sufg9jhprg1s.png",
    use_container_width=True
)

st.title("Invitation Generator")
st.markdown("Generate personalised TEDx invitations for your guest speakers.")

speaker_name = st.text_input("Speaker Name", placeholder="e.g. Dr. Satya Nadella")

why_you = st.text_area(
    "Why You Section",
    placeholder="Describe why this speaker is perfect for SANGAM..."
)

reply_date = st.date_input(
    "Reply By Date",
    value=date(2026, 3, 1)
)

if st.button("🚀 Generate Invitation", use_container_width=True):

    if not speaker_name or not why_you:
        st.error("Please fill in all fields.")
        st.stop()

    generated_html = generate_html(
        speaker_name,
        why_you,
        reply_date
    )

    st.success("Invitation generated successfully!")

    st.divider()
    st.subheader("Preview")

    components.html(generated_html, height=600, scrolling=True)

    st.download_button(
        label="📥 Download HTML Invitation",
        data=generated_html,
        file_name=f"Invitation_{speaker_name.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )
