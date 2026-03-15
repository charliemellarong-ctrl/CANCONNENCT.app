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
import time

# Page configuration
st.set_page_config(
    page_title="CanConnect",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cleaner design
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #283593 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: transparent;
        color: rgba(255, 255, 255, 0.9);
        border: none;
        text-align: left;
        padding: 12px 20px;
        margin: 2px 0;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        transform: translateX(5px);
    }
    
    /* User profile in sidebar */
    .sidebar-user {
        padding: 20px;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }
    
    .sidebar-user img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid white;
        margin-bottom: 10px;
        object-fit: cover;
    }
    
    .sidebar-user .user-name {
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .sidebar-user .user-email {
        color: rgba(255,255,255,0.7);
        font-size: 12px;
    }
    
    /* Main content area */
    .main-content {
        padding: 20px;
        background-color: #f8fafc;
        min-height: 100vh;
    }
    
    /* Cards */
    .modern-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Status badges */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-pending {
        background-color: #fff7e6;
        color: #b76e00;
    }
    
    .status-approved {
        background-color: #e6f7e6;
        color: #006600;
    }
    
    .status-processing {
        background-color: #e6f0ff;
        color: #0047b3;
    }
    
    .status-rejected {
        background-color: #ffe6e6;
        color: #cc0000;
    }
    
    /* Application table */
    .app-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .app-table th {
        text-align: left;
        padding: 12px;
        background-color: #f8fafc;
        font-weight: 600;
        color: #475569;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .app-table td {
        padding: 12px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .app-table tr:hover {
        background-color: #f8fafc;
    }
    
    /* Form styling */
    .stTextInput input, .stSelectbox select, .stDateInput input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 10px;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #1a237e;
        box-shadow: 0 0 0 2px rgba(26,35,126,0.1);
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
    }
    
    /* Dashboard stats */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #1a237e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
        margin: 5px 0;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 14px;
    }
    
    /* Chatbot styling - Simplified */
    .chat-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        border: none;
        border-radius: 60px;
        padding: 15px 25px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(26,35,126,0.3);
        transition: all 0.3s ease;
    }
    
    .chat-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26,35,126,0.4);
    }
    
    .chat-window {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        z-index: 999;
        overflow: hidden;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        background: #f8fafc;
    }
    
    .chat-message {
        margin-bottom: 10px;
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        margin-left: auto;
    }
    
    .bot-message {
        background: white;
        color: #1e293b;
        border: 1px solid #e2e8f0;
    }
    
    .chat-input-area {
        padding: 15px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 10px;
    }
    
    .chat-input {
        flex: 1;
        padding: 10px;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        outline: none;
    }
    
    .chat-input:focus {
        border-color: #1a237e;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
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
        st.session_state.payments = []
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
    # Chatbot session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "bot", "content": "Hello! I'm your CanConnect virtual assistant. How can I help you today?", "time": datetime.now().strftime("%H:%M")}
        ]
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_input_key' not in st.session_state:
        st.session_state.chat_input_key = 0

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
    hours = list(range(8, 18))
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

