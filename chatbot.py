import streamlit as st
import time
from datetime import datetime
from typing import Tuple

# ==========================================
# CanConnect AI Assistant Chatbot
# ==========================================

CHATBOT_NAME = "CanConnect AI Assistant"
CHATBOT_SUBTITLE = "Always here to help 🤖"
RESPONSE_DELAY = 0.8  # seconds for realistic UX

# Knowledge base with conversation topics
KNOWLEDGE_BASE = {
    "status": {
        "keywords": ["status", "application", "check", "progress", "track", "tracking"],
        "response": """📊 **Check Your Application Status**

To track your application:
1. Click **Dashboard** in the left sidebar
2. Go to **Recent Applications** section
3. Click **View Details** to see status and tracking number

**Processing Timeline:**
• Most services: 2-5 business days
• Permits: 5-15 business days
• Assistance programs: 5-10 business days

You'll receive SMS notifications for every update. Your tracking number was provided when you submitted the application.

Need help finding something? Let me know! 😊"""
    },
    
    "documents": {
        "keywords": ["document", "required", "what do i need", "need", "requirement"],
        "response": """📄 **Required Documents**

The documents you need depend on the service. Here's what's usually required:

**Most Applications Need:**
✓ Valid ID (Driver's License, Passport, National ID)
✓ Barangay Clearance
✓ Proof of residency (utility bill, lease)
✓ Birth Certificate (for civil registry services)

**For Business Permits:**
✓ DTI/SEC Registration
✓ Tax Clearance
✓ Barangay Clearance

**How to Find Specific Requirements:**
1. Go to **Local Government Unit** or **Barangay** services
2. Find your desired service
3. Click **Apply** to see the exact documents needed

Each service page shows required documents before you submit. Upload all documents during the application form.

What service are you applying for? I can give more specific guidance! 🏢"""
    },
    
    "apply": {
        "keywords": ["how to", "apply", "submit", "start", "begin", "apply now"],
        "response": """📝 **How to Submit an Application**

Follow these simple steps:

**Step 1: Browse Services**
• Go to **Dashboard** → **Local Government Unit** or **Barangay Government Unit**
• Browse available services by office/category
• Use the search bar to find what you need

**Step 2: Select Service**
• Click **Apply** on the service you want
• Review the fee and processing time

**Step 3: Fill Application Form**
• Enter your personal information
• Select your barangay and address
• Write the purpose (if needed)

**Step 4: Upload Documents**
• Scan or take photos of required documents
• Upload as PDF, JPG, or PNG

**Step 5: Choose Payment Method**
• E-Wallet (GCash, Maya)
• Cash (Pay at LGU)
• Online Banking

**Step 6: Submit**
• Review all information
• Check the agreement box
• Click **Submit Application**

**Step 7: Get Tracking Number**
• You'll receive a tracking number
• Check your SMS for updates
• Monitor status on Dashboard

💡 **Pro Tip:** Save your tracking number and use it to check status anytime!

Ready to apply? Go to Dashboard and select a service! 🚀"""
    },
    
    "contact": {
        "keywords": ["contact", "support", "help", "assistance", "customer service"],
        "response": """📞 **How to Get Support**

**Quick Help Options:**
1. **Check FAQ** → Go to Profile → Notification Preferences (FAQ section)
2. **Help & Support** → Visit the Help section in your Dashboard
3. **Visit Barangay Hall** → In-person assistance available
4. **Email Support** → support@canconnect.gov.ph
5. **Response Time** → 24 hours maximum

**Common Issues We Can Help With:**
✓ Application status and tracking
✓ Required documents
✓ Service information
✓ Fees and payment
✓ Account and profile
✓ Technical issues

**If You Need In-Person Help:**
📍 Visit your local Barangay Hall
📍 Our staff can assist with document verification
📍 Hours: 8 AM - 5 PM (Monday-Friday)

**For Urgent Issues:**
• Contact your Barangay Administrator directly
• Email with screenshots and details

Don't hesitate to reach out - we're here to help! 😊"""
    },
    
    "services": {
        "keywords": ["service", "what can", "available", "offer", "what services", "provides"],
        "response": """🏛️ **CanConnect Available Services**

**Civil Registry:**
• Birth Certificates
• Marriage Certificates
• Death Certificates
• CENOMAR

**Residency & IDs:**
• Barangay Clearance
• Certificate of Residency
• Senior Citizen ID
• PWD ID
• Solo Parent ID

**Business & Permits:**
• Business Permit
• Building Permit
• Zoning Certification
• Occupancy Permit

**Assistance Programs:**
• Medical/Burial Assistance
• 4Ps Program
• Financial Assistance
• Livelihood Support

**Health & Agriculture:**
• Health Clearance
• Sanitary Permit
• Farmer's Certification
• Livestock Transport Permit

**Government Services:**
• Police Clearance
• Tax Clearance
• Notarial Services
• Fire Safety Clearance

**How to Find Services:**
1. Go to **Dashboard**
2. Click **Local Government Unit** (for municipal services)
3. Click **Barangay Government Unit** (for barangay services)
4. Browse or search for your needed service

Each office has multiple services with different fees and processing times.

What service are you looking for? 🔍"""
    },
    
    "fees": {
        "keywords": ["fee", "cost", "price", "payment", "how much", "charge", "expensive"],
        "response": """💰 **Service Fees & Costs**

**Typical Fee Ranges:**

**Documents & Certificates:**
• Copy of documents: ₱50-₱100
• Special certificates: ₱75-₱200
• Civil registry docs: ₱155 (PSA), ₱75 (Local)

**Permits:**
• Business/Building Permits: ₱500-₱5,000
• Zoning Certification: ₱200-₱300
• Electrical/Plumbing: ₱500 each

**Special Services:**
• Notarial Services: ₱100
• Expedited processing: Varies by service
• Certified True Copies: ₱75-₱100

**Free Services:**
✓ Barangay Clearance
✓ Certificate of Indigency
✓ Referral Letters
✓ Social Case Studies
✓ Senior Citizen ID
✓ PWD ID

**Exact Fees:**
The exact fee for your service is shown when you:
1. Select a service
2. Click **Apply**
3. See fee information on the form

**Payment Methods:**
• E-Wallet (GCash, Maya) - Instant
• Cash at LGU - Pay on submission
• Online Banking - 2-3 days processing

**No Hidden Charges:**
All fees shown upfront. Pay only what's listed.

Ready to apply? Select a service to see exact pricing! 💳"""
    },
    
    "time": {
        "keywords": ["time", "how long", "when", "duration", "take", "processing", "days"],
        "response": """⏱️ **Service Processing Times**

**Standard Processing:**
• Most documents: 2-5 business days
• Residency certificates: 1-2 days
• Police clearance: 1-2 days
• Health clearance: 1 day

**Permits:**
• Building permits: 10-15 business days
• Business permits: 5-7 business days
• Zoning certification: 3-5 business days

**Special Services:**
• Assistance programs: 5-10 business days
• Civil registry (PSA): 5-7 business days
• Land-related documents: 7-10 business days

**What Affects Processing Time:**
✓ Document completeness (most important!)
✓ Accuracy of information
✓ Current request volume
✓ Need for additional verification
✓ Payment verification (if applicable)

**Ways to Speed Up:**
1. **Submit complete documents** - Most important!
2. **Double-check information** - No corrections needed
3. **Use correct service** - Right office, right form
4. **Pay early** - If cash payment
5. **Stay available** - For possible follow-up

**Holidays & Weekends:**
Processing time excludes:
• Weekends (Saturday-Sunday)
• Philippine holidays
• Local fiesta days

**Real-Time Updates:**
You'll get SMS notifications when:
✓ Application is received
✓ Currently being processed
✓ Ready for pickup
✓ Completed

Check your Dashboard anytime to see current status!

Submitted an application? Check your tracking number on Dashboard! 📊"""
    },
    
    "problem": {
        "keywords": ["problem", "issue", "error", "not working", "bug", "trouble", "broken"],
        "response": """🔧 **Troubleshooting Guide**

**Try These Steps First:**

**1. Clear Your Browser Cache**
• Chrome: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
• Firefox: Ctrl+Shift+Delete
• Safari: Menu → Develop → Clear Caches

**2. Update Your Browser**
• Use the latest version of Chrome, Firefox, Safari, or Edge
• Older versions may have compatibility issues

**3. Check Internet Connection**
• Try another website to confirm internet is working
• Try a different network (WiFi or mobile data)

**4. Try Again Later**
• Wait 5 minutes and try again
• The system may be temporarily busy

**5. Try a Different Browser**
• Sometimes one browser works better than another

**If Problem Persists:**

✓ Take a screenshot of the error
✓ Note the exact time it happened
✓ Write down what you were trying to do
✓ Send to: support@canconnect.gov.ph

**Common Issues & Solutions:**

**"I can't log in"**
→ Check CAPS LOCK is off
→ Ensure you registered first
→ Try another browser

**"Page won't load"**
→ Clear cache (step 1 above)
→ Check internet connection
→ Try later

**"Application won't submit"**
→ Ensure all required fields are filled
→ Check file sizes are not too large
→ Ensure you agreed to terms

**"Document upload failed"**
→ Use PDF, JPG, or PNG only
→ File should be under 5MB
→ Try another file

**Still Need Help?**
Contact us with screenshot and details:
📧 support@canconnect.gov.ph
📞 Visit your Barangay Hall
⏰ Response within 24 hours

We're here to help! 💪"""
    },
    
    "profile": {
        "keywords": ["profile", "account", "settings", "change password", "password", "edit"],
        "response": """👤 **Account & Profile Management**

**Access Your Profile:**
1. Click the **👤 Profile** button in left sidebar
2. View your complete profile information

**What You Can Do:**

**View Profile Information:**
• Full name, email, phone
• Account creation date
• Verification status

**Check Profile Completion:**
• See completion percentage
• Follow suggested steps to 100%

**Personal Information:**
• Cannot change personal data directly
• Submit update request if info is wrong
• Contact support@canconnect.gov.ph

**Account Verification:**
• Upload valid ID to get verified
• ✅ Verified = Full access to all services
• ❌ Not verified = Restricted features

**Change Password:**
1. Go to **Account Settings**
2. Click **Change Password**
3. Enter current password
4. Enter new password (min 6 characters)
5. Confirm new password
6. Click **Update**

**Two-Factor Authentication (2FA):**
• Add extra security layer
• Go to **Account Settings** → **2FA**
• Follow setup instructions
• Confirmation codes sent to email

**Notification Preferences:**
1. Click **Notification Preferences**
2. Choose preferences:
   • Email notifications ✓
   • SMS notifications ✓
   • Push notifications (optional)
3. Click **Save**

**Privacy Settings:**
• Make profile public/private
• Share application history (recommended ON)
• Control data visibility

**View Application History:**
• See all past applications
• Check statuses
• Access tracking numbers
• Download documents

**Security Tips:**
✓ Use strong password (letters + numbers)
✓ Don't share your password
✓ Enable 2FA for security
✓ Keep profile updated
✓ Log out on shared devices

**Need to Change Email?**
Contact support@canconnect.gov.ph with proof of identity

Keep your profile updated for smooth processing! 🔐"""
    },
    
    "greeting": {
        "keywords": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"],
        "response": """👋 **Welcome to CanConnect AI Assistant!**

I'm here to help you navigate CanConnect and get government services easily! 

**I can help you with:**
✓ How to submit applications
✓ Application status tracking
✓ Required documents
✓ Service information
✓ Fees and processing times
✓ Account and profile setup
✓ Technical troubleshooting
✓ General questions

**Popular Topics:**
🔍 **Need something specific?** Just ask me about:
• "How do I apply?"
• "What documents do I need?"
• "How long does it take?"
• "What services are available?"
• "What are the fees?"
• "How to check status?"

**What would you like help with today?** 🤖"""
    },
    
    "gratitude": {
        "keywords": ["thank", "thanks", "thank you", "appreciate", "appreciated"],
        "response": """😊 **You're Welcome!**

Happy to help! I'm here to make your CanConnect experience smooth and easy.

**Is there anything else I can assist you with?**
• Application questions
• Service information
• Account help
• Tracking status
• Or anything else?

Just ask anytime - I'm here 24/7! 💬"""
    }
}


