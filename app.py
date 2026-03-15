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
from streamlit_option_menu import option_menu
from chatbot import add_chatbot_to_page

# Page configuration
st.set_page_config(
    page_title="Cantilan-eCivil",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly design and blue sidebar
def load_css():
    st.markdown("""
    <style>
    /* Mobile-friendly adjustments */
    .stApp {
        max-width: 100%;
        padding: 0px;
    }
    
    /* Blue sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
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
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 4px solid white;
        margin: 0 auto;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .profile-pic:hover {
        transform: scale(1.05);
    }
    
    .profile-pic-container {
        position: relative;
        display: inline-block;
    }
    
    .profile-pic-upload {
        position: absolute;
        bottom: 10px;
        right: 10px;
        background-color: #28a745;
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 2px solid white;
        font-size: 18px;
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
    
    /* Staff stat cards */
    .staff-stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .ai-validation-card {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
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
    .status-flagged { background-color: #f8d7da; color: #721c24; }
    .status-verified { background-color: #d4edda; color: #155724; }
    
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
    
    /* Severity badges */
    .severity-high {
        background-color: #dc3545;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
    }
    
    .severity-medium {
        background-color: #ffc107;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
    }
    
    .severity-low {
        background-color: #17a2b8;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        background-color: #1e3c72;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action-btn:hover {
        background-color: #2a5298;
        transform: translateY(-2px);
    }
    
    /* Modal styling */
    .modal-content {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
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
    if 'profile_pic' not in st.session_state:
        st.session_state.profile_pic = None
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'staff_logged_in' not in st.session_state:
        st.session_state.staff_logged_in = False
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = 'dashboard_overview'
    if 'staff_page' not in st.session_state:
        st.session_state.staff_page = 'overview'
    if 'selected_department' not in st.session_state:
        st.session_state.selected_department = None
    if 'staff_members' not in st.session_state:
        st.session_state.staff_members = [
            {"id": 1, "name": "John Doe", "email": "john@cantilan.gov.ph", "role": "Processor", "status": "Active", "department": "Civil Registry", "password": hash_password("staff123")},
            {"id": 2, "name": "Jane Smith", "email": "jane@cantilan.gov.ph", "role": "Verifier", "status": "Active", "department": "Treasury", "password": hash_password("staff123")},
            {"id": 3, "name": "Mike Wilson", "email": "mike@cantilan.gov.ph", "role": "Admin", "status": "Active", "department": "Health & Sanitation", "password": hash_password("staff123")}
        ]
    if 'payments' not in st.session_state:
        st.session_state.payments = [
            {"id": "PAY001", "tracking": "BC-20240115-1234", "amount": 150, "method": "Cash", "status": "Pending Verification", "date": "2024-01-15"},
            {"id": "PAY002", "tracking": "BP-20240114-5678", "amount": 500, "method": "E-Wallet", "status": "Verified", "date": "2024-01-14"},
            {"id": "PAY003", "tracking": "BCL-20240113-9012", "amount": 50, "method": "Cash", "status": "Pending Verification", "date": "2024-01-13"}
        ]
    if 'validated_documents' not in st.session_state:
        st.session_state.validated_documents = generate_mock_validated_documents()
    if 'peak_hours_data' not in st.session_state:
        st.session_state.peak_hours_data = generate_peak_hours_data()
    if 'processing_forecasts' not in st.session_state:
        st.session_state.processing_forecasts = generate_processing_forecasts()
    if 'manpower_recommendations' not in st.session_state:
        st.session_state.manpower_recommendations = generate_manpower_recommendations()
    if 'monthly_reports' not in st.session_state:
        st.session_state.monthly_reports = generate_monthly_reports()
    if 'quick_action_modal' not in st.session_state:
        st.session_state.quick_action_modal = None

# Generate mock data functions
def generate_mock_validated_documents():
    documents = []
    departments = ["Civil Registry", "Treasury", "Health & Sanitation", "Admin"]
    statuses = ["Passed", "Flagged"]
    issues = ["Incomplete Form", "Incorrect Information", "Duplicate Submission", "Missing Signature", "Invalid ID"]
    
    for i in range(50):
        doc = {
            "id": f"DOC{i:03d}",
            "tracking": f"TRACK-{random.randint(1000,9999)}",
            "department": random.choice(departments),
            "document_type": random.choice(["Birth Certificate", "Business Permit", "Health Clearance", "Barangay Clearance"]),
            "applicant": f"Applicant {i}",
            "submission_date": (datetime.now() - timedelta(days=random.randint(0,30))).strftime("%Y-%m-%d"),
            "validation_status": random.choice(statuses),
            "validation_date": datetime.now().strftime("%Y-%m-%d"),
            "flagged_issues": [],
            "severity": None
        }
        
        if doc["validation_status"] == "Flagged":
            num_issues = random.randint(1, 3)
            doc["flagged_issues"] = random.sample(issues, num_issues)
            doc["severity"] = random.choice(["High", "Medium", "Low"])
        
        documents.append(doc)
    
    return documents

def generate_peak_hours_data():
    hours = list(range(8, 18))  # 8 AM to 5 PM
    data = []
    for hour in hours:
        volume = random.randint(5, 30)
        if volume < 10:
            level = "Low"
            color = "green"
        elif volume < 20:
            level = "Medium"
            color = "yellow"
        else:
            level = "High"
            color = "red"
        
        data.append({
            "hour": f"{hour}:00",
            "volume": volume,
            "level": level,
            "color": color
        })
    return data

def generate_processing_forecasts():
    services = [
        {"service": "Birth Certificate", "avg_time": 3.2, "trend": "↑", "confidence": 85},
        {"service": "Marriage Certificate", "avg_time": 4.1, "trend": "→", "confidence": 82},
        {"service": "Business Permit", "avg_time": 7.5, "trend": "↓", "confidence": 78},
        {"service": "Health Clearance", "avg_time": 2.3, "trend": "↑", "confidence": 91},
        {"service": "Barangay Clearance", "avg_time": 1.1, "trend": "→", "confidence": 95},
        {"service": "Police Clearance", "avg_time": 1.8, "trend": "↑", "confidence": 88}
    ]
    
    for service in services:
        service["predicted_time"] = round(service["avg_time"] * random.uniform(0.9, 1.1), 1)
    
    return services

def generate_manpower_recommendations():
    time_slots = ["8 AM - 12 PM", "12 PM - 4 PM", "4 PM - 5 PM"]
    recommendations = []
    
    for slot in time_slots:
        current = random.randint(2, 5)
        recommended = current + random.randint(0, 2)
        utilization = round((current / recommended) * 100)
        
        recommendations.append({
            "time_slot": slot,
            "current_staff": current,
            "recommended_staff": recommended,
            "utilization": utilization
        })
    
    return recommendations

def generate_monthly_reports():
    months = ["January", "February", "March", "April", "May", "June"]
    reports = []
    
    for month in months:
        pending = random.randint(10, 30)
        processing = random.randint(15, 35)
        completed = random.randint(40, 80)
        rejected = random.randint(5, 15)
        total = pending + processing + completed + rejected
        
        avg_time = round(random.uniform(2.5, 5.5), 1)
        
        reports.append({
            "month": month,
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "rejected": rejected,
            "total": total,
            "avg_processing_time": avg_time
        })
    
    return reports

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

def login_staff(email, password):
    for staff in st.session_state.staff_members:
        if staff['email'] == email and staff['password'] == hash_password(password):
            return True, staff
    return False, "Invalid staff credentials"

# Admin credentials
ADMIN_CREDENTIALS = {
    'admin@cantilan.gov.ph': hash_password('admin123')
}

# Main app structure
def main():
    load_css()
    init_session_state()
    
    # Sidebar navigation
    if st.session_state.logged_in or st.session_state.admin_logged_in or st.session_state.staff_logged_in:
        with st.sidebar:
            # Logo and title
            st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <h2 style="color: white; margin: 0;">🏛️ Cantilan-eCivil</h2>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            elif st.session_state.staff_logged_in:
                # Staff sidebar menu
                staff_info = st.session_state.get('staff_info', {})
                st.markdown(f"""
                <div style="text-align: center; color: white; padding: 10px;">
                    <div style="font-size: 40px;">👤</div>
                    <h3 style="margin: 5px 0; color: white;">{staff_info.get('name', 'Staff')}</h3>
                    <p style="margin: 0; color: rgba(255,255,255,0.8);">{staff_info.get('role', '')}</p>
                    <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 12px;">{staff_info.get('department', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                if st.button("📊 Department Overview", use_container_width=True):
                    st.session_state.staff_page = 'overview'
                    st.rerun()
                if st.button("📝 Pending Requests", use_container_width=True):
                    st.session_state.staff_page = 'pending'
                    st.rerun()
                if st.button("✅ Document Validation", use_container_width=True):
                    st.session_state.staff_page = 'validation'
                    st.rerun()
                if st.button("📈 Analytics", use_container_width=True):
                    st.session_state.staff_page = 'analytics'
                    st.rerun()
                if st.button("📋 Reports", use_container_width=True):
                    st.session_state.staff_page = 'reports'
                    st.rerun()
            
            else:
                # Regular user sidebar menu
                st.markdown(f"""
                <div style="text-align: center; color: white; padding: 10px;">
                    <div style="font-size: 40px;">👤</div>
                    <h3 style="margin: 5px 0; color: white;">{st.session_state.users.get(st.session_state.username, {}).get('first_name', 'User')}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
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
                st.session_state.staff_logged_in = False
                st.session_state.username = None
                st.session_state.page = 'login'
                st.rerun()
    
    # Page routing
    if not st.session_state.logged_in and not st.session_state.admin_logged_in and not st.session_state.staff_logged_in:
        show_login_page()
    elif st.session_state.admin_logged_in:
        show_admin_dashboard()
    elif st.session_state.staff_logged_in:
        show_staff_dashboard()
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["User Login", "User Register", "Staff Login", "Admin Login"])
    
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
                    st.session_state.profile_pic = st.session_state.users[email].get('profile_pic')
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
        st.subheader("Staff Login")
        staff_email = st.text_input("Staff Email", key="staff_email")
        staff_password = st.text_input("Staff Password", type="password", key="staff_password")
        
        if st.button("Staff Login", use_container_width=True):
            if staff_email and staff_password:
                success, staff_data = login_staff(staff_email, staff_password)
                if success:
                    st.session_state.staff_logged_in = True
                    st.session_state.staff_info = staff_data
                    st.session_state.selected_department = staff_data['department']
                    st.session_state.staff_page = 'overview'
                    st.rerun()
                else:
                    st.error(staff_data)
            else:
                st.error("Please enter email and password")
    
    with tab4:
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

def show_profile():
    st.title("Profile")
    
    user_data = st.session_state.users.get(st.session_state.username, {})
    
    # Profile header with picture upload
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="profile-pic-container">', unsafe_allow_html=True)
        
        # Display profile picture or default
        if st.session_state.profile_pic:
            st.image(st.session_state.profile_pic, width=150, output_format="auto")
        else:
            st.markdown('<div style="font-size: 150px; text-align: center;">👤</div>', unsafe_allow_html=True)
        
        # Upload new picture
        uploaded_file = st.file_uploader("Change Profile Picture", type=['png', 'jpg', 'jpeg'], key="profile_pic_upload")
        if uploaded_file is not None:
            # Convert to base64 for storage
            bytes_data = uploaded_file.getvalue()
            st.session_state.profile_pic = bytes_data
            st.session_state.users[st.session_state.username]['profile_pic'] = bytes_data
            st.success("Profile picture updated!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="profile-header">
            <h2>{user_data.get('first_name', '')} {user_data.get('last_name', '')}</h2>
            <p>{user_data.get('email', '')}</p>
            <span class="verification-badge">{'✅ Verified' if st.session_state.profile_verified else '⚠️ Not Verified'}</span>
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

def show_staff_dashboard():
    staff_info = st.session_state.staff_info
    department = staff_info['department']
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"🏛️ CanConnect | LGU Staff Portal")
        st.caption(f"Welcome back, {staff_info['name']}!")
    with col2:
        st.markdown(f"""
        <div style="background-color: #1e3c72; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <strong>{staff_info['role']}</strong><br>
            <span style="font-size: 12px;">{department}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.staff_logged_in = False
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown("---")
    
    # Department Overview Section
    if st.session_state.staff_page == 'overview':
        show_staff_overview(department)
    elif st.session_state.staff_page == 'pending':
        show_staff_pending_requests(department)
    elif st.session_state.staff_page == 'validation':
        show_staff_validation(department)
    elif st.session_state.staff_page == 'analytics':
        show_staff_analytics(department)
    elif st.session_state.staff_page == 'reports':
        show_staff_reports(department)

def show_staff_overview(department):
    st.header(f"📊 {department} Department Overview")
    
    # Department info
    department_info = {
        "Civil Registry": {"icon": "📄", "description": "Birth, Marriage, Death Certificates, CENOMAR", "services": ["Birth Certificate", "Marriage Certificate", "Death Certificate", "CENOMAR"]},
        "Treasury": {"icon": "💰", "description": "Business Permit Payments, License Renewals, Tax Payments, Fees", "services": ["Business Permit", "License Renewal", "Tax Payment", "Fees"]},
        "Health & Sanitation": {"icon": "🏥", "description": "Health Clearance, Sanitation, Workplace Inspection, Food Safety", "services": ["Health Clearance", "Sanitary Permit", "Food Handler's Certificate"]},
        "Admin": {"icon": "📋", "description": "Barangay Clearance, Police Clearance, ID Services, General Inquiries", "services": ["Barangay Clearance", "Police Clearance", "Senior Citizen ID", "PWD ID"]}
    }
    
    info = department_info.get(department, {"icon": "🏢", "description": "", "services": []})
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<h1 style='font-size: 80px;'>{info['icon']}</h1>", unsafe_allow_html=True)
    with col2:
        st.subheader(department)
        st.caption(info['description'])
        st.markdown("**Services offered:**")
        for service in info['services']:
            st.markdown(f"- {service}")
    
    st.markdown("---")
    
    # Quick stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Filter applications for this department
    dept_apps = [app for app in st.session_state.applications if app.get('office') == department]
    pending_count = len([app for app in dept_apps if app['status'] == 'Pending'])
    processing_count = len([app for app in dept_apps if app['status'] == 'Processing'])
    completed_count = len([app for app in dept_apps if app['status'] == 'Approved'])
    rejected_count = len([app for app in dept_apps if app['status'] == 'Rejected'])
    
    with col1:
        st.markdown(f"""
        <div class="staff-stat-card">
            <h3 style="margin:0; font-size:14px;">PENDING</h3>
            <h2 style="margin:0; font-size:32px;">{pending_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="staff-stat-card">
            <h3 style="margin:0; font-size:14px;">PROCESSING</h3>
            <h2 style="margin:0; font-size:32px;">{processing_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="staff-stat-card">
            <h3 style="margin:0; font-size:14px;">COMPLETED</h3>
            <h2 style="margin:0; font-size:32px;">{completed_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="staff-stat-card">
            <h3 style="margin:0; font-size:14px;">REJECTED</h3>
            <h2 style="margin:0; font-size:32px;">{rejected_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Document Validation Stats
    st.subheader("🤖 AI Document Validation System")
    
    dept_docs = [doc for doc in st.session_state.validated_documents if doc['department'] == department]
    total_scanned = len(dept_docs)
    passed = len([doc for doc in dept_docs if doc['validation_status'] == 'Passed'])
    flagged = len([doc for doc in dept_docs if doc['validation_status'] == 'Flagged'])
    total_issues = sum(len(doc['flagged_issues']) for doc in dept_docs if doc['validation_status'] == 'Flagged')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="ai-validation-card" style="text-align: center;">
            <h3 style="margin:0; color:#2196f3;">TOTAL SCANNED</h3>
            <h2 style="margin:0;">{total_scanned}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="ai-validation-card" style="text-align: center; border-left-color: #28a745;">
            <h3 style="margin:0; color:#28a745;">PASSED</h3>
            <h2 style="margin:0;">{passed}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="ai-validation-card" style="text-align: center; border-left-color: #dc3545;">
            <h3 style="margin:0; color:#dc3545;">FLAGGED</h3>
            <h2 style="margin:0;">{flagged}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="ai-validation-card" style="text-align: center; border-left-color: #ffc107;">
            <h3 style="margin:0; color:#ffc107;">TOTAL ISSUES</h3>
            <h2 style="margin:0;">{total_issues}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent flagged documents
    st.subheader("⚠️ Recent Flagged Documents")
    flagged_docs = [doc for doc in dept_docs if doc['validation_status'] == 'Flagged'][:5]
    
    if flagged_docs:
        for doc in flagged_docs:
            severity_class = f"severity-{doc['severity'].lower()}" if doc['severity'] else ""
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.write(f"**{doc['document_type']}**")
                st.caption(f"Tracking: {doc['tracking']}")
            with col2:
                st.write("Issues:")
                for issue in doc['flagged_issues']:
                    st.markdown(f"- {issue}")
            with col3:
                st.markdown(f"<span class='{severity_class}'>{doc['severity']}</span>", unsafe_allow_html=True)
                if st.button("Review", key=f"review_{doc['id']}"):
                    st.session_state.quick_action_modal = 'verify'
                    st.rerun()
            st.markdown("---")
    else:
        st.info("No flagged documents found")
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Verify Documents", use_container_width=True):
            st.session_state.quick_action_modal = 'verify'
    with col2:
        if st.button("📄 Issue Certificate", use_container_width=True):
            st.session_state.quick_action_modal = 'issue'
    with col3:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.quick_action_modal = 'reports'
    
    # Quick Action Modals
    if st.session_state.quick_action_modal == 'verify':
        show_verify_documents_modal(department)
    elif st.session_state.quick_action_modal == 'issue':
        show_issue_certificate_modal(department)
    elif st.session_state.quick_action_modal == 'reports':
        show_view_reports_modal(department)

def show_staff_pending_requests(department):
    st.header(f"📝 Pending Requests - {department}")
    
    # Filter pending requests for this department
    pending_apps = [app for app in st.session_state.applications 
                   if app.get('office') == department and app['status'] == 'Pending']
    
    if pending_apps:
        # Create dataframe for display
        data = []
        for app in pending_apps:
            data.append({
                "Service Type": app['type'],
                "Requestor Name": f"{app['first_name']} {app['last_name']}",
                "Status": app['status'],
                "Date Submitted": app['date'],
                "Tracking": app['tracking']
            })
        
        df = pd.DataFrame(data)
        
        # Display with action buttons
        for idx, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            with col1:
                st.write(f"**{row['Service Type']}**")
            with col2:
                st.write(row['Requestor Name'])
            with col3:
                status_class = f"status-{row['Status'].lower()}"
                st.markdown(f"<span class='status-badge {status_class}'>{row['Status']}</span>", unsafe_allow_html=True)
            with col4:
                st.write(row['Date Submitted'])
            with col5:
                if st.button("Review", key=f"review_{row['Tracking']}"):
                    st.info(f"Reviewing application: {row['Tracking']}")
            
            with st.expander("View Details"):
                app_details = [a for a in pending_apps if a['tracking'] == row['Tracking']][0]
                st.json(app_details)
            
            st.markdown("---")
    else:
        st.info("No pending requests for this department")

def show_staff_validation(department):
    st.header(f"✅ Document Validation - {department}")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Passed", "Flagged"])
    with col2:
        severity_filter = st.selectbox("Filter by Severity", ["All", "High", "Medium", "Low"])
    
    # Get department documents
    dept_docs = [doc for doc in st.session_state.validated_documents if doc['department'] == department]
    
    if status_filter != "All":
        dept_docs = [doc for doc in dept_docs if doc['validation_status'] == status_filter]
    
    if severity_filter != "All" and severity_filter in ["High", "Medium", "Low"]:
        dept_docs = [doc for doc in dept_docs if doc.get('severity') == severity_filter]
    
    if dept_docs:
        for doc in dept_docs:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
            with col1:
                st.write(f"**{doc['document_type']}**")
                st.caption(f"Tracking: {doc['tracking']}")
            with col2:
                st.write(f"Applicant: {doc['applicant']}")
                st.caption(f"Submitted: {doc['submission_date']}")
            with col3:
                if doc['validation_status'] == 'Passed':
                    st.markdown("<span class='status-badge status-verified'>PASSED</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='status-badge status-flagged'>FLAGGED</span>", unsafe_allow_html=True)
                
                if doc.get('severity'):
                    severity_class = f"severity-{doc['severity'].lower()}"
                    st.markdown(f"<span class='{severity_class}'>{doc['severity']}</span>", unsafe_allow_html=True)
            with col4:
                if doc['validation_status'] == 'Flagged':
                    st.write("Issues:")
                    for issue in doc['flagged_issues']:
                        st.markdown(f"- {issue}")
                else:
                    st.write("✅ No issues detected")
            
            if st.button("View Full Details", key=f"view_doc_{doc['id']}"):
                st.info(f"Showing details for document {doc['tracking']}")
            
            st.markdown("---")
    else:
        st.info("No documents found matching the filters")

def show_staff_analytics(department):
    st.header(f"📈 Analytics & Resource Planning - {department}")
    
    # Peak Request Hours
    with st.expander("📊 Peak Request Hours", expanded=True):
        st.subheader("Request Volume by Hour (8 AM - 5 PM)")
        
        # Create chart data
        hours = [d['hour'] for d in st.session_state.peak_hours_data]
        volumes = [d['volume'] for d in st.session_state.peak_hours_data]
        colors = [d['color'] for d in st.session_state.peak_hours_data]
        
        fig = go.Figure(data=[
            go.Bar(x=hours, y=volumes, marker_color=colors)
        ])
        
        fig.update_layout(
            title="Peak Request Hours",
            xaxis_title="Time",
            yaxis_title="Request Volume",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Peak level indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🟢 **Low** (<10 requests)")
        with col2:
            st.markdown("🟡 **Medium** (10-20 requests)")
        with col3:
            st.markdown("🔴 **High** (>20 requests)")
    
    # Processing Time Forecasts
    with st.expander("⏱️ Processing Time Forecasts", expanded=True):
        st.subheader("Service Processing Predictions")
        
        # Filter forecasts for department services
        dept_services = []
        if department == "Civil Registry":
            dept_services = ["Birth Certificate", "Marriage Certificate", "Death Certificate"]
        elif department == "Treasury":
            dept_services = ["Business Permit", "Tax Payment"]
        elif department == "Health & Sanitation":
            dept_services = ["Health Clearance"]
        elif department == "Admin":
            dept_services = ["Barangay Clearance", "Police Clearance"]
        
        forecast_data = [f for f in st.session_state.processing_forecasts if f['service'] in dept_services]
        
        for forecast in forecast_data:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                st.write(f"**{forecast['service']}**")
            with col2:
                st.write(f"Avg: {forecast['avg_time']} days")
            with col3:
                st.write(f"Predicted: {forecast['predicted_time']} days")
            with col4:
                trend_color = "green" if forecast['trend'] == "↑" else "orange" if forecast['trend'] == "→" else "red"
                st.markdown(f"<span style='color: {trend_color}; font-size: 20px;'>{forecast['trend']}</span>", unsafe_allow_html=True)
            with col5:
                st.progress(forecast['confidence']/100)
                st.caption(f"{forecast['confidence']}% confidence")
            
            st.markdown("---")
    
    # Manpower Allocation
    with st.expander("👥 Manpower Allocation Recommendations", expanded=True):
        st.subheader("Staffing Recommendations")
        
        for rec in st.session_state.manpower_recommendations:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            with col1:
                st.write(f"**{rec['time_slot']}**")
            with col2:
                st.write(f"Current: {rec['current_staff']}")
            with col3:
                st.write(f"Recommended: {rec['recommended_staff']}")
            with col4:
                st.progress(rec['utilization']/100)
                st.caption(f"Utilization: {rec['utilization']}%")
            
            st.markdown("---")

def show_staff_reports(department):
    st.header(f"📋 Monthly Reports - {department}")
    
    # Period selection
    col1, col2 = st.columns(2)
    with col1:
        report_period = st.selectbox("Select Period", ["Monthly", "Yearly"])
    with col2:
        if report_period == "Monthly":
            selected_month = st.selectbox("Select Month", [r['month'] for r in st.session_state.monthly_reports])
    
    # Display report
    if report_period == "Monthly":
        report = next((r for r in st.session_state.monthly_reports if r['month'] == selected_month), None)
        
        if report:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Pending", report['pending'])
            with col2:
                st.metric("Processing", report['processing'])
            with col3:
                st.metric("Completed", report['completed'])
            with col4:
                st.metric("Rejected", report['rejected'])
            with col5:
                st.metric("Avg Processing Time", f"{report['avg_processing_time']} days")
            
            # Chart
            statuses = ['Pending', 'Processing', 'Completed', 'Rejected']
            counts = [report['pending'], report['processing'], report['completed'], report['rejected']]
            
            fig = px.pie(values=counts, names=statuses, title=f"Request Status Distribution - {selected_month}")
            st.plotly_chart(fig, use_container_width=True)
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download Report (PDF)", use_container_width=True):
            st.success("Report downloaded successfully!")
    with col2:
        if st.button("🖨️ Print Report", use_container_width=True):
            st.success("Report sent to printer!")

def show_verify_documents_modal(department):
    with st.container():
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.subheader("✅ Verify Documents")
        
        # Get flagged documents
        flagged_docs = [doc for doc in st.session_state.validated_documents 
                       if doc['department'] == department and doc['validation_status'] == 'Flagged']
        
        if flagged_docs:
            # Filter options
            filter_status = st.selectbox("Filter by Severity", ["All", "High", "Medium", "Low"])
            
            filtered_docs = flagged_docs
            if filter_status != "All":
                filtered_docs = [doc for doc in flagged_docs if doc.get('severity') == filter_status]
            
            for doc in filtered_docs:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{doc['document_type']}** - {doc['applicant']}")
                        st.caption(f"Tracking: {doc['tracking']}")
                        st.write("Issues detected:")
                        for issue in doc['flagged_issues']:
                            st.markdown(f"- {issue}")
                    with col2:
                        severity_class = f"severity-{doc['severity'].lower()}"
                        st.markdown(f"<span class='{severity_class}'>{doc['severity']}</span>", unsafe_allow_html=True)
                        if st.button("Mark as Reviewed", key=f"mark_{doc['id']}"):
                            doc['validation_status'] = 'Passed'
                            st.success("Document marked as reviewed!")
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No flagged documents to review")
        
        if st.button("Close", key="close_verify"):
            st.session_state.quick_action_modal = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_issue_certificate_modal(department):
    with st.container():
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.subheader("📄 Issue Certificate")
        
        with st.form("issue_certificate_form"):
            col1, col2 = st.columns(2)
            with col1:
                recipient_name = st.text_input("Recipient Name*")
                document_type = st.selectbox("Document Type*", 
                    ["Birth Certificate", "Marriage Certificate", "Barangay Clearance", 
                     "Police Clearance", "Health Clearance", "Business Permit"])
            with col2:
                issue_date = st.date_input("Issue Date*", value=datetime.now())
                notes = st.text_area("Notes")
            
            # Generate certificate preview
            st.subheader("Certificate Preview")
            st.markdown(f"""
            <div style="border: 2px solid #1e3c72; padding: 20px; border-radius: 10px;">
                <h3 style="text-align: center;">Republic of the Philippines</h3>
                <h4 style="text-align: center;">Province of Surigao del Sur</h4>
                <h4 style="text-align: center;">Municipality of Cantilan</h4>
                <h4 style="text-align: center;">{department}</h4>
                <br>
                <p>This is to certify that <strong>{recipient_name if recipient_name else '[Recipient Name]'}</strong></p>
                <p>has been issued <strong>{document_type}</strong> on <strong>{issue_date.strftime('%B %d, %Y')}</strong>.</p>
                <br>
                <p style="text-align: right;">_________________________</p>
                <p style="text-align: right;">{st.session_state.staff_info['name']}</p>
                <p style="text-align: right;">{st.session_state.staff_info['role']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                submitted = st.form_submit_button("✅ Issue Certificate", use_container_width=True)
            with col2:
                download = st.form_submit_button("📥 Download", use_container_width=True)
            with col3:
                print_btn = st.form_submit_button("🖨️ Print", use_container_width=True)
            
            if submitted:
                if recipient_name:
                    st.success(f"Certificate issued successfully to {recipient_name}!")
                else:
                    st.error("Please fill in all required fields")
        
        if st.button("Close", key="close_issue"):
            st.session_state.quick_action_modal = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_view_reports_modal(department):
    with st.container():
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.subheader("📊 Department Reports")
        
        # Report type selection
        report_type = st.radio("Select Report Type", ["Monthly Summary", "Service Performance", "Staff Productivity"], horizontal=True)
        
        if report_type == "Monthly Summary":
            # Display monthly reports
            df_reports = pd.DataFrame(st.session_state.monthly_reports)
            st.dataframe(df_reports, use_container_width=True)
            
            # Chart
            fig = px.line(df_reports, x='month', y=['pending', 'processing', 'completed', 'rejected'],
                         title="Monthly Request Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Service Performance":
            # Service performance metrics
            services = ["Birth Certificate", "Marriage Certificate", "Barangay Clearance", "Business Permit"]
            avg_times = [3.2, 4.1, 1.1, 7.5]
            completion_rates = [95, 92, 98, 88]
            
            fig = go.Figure(data=[
                go.Bar(name='Avg Processing Time (days)', x=services, y=avg_times, yaxis='y'),
                go.Bar(name='Completion Rate (%)', x=services, y=completion_rates, yaxis='y2')
            ])
            
            fig.update_layout(
                title="Service Performance Metrics",
                yaxis=dict(title="Days", side='left'),
                yaxis2=dict(title="Percentage (%)", side='right', overlaying='y', range=[0, 100])
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Staff Productivity":
            # Mock staff productivity data
            staff_data = {
                'Staff Member': ['John Doe', 'Jane Smith', 'Mike Wilson', 'Sarah Brown'],
                'Requests Processed': [145, 132, 168, 121],
                'Avg Time (min)': [15, 12, 18, 14],
                'Accuracy Rate': [98, 97, 95, 99]
            }
            
            df_staff = pd.DataFrame(staff_data)
            st.dataframe(df_staff, use_container_width=True)
        
        # Export options
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export to CSV", use_container_width=True):
                st.success("Report exported successfully!")
        with col2:
            if st.button("📧 Email Report", use_container_width=True):
                st.success("Report sent to your email!")
        
        if st.button("Close", key="close_reports"):
            st.session_state.quick_action_modal = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# [Previous LGU and Barangay service functions remain the same]
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

# [Admin dashboard functions remain the same]
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
            new_password = st.text_input("Password", type="password", value="staff123")
        with col2:
            new_role = st.selectbox("Role", ["Processor", "Verifier", "Admin", "Encoder"])
            new_department = st.selectbox("Department", 
                ["Civil Registry", "Treasury", "Health & Sanitation", "Admin",
                 "Office of the Municipal Mayor", "Municipal Engineering Office",
                 "Municipal Police Station", "MSWDO (Social Welfare)"])
            new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        if st.button("Add Staff Member", use_container_width=True):
            if new_name and new_email:
                new_id = len(st.session_state.staff_members) + 1
                st.session_state.staff_members.append({
                    "id": new_id,
                    "name": new_name,
                    "email": new_email,
                    "password": hash_password(new_password),
                    "role": new_role,
                    "department": new_department,
                    "status": new_status
                })
                st.success(f"Staff member {new_name} added successfully to {new_department}!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    # Existing Staff Members
    st.markdown("### Existing Staff Members")
    
    # Filter by department
    dept_filter = st.selectbox("Filter by Department", 
        ["All"] + list(set([s['department'] for s in st.session_state.staff_members])))
    
    filtered_staff = st.session_state.staff_members
    if dept_filter != "All":
        filtered_staff = [s for s in st.session_state.staff_members if s['department'] == dept_filter]
    
    for staff in filtered_staff:
        with st.container():
            st.markdown(f"""
            <div class="staff-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong>{staff['name']}</strong><br>
                        <span style="color:#666;">{staff['email']} | {staff['role']} | {staff['department']}</span>
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