# Simplified Chatbot function
def add_chatbot():
    if st.session_state.user_type == 'citizen' and st.session_state.logged_in:
        st.markdown("""
        <div style="position: fixed; bottom: 30px; right: 30px; z-index: 999;">
        """, unsafe_allow_html=True)
        
        if not st.session_state.chat_open:
            if st.button("💬 Chat with Assistant", key="chat_toggle"):
                st.session_state.chat_open = True
                st.rerun()
        else:
            with st.container():
                st.markdown('<div class="chat-window">', unsafe_allow_html=True)
                
                # Header
                col1, col2 = st.columns([6,1])
                with col1:
                    st.markdown('<div class="chat-header"><b>CanConnect Assistant</b></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("✕", key="close_chat"):
                        st.session_state.chat_open = False
                        st.rerun()
                
                # Messages
                st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
                for msg in st.session_state.chat_messages[-10:]:  # Show last 10 messages
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Input
                with st.form(key=f"chat_form_{st.session_state.chat_input_key}"):
                    col1, col2 = st.columns([4,1])
                    with col1:
                        user_input = st.text_input("", placeholder="Type your message...", key="chat_input", label_visibility="collapsed")
                    with col2:
                        send = st.form_submit_button("Send")
                    
                    if send and user_input:
                        st.session_state.chat_messages.append({"role": "user", "content": user_input})
                        response = generate_chatbot_response(user_input)
                        st.session_state.chat_messages.append({"role": "bot", "content": response})
                        st.session_state.chat_input_key += 1
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def generate_chatbot_response(user_input):
    user_input_lower = user_input.lower()
    
    responses = {
        "hello": "Hello! How can I assist you with your government services today?",
        "hi": "Hi there! I'm here to help you with any questions about our services.",
        "help": "I can help you with:\n- Service applications\n- Document requirements\n- Processing times\n- Payment methods\n- Tracking your application\n- Office locations\n- Contact information",
        "requirements": "Document requirements vary by service. Common requirements include:\n- Valid ID\n- Proof of residency\n- Birth certificate\n- Completed application form\nWhich service are you interested in?",
        "fee": "Service fees:\n- Barangay Clearance: ₱50\n- Birth Certificate: ₱155 (PSA) / ₱75 (Local)\n- Business Permit: ₱500-2000\n- Police Clearance: ₱150\n- Health Clearance: ₱100",
        "payment": "We accept:\n- Cash (pay at LGU office)\n- E-Wallet (GCash, Maya)\n- Online Banking\n- Credit/Debit cards",
        "track": "To track your application:\n1. Go to 'My Requests' in the sidebar\n2. View your application status\n3. Click 'View Details' for more information",
        "contact": "Contact us:\n- Phone: (123) 456-7890\n- Email: support@cantilan.gov.ph\n- Address: Municipal Hall, Cantilan, Surigao del Sur\n- Hours: Mon-Fri, 8:00 AM - 5:00 PM"
    }
    
    for key, response in responses.items():
        if key in user_input_lower:
            return response
    
    return "I'm not sure about that. Please contact us at (123) 456-7890 or email support@cantilan.gov.ph for assistance."

# Main app structure
def main():
    load_css()
    init_session_state()
    
    # Sidebar navigation
    if st.session_state.logged_in or st.session_state.admin_logged_in or st.session_state.staff_logged_in:
        with st.sidebar:
            # User profile at top
            if st.session_state.logged_in:
                user_data = st.session_state.users.get(st.session_state.username, {})
                
                # Profile picture
                if st.session_state.profile_pic:
                    st.image(st.session_state.profile_pic, width=80, output_format="auto")
                else:
                    st.markdown('<div style="text-align: center; font-size: 60px;">👤</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; color: white; margin-bottom: 20px;">
                    <div style="font-weight: 600;">{user_data.get('first_name', '')} {user_data.get('last_name', '')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">{user_data.get('email', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif st.session_state.staff_logged_in:
                staff_info = st.session_state.get('staff_info', {})
                st.markdown(f"""
                <div style="text-align: center; color: white; margin-bottom: 20px;">
                    <div style="font-size: 60px;">👤</div>
                    <div style="font-weight: 600;">{staff_info.get('name', 'Staff')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">{staff_info.get('role', '')} - {staff_info.get('department', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif st.session_state.admin_logged_in:
                st.markdown(f"""
                <div style="text-align: center; color: white; margin-bottom: 20px;">
                    <div style="font-size: 60px;">👤</div>
                    <div style="font-weight: 600;">Administrator</div>
                    <div style="font-size: 12px; opacity: 0.8;">admin@cantilan.gov.ph</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation menu based on user type
            if st.session_state.admin_logged_in:
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
            
            else:  # Citizen
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                if st.button("👤 Profile", use_container_width=True):
                    st.session_state.page = 'profile'
                    st.rerun()
                if st.button("📋 My Requests", use_container_width=True):
                    st.session_state.page = 'my_requests'
                    st.rerun()
                if st.button("🏛️ LGU Services", use_container_width=True):
                    st.session_state.page = 'lgu'
                    st.rerun()
                if st.button("🏘️ Barangay Services", use_container_width=True):
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
        elif st.session_state.page == 'my_requests':
            show_my_requests()
        elif st.session_state.page == 'lgu':
            show_lgu_services()
        elif st.session_state.page == 'barangay':
            show_barangay_services()
        
        # Add chatbot only for citizens
        add_chatbot()

def show_login_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1a237e;">🏛️ CanConnect</h1>
        <p style="color: #64748b;">Your Digital Gateway to Government Services</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.registration_success:
        st.success("Registration successful! Please login with your credentials.")
        st.session_state.registration_success = False
    
    tab1, tab2, tab3, tab4 = st.tabs(["User Login", "User Register", "Staff Login", "Admin Login"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_type = 'citizen'
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
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*")
            with col2:
                last_name = st.text_input("Last Name*")
            
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
            password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Confirm Password*", type="password")
            
            submitted = st.form_submit_button("Register", use_container_width=True)
            
            if submitted:
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
        with st.form("staff_login_form"):
            staff_email = st.text_input("Staff Email")
            staff_password = st.text_input("Staff Password", type="password")
            submitted = st.form_submit_button("Staff Login", use_container_width=True)
            
            if submitted:
                if staff_email and staff_password:
                    success, staff_data = login_staff(staff_email, staff_password)
                    if success:
                        st.session_state.staff_logged_in = True
                        st.session_state.user_type = 'staff'
                        st.session_state.staff_info = staff_data
                        st.session_state.selected_department = staff_data['department']
                        st.session_state.staff_page = 'overview'
                        st.rerun()
                    else:
                        st.error(staff_data)
                else:
                    st.error("Please enter email and password")
    
    with tab4:
        with st.form("admin_login_form"):
            admin_email = st.text_input("Admin Email")
            admin_password = st.text_input("Admin Password", type="password")
            submitted = st.form_submit_button("Admin Login", use_container_width=True)
            
            if submitted:
                if admin_email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[admin_email] == hash_password(admin_password):
                    st.session_state.admin_logged_in = True
                    st.session_state.user_type = 'admin'
                    st.session_state.admin_page = 'dashboard_overview'
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")

def show_dashboard():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("Dashboard")
    
    # Get user-specific applications
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    # Statistics
    active_count = len([app for app in user_apps if app['status'] in ['Processing', 'Pending']])
    completed_count = len([app for app in user_apps if app['status'] == 'Approved'])
    total_count = len(user_apps)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Active Requests</div>
            <div class="stat-value">{active_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Completed</div>
            <div class="stat-value">{completed_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Requests</div>
            <div class="stat-value">{total_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Recent Applications")
    
    if user_apps:
        recent_apps = sorted(user_apps, key=lambda x: x['date'], reverse=True)[:5]
        for app in recent_apps:
            status_class = f"status-{app['status'].lower()}"
            st.markdown(f"""
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{app['type']}</strong><br>
                        <small>Tracking: {app['tracking']} | {app['date']}</small>
                    </div>
                    <span class="status-badge {status_class}">{app['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No applications yet. Start by applying for a service from LGU or Barangay services.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_my_requests():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("My Requests")
    
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    if user_apps:
        for app in user_apps:
            status_class = f"status-{app['status'].lower()}"
            with st.expander(f"{app['type']} - {app['tracking']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Service:** {app['type']}")
                    st.write(f"**Date Submitted:** {app['date']}")
                    st.write(f"**Office:** {app.get('office', 'N/A')}")
                with col2:
                    st.write(f"**Status:** <span class='status-badge {status_class}'>{app['status']}</span>", unsafe_allow_html=True)
                    st.write(f"**Payment:** {app.get('payment_method', 'N/A')}")
                    st.write(f"**Purpose:** {app.get('purpose', 'N/A')}")
                
                if app['status'] == 'Approved':
                    st.success("Your request has been approved! You can claim your document at the office.")
                elif app['status'] == 'Processing':
                    st.info("Your request is being processed.")
                elif app['status'] == 'Pending':
                    st.warning("Your request is pending review.")
    else:
        st.info("You haven't submitted any requests yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_profile():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("Profile")
    
    user_data = st.session_state.users.get(st.session_state.username, {})
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        if st.session_state.profile_pic:
            st.image(st.session_state.profile_pic, width=150, output_format="auto")
        else:
            st.markdown('<div style="font-size: 150px;">👤</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Change Photo", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            st.session_state.profile_pic = bytes_data
            st.session_state.users[st.session_state.username]['profile_pic'] = bytes_data
            st.success("Profile picture updated!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <h3>{user_data.get('first_name', '')} {user_data.get('last_name', '')}</h3>
            <p>Email: {user_data.get('email', '')}</p>
            <p>Phone: {user_data.get('phone', '')}</p>
            <p>Status: {'✅ Verified' if st.session_state.profile_verified else '⚠️ Not Verified'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.profile_verified:
            st.info("Verify your account by uploading a valid ID")
            id_file = st.file_uploader("Upload Valid ID", type=['png', 'jpg', 'jpeg', 'pdf'])
            if id_file and st.button("Submit for Verification"):
                st.session_state.profile_verified = True
                st.session_state.users[st.session_state.username]['verified'] = True
                st.success("Verification submitted successfully!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_lgu_services():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("LGU Services")
    
    # Simplified LGU services list
    services = {
        "Civil Registry": ["Birth Certificate", "Marriage Certificate", "Death Certificate", "CENOMAR"],
        "Business Permits": ["Business Permit", "Building Permit", "Occupancy Permit"],
        "Health Services": ["Health Clearance", "Sanitary Permit", "Medical Certificate"],
        "Social Welfare": ["Certificate of Indigency", "Social Case Study", "4Ps Certification"]
    }
    
    for category, items in services.items():
        st.subheader(category)
        cols = st.columns(3)
        for idx, service in enumerate(items):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="modern-card">
                        <strong>{service}</strong><br>
                        <small>Click to apply</small>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Apply", key=f"apply_{service}"):
                        st.session_state['selected_service'] = {"name": service, "fee": "₱150"}
                        st.session_state['selected_office'] = category
                        show_application_form(service, category)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_barangay_services():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("Barangay Services")
    
    services = {
        "Clearances": ["Barangay Clearance", "Certificate of Residency", "Certificate of Indigency"],
        "IDs": ["Senior Citizen ID", "PWD ID", "Solo Parent ID"],
        "Assistance": ["Medical Assistance", "Financial Assistance", "Burial Assistance"]
    }
    
    for category, items in services.items():
        st.subheader(category)
        cols = st.columns(3)
        for idx, service in enumerate(items):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="modern-card">
                        <strong>{service}</strong><br>
                        <small>Click to apply</small>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Apply", key=f"apply_{service}"):
                        st.session_state['selected_service'] = {"name": service, "fee": "₱50"}
                        st.session_state['selected_office'] = "Barangay Hall"
                        show_application_form(service, "Barangay Hall")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_application_form(service_name, office_name):
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.subheader(f"Apply for {service_name}")
    st.caption(f"Office: {office_name}")
    
    with st.form(key=f"form_{service_name.replace(' ', '_')}"):
        st.info(f"This application will be processed by: **{office_name}**")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*")
            birth_date = st.date_input("Date of Birth*", min_value=datetime(1900,1,1), max_value=datetime.now())
            contact_no = st.text_input("Contact Number*")
        with col2:
            last_name = st.text_input("Last Name*")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
            email = st.text_input("Email*", value=st.session_state.username if st.session_state.username else "")
        
        barangay = st.selectbox("Barangay*", ["Barangay 1", "Barangay 2", "Barangay 3", "Barangay 4"])
        street = st.text_input("Street/Purok*")
        
        if "Certificate" in service_name or "Clearance" in service_name:
            purpose = st.text_area("Purpose of Application*")
        
        payment_method = st.radio("Payment Method", ["E-Wallet", "Cash (Pay at Office)", "Online Banking"], horizontal=True)
        agree = st.checkbox("I certify that all information provided is true and correct*")
        
        submitted = st.form_submit_button("Submit Application", use_container_width=True)
        
        if submitted:
            if agree and first_name and last_name and contact_no and email:
                tracking_no = f"{service_name[:2].upper()}-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
                
                new_app = {
                    "user_email": st.session_state.username,
                    "type": service_name,
                    "office": office_name,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Pending",
                    "tracking": tracking_no,
                    "first_name": first_name,
                    "last_name": last_name,
                    "contact_no": contact_no,
                    "email": email,
                    "barangay": barangay,
                    "purpose": purpose if 'purpose' in locals() else "N/A",
                    "payment_method": payment_method,
                    "payment_status": "Pending"
                }
                
                st.session_state.applications.append(new_app)
                st.success(f"Application submitted successfully! Tracking Number: **{tracking_no}**")
                st.info("You can track your application status in 'My Requests'.")
                
                if st.button("Apply for Another Service"):
                    st.rerun()
            else:
                st.error("Please fill in all required fields and agree to terms")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_staff_dashboard():
    staff_info = st.session_state.staff_info
    department = staff_info['department']
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title(f"Staff Portal - {department}")
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_staff_overview(department):
    st.subheader("Department Overview")
    
    dept_apps = [app for app in st.session_state.applications if app.get('office') == department]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending", len([app for app in dept_apps if app['status'] == 'Pending']))
    with col2:
        st.metric("Processing", len([app for app in dept_apps if app['status'] == 'Processing']))
    with col3:
        st.metric("Completed", len([app for app in dept_apps if app['status'] == 'Approved']))
    with col4:
        st.metric("Rejected", len([app for app in dept_apps if app['status'] == 'Rejected']))
    
    st.markdown("---")
    st.subheader("Recent Applications")
    
    if dept_apps:
        for app in dept_apps[-5:]:
            status_class = f"status-{app['status'].lower()}"
            st.markdown(f"""
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{app['type']}</strong><br>
                        <small>{app['first_name']} {app['last_name']} | {app['date']}</small>
                    </div>
                    <span class="status-badge {status_class}">{app['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_staff_pending_requests(department):
    st.subheader("Pending Requests")
    
    pending_apps = [app for app in st.session_state.applications 
                   if app.get('office') == department and app['status'] == 'Pending']
    
    if pending_apps:
        for app in pending_apps:
            with st.expander(f"{app['type']} - {app['first_name']} {app['last_name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Tracking:** {app['tracking']}")
                    st.write(f"**Date:** {app['date']}")
                    st.write(f"**Contact:** {app['contact_no']}")
                with col2:
                    st.write(f"**Purpose:** {app.get('purpose', 'N/A')}")
                    st.write(f"**Payment:** {app.get('payment_method', 'N/A')}")
                
                new_status = st.selectbox("Update Status", ["Pending", "Processing", "Approved", "Rejected"], key=f"status_{app['tracking']}")
                if st.button("Update", key=f"update_{app['tracking']}"):
                    app['status'] = new_status
                    st.success(f"Status updated to {new_status}")
                    st.rerun()
    else:
        st.info("No pending requests")

def show_staff_validation(department):
    st.subheader("Document Validation")
    st.info("Document validation interface would appear here")

def show_staff_analytics(department):
    st.subheader("Analytics")
    st.info("Analytics dashboard would appear here")

def show_staff_reports(department):
    st.subheader("Reports")
    st.info("Reports interface would appear here")

def show_admin_dashboard():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_admin_dashboard_overview():
    st.title("Admin Dashboard")
    
    total_apps = len(st.session_state.applications)
    pending_apps = len([app for app in st.session_state.applications if app['status'] == 'Pending'])
    total_users = len(st.session_state.users)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Applications", total_apps)
    with col2:
        st.metric("Pending Requests", pending_apps)
    with col3:
        st.metric("Registered Users", total_users)

def show_admin_manage_request():
    st.subheader("Manage Requests")
    
    if st.session_state.applications:
        for app in st.session_state.applications:
            with st.expander(f"{app['type']} - {app['tracking']}"):
                st.json(app)
    else:
        st.info("No applications found")

def show_admin_manage_payment():
    st.subheader("Manage Payments")
    st.info("Payment management interface would appear here")

def show_admin_reports_analytics():
    st.subheader("Reports & Analytics")
    st.info("Reports and analytics interface would appear here")

def show_admin_user_management():
    st.subheader("User Management")
    
    # Manage Staff
    st.markdown("### Staff Members")
    
    with st.expander("Add New Staff"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
        with col2:
            new_role = st.selectbox("Role", ["Processor", "Verifier", "Admin"])
            new_department = st.selectbox("Department", 
                ["Civil Registry", "Treasury", "Health & Sanitation", "Admin",
                 "Office of the Municipal Mayor", "Municipal Engineering Office"])
            new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        if st.button("Add Staff"):
            if new_name and new_email:
                new_id = len(st.session_state.staff_members) + 1
                st.session_state.staff_members.append({
                    "id": new_id,
                    "name": new_name,
                    "email": new_email,
                    "password": hash_password("staff123"),
                    "role": new_role,
                    "department": new_department,
                    "status": new_status
                })
                st.success(f"Staff member {new_name} added successfully!")
                st.rerun()
    
    # Display staff members
    for staff in st.session_state.staff_members:
        st.markdown(f"""
        <div class="modern-card">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong>{staff['name']}</strong><br>
                    <small>{staff['email']} | {staff['role']} | {staff['department']}</small>
                </div>
                <span class="status-badge status-{'approved' if staff['status'] == 'Active' else 'pending'}">
                    {staff['status']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