class CanConnectChatbot:
    """AI-powered chatbot for CanConnect platform"""
    
    def __init__(self):
        self.name = CHATBOT_NAME
        self.subtitle = CHATBOT_SUBTITLE
        
    def detect_intent(self, user_message: str) -> Tuple[str, str]:
        """Detect user intent and return matching response"""
        user_message_lower = user_message.lower().strip()
        
        # Check each category in knowledge base
        for intent_key, intent_data in KNOWLEDGE_BASE.items():
            keywords = intent_data["keywords"]
            
            # Check if any keyword matches
            for keyword in keywords:
                if keyword in user_message_lower:
                    return intent_key, intent_data["response"]
        
        # No keywords matched - return default response
        return "default", self._get_default_response()
    
    def _get_default_response(self) -> str:
        """Return default response when no keywords match"""
        return """🤖 **I'm Here to Help!**

I didn't quite catch that, but I'm still ready to assist!

**You can ask me about:**
• How to submit applications
• Application status and tracking
• Required documents
• Available services
• Fees and processing times
• Account and profile help
• Technical issues
• Anything about CanConnect!

**Quick Links:**
📊 Dashboard → Check your applications
🏛️ Services → Browse government services
👤 Profile → Manage your account

What would you like to know? 😊"""
    
    def get_response(self, user_message: str) -> str:
        """Generate AI response"""
        intent, response = self.detect_intent(user_message)
        return response


