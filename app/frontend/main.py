import streamlit as st
from wpl_dashboard import show_wpl_dashboard

# Configure the page
st.set_page_config(
    page_title="Skye Analytics - Cricket",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .tournament-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .status-live {
        color: #00cc00;
        font-weight: bold;
    }
    .status-upcoming {
        color: #ff4b4b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def show_home():
    st.title("🏏 Welcome to Skye Cricket Analytics")
    
    # Featured Tournaments
    st.markdown("### Featured Tournaments")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tournament-card">
            <h3>WPL 2025</h3>
            <p class="status-live">● LIVE NOW</p>
            <p>Comprehensive analytics for Women's Premier League</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tournament-card">
            <h3>Champions Trophy 2025</h3>
            <p class="status-upcoming">COMING SOON</p>
            <p>Get ready for detailed Champions Trophy analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tournament-card">
            <h3>IPL 2025</h3>
            <p class="status-upcoming">COMING SOON</p>
            <p>Stay tuned for comprehensive IPL insights</p>
        </div>
        """, unsafe_allow_html=True)

def show_coming_soon(tournament):
    st.title(tournament.replace(" (Coming Soon)", ""))
    st.info("🚧 This section is under development. Stay tuned for updates!")
    
    st.markdown("### Join the Waitlist")
    col1, col2 = st.columns([2,1])
    with col1:
        email = st.text_input("Enter your email to get notified when this goes live:")
    with col2:
        if st.button("Notify Me"):
            st.success("Thanks for joining the waitlist!")

def main():
    # Sidebar Navigation
    st.sidebar.title("🏏 Cricket Analytics")
    st.sidebar.markdown("---")
    
    # Tournament Selection
    selected_page = st.sidebar.radio(
        "Select Tournament",
        ["Home", "WPL 2025", "Champions Trophy 2025 (Coming Soon)", "IPL 2025 (Coming Soon)"]
    )
    
    # Display selected content
    if selected_page == "Home":
        show_home()
    elif selected_page == "WPL 2025":
        show_wpl_dashboard()
    else:
        show_coming_soon(selected_page)
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("v1.0.0")

if __name__ == "__main__":
    main()