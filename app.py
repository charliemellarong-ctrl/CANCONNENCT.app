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
                st.info(f"Redirecting to {office} for {doc_name} application")
                # Find and highlight the relevant office
                for office_name, office_data in lgu_offices.items():
                    if office in office_name:
                        # You would need to implement logic to scroll to or highlight the office
                        pass