def initialize_chatbot_state():
    """Initialize chatbot session state"""
    if 'chatbot_messages' not in st.session_state:
        st.session_state.chatbot_messages = []
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CanConnectChatbot()


def add_chatbot_to_page():
    """Add chatbot to the current page"""
    initialize_chatbot_state()
    
    # Chat interface styling
    st.markdown("""
    <style>
    .chatbot-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .chatbot-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    .chatbot-header h3 {
        margin: 0 0 5px 0;
        font-size: 18px;
    }
    
    .chatbot-header p {
        margin: 0;
        font-size: 12px;
        opacity: 0.9;
    }
    
    .chat-messages {
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 15px;
        padding: 10px 0;
    }
    
    .chat-message {
        margin-bottom: 12px;
        display: flex;
        gap: 10px;
    }
    
    .chat-message.user {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .message-bubble.user {
        background: #667eea;
        color: white;
        border-radius: 12px 4px 12px 12px;
    }
    
    .message-bubble.ai {
        background: #f0f0f0;
        color: #333;
        border-radius: 4px 12px 12px 12px;
    }
    
    .input-helper {
        font-size: 11px;
        color: #999;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Chat header
    st.markdown(f"""
    <div class="chatbot-header">
        <h3>{CHATBOT_NAME}</h3>
        <p>{CHATBOT_SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    if st.session_state.chatbot_messages:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        for msg in st.session_state.chatbot_messages:
            role_class = "user" if msg["role"] == "user" else "ai"
            st.markdown(f"""
            <div class="chat-message {role_class}">
                <div class="message-bubble {role_class}">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show initial message
        initial_msg = "👋 Welcome! I'm here to help with any questions about CanConnect services. What can I assist you with?"
        st.session_state.chatbot_messages.append({"role": "ai", "content": initial_msg})
        st.markdown(f"""
        <div class="chat-messages">
            <div class="chat-message ai">
                <div class="message-bubble ai">{initial_msg}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me anything...",
            label_visibility="collapsed",
            key="chatbot_input"
        )
    
    with col2:
        send = st.button("Send ✈️", use_container_width=True, key="chatbot_send")
    
    st.markdown(
        '<div class="input-helper">💡 Type your question and press Enter or click Send</div>',
        unsafe_allow_html=True
    )
    
    # Process user input
    if send and user_input.strip():
        # Add user message
        st.session_state.chatbot_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        with st.spinner("Processing..."):
            time.sleep(RESPONSE_DELAY)
            response = st.session_state.chatbot.get_response(user_input)
            
            # Add AI response
            st.session_state.chatbot_messages.append({
                "role": "ai",
                "content": response
            })
        
        st.rerun()
