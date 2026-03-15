import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import hashlib
import json
import os
from PIL import Image
import io
import base64
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Cantilan-eCivil",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
def load_css():
    st.markdown("""
    <style>
    /* Mobile-friendly adjustments */
    .stApp {
        max-width: 100%;
        padding: 0px;
    }
    
    /* Container styling */
    .service-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .service-header {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    .apply-button {
        background-color: #28a745;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        border: none;
        width: 100%;
        font-size: 16px;
        margin-top: 10px;
    }
    
    .apply-button:hover {
        background-color: #218838;
    }
    
    /* Profile section styling */
    .profile-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .profile-pic {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid white;
        margin: 0 auto;
    }
    
    .verification-badge {
        background-color: #ffc107;
        color: #000;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 5px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 5px;
    }
    
    /* Card styling */
    .dashboard-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
    }
    
    .admin-stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Recent applications */
    .recent-app {
        background-color: white;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border: 1px solid #e9ecef;
    }
    
    .status-badge {
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .status-pending { background-color: #fff3cd; color: #856404; }
    .status-approved { background-color: #d4edda; color: #155724; }
    .status-rejected { background-color: #f8d7da; color: #721c24; }
    .status-processing { background-color: #cce5ff; color: #004085; }
    
    /* Success message styling */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Admin container */
    .admin-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
    
    .staff-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'applications' not in st.session_state:
        st.session_state.applications = []
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'profile_verified' not in st.session_state:
        st.session_state.profile_verified = False
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = 'dashboard_overview'
    if 'staff_members' not in st.session_state:
        st.session_state.staff_members = [
            {"id": 1, "name": "John Doe", "email": "john@cantilan.gov.ph", "role": "Processor", "status": "Active"},
            {"id": 2, "name": "Jane Smith", "email": "jane@cantilan.gov.ph", "role": "Verifier", "status": "Active"},
            {"id": 3, "name": "Mike Wilson", "email": "mike@cantilan.gov.ph", "role": "Admin", "status": "Active"}
        ]
    if 'payments' not in st.session_state:
        st.session_state.payments = [
            {"id": "PAY001", "tracking": "BC-20240115-1234", "amount": 150, "method": "Cash", "status": "Pending Verification", "date": "2024-01-15"},
            {"id": "PAY002", "tracking": "BP-20240114-5678", "amount": 500, "method": "E-Wallet", "status": "Verified", "date": "2024-01-14"},
            {"id": "PAY003", "tracking": "BCL-20240113-9012", "amount": 50, "method": "Cash", "status": "Pending Verification", "date": "2024-01-13"}
        ]

# User authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(first_name, last_name, email, phone, password):
    # Check if user already exists
    if email in st.session_state.users:
        return False, "Email already registered"
    
    user_id = f"user_{len(st.session_state.users) + 1}"
    st.session_state.users[email] = {
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'password': hash_password(password),
        'verified': False,
        'profile_pic': None,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return True, "Registration successful"

def login_user(email, password):
    if email in st.session_state.users:
        if st.session_state.users[email]['password'] == hash_password(password):
            return True, "Login successful"
        else:
            return False, "Invalid password"
    return False, "Email not found"

# Admin credentials
ADMIN_CREDENTIALS = {
    'admin@cantilan.gov.ph': hash_password('admin123')
}

# Main app structure
def main():
    load_css()
    init_session_state()
    
    # Sidebar navigation
    if st.session_state.logged_in or st.session_state.admin_logged_in:
        with st.sidebar:
            st.image("https://via.placeholder.com/150x50?text=Cantilan-eCivil", use_column_width=True)
            st.markdown("---")
            
            if st.session_state.admin_logged_in:
                # Admin sidebar menu
                if st.button("📊 Dashboard Overview", use_container_width=True):
                    st.session_state.admin_page = 'dashboard_overview'
                    st.rerun()
                if st.button("📝 Manage Request", use_container_width=True):
                    st.session_state.admin_page = 'manage_request'
                    st.rerun()
                if st.button("💰 Manage Payment", use_container_width=True):
                    st.session_state.admin_page = 'manage_payment'
                    st.rerun()
                if st.button("📈 Reports & Analytics", use_container_width=True):
                    st.session_state.admin_page = 'reports_analytics'
                    st.rerun()
                if st.button("👥 User Management", use_container_width=True):
                    st.session_state.admin_page = 'user_management'
                    st.rerun()
            else:
                # Regular user sidebar menu
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                if st.button("👤 Profile", use_container_width=True):
                    st.session_state.page = 'profile'
                    st.rerun()
                if st.button("🏛️ Local Government Unit", use_container_width=True):
                    st.session_state.page = 'lgu'
                    st.rerun()
                if st.button("🏘️ Barangay Government Unit", use_container_width=True):
                    st.session_state.page = 'barangay'
                    st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.admin_logged_in = False
                st.session_state.username = None
                st.session_state.page = 'login'
                st.rerun()
    
    # Page routing
    if not st.session_state.logged_in and not st.session_state.admin_logged_in:
        show_login_page()
    elif st.session_state.admin_logged_in:
        show_admin_dashboard()
    else:
        if st.session_state.page == 'dashboard':
            show_dashboard()
        elif st.session_state.page == 'profile':
            show_profile()
        elif st.session_state.page == 'lgu':
            show_lgu_services()
        elif st.session_state.page == 'barangay':
            show_barangay_services()

def show_login_page():
    st.title("🏛️ Cantilan-eCivil")
    st.markdown("---")
    
    # Check if we should show login form after registration
    if st.session_state.registration_success:
        st.success("Registration successful! Please login with your credentials.")
        st.session_state.registration_success = False
    
    tab1, tab2, tab3 = st.tabs(["User Login", "User Register", "Admin Login"])
    
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True):
            if email and password:
                success, message = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = email
                    st.session_state.page = 'dashboard'
                    st.session_state.profile_verified = st.session_state.users[email]['verified']
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter email and password")
    
    with tab2:
        st.subheader("Create New Account")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*", key="reg_firstname")
        with col2:
            last_name = st.text_input("Last Name*", key="reg_lastname")
        
        email = st.text_input("Email*", key="reg_email")
        phone = st.text_input("Phone Number*", key="reg_phone")
        password = st.text_input("Password*", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password*", type="password", key="reg_confirm_password")
        
        if st.button("Register", use_container_width=True):
            # Validate inputs
            if not all([first_name, last_name, email, phone, password, confirm_password]):
                st.error("Please fill in all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                success, message = register_user(first_name, last_name, email, phone, password)
                if success:
                    st.session_state.registration_success = True
                    st.rerun()
                else:
                    st.error(message)
    
    with tab3:
        st.subheader("Admin Login")
        admin_email = st.text_input("Admin Email", key="admin_email")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        
        if st.button("Admin Login", use_container_width=True):
            if admin_email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[admin_email] == hash_password(admin_password):
                st.session_state.admin_logged_in = True
                st.session_state.admin_page = 'dashboard_overview'
                st.rerun()
            else:
                st.error("Invalid admin credentials")

def show_dashboard():
    st.title("Dashboard")
    
    # Get user-specific applications (filter by user)
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    # Calculate statistics
    active_count = len([app for app in user_apps if app['status'] in ['Processing', 'Pending']])
    completed_count = len([app for app in user_apps if app['status'] == 'Approved'])
    total_count = len(user_apps)
    
    # Statistics cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <h3 style="margin:0; color:#666;">Active</h3>
            <h2 style="margin:0; color:#28a745;">{active_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <h3 style="margin:0; color:#666;">Completed</h3>
            <h2 style="margin:0; color:#28a745;">{completed_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <h3 style="margin:0; color:#666;">Total</h3>
            <h2 style="margin:0; color:#28a745;">{total_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Recent Applications")
    
    # Show recent applications or empty state
    if user_apps:
        recent_apps = sorted(user_apps, key=lambda x: x['date'], reverse=True)[:5]
        for app in recent_apps:
            status_class = f"status-{app['status'].lower()}"
            st.markdown(f"""
            <div class="recent-app">
                <div style="display:flex; justify-content:space-between;">
                    <strong>{app['type']}</strong>
                    <span class="status-badge {status_class}">{app['status']}</span>
                </div>
                <div style="color:#666; font-size:12px;">Tracking: {app['tracking']}</div>
                <div style="color:#666; font-size:12px;">{app['date']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No applications yet. Start by applying for a service from the LGU or Barangay sections.")

def show_profile():
    st.title("Profile")
    
    user_data = st.session_state.users.get(st.session_state.username, {})
    
    # Profile header
    st.markdown(f"""
    <div class="profile-header">
        <div style="text-align:center;">
            <div style="font-size:50px;">👤</div>
            <h2>{user_data.get('first_name', '')} {user_data.get('last_name', '')}</h2>
            <p>{user_data.get('email', '')}</p>
            <span class="verification-badge">{'✅ Verified' if st.session_state.profile_verified else '⚠️ Not Verified'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Profile completion
    st.subheader("Profile Completion")
    progress = 60 if not st.session_state.profile_verified else 100
    st.progress(progress/100)
    st.caption(f"{progress}% Complete")
    
    # Personal Information
    with st.expander("Personal Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", value=user_data.get('first_name', ''), disabled=True)
        with col2:
            st.text_input("Last Name", value=user_data.get('last_name', ''), disabled=True)
        
        st.text_input("Email", value=user_data.get('email', ''), disabled=True)
        st.text_input("Phone", value=user_data.get('phone', ''), disabled=True)
    
    # Account Verification
    st.subheader("Account Verification")
    if not st.session_state.profile_verified:
        st.info("Please verify your account by uploading a valid ID")
        uploaded_file = st.file_uploader("Upload Valid ID", type=['png', 'jpg', 'jpeg', 'pdf'])
        if uploaded_file and st.button("Submit for Verification", use_container_width=True):
            st.session_state.profile_verified = True
            st.session_state.users[st.session_state.username]['verified'] = True
            st.success("Verification submitted successfully! Your account is now verified.")
            st.rerun()
    else:
        st.success("✅ Your account is verified")
    
    # My Applications
    st.subheader("My Applications")
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    if user_apps:
        for app in user_apps[:5]:  # Show last 5 applications
            with st.container():
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.write(f"**{app['type']}**")
                with col2:
                    st.write(app['date'])
                with col3:
                    status_color = "🟡" if app['status'] == "Processing" else "🟢" if app['status'] == "Approved" else "🔴"
                    st.write(f"{status_color}")
                with st.expander("View Details"):
                    st.write(f"Tracking Number: {app['tracking']}")
                    st.write(f"Status: {app['status']}")
                    if 'purpose' in app:
                        st.write(f"Purpose: {app['purpose']}")
    else:
        st.info("No applications yet")
    
    # Account Settings
    st.subheader("Account Settings")
    
    with st.expander("Change Password"):
        current_pw = st.text_input("Current Password", type="password", key="current_pw")
        new_pw = st.text_input("New Password", type="password", key="new_pw")
        confirm_pw = st.text_input("Confirm New Password", type="password", key="confirm_pw")
        if st.button("Update Password", use_container_width=True):
            if current_pw and new_pw and confirm_pw:
                if st.session_state.users[st.session_state.username]['password'] == hash_password(current_pw):
                    if new_pw == confirm_pw:
                        if len(new_pw) >= 6:
                            st.session_state.users[st.session_state.username]['password'] = hash_password(new_pw)
                            st.success("Password updated successfully!")
                        else:
                            st.error("New password must be at least 6 characters long")
                    else:
                        st.error("New passwords do not match")
                else:
                    st.error("Current password is incorrect")
            else:
                st.error("Please fill in all fields")
    
    with st.expander("Two-Factor Authentication"):
        st.write("Enable 2FA for added security")
        twofa_enabled = st.toggle("Enable 2FA", value=False)
        if twofa_enabled:
            st.info("2FA setup instructions would be sent to your email")
    
    with st.expander("Notification Preferences"):
        email_notif = st.checkbox("Email notifications", value=True)
        sms_notif = st.checkbox("SMS notifications", value=True)
        push_notif = st.checkbox("Push notifications", value=False)
        if st.button("Save Preferences", use_container_width=True):
            st.success("Notification preferences saved!")
    
    with st.expander("Privacy Settings"):
        make_public = st.checkbox("Make profile public", value=False)
        share_history = st.checkbox("Share application history with LGUs", value=True)
        if st.button("Save Privacy Settings", use_container_width=True):
            st.success("Privacy settings saved!")

def show_lgu_services():
    st.title("Local Government Unit Services")
    
    # LGU Offices and their documents data structure
    lgu_offices = {
        "Office of the Municipal Mayor": {
            "icon": "👔",
            "description": "Chief executive of the municipality",
            "documents": [
                {"name": "Executive Order", "fee": "Free", "processing": "3-5 days"},
                {"name": "Certificate of Appearance", "fee": "₱50", "processing": "1 day"},
                {"name": "Letter of Support/Endorsement", "fee": "Free", "processing": "2-3 days"},
                {"name": "Mayor's Permit (Special)", "fee": "₱100", "processing": "2 days"}
            ]
        },
        "Office of the Municipal Vice Mayor": {
            "icon": "🗳️",
            "description": "Presiding officer of the Sangguniang Bayan",
            "documents": [
                {"name": "Certificate of Appearance (Session)", "fee": "Free", "processing": "1 day"},
                {"name": "Vice Mayor's Clearance", "fee": "₱50", "processing": "1-2 days"}
            ]
        },
        "Sangguniang Bayan": {
            "icon": "📜",
            "description": "Municipal legislative body",
            "documents": [
                {"name": "Certified True Copy of Ordinance", "fee": "₱75", "processing": "2-3 days"},
                {"name": "Certified True Copy of Resolution", "fee": "₱75", "processing": "2-3 days"},
                {"name": "Excerpt of Minutes (Session)", "fee": "₱50", "processing": "2 days"},
                {"name": "Legislative History", "fee": "₱100", "processing": "3-5 days"}
            ]
        },
        "Municipal Civil Registrar": {
            "icon": "📄",
            "description": "Birth, marriage, and death records",
            "documents": [
                {"name": "Birth Certificate (PSA)", "fee": "₱155", "processing": "3-5 days"},
                {"name": "Marriage Certificate (PSA)", "fee": "₱155", "processing": "3-5 days"},
                {"name": "Death Certificate (PSA)", "fee": "₱155", "processing": "3-5 days"},
                {"name": "CENOMAR", "fee": "₱210", "processing": "5-7 days"},
                {"name": "Certificate of Live Birth (Local)", "fee": "₱75", "processing": "2-3 days"},
                {"name": "Certificate of Marriage (Local)", "fee": "₱75", "processing": "2-3 days"},
                {"name": "Certificate of Death (Local)", "fee": "₱75", "processing": "2-3 days"},
                {"name": "Marriage License Application", "fee": "₱200", "processing": "10 days"}
            ]
        },
        "Municipal Assessor's Office": {
            "icon": "🏠",
            "description": "Property assessment and taxation",
            "documents": [
                {"name": "Tax Declaration (Current)", "fee": "₱150", "processing": "3-5 days"},
                {"name": "Tax Declaration (Historical)", "fee": "₱200", "processing": "5-7 days"},
                {"name": "Certificate of Land Holdings", "fee": "₱100", "processing": "2-3 days"},
                {"name": "Assessment of Real Property", "fee": "₱200", "processing": "3-5 days"},
                {"name": "Sketch Plan/Lot Plan", "fee": "₱300", "processing": "5-7 days"}
            ]
        },
        "Municipal Treasurer's Office": {
            "icon": "💰",
            "description": "Financial management and collections",
            "documents": [
                {"name": "Certificate of Tax Clearance", "fee": "₱100", "processing": "1-2 days"},
                {"name": "Certificate of No Tax Delinquency", "fee": "₱100", "processing": "1-2 days"},
                {"name": "Official Receipt (Duplicate)", "fee": "₱50", "processing": "1 day"},
                {"name": "Statement of Accounts", "fee": "Free", "processing": "2-3 days"}
            ]
        },
        "Municipal Budget Office": {
            "icon": "📊",
            "description": "Budget planning and management",
            "documents": [
                {"name": "Budget Execution Document", "fee": "Free", "processing": "3-5 days"},
                {"name": "Annual Investment Program", "fee": "Free", "processing": "5-7 days"},
                {"name": "Financial Reports", "fee": "Free", "processing": "3-5 days"}
            ]
        },
        "Municipal Accounting Office": {
            "icon": "🧾",
            "description": "Accounting and financial reporting",
            "documents": [
                {"name": "Statement of Receipts & Expenditures", "fee": "Free", "processing": "3-5 days"},
                {"name": "Trial Balance Report", "fee": "Free", "processing": "2-3 days"},
                {"name": "Financial Statements", "fee": "Free", "processing": "5-7 days"}
            ]
        },
        "Municipal Planning and Development Office": {
            "icon": "📐",
            "description": "Development planning and coordination",
            "documents": [
                {"name": "Zoning Certification", "fee": "₱200", "processing": "3-5 days"},
                {"name": "Locational Clearance", "fee": "₱300", "processing": "5-7 days"},
                {"name": "Development Plan Excerpt", "fee": "₱100", "processing": "2-3 days"},
                {"name": "CLUP (Comprehensive Land Use Plan)", "fee": "₱500", "processing": "7-10 days"}
            ]
        },
        "Municipal Engineering Office": {
            "icon": "🏗️",
            "description": "Infrastructure and construction",
            "documents": [
                {"name": "Building Permit", "fee": "₱1000-5000", "processing": "10-15 days"},
                {"name": "Occupancy Permit", "fee": "₱800", "processing": "5-7 days"},
                {"name": "Fencing Permit", "fee": "₱500", "processing": "3-5 days"},
                {"name": "Demolition Permit", "fee": "₱1000", "processing": "5-7 days"},
                {"name": "Electrical Permit", "fee": "₱500", "processing": "3-5 days"},
                {"name": "Plumbing Permit", "fee": "₱500", "processing": "3-5 days"},
                {"name": "Location Plan/Site Plan", "fee": "₱300", "processing": "3-5 days"}
            ]
        },
        "Municipal Health Office": {
            "icon": "🏥",
            "description": "Health services and sanitation",
            "documents": [
                {"name": "Health Clearance", "fee": "₱100", "processing": "1-2 days"},
                {"name": "Sanitary Permit", "fee": "₱300", "processing": "3-5 days"},
                {"name": "Medical Certificate", "fee": "₱50", "processing": "1 day"},
                {"name": "Dental Certificate", "fee": "₱50", "processing": "1 day"},
                {"name": "Food Handler's Certificate", "fee": "₱200", "processing": "2-3 days"}
            ]
        },
        "MSWDO (Social Welfare)": {
            "icon": "🤝",
            "description": "Social welfare and development",
            "documents": [
                {"name": "Certificate of Indigency", "fee": "Free", "processing": "1 day"},
                {"name": "Social Case Study Report", "fee": "Free", "processing": "2-3 days"},
                {"name": "Referral Letter", "fee": "Free", "processing": "1 day"},
                {"name": "Assessment Report", "fee": "Free", "processing": "2-3 days"},
                {"name": "4Ps Certification", "fee": "Free", "processing": "2 days"}
            ]
        },
        "Municipal Agriculture Office": {
            "icon": "🌾",
            "description": "Agricultural services",
            "documents": [
                {"name": "Farmer's Certification", "fee": "Free", "processing": "1-2 days"},
                {"name": "Agricultural Technician Report", "fee": "Free", "processing": "3-5 days"},
                {"name": "Soil Analysis Report", "fee": "₱100", "processing": "5-7 days"},
                {"name": "Livestock Transport Permit", "fee": "₱50", "processing": "1 day"}
            ]
        },
        "MENRO (Environment)": {
            "icon": "🌳",
            "description": "Environment and natural resources",
            "documents": [
                {"name": "Environmental Compliance Certificate", "fee": "₱500", "processing": "7-10 days"},
                {"name": "Tree Cutting Permit", "fee": "₱200", "processing": "3-5 days"},
                {"name": "Waste Generator's ID", "fee": "₱100", "processing": "2-3 days"},
                {"name": "Environmental Clearance", "fee": "₱300", "processing": "5-7 days"}
            ]
        },
        "MDRRMO (Disaster Risk Reduction)": {
            "icon": "⚠️",
            "description": "Disaster management",
            "documents": [
                {"name": "Geohazard Clearance", "fee": "Free", "processing": "2-3 days"},
                {"name": "Certificate of No Incident", "fee": "Free", "processing": "1 day"},
                {"name": "Disaster Report Certification", "fee": "Free", "processing": "2 days"},
                {"name": "Evacuation Center Referral", "fee": "Free", "processing": "1 day"}
            ]
        },
        "Municipal Police Station": {
            "icon": "👮",
            "description": "Peace and order",
            "documents": [
                {"name": "Police Clearance", "fee": "₱150", "processing": "1-2 days"},
                {"name": "Blotter Certificate", "fee": "₱50", "processing": "1 day"},
                {"name": "Incident Report", "fee": "₱100", "processing": "2-3 days"},
                {"name": "Traffic Violation Report", "fee": "₱100", "processing": "1-2 days"}
            ]
        },
        "Bureau of Fire Protection": {
            "icon": "🔥",
            "description": "Fire safety and prevention",
            "documents": [
                {"name": "Fire Safety Inspection Certificate", "fee": "₱300", "processing": "3-5 days"},
                {"name": "Fire Clearance", "fee": "₱200", "processing": "2-3 days"},
                {"name": "Incident Report (Fire)", "fee": "Free", "processing": "2 days"}
            ]
        },
        "PESO (Public Employment Service Office)": {
            "icon": "💼",
            "description": "Employment services",
            "documents": [
                {"name": "Job Seeker Registration", "fee": "Free", "processing": "1 day"},
                {"name": "Employment Certificate", "fee": "Free", "processing": "1-2 days"},
                {"name": "Referral Letter (Employment)", "fee": "Free", "processing": "1 day"},
                {"name": "Training Certificate", "fee": "Free", "processing": "2-3 days"}
            ]
        },
        "OSCA (Senior Citizens Office)": {
            "icon": "👴",
            "description": "Senior citizen affairs",
            "documents": [
                {"name": "Senior Citizen ID", "fee": "Free", "processing": "3-5 days"},
                {"name": "OSCA ID", "fee": "Free", "processing": "3-5 days"},
                {"name": "Senior Citizen Certification", "fee": "Free", "processing": "1 day"}
            ]
        },
        "PDAO (Persons with Disability)": {
            "icon": "♿",
            "description": "PWD affairs",
            "documents": [
                {"name": "PWD ID", "fee": "Free", "processing": "3-5 days"},
                {"name": "PWD Certification", "fee": "Free", "processing": "1-2 days"},
                {"name": "Discount Privilege Letter", "fee": "Free", "processing": "1 day"}
            ]
        },
        "Tourism Office": {
            "icon": "🏖️",
            "description": "Tourism promotion and development",
            "documents": [
                {"name": "Tourist Assistance Letter", "fee": "Free", "processing": "1 day"},
                {"name": "Tour Guide Certification", "fee": "₱100", "processing": "3-5 days"},
                {"name": "Tourism Establishment Registration", "fee": "₱200", "processing": "5-7 days"},
                {"name": "Event Permit (Tourism-related)", "fee": "₱300", "processing": "5-7 days"}
            ]
        },
        "Municipal Legal Office": {
            "icon": "⚖️",
            "description": "Legal services",
            "documents": [
                {"name": "Legal Opinion", "fee": "Free", "processing": "5-7 days"},
                {"name": "Contract Review", "fee": "Free", "processing": "3-5 days"},
                {"name": "Notarial Services", "fee": "₱100", "processing": "1 day"},
                {"name": "Certified True Copy (Legal Docs)", "fee": "₱75", "processing": "1-2 days"}
            ]
        }
    }
    
    # Search functionality
    search_term = st.text_input("🔍 Search for offices or documents", placeholder="e.g., birth certificate, permit, clearance...")
    
    # Category filters
    categories = ["All Offices", "Executive", "Legislative", "Administrative", "Civil Registry", 
                  "Health & Social", "Engineering", "Peace & Order", "Economic", "Environment"]
    
    selected_category = st.selectbox("Filter by Category", categories)
    
    # Filter offices based on category
    category_mapping = {
        "Executive": ["Office of the Municipal Mayor", "Office of the Municipal Vice Mayor"],
        "Legislative": ["Sangguniang Bayan"],
        "Administrative": ["Municipal Assessor's Office", "Municipal Treasurer's Office", "Municipal Budget Office", 
                          "Municipal Accounting Office", "Municipal Planning and Development Office"],
        "Civil Registry": ["Municipal Civil Registrar"],
        "Health & Social": ["Municipal Health Office", "MSWDO (Social Welfare)", "OSCA (Senior Citizens Office)", 
                           "PDAO (Persons with Disability)"],
        "Engineering": ["Municipal Engineering Office"],
        "Peace & Order": ["Municipal Police Station", "Bureau of Fire Protection", "MDRRMO (Disaster Risk Reduction)"],
        "Economic": ["Municipal Agriculture Office", "PESO (Public Employment Service Office)", "Tourism Office"],
        "Environment": ["MENRO (Environment)"]
    }
    
    # Display offices
    offices_found = False
    for office_name, office_data in lgu_offices.items():
        # Apply category filter
        if selected_category != "All Offices" and office_name not in category_mapping.get(selected_category, []):
            continue
            
        # Apply search filter
        if search_term:
            search_term_lower = search_term.lower()
            doc_matches = any(search_term_lower in doc['name'].lower() for doc in office_data['documents'])
            office_matches = search_term_lower in office_name.lower()
            if not (doc_matches or office_matches):
                continue
        
        offices_found = True
        with st.expander(f"{office_data['icon']} {office_name}"):
            st.caption(office_data['description'])
            st.markdown("---")
            
            # Display documents for this office
            for doc in office_data['documents']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{doc['name']}**")
                with col2:
                    st.markdown(f"`{doc['fee']}`")
                with col3:
                    if st.button("Apply", key=f"{office_name}_{doc['name']}"):
                        st.session_state['selected_service'] = doc
                        st.session_state['selected_office'] = office_name
                        st.session_state['service_type'] = 'lgu'
                        show_application_form(doc['name'], office_name)
                
                st.caption(f"⏱️ Processing: {doc['processing']}")
                st.markdown("---")
    
    if not offices_found:
        st.info("No offices or documents match your search criteria.")
    
    # Quick apply section for popular documents
    st.markdown("---")
    st.subheader("📋 Popular Requests")
    
    popular_docs = [
        ("Birth Certificate", "Municipal Civil Registrar"),
        ("Barangay Clearance", "Barangay Hall"),
        ("Police Clearance", "Municipal Police Station"),
        ("Business Permit", "Municipal Engineering Office"),
        ("Certificate of Indigency", "MSWDO (Social Welfare)")
    ]
    
    cols = st.columns(5)
    for idx, (doc_name, office) in enumerate(popular_docs):
        with cols[idx]:
            if st.button(f"{doc_name}\n({office})", use_container_width=True):
                st.info(f"Please go to the {office} section above to apply for {doc_name}")

def show_barangay_services():
    st.title("Barangay Government Unit Services")
    
    # Residency Documents
    st.markdown('<div class="service-header">📋 Residency Documents</div>', unsafe_allow_html=True)
    
    residency_services = [
        {"name": "Barangay Clearance", "fee": "₱50", "processing": "1 day"},
        {"name": "Certificate of Residency", "fee": "₱30", "processing": "1 day"},
        {"name": "Certificate of Indigency", "fee": "Free", "processing": "1 day"}
    ]
    
    for service in residency_services:
        with st.container():
            st.markdown(f"""
            <div class="service-container">
                <strong>{service['name']}</strong><br>
                <span style="color:#666;">Fee: {service['fee']} | Processing: {service['processing']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Apply Now", key=f"residency_{service['name']}"):
                st.session_state['selected_service'] = service
                st.session_state['service_type'] = 'residency'
                show_application_form(service['name'], "Barangay Hall")
    
    # Special IDs
    st.markdown('<div class="service-header">🆔 Special IDs</div>', unsafe_allow_html=True)
    
    special_ids = [
        {"name": "Senior Citizen ID", "fee": "Free", "processing": "3-5 days"},
        {"name": "PWD ID", "fee": "Free", "processing": "3-5 days"},
        {"name": "Solo Parent ID", "fee": "Free", "processing": "3-5 days"},
        {"name": "Police Clearance", "fee": "₱150", "processing": "1-2 days"}
    ]
    
    for service in special_ids:
        with st.container():
            st.markdown(f"""
            <div class="service-container">
                <strong>{service['name']}</strong><br>
                <span style="color:#666;">Fee: {service['fee']} | Processing: {service['processing']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Apply Now", key=f"special_{service['name']}"):
                st.session_state['selected_service'] = service
                st.session_state['service_type'] = 'special'
                show_application_form(service['name'], "Barangay Hall")
    
    # Assistance Programs
    st.markdown('<div class="service-header">🤝 Assistance Programs</div>', unsafe_allow_html=True)
    
    assistance_programs = [
        {"name": "Medical/Burial Assistance", "fee": "Free", "processing": "3-5 days"},
        {"name": "4Ps Program", "fee": "Free", "processing": "7-10 days"},
        {"name": "Financial Assistance", "fee": "Free", "processing": "5-7 days"}
    ]
    
    for service in assistance_programs:
        with st.container():
            st.markdown(f"""
            <div class="service-container">
                <strong>{service['name']}</strong><br>
                <span style="color:#666;">Fee: {service['fee']} | Processing: {service['processing']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Apply Now", key=f"assistance_{service['name']}"):
                st.session_state['selected_service'] = service
                st.session_state['service_type'] = 'assistance'
                show_application_form(service['name'], "Barangay Hall")
    
    # Permits
    st.markdown('<div class="service-header">📜 Permits</div>', unsafe_allow_html=True)
    
    permit_services = [
        {"name": "Tricycle Franchise", "fee": "₱1000", "processing": "7-10 days"}
    ]
    
    for service in permit_services:
        with st.container():
            st.markdown(f"""
            <div class="service-container">
                <strong>{service['name']}</strong><br>
                <span style="color:#666;">Fee: {service['fee']} | Processing: {service['processing']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Apply Now", key=f"permit_{service['name']}"):
                st.session_state['selected_service'] = service
                st.session_state['service_type'] = 'permit'
                show_application_form(service['name'], "Barangay Hall")

def show_application_form(service_name, office_name=None):
    st.markdown("---")
    if office_name:
        st.subheader(f"Application Form - {service_name}")
        st.caption(f"Office: {office_name}")
    else:
        st.subheader(f"Application Form - {service_name}")
    
    with st.form(key=f"form_{service_name.replace(' ', '_')}"):
        # Display office info
        if office_name:
            st.info(f"This application will be processed by: **{office_name}**")
        
        # Personal Information
        st.write("**Personal Information**")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*")
        with col2:
            last_name = st.text_input("Last Name*")
        
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input("Date of Birth*", min_value=datetime(1900,1,1), max_value=datetime.now())
        with col2:
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
        
        # Contact Information
        st.write("**Contact Information**")
        col1, col2 = st.columns(2)
        with col1:
            contact_no = st.text_input("Contact Number*")
        with col2:
            email = st.text_input("Email Address*", value=st.session_state.username if st.session_state.username else "")
        
        # Address
        st.write("**Address**")
        col1, col2 = st.columns(2)
        with col1:
            barangay = st.selectbox("Barangay*", [
                "Barangay 1", "Barangay 2", "Barangay 3", "Barangay 4", 
                "Barangay 5", "Barangay 6", "Barangay 7", "Barangay 8"
            ])
        with col2:
            municipality = st.text_input("Municipality*", value="Cantilan", disabled=True)
        
        street = st.text_input("Street/Purok*")
        
        # Service Specific Fields
        st.write("**Application Details**")
        purpose = ""
        if "Certificate" in service_name or "Clearance" in service_name:
            purpose = st.text_area("Purpose of Application*")
        
        business_name = ""
        business_type = ""
        if service_name in ["Business Permit", "Building Permit"]:
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business Name*")
            with col2:
                business_type = st.selectbox("Business Type*", ["Sole Proprietorship", "Partnership", "Corporation", "Cooperative"])
        
        plate_no = ""
        franchise_type = ""
        if "Tricycle Franchise" in service_name:
            col1, col2 = st.columns(2)
            with col1:
                plate_no = st.text_input("Plate Number*")
            with col2:
                franchise_type = st.selectbox("Franchise Type*", ["New", "Renewal", "Transfer"])
        
        # Document Upload
        st.write("**Required Documents**")
        uploaded_files = st.file_uploader("Upload supporting documents", 
                                          accept_multiple_files=True,
                                          type=['pdf', 'jpg', 'jpeg', 'png'])
        
        # Payment Method
        st.write("**Payment Method**")
        payment_method = st.radio("Select Payment Method", 
                                  ["E-Wallet (GCash, Maya)", "Cash (Pay at LGU)", "Online Banking"],
                                  horizontal=True)
        
        # Terms and Conditions
        agree = st.checkbox("I certify that all information provided is true and correct*")
        
        # Submit button
        submitted = st.form_submit_button("Submit Application", use_container_width=True)
        
        if submitted:
            if agree and first_name and last_name and contact_no and email:
                tracking_no = f"{service_name[:2].upper()}-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
                
                # Create application record
                new_app = {
                    "user_email": st.session_state.username,
                    "type": service_name,
                    "office": office_name if office_name else "N/A",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Pending",
                    "tracking": tracking_no,
                    "first_name": first_name,
                    "last_name": last_name,
                    "contact_no": contact_no,
                    "email": email,
                    "barangay": barangay,
                    "purpose": purpose if purpose else "N/A",
                    "payment_method": payment_method,
                    "payment_status": "Pending"
                }
                
                # Add service-specific fields
                if business_name:
                    new_app['business_name'] = business_name
                if business_type:
                    new_app['business_type'] = business_type
                if plate_no:
                    new_app['plate_no'] = plate_no
                if franchise_type:
                    new_app['franchise_type'] = franchise_type
                
                st.session_state.applications.append(new_app)
                
                # Create payment record
                payment_id = f"PAY{random.randint(1000,9999)}"
                
                # Extract fee amount (remove ₱ and handle ranges)
                fee_text = st.session_state['selected_service']['fee'] if 'selected_service' in st.session_state else "₱150"
                try:
                    if "-" in fee_text:
                        amount = int(fee_text.split('-')[0].replace('₱', '').strip())
                    elif "Free" in fee_text:
                        amount = 0
                    else:
                        amount = int(fee_text.replace('₱', '').strip())
                except:
                    amount = 150  # default amount
                
                st.session_state.payments.append({
                    "id": payment_id,
                    "tracking": tracking_no,
                    "amount": amount,
                    "method": payment_method,
                    "status": "Pending Verification" if "Cash" in payment_method else "Verified",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                
                st.success(f"✅ Application submitted successfully!")
                st.info(f"📱 Tracking Number: **{tracking_no}**")
                st.info(f"🏢 Processing Office: **{office_name if office_name else 'LGU Office'}**")
                st.info("📨 You will receive SMS notifications for updates on your application.")
                
                # Add a button to go back to services
                if st.button("Apply for Another Service", key="another_service"):
                    st.rerun()
            else:
                st.error("Please fill in all required fields and agree to terms and conditions")

def show_admin_dashboard():
    st.title("Admin Dashboard")
    st.markdown("---")
    
    # Route to appropriate admin page
    if st.session_state.admin_page == 'dashboard_overview':
        show_admin_dashboard_overview()
    elif st.session_state.admin_page == 'manage_request':
        show_admin_manage_request()
    elif st.session_state.admin_page == 'manage_payment':
        show_admin_manage_payment()
    elif st.session_state.admin_page == 'reports_analytics':
        show_admin_reports_analytics()
    elif st.session_state.admin_page == 'user_management':
        show_admin_user_management()

def show_admin_dashboard_overview():
    st.subheader("📊 Dashboard Overview")
    
    # Calculate statistics
    total_apps = len(st.session_state.applications)
    pending_apps = len([app for app in st.session_state.applications if app['status'] == 'Pending'])
    processed_today = len([app for app in st.session_state.applications if app['date'] == datetime.now().strftime("%Y-%m-%d")])
    
    # Calculate today's revenue
    today_revenue = sum([150 for app in st.session_state.applications if app['date'] == datetime.now().strftime("%Y-%m-%d")])
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="admin-stat-card">
            <h3 style="margin:0; font-size:14px;">PENDING REQUESTS</h3>
            <h2 style="margin:0; font-size:24px;">{pending_apps}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="admin-stat-card">
            <h3 style="margin:0; font-size:14px;">PROCESSED TODAY</h3>
            <h2 style="margin:0; font-size:24px;">{processed_today}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="admin-stat-card">
            <h3 style="margin:0; font-size:14px;">TODAY REVENUE</h3>
            <h2 style="margin:0; font-size:24px;">₱{today_revenue}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_processing_time = "2.5 days"
        st.markdown(f"""
        <div class="admin-stat-card">
            <h3 style="margin:0; font-size:14px;">AVG PROCESSING</h3>
            <h2 style="margin:0; font-size:24px;">{avg_processing_time}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests by Service (Last 7 Days)")
        
        # Sample data for service requests
        service_data = {
            'Barangay Clearance': 45,
            'Business Permit': 23,
            'Police Clearance': 34,
            'Birth Certificate': 56,
            'Residency Cert': 12
        }
        
        df_services = pd.DataFrame(list(service_data.items()), columns=['Service', 'Count'])
        fig = px.bar(df_services, x='Service', y='Count', color='Count', 
                     color_continuous_scale='Viridis')
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Daily Request Trends (Last 30 Days)")
        
        # Generate sample daily trend data
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
        requests = [random.randint(10, 50) for _ in range(30)]
        
        df_trends = pd.DataFrame({'Date': dates, 'Requests': requests})
        fig = px.line(df_trends, x='Date', y='Requests', title='Daily Request Trends')
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

def show_admin_manage_request():
    st.subheader("📝 Manage Service Requests")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Processing", "Approved", "Rejected"])
    with col2:
        service_filter = st.selectbox("Filter by Service", ["All", "Barangay Clearance", "Business Permit", "Birth Certificate", "Police Clearance"])
    with col3:
        date_filter = st.date_input("Filter by Date", value=datetime.now())
    
    # Display applications
    if st.session_state.applications:
        filtered_apps = st.session_state.applications
        
        if status_filter != "All":
            filtered_apps = [app for app in filtered_apps if app['status'] == status_filter]
        
        for app in filtered_apps:
            with st.container():
                st.markdown(f"""
                <div class="admin-container">
                    <div style="display:flex; justify-content:space-between;">
                        <strong>{app['type']}</strong>
                        <span class="status-badge status-{app['status'].lower()}">{app['status']}</span>
                    </div>
                    <p>Tracking: {app['tracking']} | Date: {app['date']}</p>
                    <p>Applicant: {app['first_name']} {app['last_name']}</p>
                    <p>Office: {app.get('office', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("View Details", key=f"view_{app['tracking']}"):
                        st.info(f"Showing details for {app['tracking']}")
                with col2:
                    new_status = st.selectbox("Update Status", 
                                             ["Pending", "Processing", "Approved", "Rejected"],
                                             key=f"status_{app['tracking']}")
                with col3:
                    if st.button("Update", key=f"update_{app['tracking']}"):
                        app['status'] = new_status
                        st.success(f"Status updated to {new_status}")
                        st.rerun()
                with col4:
                    if st.button("Assign Officer", key=f"assign_{app['tracking']}"):
                        st.info("Assign to processing officer")
    else:
        st.info("No applications found")

def show_admin_manage_payment():
    st.subheader("💰 Manage Payments")
    
    # Cash Payments - Pending Verification
    st.markdown("### Cash Payments - Pending Verification")
    
    pending_cash = [p for p in st.session_state.payments if p['method'] == 'Cash' and p['status'] == 'Pending Verification']
    
    if pending_cash:
        for payment in pending_cash:
            with st.container():
                st.markdown(f"""
                <div class="admin-container">
                    <div style="display:flex; justify-content:space-between;">
                        <strong>Payment ID: {payment['id']}</strong>
                        <span class="status-badge status-pending">Pending</span>
                    </div>
                    <p>Tracking: {payment['tracking']} | Amount: ₱{payment['amount']}</p>
                    <p>Date: {payment['date']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Verify Payment", key=f"verify_{payment['id']}"):
                        payment['status'] = 'Verified'
                        st.success(f"Payment {payment['id']} verified!")
                        st.rerun()
                with col2:
                    if st.button("Reject", key=f"reject_{payment['id']}"):
                        payment['status'] = 'Rejected'
                        st.warning(f"Payment {payment['id']} rejected")
                        st.rerun()
    else:
        st.info("No pending cash payments")
    
    # Verified Payments
    st.markdown("### Verified Payments")
    verified_payments = [p for p in st.session_state.payments if p['status'] == 'Verified']
    
    if verified_payments:
        df_verified = pd.DataFrame(verified_payments)
        st.dataframe(df_verified, use_container_width=True)
    else:
        st.info("No verified payments")

def show_admin_reports_analytics():
    st.subheader("📈 Reports & Analytics")
    
    # Report Type Selection
    report_type = st.selectbox("Select Report Type", 
                               ["Service Request Summary", 
                                "Revenue Report", 
                                "User Activity Report",
                                "Processing Time Analysis"])
    
    if report_type == "Service Request Summary":
        st.markdown("### Service Request Summary")
        
        # Sample data
        services = ['Barangay Clearance', 'Business Permit', 'Birth Certificate', 
                   'Police Clearance', 'Residency Cert', 'Others']
        counts = [156, 89, 234, 67, 45, 23]
        statuses = ['Completed', 'Pending', 'Processing', 'Approved', 'Rejected']
        status_counts = [98, 45, 67, 34, 12]
        
        col1, col2 = st.columns(2)
        
        with col1:
            df_services = pd.DataFrame({'Service': services, 'Count': counts})
            fig = px.pie(df_services, values='Count', names='Service', title='Service Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df_status = pd.DataFrame({'Status': statuses, 'Count': status_counts})
            fig = px.bar(df_status, x='Status', y='Count', color='Status', title='Request Status Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        st.markdown("### Detailed Summary")
        summary_data = {
            'Service': services,
            'Total Requests': counts,
            'Completed': [random.randint(30, 100) for _ in range(len(services))],
            'Pending': [random.randint(5, 30) for _ in range(len(services))],
            'Processing': [random.randint(10, 40) for _ in range(len(services))]
        }
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)
    
    elif report_type == "Revenue Report":
        st.markdown("### Revenue Report")
        
        # Generate sample revenue data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [random.randint(5000, 15000) for _ in range(6)]
        
        df_revenue = pd.DataFrame({'Month': months, 'Revenue': revenue})
        fig = px.line(df_revenue, x='Month', y='Revenue', title='Monthly Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue by service
        st.markdown("### Revenue by Service")
        services = ['Barangay Clearance', 'Business Permit', 'Birth Certificate', 'Police Clearance']
        service_revenue = [7800, 15000, 23400, 10050]
        
        df_service_rev = pd.DataFrame({'Service': services, 'Revenue': service_revenue})
        fig = px.bar(df_service_rev, x='Service', y='Revenue', color='Revenue', title='Revenue by Service')
        st.plotly_chart(fig, use_container_width=True)

def show_admin_user_management():
    st.subheader("👥 User Management")
    
    # Manage LGU Staff Accounts
    st.markdown("### Manage LGU Staff Accounts")
    
    # Add New Staff
    with st.expander("➕ Add New Staff"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
        with col2:
            new_role = st.selectbox("Role", ["Processor", "Verifier", "Admin", "Encoder"])
            new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        if st.button("Add Staff Member", use_container_width=True):
            if new_name and new_email:
                new_id = len(st.session_state.staff_members) + 1
                st.session_state.staff_members.append({
                    "id": new_id,
                    "name": new_name,
                    "email": new_email,
                    "role": new_role,
                    "status": new_status
                })
                st.success(f"Staff member {new_name} added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    # Existing Staff Members
    st.markdown("### Existing Staff Members")
    
    for staff in st.session_state.staff_members:
        with st.container():
            st.markdown(f"""
            <div class="staff-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong>{staff['name']}</strong><br>
                        <span style="color:#666;">{staff['email']} | {staff['role']}</span>
                    </div>
                    <span class="status-badge status-{'approved' if staff['status'] == 'Active' else 'pending'}">
                        {staff['status']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Edit", key=f"edit_{staff['id']}"):
                    st.session_state['editing_staff'] = staff['id']
            
            with col2:
                new_staff_status = st.selectbox("Status", ["Active", "Inactive"], 
                                               key=f"status_{staff['id']}",
                                               index=0 if staff['status'] == 'Active' else 1)
                if st.button("Update Status", key=f"update_status_{staff['id']}"):
                    staff['status'] = new_staff_status
                    st.success(f"Status updated for {staff['name']}")
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{staff['id']}"):
                    st.session_state.staff_members = [s for s in st.session_state.staff_members if s['id'] != staff['id']]
                    st.warning(f"Staff member {staff['name']} removed")
                    st.rerun()
    
    # Regular Users Management
    st.markdown("---")
    st.markdown("### Regular Users")
    
    if st.session_state.users:
        users_data = []
        for email, data in st.session_state.users.items():
            users_data.append({
                "Name": f"{data['first_name']} {data['last_name']}",
                "Email": email,
                "Phone": data['phone'],
                "Verified": "✅" if data.get('verified', False) else "❌",
                "Joined": data['created_at']
            })
        
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users, use_container_width=True)
        
        # User verification management
        st.subheader("Verify Users")
        unverified_users = [email for email, data in st.session_state.users.items() if not data.get('verified', False)]
        if unverified_users:
            user_to_verify = st.selectbox("Select user to verify", unverified_users)
            if st.button("Verify User", use_container_width=True):
                st.session_state.users[user_to_verify]['verified'] = True
                if user_to_verify == st.session_state.username:
                    st.session_state.profile_verified = True
                st.success(f"User {user_to_verify} verified successfully!")
                st.rerun()
        else:
            st.info("All users are verified")
    else:
        st.info("No users registered yet")

if __name__ == "__main__":
    main()
