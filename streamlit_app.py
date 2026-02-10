import streamlit as st
import re
import pandas as pd
from collections import defaultdict

# Page configuration for a professional data tool appearance
st.set_page_config(
    page_title="AVANA Marketing",
    page_icon="📧",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #4f46e5;
        color: white;
    }
    .skipped-box {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ff9800;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.title("📧 AVANA Marketing")
st.markdown("Automated AI-based selection tool for domain-specific email filtering and marketing extraction.")

# Sidebar/Filters Column
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.header("Data Input")
    raw_text = st.text_area(
        "Paste Email List",
        height=250,
        placeholder="Paste your raw list of emails here...",
        help="Supports any text format containing email addresses."
    )
    
    # Real-time counter logic for Streamlit
    total_raw_detected = 0
    if raw_text:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        temp_found = re.findall(email_pattern, raw_text)
        total_raw_detected = len(set(e.lower() for e in temp_found))
        st.success(f"📊 **{total_raw_detected}** unique emails detected in your upload.")
    
    st.header("Extraction Settings")
    max_per_domain = st.slider(
        "Max emails per domain", 
        min_value=1, 
        max_value=200, 
        value=5,
        help="To prevent skipping emails from large domain lists, increase this value."
    )
    
    default_roles = "ceo, founder, cto, cfo, president, director, lead, manager, vp"
    role_input = st.text_input(
        "Role Filter Keywords", 
        value=default_roles,
        help="Comma separated keywords to prioritize matching emails."
    )
    keywords = [k.strip().lower() for k in role_input.split(",") if k.strip()]

with col2:
    st.header("Extraction Results")
    
    if st.button("Run Extraction", type="primary"):
        if not raw_text:
            st.warning("Please enter some email data to process.")
        else:
            # 1. Extraction (Preserving sequence)
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            found_emails = re.findall(email_pattern, raw_text)
            
            seen = set()
            unique_emails = []
            for e in found_emails:
                e_low = e.lower()
                if e_low not in seen:
                    seen.add(e_low)
                    unique_emails.append(e_low)
            
            # 2. Grouping by Domain
            domain_map = defaultdict(list)
            domain_order = []
            for email in unique_emails:
                try:
                    domain = email.split('@')[1]
                    if domain not in domain_map:
                        domain_order.append(domain)
                    domain_map[domain].append(email)
                except IndexError:
                    continue
            
            # 3. Selection Logic
            final_selection = []
            skipped_emails = []
            
            for domain in domain_order:
                emails = domain_map[domain]
                priority = []
                others = []
                for e in emails:
                    local_part = e.split('@')[0]
                    if any(k in local_part for k in keywords):
                        priority.append(e)
                    else:
                        others.append(e)
                
                priority.sort(key=len)
                others.sort()
                
                # Selection
                top_selection = (priority + others)[:max_per_domain]
                top_set = set(top_selection)
                
                for s in top_selection:
                    final_selection.append({
                        "Domain": domain,
                        "Email": s,
                        "Type": "🎯 Match" if s in priority else "✉️ General"
                    })
                
                # Track Skipped
                for e in emails:
                    if e not in top_set:
                        skipped_emails.append(e)
            
            # 4. Display Results
            if final_selection:
                df = pd.DataFrame(final_selection)
                
                s1, s2, s3 = st.columns(3)
                s1.metric("Uploaded Emails", len(unique_emails))
                s2.metric("Selected Count", len(final_selection))
                s3.metric("Skipped Count", len(skipped_emails))
                
                st.subheader("Selected Emails")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Selected (CSV)",
                    data=csv,
                    file_name='avana_selected_emails.csv',
                    mime='text/csv',
                )
                
                # 5. Display Skipped List Below
                st.divider()
                st.subheader("🚫 Skipped Emails List")
                if skipped_emails:
                    st.info(f"The following {len(skipped_emails)} emails were filtered out based on your settings.")
                    skipped_df = pd.DataFrame(skipped_emails, columns=["Skipped Email Address"])
                    st.dataframe(skipped_df, use_container_width=True, hide_index=True)
                else:
                    st.write("No emails were skipped! All detected emails were included in the results.")
            else:
                st.error("No valid emails found in the input text.")
    else:
        st.info("Results and skipped emails will appear here after processing.")

st.divider()
st.caption("Built with AVANA Marketing AI Engine.")
