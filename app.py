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
    /* Mobile-friendly adjustments */
    .stApp {
        max-width: 100%;
        padding: 0px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Blue sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        text-align: left;
        padding: 12px 20px;
        margin: 2px 0;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Profile picture in sidebar */
    .sidebar-profile {
        text-align: center;
        padding: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }
    
    .sidebar-profile img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid white;
        margin-bottom: 10px;
        object-fit: cover;
    }
    
    .sidebar-profile .user-name {
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .sidebar-profile .user-email {
        color: rgba(255,255,255,0.8);
        font-size: 12px;
    }
    
    /* Center application form */
    .centered-form {
        display: block !important;
        width: 100% !important;
        max-width: none !important;
        margin: 0 !important;
        padding: 20px !important;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
        object-fit: cover;
    }
    
    .profile-pic-container {
        position: relative;
        display: inline-block;
    }
    
    .verification-badge {
        background-color: #ffc107;
        color: #000;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 2px rgba(30,60,114,0.1);
    }
    
    /* Card styling */
    .dashboard-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .admin-stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Staff stat cards */
    .staff-stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 12px;
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
    
    /* Application items */
    .recent-app {
        background-color: white;
        padding: 15px;
        margin: 5px 0;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
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
    
    /* Chat page styling */
    .chat-messages {
        height: 400px;
        overflow-y: auto;
        padding: 20px;
        background: #f8fafc;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .message {
        margin-bottom: 15px;
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 70%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        margin-left: auto;
    }
    
    .bot-message {
        background: white;
        color: #333;
        border: 1px solid #e2e8f0;
        margin-right: auto;
    }
    
    .quick-reply-btn {
        background: white;
        border: 1px solid #1e3c72;
        color: #1e3c72;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 5px;
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
        padding: 10px;
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
    
    /* Make forms full-width */
    .stForm {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Make containers full-width */
    .stContainer {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Remove form padding constraints */
    .stForm > div:first-child {
        width: 100% !important;
        padding: 0 !important;
    }
    
    /* Full-width for centered-form wrapper */
    .centered-form {
        display: block !important;
        width: 100% !important;
        padding: 20px !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Force full-width for all Streamlit containers */
    [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 1rem !important;
    }
    
    /* Remove max-width from main content */
    .main {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Streamlit block container */
    .stBlock {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Element container full width */
    [data-testid="stElementContainer"] {
        width: 100% !important;
        max-width: 100% !important;
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
        st.session_state.applications = generate_sample_applications()
    if 'users' not in st.session_state:
        st.session_state.users = generate_sample_users()
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
    if 'page' not in st.session_state or 'settings' not in str(st.session_state):
        st.session_state.settings_page = None
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = {
            'notifications': True,
            'email_alerts': True,
            'dark_mode': False,
            'language': 'English',
            'theme': 'light'
        }
    if 'selected_department' not in st.session_state:
        st.session_state.selected_department = None
    if 'staff_members' not in st.session_state:
        st.session_state.staff_members = [
            {"id": 1, "name": "John Doe", "email": "john@cantilan.gov.ph", "role": "Processor", "status": "Active", "department": "Civil Registry", "password": hash_password("staff123")},
            {"id": 2, "name": "Jane Smith", "email": "jane@cantilan.gov.ph", "role": "Staff", "status": "Active", "department": "Treasury", "password": hash_password("staff123")},
            {"id": 3, "name": "Mike Wilson", "email": "mike@cantilan.gov.ph", "role": "Admin", "status": "Active", "department": "Health & Sanitation", "password": hash_password("staff123")},
            {"id": 4, "name": "Sofia Cruz", "email": "sofia@cantilan.gov.ph", "role": "Processor", "status": "Active", "department": "Civil Registry", "password": hash_password("staff123")},
            {"id": 5, "name": "Ramon Torres", "email": "ramon@cantilan.gov.ph", "role": "Staff", "status": "Active", "department": "Barangay Services", "password": hash_password("staff123")},
            {"id": 6, "name": "Angela Lopez", "email": "angela@cantilan.gov.ph", "role": "Processor", "status": "Inactive", "department": "Health & Sanitation", "password": hash_password("staff123")}
        ]
    if 'payments' not in st.session_state:
        st.session_state.payments = generate_sample_payments()
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
    if 'notifications' not in st.session_state:
        st.session_state.notifications = generate_sample_notifications()
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = generate_sample_activity_log()
    # Admin/Staff specific data
    if 'admin_dashboard_data' not in st.session_state:
        st.session_state.admin_dashboard_data = generate_admin_dashboard_data()
    if 'staff_workload' not in st.session_state:
        st.session_state.staff_workload = generate_staff_workload_data()
    if 'department_statistics' not in st.session_state:
        st.session_state.department_statistics = generate_department_statistics()
    if 'quick_action_modal' not in st.session_state:
        st.session_state.quick_action_modal = None
    # Chatbot session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "bot", "content": "Hello! I'm your CanConnect virtual assistant. How can I help you today?"}
        ]
    if 'chat_input_key' not in st.session_state:
        st.session_state.chat_input_key = 0
    if 'just_submitted' not in st.session_state:
        st.session_state.just_submitted = False
    if 'submitted_tracking' not in st.session_state:
        st.session_state.submitted_tracking = None
    if 'updated_profile' not in st.session_state:
        st.session_state.updated_profile = False

# User authentication functions - must be defined before generate functions that use them
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

def generate_sample_applications():
    """Generate diverse sample applications for demo purposes"""
    sample_apps = []
    
    # Service to office mapping
    service_office_map = {
        "Birth Certificate": "Civil Registry",
        "Marriage Certificate": "Civil Registry",
        "Death Certificate": "Civil Registry",
        "CENOMAR": "Civil Registry",
        "Barangay Clearance": "Barangay Hall",
        "Police Clearance": "Admin",
        "Senior Citizen ID": "Admin",
        "PWD ID": "Admin",
        "Health Clearance": "Health & Sanitation",
        "Sanitary Permit": "Health & Sanitation",
        "Food Handler Certificate": "Health & Sanitation",
        "Business Permit": "Treasury",
        "License Renewal": "Treasury",
        "Building Permit": "Treasury",
        "Tricycle Franchise": "Treasury",
        "Job Seeker Certificate": "Admin",
        "Certificate of Residency": "Barangay Hall"
    }
    
    services = list(service_office_map.keys())
    statuses = ["Pending", "Processing", "Approved", "Rejected"]
    barangays = ["Barangay 1", "Barangay 2", "Barangay 3", "Barangay 4", "Barangay 5"]
    payment_methods = ["E-Wallet (GCash, Maya)", "Cash (Pay at LGU)", "Online Banking"]
    
    sample_names = [
        {"first": "Juan", "last": "Dela Cruz"},
        {"first": "Maria", "last": "Santos"},
        {"first": "Pedro", "last": "Reyes"},
        {"first": "Anna", "last": "Rodriguez"},
        {"first": "Carlos", "last": "Garcia"},
        {"first": "Rosa", "last": "Lopez"},
        {"first": "Miguel", "last": "Torres"},
        {"first": "Elena", "last": "Morales"},
        {"first": "Fernando", "last": "Gonzales"},
        {"first": "Lisa", "last": "Mendoza"}
    ]
    
    # Generate 40 applications across different departments
    for i in range(40):
        idx = i % len(sample_names)
        name = sample_names[idx]
        service = services[i % len(services)]
        office = service_office_map[service]
        
        # Weighted status distribution (more pending than others)
        rand_val = random.random()
        if rand_val < 0.4:
            status = "Pending"
        elif rand_val < 0.7:
            status = "Processing"
        elif rand_val < 0.9:
            status = "Approved"
        else:
            status = "Rejected"
        
        tracking_no = f"{service[:2].upper()}-{(datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        submit_date = (datetime.now() - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d")
        
        app = {
            "user_email": f"{name['first'].lower()}.{name['last'].lower()}{i}@email.com",
            "type": service,
            "office": office,
            "date": submit_date,
            "status": status,
            "tracking": tracking_no,
            "first_name": name["first"],
            "last_name": name["last"],
            "contact_no": f"09{random.randint(100000000, 999999999)}",
            "email": f"{name['first'].lower()}.{name['last'].lower()}{i}@email.com",
            "barangay": random.choice(barangays),
            "purpose": "Application for service",
            "payment_method": random.choice(payment_methods),
            "payment_status": "Verified" if random.random() > 0.3 else "Pending Verification",
            "processed_by": random.choice(["John Doe", "Jane Smith", "Sofia Cruz", "Ramon Torres"])
        }
        sample_apps.append(app)
    
    return sample_apps

def generate_admin_dashboard_data():
    """Generate admin-specific metrics and statistics"""
    return {
        "daily_revenue": [random.randint(5000, 15000) for _ in range(30)],
        "department_workload": {
            "Civil Registry": random.randint(40, 80),
            "Treasury": random.randint(30, 70),
            "Health & Sanitation": random.randint(20, 60),
            "Admin": random.randint(35, 75),
            "Barangay Hall": random.randint(25, 65)
        },
        "service_statistics": {
            "Birth Certificate": {"total": random.randint(40, 100), "completed": random.randint(30, 90)},
            "Business Permit": {"total": random.randint(20, 60), "completed": random.randint(10, 50)},
            "Barangay Clearance": {"total": random.randint(50, 120), "completed": random.randint(40, 110)},
            "Health Clearance": {"total": random.randint(15, 45), "completed": random.randint(10, 40)},
            "Police Clearance": {"total": random.randint(20, 60), "completed": random.randint(15, 55)},
        },
        "staff_performance": {
            "John Doe": {"processed": 45, "avg_time": "2.3 days", "satisfaction": "95%"},
            "Jane Smith": {"processed": 52, "avg_time": "2.1 days", "satisfaction": "98%"},
            "Sofia Cruz": {"processed": 38, "avg_time": "2.8 days", "satisfaction": "92%"},
            "Ramon Torres": {"processed": 41, "avg_time": "2.5 days", "satisfaction": "94%"},
            "Angela Lopez": {"processed": 0, "avg_time": "N/A", "satisfaction": "N/A"}
        }
    }

def generate_staff_workload_data():
    """Generate staff-specific workload and pending requests"""
    departments = ["Civil Registry", "Treasury", "Health & Sanitation", "Admin", "Barangay Hall"]
    workload = {}
    
    for dept in departments:
        pending_count = random.randint(5, 20)
        processing_count = random.randint(3, 15)
        urgent_count = random.randint(1, 5)
        
        workload[dept] = {
            "pending": pending_count,
            "processing": processing_count,
            "urgent": urgent_count,
            "total_today": random.randint(10, 40),
            "avg_processing_time": f"{random.uniform(1.5, 4.0):.1f} days",
            "queue_position": random.randint(1, 50)
        }
    
    return workload

def generate_department_statistics():
    """Generate department-specific statistics for staff dashboard"""
    return {
        "Civil Registry": {
            "icon": "📄",
            "total_processed": 234,
            "pending": 12,
            "avg_time": 2.3,
            "services": ["Birth Certificate", "Marriage Certificate", "Death Certificate", "CENOMAR"]
        },
        "Treasury": {
            "icon": "💰",
            "total_processed": 167,
            "pending": 8,
            "avg_time": 2.8,
            "services": ["Business Permit", "License Renewal", "Building Permit", "Tricycle Franchise"]
        },
        "Health & Sanitation": {
            "icon": "🏥",
            "total_processed": 89,
            "pending": 5,
            "avg_time": 1.9,
            "services": ["Health Clearance", "Sanitary Permit", "Food Handler Certificate"]
        },
        "Admin": {
            "icon": "📋",
            "total_processed": 156,
            "pending": 11,
            "avg_time": 2.1,
            "services": ["Police Clearance", "Senior Citizen ID", "PWD ID", "Job Seeker Certificate"]
        },
        "Barangay Hall": {
            "icon": "🏘️",
            "total_processed": 198,
            "pending": 9,
            "avg_time": 1.5,
            "services": ["Barangay Clearance", "Certificate of Residency", "Residency Verification"]
        }
    }

def generate_sample_users():
    """Generate diverse sample users for the system"""
    sample_users = {}
    
    sample_names = [
        ("Juan", "Dela Cruz"),
        ("Maria", "Santos"),
        ("Pedro", "Reyes"),
        ("Anna", "Rodriguez"),
        ("Carlos", "Garcia"),
        ("Rosa", "Lopez"),
        ("Miguel", "Torres"),
        ("Elena", "Morales"),
        ("Francisco", "Mendoza"),
        ("Aurora", "Navarro")
    ]
    
    for first, last in sample_names:
        email = f"{first.lower()}.{last.lower()}@email.com"
        sample_users[email] = {
            'user_id': f"user_{len(sample_users) + 1}",
            'first_name': first,
            'last_name': last,
            'email': email,
            'phone': f"09{random.randint(100000000, 999999999)}",
            'password': hash_password("password123"),
            'verified': random.choice([True, True, True, False]),
            'profile_pic': None,
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return sample_users

def generate_sample_payments():
    """Generate diverse payment records"""
    payments = []
    
    services = ["Birth Certificate", "Business Permit", "Health Clearance", "Barangay Clearance"]
    methods = ["Cash", "E-Wallet", "Online Banking"]
    payment_statuses = ["Verified", "Pending Verification", "Failed"]
    
    for i in range(20):
        tracking = f"{random.choice(['BC', 'BP', 'HC', 'BCL'])}-{(datetime.now() - timedelta(days=i)).strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        
        # Fee amounts based on service
        fee_map = {"Birth Certificate": 155, "Business Permit": 500, "Health Clearance": 100, "Barangay Clearance": 50}
        amount = fee_map[random.choice(services)]
        
        payment = {
            "id": f"PAY{random.randint(10000, 99999)}",
            "tracking": tracking,
            "amount": amount,
            "method": random.choice(methods),
            "status": random.choice(payment_statuses),
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        }
        payments.append(payment)
    
    return payments

def generate_sample_notifications():
    """Generate sample notifications for users"""
    notifications = [
        {"type": "success", "title": "Application Approved", "message": "Your birth certificate application has been approved!", "date": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"type": "info", "title": "Application Received", "message": "Your business permit application has been received.", "date": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")},
        {"type": "warning", "title": "Missing Documents", "message": "Please submit the required documents for your clearance.", "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")},
        {"type": "info", "title": "Ready for Pickup", "message": "Your certificate is now ready for pickup at the office.", "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")},
        {"type": "success", "title": "Payment Confirmed", "message": "Payment for your application has been confirmed.", "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M")},
    ]
    return notifications

def generate_sample_activity_log():
    """Generate sample activity log for profile"""
    activities = [
        {"action": "Applied for Birth Certificate", "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "status": "In Progress"},
        {"action": "Submitted Payment", "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"), "status": "Completed"},
        {"action": "Approved Business Permit", "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"), "status": "Completed"},
        {"action": "Uploaded Documents", "date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M"), "status": "Completed"},
        {"action": "Updated Profile Information", "date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M"), "status": "Completed"},
        {"action": "Verified Email Address", "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d %H:%M"), "status": "Completed"},
    ]
    return activities

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

# Chatbot page function
def show_chat_page():
    st.title("💬 CanConnect Assistant")
    
    quick_replies = [
        "What are the requirements?",
        "How much is the fee?",
        "Processing time?",
        "Payment methods",
        "Track my application",
        "Contact info"
    ]
    
    # Display chat history
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick replies
    st.markdown("### Quick Questions")
    cols = st.columns(3)
    for idx, reply in enumerate(quick_replies):
        with cols[idx % 3]:
            if st.button(reply, key=f"qr_{idx}"):
                st.session_state.chat_messages.append({"role": "user", "content": reply})
                response = generate_chatbot_response(reply)
                st.session_state.chat_messages.append({"role": "bot", "content": response})
                st.rerun()
    
    # Chat input
    with st.form(key=f"chat_form_{st.session_state.chat_input_key}"):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
        with col2:
            send = st.form_submit_button("Send", use_container_width=True)
        
        if send and user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            response = generate_chatbot_response(user_input)
            st.session_state.chat_messages.append({"role": "bot", "content": response})
            st.session_state.chat_input_key += 1
            st.rerun()

def generate_chatbot_response(user_input):
    """Generate chatbot response based on user input"""
    user_input_lower = user_input.lower()
    
    responses = {
        "hello": "Hello! How can I assist you with your government services today?",
        "hi": "Hi there! I'm here to help you with any questions about our services.",
        "help": "I can help you with:\n• Service applications\n• Document requirements\n• Processing times\n• Payment methods\n• Tracking your application\n• Office locations\n• Contact information",
        "requirements": "Document requirements vary by service. Common requirements include:\n• Valid ID\n• Proof of residency\n• Birth certificate\n• Completed application form\nWhich service are you interested in?",
        "fee": "Service fees:\n• Barangay Clearance: ₱50\n• Birth Certificate: ₱155 (PSA) / ₱75 (Local)\n• Business Permit: ₱500-2000\n• Police Clearance: ₱150\n• Health Clearance: ₱100",
        "payment": "We accept:\n• Cash (pay at LGU office)\n• E-Wallet (GCash, Maya)\n• Online Banking\n• Credit/Debit cards",
        "track": "To track your application:\n1. Go to 'My Requests' in the sidebar\n2. View your application status\n3. Click 'View Details' for more information",
        "contact": "Contact us:\n• Phone: (123) 456-7890\n• Email: support@cantilan.gov.ph\n• Address: Municipal Hall, Cantilan, Surigao del Sur\n• Hours: Mon-Fri, 8:00 AM - 5:00 PM"
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
            # Profile picture at top for citizens
            if st.session_state.logged_in and st.session_state.user_type == 'citizen':
                user_data = st.session_state.users.get(st.session_state.username, {})
                
                if st.session_state.profile_pic:
                    st.image(st.session_state.profile_pic, width=80)
                else:
                    st.markdown('<div style="text-align: center; font-size: 60px; color: white;">👤</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; color: white; margin-bottom: 20px;">
                    <div style="font-weight: 600;">{user_data.get('first_name', '')} {user_data.get('last_name', '')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">{user_data.get('email', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
            
            elif st.session_state.staff_logged_in:
                staff_info = st.session_state.get('staff_info', {})
                st.markdown(f"""
                <div style="text-align: center; color: white; padding: 10px;">
                    <div style="font-size: 60px;">👤</div>
                    <div style="font-weight: 600;">{staff_info.get('name', 'Staff')}</div>
                    <div style="font-size: 12px; opacity: 0.8;">{staff_info.get('role', '')} - {staff_info.get('department', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
            
            elif st.session_state.admin_logged_in:
                st.markdown(f"""
                <div style="text-align: center; color: white; padding: 10px;">
                    <div style="font-size: 60px;">👤</div>
                    <div style="font-weight: 600;">Administrator</div>
                    <div style="font-size: 12px; opacity: 0.8;">admin@cantilan.gov.ph</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
            
            # Navigation menu
            if st.session_state.admin_logged_in:
                if st.button("📊 Dashboard Overview", use_container_width=True):
                    st.session_state.admin_page = 'dashboard_overview'
                    st.rerun()
                if st.button("📝 Manage Request", use_container_width=True):
                    st.session_state.admin_page = 'manage_request'
                    st.rerun()
                if st.button("⚙️ Settings", use_container_width=True):
                    st.session_state.admin_page = 'settings'
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
                if st.button("⚙️ Settings", use_container_width=True):
                    st.session_state.staff_page = 'settings'
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
                if st.button("💬 AI Chatbot", use_container_width=True):
                    st.session_state.page = 'chat'
                    st.rerun()
                if st.button("⚙️ Settings", use_container_width=True):
                    st.session_state.page = 'settings'
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
        elif st.session_state.page == 'settings':
            show_user_settings()
        elif st.session_state.page == 'lgu':
            show_lgu_services()
        elif st.session_state.page == 'barangay':
            show_barangay_services()
        elif st.session_state.page == 'chat':
            show_chat_page()

def show_login_page():
    st.title("🏛️ CanConnect")
    st.markdown("---")
    
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
        st.subheader("Admin Login")
        admin_email = st.text_input("Admin Email", key="admin_email")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        
        if st.button("Admin Login", use_container_width=True):
            if admin_email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[admin_email] == hash_password(admin_password):
                st.session_state.admin_logged_in = True
                st.session_state.user_type = 'admin'
                st.session_state.admin_page = 'dashboard_overview'
                st.rerun()
            else:
                st.error("Invalid admin credentials")

def show_dashboard():
    st.title("🏠 Dashboard")
    
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    active_count = len([app for app in user_apps if app['status'] in ['Processing', 'Pending']])
    completed_count = len([app for app in user_apps if app['status'] == 'Approved'])
    rejected_count = len([app for app in user_apps if app['status'] == 'Rejected'])
    total_count = len(user_apps)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total", total_count)
    with col2:
        st.metric("⏳ Active", active_count, delta=None)
    with col3:
        st.metric("✅ Completed", completed_count, delta=None)
    with col4:
        st.metric("❌ Rejected", rejected_count, delta=None)
    
    st.markdown("---")
    
    # Two main sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Recent Applications")
        
        if user_apps:
            # Filter options
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            with filter_col1:
                show_filter = st.selectbox("Filter by Status", ["All", "Pending", "Processing", "Approved", "Rejected"], key="dashboard_filter")
            
            recent_apps = sorted(user_apps, key=lambda x: x['date'], reverse=True)
            
            if show_filter != "All":
                recent_apps = [app for app in recent_apps if app['status'] == show_filter]
            
            recent_apps = recent_apps[:5]
            
            for app in recent_apps:
                status_icon = {
                    'Pending': '🟡',
                    'Processing': '🔵',
                    'Approved': '🟢',
                    'Rejected': '🔴'
                }.get(app['status'], '⚪')
                
                status_color = {
                    'Pending': '#FFC107',
                    'Processing': '#2196F3',
                    'Approved': '#4CAF50',
                    'Rejected': '#F44336'
                }.get(app['status'], '#CCCCCC')
                
                st.markdown(f"""
                <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid {status_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong style="font-size:16px;">{status_icon} {app['type']}</strong><br>
                            <span style="color:#666; font-size:12px;">Tracking: <code>{app['tracking']}</code></span><br>
                            <span style="color:#999; font-size:11px;">Submitted: {app['date']}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="background-color:{status_color}; color:white; padding:5px 10px; border-radius:15px; font-size:12px; font-weight:bold;">{app['status']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No applications yet. Start by applying for a service!")
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        if total_count > 0:
            st.markdown(f"""
            <div style="background-color:#f0f0f0; padding:15px; border-radius:10px;">
                <div style="text-align:center; margin-bottom:10px;">
                    <div style="font-size:24px; font-weight:bold; color:#2196F3;">{completed_count}/{total_count}</div>
                    <div style="font-size:12px; color:#666;">Completion Rate</div>
                </div>
                <hr style="margin:10px 0;">
                <div style="font-size:12px;  color:#666;">
                    <div>✅ Approved: {completed_count}</div>
                    <div>⏳ In Progress: {active_count}</div>
                    <div>❌ Rejected: {rejected_count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color:#f0f0f0; padding:15px; border-radius:10px; text-align:center; color:#999;">
                <div>No applications to display</div>
                <div style="font-size:12px; margin-top:10px;">Submit your first application to get started!</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Action Buttons
    st.subheader("⚡ Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📋 View All Requests", use_container_width=True):
            st.session_state.page = 'my_requests'
            st.rerun()
    
    with action_col2:
        if st.button("📝 New Application", use_container_width=True):
            st.session_state.page = 'lgu'
            st.rerun()
    
    with action_col3:
        if st.button("👤 My Profile", use_container_width=True):
            st.session_state.page = 'profile'
            st.rerun()


def show_my_requests():
    st.title("📋 My Requests & Applications")
    
    # Show success alert if just submitted
    if st.session_state.get('just_submitted', False):
        st.balloons()
        st.success("✅ **Application Submitted Successfully!**")
        st.info(f"🔍 **Tracking Number:** `{st.session_state.get('submitted_tracking', 'N/A')}`")
        st.markdown("Your application is now being processed. You can track its status below.")
        st.markdown("---")
        st.session_state.just_submitted = False
    
    user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
    
    if user_apps:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "📝 All Applications", "⭐ Recent"])
        
        with tab1:
            st.markdown("### Request Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Requests", len(user_apps))
            with col2:
                pending = len([a for a in user_apps if a['status'] == 'Pending'])
                st.metric("Pending", pending)
            with col3:
                processing = len([a for a in user_apps if a['status'] == 'Processing'])
                st.metric("Processing", processing)
            with col4:
                approved = len([a for a in user_apps if a['status'] == 'Approved'])
                st.metric("Approved", approved)
            
            st.markdown("---")
            
            # Status breakdown chart
            st.markdown("### Status Breakdown")
            status_counts = {
                'Pending': len([a for a in user_apps if a['status'] == 'Pending']),
                'Processing': len([a for a in user_apps if a['status'] == 'Processing']),
                'Approved': len([a for a in user_apps if a['status'] == 'Approved']),
                'Rejected': len([a for a in user_apps if a['status'] == 'Rejected'])
            }
            
            col1, col2 = st.columns(2)
            with col1:
                import pandas as pd
                status_df = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
                st.bar_chart(status_df.set_index('Status'))
            
            with col2:
                st.markdown("**Distribution:**")
                for status, count in status_counts.items():
                    if count > 0:
                        pct = (count / len(user_apps)) * 100
                        st.write(f"• {status}: {count} ({pct:.1f}%)")
        
        with tab2:
            st.markdown("### Your Applications")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Processing", "Approved", "Rejected"], key="my_req_filter")
            with col2:
                sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Service Type"], key="my_req_sort")
            with col3:
                view_type = st.selectbox("View", ["Detailed", "Compact"], key="my_req_view")
            
            # Sort applications
            sorted_apps = sorted(user_apps, key=lambda x: x['date'], reverse=(sort_by == "Newest First"))
            if sort_by == "Oldest First":
                sorted_apps = sorted(user_apps, key=lambda x: x['date'])
            elif sort_by == "Service Type":
                sorted_apps = sorted(user_apps, key=lambda x: x['type'])
            
            # Filter applications
            if filter_status != "All":
                sorted_apps = [app for app in sorted_apps if app['status'] == filter_status]
            
            # Display based on view type
            if view_type == "Detailed":
                for idx, app in enumerate(sorted_apps):
                    status_color = {
                        'Pending': '🟡',
                        'Processing': '🔵',
                        'Approved': '🟢',
                        'Rejected': '🔴'
                    }.get(app['status'], '⚪')
                    
                    with st.expander(f"{status_color} {app['type']} - {app['tracking']}", expanded=idx == 0):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**Application Details**")
                            st.write(f"📌 **Type:** {app['type']}")
                            st.write(f"📅 **Date Submitted:** {app['date']}")
                            st.write(f"🏢 **Office:** {app.get('office', 'N/A')}")
                            st.write(f"📍 **Barangay:** {app.get('barangay', 'N/A')}")
                        
                        with col2:
                            st.write("**Personal Information**")
                            st.write(f"👤 **Name:** {app['first_name']} {app['last_name']}")
                            st.write(f"📧 **Email:** {app['email']}")
                            st.write(f"📞 **Contact:** {app['contact_no']}")
                            st.write(f"📝 **Purpose:** {app.get('purpose', 'N/A')}")
                        
                        with col3:
                            st.write("**Status & Payment**")
                            status_colors = {
                                'Pending': 'FFC107',
                                'Processing': '2196F3',
                                'Approved': '4CAF50',
                                'Rejected': 'F44336'
                            }
                            status_color = status_colors.get(app['status'], 'CCCCCC')
                            st.markdown(f"**Status:** <span style='background-color: #{status_color}; color: white; padding: 5px 10px; border-radius: 15px;'>{app['status']}</span>", unsafe_allow_html=True)
                            st.write(f"💳 **Payment Method:** {app.get('payment_method', 'N/A')}")
                            st.write(f"💰 **Payment Status:** {app.get('payment_status', 'N/A')}")
                            st.write(f"🔢 **Tracking Number:** `{app['tracking']}`")
                        
                        st.markdown("---")
                        
                        # Status-specific messages
                        if app['status'] == 'Approved':
                            st.success("✅ Your request has been approved! You can claim your document at the office.")
                            if st.button("View Claim Instructions", key=f"claim_{app['tracking']}"):
                                st.info("""
                                **How to Claim Your Document:**
                                1. Visit the indicated office during business hours
                                2. Bring a valid ID and this tracking number: `{}`
                                3. Present your tracking number to the staff
                                4. Complete the claim process
                                
                                **Office Hours:** Monday - Friday, 8:00 AM - 5:00 PM
                                """.format(app['tracking']))
                        elif app['status'] == 'Processing':
                            st.info("⏳ Your request is being processed. Check back soon for updates.")
                            st.progress(0.5)
                        elif app['status'] == 'Pending':
                            st.warning("⏳ Your request is pending review by the office staff.")
                            st.progress(0.25)
                        elif app['status'] == 'Rejected':
                            st.error("❌ Your request has been rejected. Please contact the office for more information.")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📧 Contact Office", key=f"contact_{app['tracking']}"):
                                st.info("Email sent to the processing office.")
                        with col2:
                            if st.button("🔄 Resubmit", key=f"resubmit_{app['tracking']}"):
                                st.warning("Resubmission feature coming soon.")
                        with col3:
                            if st.button("📥 Download", key=f"download_{app['tracking']}"):
                                st.success("Application details downloaded.")
            
            else:  # Compact view
                for app in sorted_apps:
                    status_icon = {
                        'Pending': '🟡',
                        'Processing': '🔵',
                        'Approved': '🟢',
                        'Rejected': '🔴'
                    }.get(app['status'], '⚪')
                    
                    status_color = {
                        'Pending': '#FFC107',
                        'Processing': '#2196F3',
                        'Approved': '#4CAF50',
                        'Rejected': '#F44336'
                    }.get(app['status'], '#CCCCCC')
                    
                    st.markdown(f"""
                    <div style="background-color:#f8f9fa; padding:12px; border-radius:8px; margin-bottom:8px; border-left:4px solid {status_color};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <strong>{status_icon} {app['type']}</strong> | <code style="background-color:#e0e0e0; padding:2px 6px; border-radius:3px;">{app['tracking']}</code>
                                <br><span style="color:#999; font-size:11px;">{app['date']} • {app['first_name']} {app['last_name']}</span>
                            </div>
                            <span style="background-color:{status_color}; color:white; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">{app['status']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### ⭐ Recent Applications (Last 5)")
            
            recent_apps = sorted(user_apps, key=lambda x: x['date'], reverse=True)[:5]
            
            for idx, app in enumerate(recent_apps, 1):
                status_icon = {
                    'Pending': '🟡',
                    'Processing': '🔵',
                    'Approved': '🟢',
                    'Rejected': '🔴'
                }.get(app['status'], '⚪')
                
                status_color_hex = {
                    'Pending': '#FFC107',
                    'Processing': '#2196F3',
                    'Approved': '#4CAF50',
                    'Rejected': '#F44336'
                }.get(app['status'], '#CCCCCC')
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding:15px; border-radius:10px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div style="font-size:18px; font-weight:bold; color:#333;">#{idx} {status_icon} {app['type']}</div>
                            <div style="color:#666; font-size:13px; margin-top:5px;">
                                <div>📌 Tracking: <code>{app['tracking']}</code></div>
                                <div>👤 Applicant: {app['first_name']} {app['last_name']}</div>
                                <div>📅 Submitted: {app['date']}</div>
                                <div>💰 Payment: {app.get('payment_status', 'N/A')}</div>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span style="background-color:{status_color_hex}; color:white; padding:6px 12px; border-radius:20px; font-size:13px; font-weight:bold;">{app['status']}</span>
                            <br><span style="font-size:11px; color:#999; margin-top:5px; display:block;">From {app.get('office', 'LGU Office')}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.info("ℹ️ You haven't submitted any requests yet.")
        st.markdown("---")
        st.subheader("Get Started")
        st.write("Visit the **LGU Services** or **Barangay Services** page to submit an application!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Go to LGU Services", use_container_width=True):
                st.session_state.page = 'lgu'
                st.rerun()
        with col2:
            if st.button("🏘️ Go to Barangay Services", use_container_width=True):
                st.session_state.page = 'barangay'
                st.rerun()

def show_user_settings(user_type='citizen'):
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Notifications", "Preferences", "Privacy", "Account"])
    
    with tab1:
        st.subheader("Notification Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            notify_toggle = st.checkbox(
                "Enable Notifications",
                value=st.session_state.user_settings.get('notifications', True),
                key="notify_toggle"
            )
            st.session_state.user_settings['notifications'] = notify_toggle
        
        with col2:
            email_toggle = st.checkbox(
                "Email Alerts",
                value=st.session_state.user_settings.get('email_alerts', True),
                key="email_toggle"
            )
            st.session_state.user_settings['email_alerts'] = email_toggle
        
        st.markdown("---")
        st.write("**Notification Types**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Application Status Updates", value=True, disabled=False)
            st.checkbox("Payment Confirmations", value=True, disabled=False)
        with col2:
            st.checkbox("System Announcements", value=True, disabled=False)
            st.checkbox("Document Ready Notices", value=True, disabled=False)
    
    with tab2:
        st.subheader("Preferences")
        
        language = st.selectbox(
            "Language Preference",
            ["English", "Filipino", "Spanish"],
            index=0,
            key="language_select"
        )
        st.session_state.user_settings['language'] = language
        
        theme = st.radio(
            "Theme",
            ["Light", "Dark", "Auto"],
            index=0,
            horizontal=True,
            key="theme_radio"
        )
        st.session_state.user_settings['theme'] = theme.lower()
        
        st.markdown("---")
        st.write("**Display Options**")
        st.checkbox("Show tutorial on startup", value=False)
        st.checkbox("Compact view", value=False)
    
    with tab3:
        st.subheader("Privacy Settings")
        
        st.write("**Data Sharing**")
        st.checkbox("Allow analytics tracking", value=True)
        st.checkbox("Share usage data for improvements", value=False)
        
        st.markdown("---")
        st.write("**Profile Visibility**")
        visibility = st.radio(
            "Who can see your profile",
            ["Only Me", "Government Staff", "Public"],
            index=0,
            horizontal=True
        )
        
        st.markdown("---")
        st.write("**Download Your Data**")
        if st.button("📥 Download Personal Data", use_container_width=True):
            st.success("Your data has been prepared for download.")
            st.info("Check your email for the download link.")
    
    with tab4:
        st.subheader("Account Settings")
        
        user_email = st.session_state.username if st.session_state.logged_in else "admin@cantilan.gov.ph"
        st.text_input("Email Address", value=user_email, disabled=True)
        
        st.markdown("---")
        st.write("**Change Password**")
        
        col1, col2 = st.columns(2)
        with col1:
            current_pw = st.text_input("Current Password", type="password", key="current_pw_settings")
        with col2:
            new_pw = st.text_input("New Password", type="password", key="new_pw_settings")
        
        col1, col2 = st.columns(2)
        with col1:
            confirm_pw = st.text_input("Confirm New Password", type="password", key="confirm_pw_settings")
        with col2:
            if st.button("Update Password", use_container_width=True):
                if current_pw and new_pw == confirm_pw:
                    st.success("Password updated successfully!")
                else:
                    st.error("Passwords don't match or missing current password.")
        
        st.markdown("---")
        st.write("**Danger Zone**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Deactivate Account", use_container_width=True):
                st.warning("Account deactivation is not reversible. Are you sure?")
        with col2:
            if st.button("🗑️ Delete Account", use_container_width=True):
                st.error("This action cannot be undone. All your data will be permanently deleted.")
        
        if st.button("Save Settings", use_container_width=True, type="primary"):
            st.success("✅ All settings have been saved successfully!")

def show_profile():
    st.title("👤 Profile")
    
    # Fetch fresh user data to ensure we always have the latest
    user_data = st.session_state.users.get(st.session_state.username, {})
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Profile Info", "Edit Details", "Documents", "Activity", "Security"])
    
    # TAB 1: Profile Info
    with tab1:
        # Show update indicator
        if st.session_state.get('updated_profile', False):
            st.success("✅ Profile has been updated! Changes are now visible.")
            st.session_state.updated_profile = False
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.session_state.profile_pic:
                st.image(st.session_state.profile_pic, width=150, caption="Your Profile Picture")
            else:
                st.markdown('<div style="font-size: 120px; text-align: center;">👤</div>', unsafe_allow_html=True)
            
            if st.button("📷 Change Picture", use_container_width=True):
                uploaded_file = st.file_uploader("Upload Profile Picture", type=['png', 'jpg', 'jpeg'], key="profile_pic_upload")
                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    st.session_state.profile_pic = bytes_data
                    st.session_state.users[st.session_state.username]['profile_pic'] = bytes_data
                    st.success("✅ Profile picture updated!")
                    st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="profile-header" style="margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:10px;">
                <h2 style="color: white; margin: 5px 0;">{user_data.get('first_name', 'User')} {user_data.get('last_name', '')}</h2>
                <p style="color: rgba(255,255,255,0.9); margin: 5px 0;">📧 {user_data.get('email', 'Not provided')}</p>
                <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin: 5px 0;">📱 {user_data.get('phone', 'Not provided')}</p>
                <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin: 5px 0;">📍 {user_data.get('address', 'Not provided')}</p>
                <span style="background-color: {'#4CAF50' if st.session_state.profile_verified else '#FFC107'}; color: #000; padding: 5px 10px; border-radius: 20px; font-size: 12px; display: inline-block; margin-top: 10px; font-weight:bold;">
                    {'✅ Verified' if st.session_state.profile_verified else '⏳ Not Verified'}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistics
        st.subheader("📊 Account Statistics")
        user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Applications", len(user_apps))
        with col2:
            approved = len([a for a in user_apps if a['status'] == 'Approved'])
            st.metric("Approved", approved)
        with col3:
            pending = len([a for a in user_apps if a['status'] == 'Pending'])
            st.metric("Pending", pending)
        with col4:
            processing = len([a for a in user_apps if a['status'] == 'Processing'])
            st.metric("Processing", processing)
        
        st.markdown("---")
        
        # Account Info
        st.subheader("📋 Account Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Account Created:** {user_data.get('created_at', 'N/A')}")
        with col2:
            st.write(f"**User ID:** {user_data.get('user_id', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Last Updated:** {user_data.get('profile_updated_at', user_data.get('created_at', 'N/A'))}")
        with col2:
            st.write(f"**Verification Status:** {'✅ Verified' if st.session_state.profile_verified else '⏳ Pending'}")
        
        st.markdown("---")
        
        # Full details
        st.subheader("📝 Full Profile Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**First Name:** {user_data.get('first_name', 'Not set')}")
            st.write(f"**Last Name:** {user_data.get('last_name', 'Not set')}")
            st.write(f"**Gender:** {user_data.get('gender', 'Not set')}")
        with col2:
            st.write(f"**Phone:** {user_data.get('phone', 'Not set')}")
            st.write(f"**Email:** {user_data.get('email', 'Not set')}")
            st.write(f"**Birth Date:** {user_data.get('birth_date', 'Not set')}")
        
        st.write(f"**Address:** {user_data.get('address', 'Not set')}")
    
    # TAB 2: Edit Details
    with tab2:
        st.subheader("📝 Edit Personal Information")
        
        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*", value=user_data.get('first_name', ''), placeholder="Enter first name")
            with col2:
                last_name = st.text_input("Last Name*", value=user_data.get('last_name', ''), placeholder="Enter last name")
            
            phone = st.text_input("Phone Number*", value=user_data.get('phone', ''), placeholder="Enter phone number")
            
            col1, col2 = st.columns(2)
            with col1:
                gender = st.selectbox("Gender*", ["Not specified", "Male", "Female", "Other"], 
                                     index=0 if user_data.get('gender') is None else ["Not specified", "Male", "Female", "Other"].index(user_data.get('gender', 'Not specified')))
            with col2:
                birth_date = st.date_input("Date of Birth", value=None, help="Your date of birth")
            
            address = st.text_area("Address*", value=user_data.get('address', ''), placeholder="Enter your complete address", height=100)
            
            email = st.text_input("Email Address (Cannot be changed)", value=user_data.get('email', ''), disabled=True)
            
            submit_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
            
            if submit_button:
                if first_name.strip() and last_name.strip() and phone.strip() and address.strip():
                    # Update user data in session state
                    st.session_state.users[st.session_state.username].update({
                        'first_name': first_name.strip(),
                        'last_name': last_name.strip(),
                        'phone': phone.strip(),
                        'address': address.strip(),
                        'birth_date': str(birth_date) if birth_date else None,
                        'gender': gender,
                        'profile_updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Store the updated data
                    st.session_state.updated_profile = True
                    
                    st.success("✅ Profile updated successfully!")
                    st.info(f"""
                    **Saved Profile Information:**
                    - **Name:** {first_name} {last_name}
                    - **Phone:** {phone}
                    - **Gender:** {gender}
                    - **Address:** {address}
                    - **Updated at:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
                    """)
                    
                    # Rerun to reflect changes immediately
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields (marked with *)")
        
        st.markdown("---")
        
        st.subheader("✅ Current Profile Status")
        
        # Show what's currently saved
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
            <strong>📋 Currently Saved:</strong>
            <div style="margin-top: 10px; font-size: 14px;">
                <div>👤 <strong>Name:</strong> {user_data.get('first_name', 'Not set')} {user_data.get('last_name', 'Not set')}</div>
                <div>📱 <strong>Phone:</strong> {user_data.get('phone', 'Not set')}</div>
                <div>⚧ <strong>Gender:</strong> {user_data.get('gender', 'Not set')}</div>
                <div>📍 <strong>Address:</strong> {user_data.get('address', 'Not set')}</div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            last_update = user_data.get('profile_updated_at', user_data.get('created_at', 'N/A'))
            completion = sum([1 for field in ['first_name', 'last_name', 'phone', 'address'] if user_data.get(field)]) / 4 * 100
            
            st.markdown(f"""
            <div style="background-color:#e8f5e9; padding:15px; border-radius:10px;">
            <strong>📊 Profile Completion:</strong>
            <div style="margin-top: 10px;">
                <div style="background-color:#ddd; height:25px; border-radius:5px; overflow:hidden;">
                    <div style="background-color:#4CAF50; height:100%; width:{completion}%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:12px;">
                        {completion:.0f}%
                    </div>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 12px; color:#666;">
                ⏰ <strong>Last updated:</strong><br>{last_update}
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.subheader("🔐 Account Verification")
        if not st.session_state.profile_verified:
            st.info("Verify your account by uploading a valid government ID")
            uploaded_id = st.file_uploader("Upload Valid ID (PNG, JPG, or PDF)", type=['png', 'jpg', 'jpeg', 'pdf'], key="id_upload")
            
            if uploaded_id:
                st.write("**ID Type:** ", uploaded_id.name)
                if st.button("Submit for Verification", use_container_width=True):
                    st.session_state.profile_verified = True
                    st.session_state.users[st.session_state.username]['verified'] = True
                    st.session_state.users[st.session_state.username]['verified_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("✅ Verification submitted! Your account is now verified.")
                    st.rerun()
        else:
            verify_date = user_data.get('verified_at', datetime.now().strftime("%B %d, %Y"))
            st.success("✅ Your account is verified")
            st.write(f"Verification Date: {verify_date}")
    
    # TAB 3: Documents
    with tab3:
        st.subheader("📄 My Uploaded Documents")
        
        uploaded_docs = st.file_uploader("Upload Supporting Documents", 
                                        accept_multiple_files=True,
                                        type=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])
        
        if uploaded_docs:
            st.success(f"✅ {len(uploaded_docs)} document(s) uploaded successfully!")
            for doc in uploaded_docs:
                st.write(f"📎 {doc.name} ({doc.size} bytes)")
        
        st.markdown("---")
        
        st.subheader("📋 Document Requirements Checklist")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.checkbox("Valid Government ID", value=True)
        with col2:
            st.write("✅")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.checkbox("Proof of Residency", value=False)
        with col2:
            st.write("❌")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.checkbox("Business Permit (if applicable)", value=False)
        with col2:
            st.write("⏳")
    
    # TAB 4: Activity
    with tab4:
        st.subheader("📊 Activity History")
        
        user_apps = [app for app in st.session_state.applications if app.get('user_email') == st.session_state.username]
        
        if user_apps:
            for idx, app in enumerate(reversed(user_apps)):
                with st.expander(f"📌 {app['type']} - {app['tracking']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Status:** {app['status']}")
                        st.write(f"**Date:** {app['date']}")
                    with col2:
                        st.write(f"**Office:** {app.get('office', 'N/A')}")
                        st.write(f"**Payment:** {app.get('payment_method', 'N/A')}")
                    with col3:
                        st.write(f"**Amount:** ₱{app.get('amount', 'TBD')}")
                        st.write(f"**Barangay:** {app.get('barangay', 'N/A')}")
        else:
            st.info("No application history yet.")
    
    # TAB 5: Security
    with tab5:
        st.subheader("🔒 Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Two-Factor Authentication**")
            st.toggle("Enable 2FA", value=False, help="Add extra security to your account")
        with col2:
            st.write("**Login Activity**")
            st.button("View Recent Logins", use_container_width=True, key="login_activity")
        
        st.markdown("---")
        
        st.subheader("🔑 Change Password")
        with st.form("change_password_form"):
            current_pwd = st.text_input("Current Password", type="password", key="current_pwd")
            new_pwd = st.text_input("New Password", type="password", key="new_pwd")
            confirm_pwd = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            if st.form_submit_button("Update Password", use_container_width=True):
                if new_pwd == confirm_pwd:
                    st.success("✅ Password updated successfully!")
                else:
                    st.error("❌ Passwords don't match!")
        
        st.markdown("---")
        
        st.subheader("⚙️ Active Sessions")
        st.write("**Current Session**")
        st.write(f"🖥️ Device: Desktop Browser")
        st.write(f"📍 Location: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("Sign Out This Device", use_container_width=True):
            st.info("Session ended successfully.")
        
        st.markdown("---")
        
        st.subheader("⚠️ Danger Zone")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Deactivate Account", use_container_width=True, key="deactivate"):
                if st.checkbox("I understand this action is reversible", key="deactivate_confirm"):
                    st.warning("Account deactivation requested.")
        with col2:
            if st.button("🗑️ Delete Account Permanently", use_container_width=True, key="delete"):
                if st.checkbox("I understand this is permanent", key="delete_confirm"):
                    st.error("This action cannot be undone!")


def show_lgu_services():
    st.title("Local Government Unit Services")
    
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
    
    search_term = st.text_input("🔍 Search for offices or documents", placeholder="e.g., birth certificate, permit, clearance...")
    
    categories = ["All Offices", "Executive", "Legislative", "Administrative", "Civil Registry", 
                  "Health & Social", "Engineering", "Peace & Order", "Economic", "Environment"]
    
    selected_category = st.selectbox("Filter by Category", categories)
    
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
    
    offices_found = False
    for office_name, office_data in lgu_offices.items():
        if selected_category != "All Offices" and office_name not in category_mapping.get(selected_category, []):
            continue
            
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
    # Full-width form
    st.markdown('<div class="centered-form">', unsafe_allow_html=True)
    
    if office_name:
        st.subheader(f"Apply for {service_name}")
        st.caption(f"Office: {office_name}")
    else:
        st.subheader(f"Apply for {service_name}")
    
    with st.form(key=f"form_{service_name.replace(' ', '_')}"):
        if office_name:
            st.info(f"This application will be processed by: **{office_name}**")
        
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
        
        st.write("**Contact Information**")
        col1, col2 = st.columns(2)
        with col1:
            contact_no = st.text_input("Contact Number*")
        with col2:
            email = st.text_input("Email Address*", value=st.session_state.username if st.session_state.username else "")
        
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
        
        st.write("**Required Documents**")
        uploaded_files = st.file_uploader("Upload supporting documents", 
                                          accept_multiple_files=True,
                                          type=['pdf', 'jpg', 'jpeg', 'png'])
        
        st.write("**Payment Method**")
        payment_method = st.radio("Select Payment Method", 
                                  ["E-Wallet (GCash, Maya)", "Cash (Pay at LGU)", "Online Banking"],
                                  horizontal=True)
        
        agree = st.checkbox("I certify that all information provided is true and correct*")
        
        submitted = st.form_submit_button("Submit Application", use_container_width=True)
        
        if submitted:
            if agree and first_name and last_name and contact_no and email:
                tracking_no = f"{service_name[:2].upper()}-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
                
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
                
                if business_name:
                    new_app['business_name'] = business_name
                if business_type:
                    new_app['business_type'] = business_type
                if plate_no:
                    new_app['plate_no'] = plate_no
                if franchise_type:
                    new_app['franchise_type'] = franchise_type
                
                st.session_state.applications.append(new_app)
                
                payment_id = f"PAY{random.randint(1000,9999)}"
                
                fee_text = st.session_state['selected_service']['fee'] if 'selected_service' in st.session_state else "₱150"
                try:
                    if "-" in fee_text:
                        amount = int(fee_text.split('-')[0].replace('₱', '').strip())
                    elif "Free" in fee_text:
                        amount = 0
                    else:
                        amount = int(fee_text.replace('₱', '').strip())
                except:
                    amount = 150
                
                st.session_state.payments.append({
                    "id": payment_id,
                    "tracking": tracking_no,
                    "amount": amount,
                    "method": payment_method,
                    "status": "Pending Verification" if "Cash" in payment_method else "Verified",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                
                # Store submission state
                st.session_state.just_submitted = True
                st.session_state.submitted_tracking = tracking_no
                st.session_state.page = 'my_requests'
                
                # Show success message and redirect
                st.success(f"✅ Application submitted successfully!")
                st.info(f"📱 Tracking Number: **{tracking_no}**")
                st.rerun()
            else:
                st.error("⚠️ Please fill in all required fields and check the agreement box to proceed.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Staff dashboard functions
def show_staff_dashboard():
    staff_info = st.session_state.staff_info
    department = staff_info['department']
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"CanConnect | Staff Portal")
        st.caption(f"Welcome back, {staff_info['name']}!")
    
    st.markdown("---")
    
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
    elif st.session_state.staff_page == 'settings':
        show_user_settings('staff')

def show_staff_overview(department):
    st.header(f"📊 {department} Department Overview")
    
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
    
    col1, col2, col3, col4 = st.columns(4)
    
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

def show_staff_pending_requests(department):
    st.header(f"📝 Pending Requests - {department}")
    
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
        st.info("No pending requests for this department")

def show_staff_validation(department):
    st.header(f"✅ Document Validation - {department}")
    st.info("Document validation interface")

def show_staff_analytics(department):
    st.header(f"📈 Analytics - {department}")
    st.info("Analytics dashboard")

def show_staff_reports(department):
    st.header(f"📋 Reports - {department}")
    st.info("Reports interface")

# Admin dashboard functions
def show_admin_dashboard():
    st.title("Admin Dashboard")
    st.markdown("---")
    
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
    elif st.session_state.admin_page == 'settings':
        show_user_settings('admin')

def show_admin_dashboard_overview():
    st.subheader("📊 Dashboard Overview")
    
    total_apps = len(st.session_state.applications)
    pending_apps = len([app for app in st.session_state.applications if app['status'] == 'Pending'])
    processed_today = len([app for app in st.session_state.applications if app['date'] == datetime.now().strftime("%Y-%m-%d")])
    today_revenue = sum([150 for app in st.session_state.applications if app['date'] == datetime.now().strftime("%Y-%m-%d")])
    
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
        st.markdown(f"""
        <div class="admin-stat-card">
            <h3 style="margin:0; font-size:14px;">AVG PROCESSING</h3>
            <h2 style="margin:0; font-size:24px;">2.5 days</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests by Service")
        service_data = {
            'Barangay Clearance': 45,
            'Business Permit': 23,
            'Police Clearance': 34,
            'Birth Certificate': 56,
            'Residency Cert': 12
        }
        df_services = pd.DataFrame(list(service_data.items()), columns=['Service', 'Count'])
        fig = px.bar(df_services, x='Service', y='Count', color='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Daily Request Trends")
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
        requests = [random.randint(10, 50) for _ in range(7)]
        df_trends = pd.DataFrame({'Date': dates, 'Requests': requests})
        fig = px.line(df_trends, x='Date', y='Requests')
        st.plotly_chart(fig, use_container_width=True)

def show_admin_manage_request():
    st.subheader("📝 Manage Service Requests")
    
    if st.session_state.applications:
        for app in st.session_state.applications:
            with st.expander(f"{app['type']} - {app['tracking']}"):
                st.json(app)
    else:
        st.info("No applications found")

def show_admin_manage_payment():
    st.subheader("💰 Manage Payments")
    st.info("Payment management interface")

def show_admin_reports_analytics():
    st.subheader("📈 Reports & Analytics")
    st.info("Reports and analytics interface")

def show_admin_user_management():
    st.subheader("👥 User Management")
    
    st.markdown("### Manage Staff Accounts")
    
    with st.expander("➕ Add New Staff"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password", value="staff123")
        with col2:
            new_role = st.selectbox("Role", ["Processor", "Staff", "Admin"])
            new_department = st.selectbox("Department", 
                ["Civil Registry", "Treasury", "Health & Sanitation", "Admin"])
            new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        if st.button("Add Staff Member"):
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
                st.success(f"Staff member {new_name} added successfully!")
                st.rerun()
    
    st.markdown("### Existing Staff Members")
    
    for staff in st.session_state.staff_members:
        with st.container():
            st.markdown(f"""
            <div class="staff-card">
                <div style="display:flex; justify-content:space-between;">
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
            
            col1, col2 = st.columns(2)
            with col1:
                new_staff_status = st.selectbox("Status", ["Active", "Inactive"], 
                                               key=f"status_{staff['id']}",
                                               index=0 if staff['status'] == 'Active' else 1)
                if st.button("Update Status", key=f"update_{staff['id']}"):
                    staff['status'] = new_staff_status
                    st.success(f"Status updated")
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{staff['id']}"):
                    st.session_state.staff_members = [s for s in st.session_state.staff_members if s['id'] != staff['id']]
                    st.warning(f"Staff member removed")
                    st.rerun()

if __name__ == "__main__":
    main()
