import streamlit as st
import requests
from datetime import date
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="TEDx GGSIPU EDC | Invitation Generator",
    page_icon="🔴",
    layout="centered"
)

# Constants
BACKEND_URL = "http://localhost:8000/generate"

def main():
    st.image("https://res.cloudinary.com/dtizjcnzm/image/upload/v1740243074/yrxsqk33sufg9jhprg1s.png", use_container_width=True)
    st.title("Invitation Generator")
    st.markdown("Generate personalized TEDx invitations for your guest speakers.")

    with st.container():
        st.subheader("Speaker Details")
        
        speaker_name = st.text_input("Speaker Name", placeholder="e.g. Dr. Satya Nadella")
        
        why_you = st.text_area(
            "Why You Section", 
            placeholder="Describe why this speaker is perfect for SANGAM...",
            help="This content will appear under the 'Why YOU?' heading."
        )
        
        reply_date = st.date_input(
            "Reply By Date", 
            value=date(2026, 3, 1),
            help="Deadline for the speaker to confirm."
        )

        generate_btn = st.button("🚀 Generate Invitation", use_container_width=True)

    if generate_btn:
        if not speaker_name or not why_you:
            st.error("Please fill in all fields before generating.")
            return

        payload = {
            "speaker_name": speaker_name,
            "why_you": why_you,
            "reply_date": reply_date.isoformat()
        }

        with st.spinner("Communicating with backend..."):
            try:
                response = requests.post(BACKEND_URL, json=payload, timeout=10)
                
                if response.status_code == 200:
                    generated_html = response.text
                    st.success("Invitation generated successfully!")

                    # Preview Section
                    st.divider()
                    st.subheader("Preview")
                    components.html(generated_html, height=600, scrolling=True)

                    # Download Action
                    st.download_button(
                        label="📥 Download HTML Invitation",
                        data=generated_html,
                        file_name=f"Invitation_{speaker_name.replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                else:
                    st.error(f"Backend Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the Backend. Please ensure FastAPI is running on port 8000.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()