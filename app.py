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
    page_title="CanConnect",
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
        display: inline-block;
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
        display: inline-block;
    }
    
    .severity-medium {
        background-color: #ffc107;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        display: inline-block;
    }
    
    .severity-low {
        background-color: #17a2b8;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        display: inline-block;
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
        position: relative;
        z-index: 1000;
    }
    
    /* Chatbot styling - Fixed version */
    .chat-fixed-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        width: 380px;
        max-width: 90vw;
    }
    
    .chat-toggle-btn {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 60px;
        padding: 15px 25px;
        cursor: pointer;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: auto;
        float: right;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .chat-toggle-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
    }
    
    .chat-window {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        overflow: hidden;
        margin-top: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .chat-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .chat-header h4 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .chat-close-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        padding: 0 8px;
        border-radius: 8px;
        transition: all 0.3s ease;
        line-height: 1;
    }
    
    .chat-close-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
    }
    
    .chat-messages {
        height: 350px;
        overflow-y: auto;
        padding: 20px;
        background: #f8faff;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .message {
        display: flex;
        flex-direction: column;
        max-width: 85%;
    }
    
    .user-message {
        align-self: flex-end;
    }
    
    .bot-message {
        align-self: flex-start;
    }
    
    .message-bubble {
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 14px;
        line-height: 1.5;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .user-message .message-bubble {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .bot-message .message-bubble {
        background: white;
        color: #333;
        border-bottom-left-radius: 5px;
        border: 1px solid #e0e5f0;
    }
    
    .message-time {
        font-size: 10px;
        color: #999;
        margin-top: 4px;
        margin-left: 8px;
    }
    
    .chat-input-area {
        padding: 20px;
        background: white;
        border-top: 2px solid #f0f2f5;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .chat-input-field {
        flex: 1;
        padding: 12px 16px;
        border: 2px solid #e0e5f0;
        border-radius: 30px;
        outline: none;
        font-size: 14px;
        transition: all 0.3s ease;
        background: #f8faff;
    }
    
    .chat-input-field:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30,60,114,0.1);
        background: white;
    }
    
    .chat-send-btn {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .chat-send-btn:hover {
        transform: translateX(2px);
        box-shadow: 0 5px 15px rgba(30,60,114,0.3);
    }
    
    /* Quick reply buttons */
    .quick-replies {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
    }
    
    .quick-reply-btn {
        background: white;
        border: 1px solid #1e3c72;
        color: #1e3c72;
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-reply-btn:hover {
        background: #1e3c72;
        color: white;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
        background: white;
        border-radius: 18px;
        border: 1px solid #e0e5f0;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #1e3c72;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
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
    # Chatbot session state - Fixed
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "bot", "content": "👋 Hello! I'm your Cantilan-eCivil virtual assistant. How can I help you today?", "time": datetime.now().strftime("%H:%M")}
        ]
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_typing' not in st.session_state:
        st.session_state.chat_typing = False
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

# Fixed Chatbot function
def add_chatbot():
    """Add a floating chatbot to the page"""
    
    # Quick reply options
    quick_replies = [
        "What are the requirements?",
        "How much is the fee?",
        "Processing time?",
        "Payment methods",
        "Track my application",
        "Contact info"
    ]
    
    # Chatbot container - Fixed positioning
    st.markdown('<div class="chat-fixed-container">', unsafe_allow_html=True)
    
    # Toggle button
    if not st.session_state.chat_open:
        if st.button("💬 Chat with Assistant", key="chat_toggle_main", use_container_width=True):
            st.session_state.chat_open = True
            st.rerun()
    else:
        # Chat window
        with st.container():
            st.markdown('<div class="chat-window">', unsafe_allow_html=True)
            
            # Header
            st.markdown("""
            <div class="chat-header">
                <h4>💬 Cantilan-eCivil Assistant</h4>
            """, unsafe_allow_html=True)
            
            # Close button as Streamlit button
            col1, col2 = st.columns([6, 1])
            with col2:
                if st.button("✕", key="close_chat_btn"):
                    st.session_state.chat_open = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Messages
            st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
            
            # Display all messages
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <div class="message-bubble">{msg['content']}</div>
                        <div class="message-time">{msg['time']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message bot-message">
                        <div class="message-bubble">{msg['content']}</div>
                        <div class="message-time">{msg['time']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Typing indicator
            if st.session_state.chat_typing:
                st.markdown("""
                <div class="message bot-message">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick replies
            st.markdown('<div class="quick-replies">', unsafe_allow_html=True)
            cols = st.columns(3)
            for idx, reply in enumerate(quick_replies):
                with cols[idx % 3]:
                    if st.button(reply, key=f"quick_reply_{idx}_{st.session_state.chat_input_key}"):
                        # Add user message
                        st.session_state.chat_messages.append({
                            "role": "user",
                            "content": reply,
                            "time": datetime.now().strftime("%H:%M")
                        })
                        
                        # Show typing indicator
                        st.session_state.chat_typing = True
                        st.rerun()
                        
                        # Generate response
                        bot_response = generate_chatbot_response(reply)
                        
                        # Add bot response
                        st.session_state.chat_messages.append({
                            "role": "bot",
                            "content": bot_response,
                            "time": datetime.now().strftime("%H:%M")
                        })
                        
                        # Hide typing indicator
                        st.session_state.chat_typing = False
                        st.session_state.chat_input_key += 1
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input area
            with st.form(key=f"chat_form_{st.session_state.chat_input_key}"):
                cols = st.columns([4, 1])
                with cols[0]:
                    user_input = st.text_input("Type your message...", key=f"chat_input_{st.session_state.chat_input_key}", label_visibility="collapsed")
                with cols[1]:
                    send = st.form_submit_button("Send", use_container_width=True)
                
                if send and user_input:
                    # Add user message
                    st.session_state.chat_messages.append({
                        "role": "user",
                        "content": user_input,
                        "time": datetime.now().strftime("%H:%M")
                    })
                    
                    # Show typing indicator
                    st.session_state.chat_typing = True
                    st.rerun()
                    
                    # Generate response
                    bot_response = generate_chatbot_response(user_input)
                    
                    # Add bot response
                    st.session_state.chat_messages.append({
                        "role": "bot",
                        "content": bot_response,
                        "time": datetime.now().strftime("%H:%M")
                    })
                    
                    # Hide typing indicator
                    st.session_state.chat_typing = False
                    st.session_state.chat_input_key += 1
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_chatbot_response(user_input):
    """Generate chatbot response based on user input"""
    user_input_lower = user_input.lower()
    
    # FAQ responses
    responses = {
        "hello": "👋 Hello! How can I assist you with your government services today?",
        "hi": "👋 Hi there! I'm here to help you with any questions about our services.",
        "help": "I can help you with:\n• Service applications\n• Document requirements\n• Processing times\n• Payment methods\n• Tracking your application\n• Office locations\n• Contact information\n\nJust ask me anything!",
        "requirements": "📋 **Document requirements** vary by service. Common requirements include:\n• Valid ID (any government ID)\n• Proof of residency (Barangay Clearance)\n• Birth certificate (for civil registry services)\n• Completed application form\n• 1x1 or 2x2 ID pictures\n\nWhich specific service are you interested in?",
        "fee": "💰 **Service fees:**\n• Barangay Clearance: ₱50\n• Birth Certificate: ₱155 (PSA) / ₱75 (Local)\n• Marriage Certificate: ₱155 (PSA) / ₱75 (Local)\n• Business Permit: ₱500-2000\n• Police Clearance: ₱150\n• Health Clearance: ₱100\n\n*Fees may vary. Check specific service for exact amount.*",
        "payment": "💳 We accept the following payment methods:\n• **Cash** - Pay at the LGU office\n• **E-Wallet** - GCash, Maya\n• **Online Banking** - BDO, BPI, etc.\n• **Credit/Debit Cards** - At the office\n\nOnline payments are processed immediately, while cash payments need verification.",
        "track": "🔍 To **track your application**:\n1. Log in to your account\n2. Go to Dashboard\n3. Check 'Recent Applications'\n4. Click 'View Details' for status\n\nYou'll also receive SMS notifications at every step!",
        "tracking": "🔍 To **track your application**:\n1. Log in to your account\n2. Go to Dashboard\n3. Check 'Recent Applications'\n4. Click 'View Details' for status\n\nYou'll also receive SMS notifications at every step!",
        "processing time": "⏱️ **Processing times:**\n• Barangay Clearance: 1 day\n• Birth Certificate: 3-5 days\n• Marriage Certificate: 3-5 days\n• Business Permit: 7-10 days\n• Police Clearance: 1-2 days\n• Health Clearance: 1-2 days\n\n*Times may vary during peak periods.*",
        "contact": "📞 **Contact us:**\n• Phone: (123) 456-7890\n• Email: support@cantilan.gov.ph\n• Address: Municipal Hall, Cantilan, Surigao del Sur\n• Office hours: Mon-Fri, 8:00 AM - 5:00 PM\n\nFeel free to visit or call during office hours!",
        "location": "📍 Our office is located at:\n**Municipal Hall**\nCantilan, Surigao del Sur\n\nOffice hours: Monday-Friday, 8:00 AM - 5:00 PM\n\nYou can find us on Google Maps: [View Map](https://maps.google.com)",
        "barangay clearance": "📄 **Barangay Clearance**\n• Fee: ₱50\n• Processing: 1 day\n• Requirements:\n  - Valid ID\n  - Proof of residency\n  - Community tax certificate (cedula)\n  - 1x1 ID picture",
        "birth certificate": "📄 **Birth Certificate**\n• Fee: ₱155 (PSA) / ₱75 (Local)\n• Processing: 3-5 days\n• Requirements:\n  - Valid ID of requesting party\n  - Completed application form\n  - If requesting for others: authorization letter",
        "business permit": "🏢 **Business Permit**\n• Fee: ₱500-2000 (varies by business type)\n• Processing: 7-10 days\n• Requirements:\n  - Barangay Clearance\n  - Tax Clearance\n  - DTI/SEC registration\n  - Lease contract or proof of ownership\n  - Occupancy permit",
        "police clearance": "👮 **Police Clearance**\n• Fee: ₱150\n• Processing: 1-2 days\n• Requirements:\n  - Valid ID\n  - Barangay Clearance\n  - 2x2 ID picture (white background)\n  - Proof of residency",
        "health clearance": "🏥 **Health Clearance**\n• Fee: ₱100\n• Processing: 1-2 days\n• Requirements:\n  - Valid ID\n  - Chest X-ray result (if required)\n  - Stool exam result (for food handlers)",
        "thanks": "You're welcome! 😊 Is there anything else I can help you with?",
        "thank you": "You're welcome! 😊 Is there anything else I can help you with?",
        "bye": "👋 Goodbye! Feel free to chat again if you need assistance. Have a great day!",
        "goodbye": "👋 Goodbye! Feel free to chat again if you need assistance. Have a great day!"
    }
    
    # Check for keywords
    for key, response in responses.items():
        if key in user_input_lower:
            return response
    
    # Default response with helpful suggestions
    return "I'm not sure about that. 🤔 Here are some things you can ask me:\n• Service requirements\n• Processing times\n• Payment methods\n• Office locations\n• Contact information\n\nOr you can contact us directly at (123) 456-7890 or support@cantilan.gov.ph"

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
                user_data = st.session_state.users.get(st.session_state.username, {})
                st.markdown(f"""
                <div style="text-align: center; color: white; padding: 10px;">
                    <div style="font-size: 40px;">👤</div>
                    <h3 style="margin: 5px 0; color: white;">{user_data.get('first_name', 'User')} {user_data.get('last_name', '')}</h3>
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
    
    # Add chatbot to all pages except login
    if st.session_state.logged_in or st.session_state.admin_logged_in or st.session_state.staff_logged_in:
        add_chatbot()

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

# [Previous LGU, Barangay, Staff, and Admin functions remain the same - they are too long to repeat here]
# For brevity, I'm showing only the modified parts. In your actual code, keep all the existing functions
# and just add the chatbot function and the add_chatbot() calls at the end of main()

if __name__ == "__main__":
    main()
