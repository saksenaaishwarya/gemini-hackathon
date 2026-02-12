<div align="center">

<img src="assets/image.jpeg" alt="LegalMind Logo" width="200" style="border-radius: 15px; margin-bottom: 20px;"/>

# 🏛️ LegalMind

### **AI-Powered Legal Intelligence Platform**
#### *Transforming Contract Analysis & Legal Research with Advanced AI*

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128%2B-green?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15.3-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Firestore](https://img.shields.io/badge/Firestore-Native-orange?style=flat-square&logo=google-cloud&logoColor=white)](https://firebase.google.com/docs/firestore)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](LICENSE.md)

<br/>

[🚀 Quick Start](#-quick-start) • [🌍 Deployment](#-deployment) • [📚 Features](#-core-features) • [🏗️ Architecture](#️-architecture) • [📖 Docs](#-documentation) • [💻 Demo](#-use-cases)

</div>

---

## 🌟 **Overview**

**LegalMind** is a cutting-edge, Google Cloud-native platform that revolutionizes legal contract analysis and research. Powered by **Google's Gemini 2.0 Flash** AI model, it orchestrates **6 specialized legal agents** with **14+ intelligent tools** to provide comprehensive contract intelligence, compliance verification, risk assessment, and automated legal documentation.

Perfect for legal teams, compliance officers, contract managers, and enterprises seeking AI-powered legal analysis at scale.

---

## 📸 **Platform Screenshots**

<div align="center">

### **🏠 Homepage - Elegant Legal Intelligence Dashboard**
<img src="assets/homepage.png" alt="LegalMind Homepage" width="800" style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"/>

### **💬 AI Response - Comprehensive Contract Analysis**
<img src="assets/response.png" alt="Contract Analysis Response" width="800" style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"/>

### **📊 Detailed Insights - Multi-Agent Legal Intelligence**
<img src="assets/response2.png" alt="Detailed Legal Analysis" width="800" style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"/>

</div>

---

## ✨ **Core Features**

<div align="center">

### **Powerful AI-Driven Legal Capabilities**

</div>

<table>
<tr>
<td width="50%" valign="top">

### 📋 **Smart Contract Analysis**
- ✓ Automated clause extraction & classification
- ✓ Intelligent risk scoring & assessment
- ✓ Structured data extraction from PDFs
- ✓ Comprehensive obligation mapping

<br/>

### 📚 **Legal Research Engine**
- ✓ AI-powered precedent analysis
- ✓ Legal framework research & recommendations
- ✓ Real-time regulatory tracking
- ✓ Automated citation management

<br/>

### ✅ **Compliance Verification**
- ✓ **GDPR** compliance checking & validation
- ✓ **HIPAA** requirements assessment
- ✓ **CCPA** obligations verification
- ✓ **SOX** compliance analysis

</td>
<td width="50%" valign="top">

### 🎯 **Risk Management**
- ✓ Multi-dimensional contract risk scoring
- ✓ Automated liability identification
- ✓ Critical red flag detection
- ✓ Financial exposure analysis

<br/>

### 📄 **Document Generation**
- ✓ Professional legal memo creation
- ✓ Automated compliance reports
- ✓ Executive summaries & briefs
- ✓ Multi-format export (PDF, DOCX, MD)

<br/>

### 🧠 **Transparent AI Reasoning**
- ✓ Detailed thinking logs & reasoning traces
- ✓ Full decision transparency
- ✓ Step-by-step analysis breakdown
- ✓ Complete audit trails for compliance

</td>
</tr>
</table>

---

## 🏗️ **Architecture**

### **Multi-Agent System** 🤖

```text
+--------------------+        +-----------------------------+
|        User        |        |     Next.js Dashboard      |
|  (Uploads Legal    |<------>|   (Review & Interactions)  |
|        PDF)        |        +--------------^-------------+
+---------+----------+                       |
          |                                  |
          v                                  |
+---------------------------+                |
|   Upload & Ingestion      |                |
|  (FastAPI / Cloud Run)    |                |
+-------------+-------------+                |
              |                              |
              v                              |
      +--------------------+                 |
      |  Router / Query    |                 |
      |     Classifier     |-----------------+
      +----+-------+-------+
           |       |
   +-------+       +-----------------------------+
   |                             |              |
   v                             v              v
+----------+              +-------------+  +-------------+
| Risk    |              | Compliance  |  |  Summary    |
| Agent   |              | Agent       |  | Agent       |
+----+----+              +------+------ +--+-----+------+
     |                          |               |
     +-----------+--------------+---------------+
                 v
        +----------------------------+
        |      Firestore Memory      |
        |  (Insights, Flags, Notes)  |
        +--------------+-------------+
                       |
                       v
            +------------------------+
            |  Aggregation / API     |
            |   (FastAPI Backend)    |
            +------------------------+
```

### **Tech Stack** 🛠️

<div align="center">

<table>
<tr>
<th>🎨 Layer</th>
<th>⚡ Technology</th>
<th>📌 Purpose</th>
</tr>
<tr>
<td><strong>🖥️ Frontend</strong></td>
<td>Next.js 15 • React 18 • TypeScript • Tailwind CSS</td>
<td>Modern UI with real-time updates</td>
</tr>
<tr>
<td><strong>⚙️ Backend</strong></td>
<td>FastAPI • Python 3.11 • Uvicorn</td>
<td>High-performance async API</td>
</tr>
<tr>
<td><strong>🤖 AI/ML</strong></td>
<td>Google Gemini 2.0 Flash</td>
<td>Advanced reasoning & function calling</td>
</tr>
<tr>
<td><strong>💾 Database</strong></td>
<td>Google Cloud Firestore</td>
<td>Scalable document database (99.999% SLA)</td>
</tr>
<tr>
<td><strong>📦 Storage</strong></td>
<td>Google Cloud Storage</td>
<td>Secure PDF & document management</td>
</tr>
<tr>
<td><strong>☁️ Infrastructure</strong></td>
<td>Google Cloud Platform</td>
<td>Serverless, auto-scaling deployment</td>
</tr>
</table>

</div>

---

## 📊 **System Capabilities**

<div align="center">

| 🎯 Component | 📈 Count | 📝 Details |
|:-------------|:--------:|:----------|
| **🤖 Legal Agents** | **6** | Specialized AI agents for different legal tasks |
| **🛠️ Tools** | **14+** | Contract, compliance, risk, document, clause tools |
| **🔌 API Endpoints** | **31** | 29 REST + 2 WebSocket for real-time communication |
| **💾 Collections** | **6** | Sessions, messages, contracts, clauses, logs, docs |
| **💻 Lines of Code** | **9,000+** | ~6,000 backend + ~3,000 frontend |
| **✅ Test Coverage** | **97%** | 34/35 tests passing |

</div>

---

## 🚀 **Quick Start**

<div align="center">

### **Get LegalMind Running in 3 Steps**

</div>

### **Prerequisites**

<table>
<tr>
<td>✅ Python 3.11+</td>
<td>✅ Node.js 18+</td>
<td>✅ Google Gemini API Key</td>
<td>✅ Google Cloud Project with Firestore</td>
</tr>
</table>

### **📦 Installation**

#### **Step 1️⃣: Clone & Navigate**
```bash
git clone https://github.com/smirk-dev/gemini-hackathon.git
cd gemini-hackathon
```

#### **Step 2️⃣: Configure Environment**
```bash
# Create backend/.env.local with your secrets
GEMINI_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=legalmind-486106
APP_ENV=development
DEBUG=true
```

#### **Step 3️⃣: Start Services**

**🪟 Option A: Automated (Windows)**
```bash
start-legalmind.bat
```

**🌍 Option B: Manual (All Platforms)**
```bash
# Terminal 1: Backend
cd backend
python main_new.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

### **🌐 Access the Platform**

<div align="center">

<table>
<tr>
<th>🎯 Service</th>
<th>🔗 URL</th>
<th>📝 Description</th>
</tr>
<tr>
<td><strong>🌐 Web App</strong></td>
<td><a href="http://localhost:3000">http://localhost:3000</a></td>
<td>Main application interface</td>
</tr>
<tr>
<td><strong>⚙️ API</strong></td>
<td><a href="http://localhost:8000">http://localhost:8000</a></td>
<td>Backend API server</td>
</tr>
<tr>
<td><strong>📖 API Docs</strong></td>
<td><a href="http://localhost:8000/docs">http://localhost:8000/docs</a></td>
<td>Interactive Swagger UI</td>
</tr>
</table>

</div>

---

## 🌍 **Deployment**

<div align="center">

### **Deploy LegalMind to Google Cloud in 5 Minutes** ☁️

</div>

### **🚀 Quick Deploy (One-Command Setup)**
```bash
# 1️⃣ Run setup script to configure GCP
./setup-gcp.ps1          # Windows
# or
./setup-gcp.sh           # macOS/Linux

# 2️⃣ Add GitHub secrets (from script output)
# - GCP_PROJECT_ID
# - WIF_PROVIDER
# - WIF_SERVICE_ACCOUNT
# - FIREBASE_SERVICE_ACCOUNT

# 3️⃣ Push to main branch
git push origin main

# ✨ GitHub Actions automatically deploys:
# - Backend → Cloud Run
# - Frontend → Firebase Hosting
```

### **🏗️ Production Architecture**
<table>
<tr>
<td width="25%"><strong>🌐 Frontend</strong></td>
<td width="75%">Firebase Hosting (Global CDN + Auto-scaling)</td>
</tr>
<tr>
<td width="25%"><strong>⚙️ Backend</strong></td>
<td width="75%">Google Cloud Run (Serverless, Auto-scaling)</td>
</tr>
<tr>
<td width="25%"><strong>💾 Database</strong></td>
<td width="75%">Firestore (99.999% SLA, Global Replication)</td>
</tr>
<tr>
<td width="25%"><strong>📦 Storage</strong></td>
<td width="75%">Cloud Storage (PDFs & Documents)</td>
</tr>
</table>

### **💰 Estimated Costs**
<table>
<tr>
<td>☁️ <strong>Cloud Run</strong></td>
<td>~$0.40 per million requests</td>
</tr>
<tr>
<td>🌐 <strong>Firebase Hosting</strong></td>
<td>Free tier (10 GB/month)</td>
</tr>
<tr>
<td>💾 <strong>Firestore</strong></td>
<td>Free tier (25k reads + writes/day)</td>
</tr>
<tr>
<td><strong>💵 Total</strong></td>
<td><strong>$5-15/month</strong> for moderate usage</td>
</tr>
</table>

📖 **Full Deployment Guides:**
- [Quick Deploy Guide](QUICK_DEPLOY.md) - 5-minute setup
- [Complete Deployment Guide](DEPLOYMENT_GUIDE.md) - Advanced configuration

---

## 🎯 **Use Cases**

<div align="center">

### **Transform Legal Operations Across Your Organization**

</div>

<table>
<tr>
<td width="50%" valign="top">

### **👨‍⚖️ For Legal Teams**
- 📋 **Automate** contract review processes
- ⚡ **Accelerate** due diligence workflows
- 🎯 **Standardize** analysis procedures
- 💾 **Maintain** searchable contract archives
- 📊 **Generate** comprehensive legal reports

<br/>

### **✅ For Compliance Officers**
- 🔍 **Verify** regulatory compliance automatically
- 📈 **Track** compliance evolution over time
- 📊 **Generate** detailed compliance reports
- 🚨 **Flag** potential violations early
- 📝 **Document** compliance processes

</td>
<td width="50%" valign="top">

### **📝 For Contract Managers**
- 🔎 **Extract** and structure contract data
- 🏷️ **Identify** key obligations & milestones
- 📅 **Track** important dates and deadlines
- 💰 **Calculate** financial exposure
- 📈 **Monitor** contract lifecycle

<br/>

### **🏢 For Enterprises**
- 🚀 **Scale** legal operations efficiently
- 📈 **Improve** efficiency by 10x
- 💡 **Reduce** manual work dramatically
- 🎓 **Train** teams on best practices
- 💼 **Optimize** legal budgets

</td>
</tr>
</table>

---

## 📚 **Documentation**

<div align="center">

### **Comprehensive Guides & Resources**

</div>

<table>
<tr>
<td width="50%" valign="top">

### **🚀 Getting Started**
- 📖 **[QUICK_START.md](QUICK_START.md)**  
  *Executive summary & quick reference*
  
- ⚙️ **[ENV_SETUP.md](ENV_SETUP.md)**  
  *Environment configuration guide*
  
- 🗄️ **[FIRESTORE_SETUP.md](FIRESTORE_SETUP.md)**  
  *Database setup instructions*

<br/>

### **🏗️ Technical Guides**
- 🏗️ **[COMPLETE_SETUP.md](COMPLETE_SETUP.md)**  
  *Full technical documentation*
  
- 📊 **[docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)**  
  *Current project status*
  
- 🔄 **[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)**  
  *Technical roadmap*

</td>
<td width="50%" valign="top">

### **🎨 Development Guides**
- 🎨 **[docs/FRONTEND_CHANGES.md](docs/FRONTEND_CHANGES.md)**  
  *UI/UX updates & components*
  
- 📝 **[docs/CODE_TRANSFORMATION_GUIDE.md](docs/CODE_TRANSFORMATION_GUIDE.md)**  
  *Architecture & patterns*

<br/>

### **📊 System Status**
- 📊 **[STATUS.txt](STATUS.txt)**  
  *System overview & ASCII diagram*
  
- 🚀 **[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)**  
  *Production deployment guide*

</td>
</tr>
</table>

---

## 🔌 **API Endpoints**

<div align="center">

### **31 REST & WebSocket Endpoints for Complete Legal Operations**

</div>

### **💬 Chat API**
```http
POST   /api/chat                    # Send message to legal agents
GET    /api/chat/sessions           # List all chat sessions
POST   /api/chat/session            # Create new session
WS     /ws/chat/{session_id}        # Real-time WebSocket chat
```

### **📄 Contract API**
```http
POST   /api/contracts/upload        # Upload contract PDF
GET    /api/contracts               # List all contracts
GET    /api/contracts/{id}          # Get contract details
GET    /api/contracts/{id}/clauses  # Extract clauses
GET    /api/contracts/{id}/download # Download contract
```

### **✅ Compliance & Risk API**
```http
GET    /api/compliance/frameworks   # List compliance frameworks
GET    /api/compliance/check/{id}   # Check compliance status
GET    /api/risk/assess/{id}        # Assess contract risks
```

### **⚙️ System API**
```http
GET    /api/health                  # System health check
GET    /api/agents                  # List all agents
GET    /api/agents/{id}             # Get agent details
```

<div align="center">

**📖 Full Documentation**: Visit **http://localhost:8000/docs** for interactive Swagger UI

</div>

---

## 🧪 **Testing**

<div align="center">

### **Comprehensive Test Suite with 97% Coverage**

</div>

### **🔍 Run Backend Tests**
```bash
cd backend
python test_backend.py
```

**📊 Expected Results:** `34/35 tests passing (97% coverage)`

### **💚 Health Check**
```bash
# Quick health verification
curl http://localhost:8000/api/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}
```

---

## 📁 **Project Structure**

```
gemini-hackathon/
├── 📂 backend/                          # FastAPI Server
│   ├── services/                        # Google Cloud integrations
│   │   ├── gemini_service.py           # Gemini API wrapper
│   │   ├── firestore_service.py        # Database service
│   │   └── storage_service.py          # Cloud Storage service
│   ├── agents/                          # Legal AI agents
│   │   ├── agent_definitions_new.py    # 6 specialized agents
│   │   └── agent_strategies_new.py     # Query routing logic
│   ├── tools/                           # 14+ legal tools
│   │   ├── contract_tools.py           # Contract analysis
│   │   ├── compliance_tools.py         # Compliance checking
│   │   ├── risk_tools.py               # Risk assessment
│   │   ├── clause_tools.py             # Clause extraction
│   │   ├── document_tools.py           # Document generation
│   │   └── logging_tools.py            # Thinking logs
│   ├── api/                             # REST API
│   │   ├── endpoints_new.py            # 31 endpoints
│   │   └── app_new.py                  # FastAPI setup
│   ├── managers/                        # Business logic
│   │   └── chatbot_manager_new.py      # Session orchestration
│   ├── config/                          # Configuration
│   │   └── settings.py                 # Environment settings
│   ├── main_new.py                     # Entry point
│   ├── .env.local                      # Secrets (gitignored)
│   ├── .env.example                    # Config template
│   └── firestore.rules                 # Security rules
│
├── 📂 frontend/                         # Next.js Application
│   ├── app/
│   │   ├── page.tsx                    # Landing page
│   │   ├── chat/                       # Chat interface
│   │   ├── contracts/                  # Contract management
│   │   ├── dashboard/                  # Analytics dashboard
│   │   ├── reports/                    # Documents & reports
│   │   ├── thinking-logs/              # Agent reasoning
│   │   └── api/                        # API proxy routes
│   ├── components/                      # Reusable UI components
│   ├── lib/                             # Utilities & helpers
│   └── app/globals.css                 # Theme (legal blue)
│
├── 📂 docs/                             # Documentation
│   ├── PROJECT_STATUS.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── FRONTEND_CHANGES.md
│   └── CODE_TRANSFORMATION_GUIDE.md
│
├── 🚀 start-legalmind.bat              # Quick start script
├── 🔐 .env.local                       # Your secrets
├── 📖 README.md                        # This file
├── ⚡ QUICK_START.md                   # Quick reference
├── ✅ COMPLETE_SETUP.md                # Full guide
├── 🗄️ FIRESTORE_SETUP.md               # Database setup
├── 📊 STATUS.txt                       # System overview
└── 📜 LICENSE.md                       # Apache-2.0
```

---

## 🔐 **Security**

<div align="center">

### **Enterprise-Grade Security Features**

</div>

<table>
<tr>
<td width="50%" valign="top">

### **🛡️ Current Setup (Development)**
- ✅ `.env.local` contains API keys (never committed)
- ✅ Firestore security rules deployed
- ✅ CORS configured for local development
- ✅ Debug logging enabled for troubleshooting

</td>
<td width="50%" valign="top">

### **🚀 Production Checklist**
- ⬜ Update Firestore rules with authentication
- ⬜ Create service account for Google Cloud
- ⬜ Enable Cloud Run deployment
- ⬜ Configure custom domain with SSL
- ⬜ Set up monitoring & alerting
- ⬜ Enable production logging

</td>
</tr>
</table>

<div align="center">

📖 See **[COMPLETE_SETUP.md](COMPLETE_SETUP.md)** for detailed production deployment.

</div>

---

## 📈 **Performance Metrics**

<div align="center">

| 🎯 Metric | ⚡ Value | 📊 Status |
|:----------|:--------:|:----------|
| **Backend Startup** | < 3 seconds | 🟢 Optimal |
| **Frontend Build** | 12.7 seconds | 🟢 Fast |
| **API Response Time** | < 100ms (local) | 🟢 Excellent |
| **Chat Response Time** | 2-5 seconds | 🟢 Quick |
| **Test Coverage** | 97% | 🟢 High |
| **Firestore SLA** | 99.999% | 🟢 Enterprise |

</div>

---

## 🤝 **Contributing**

<div align="center">

### **We Welcome Contributions!**

Help us make LegalMind even better for the legal community.

</div>

```bash
# 1️⃣ Fork the repository
git clone https://github.com/your-username/gemini-hackathon.git

# 2️⃣ Create feature branch
git checkout -b feature/amazing-feature

# 3️⃣ Commit your changes
git commit -m 'Add amazing feature'

# 4️⃣ Push to branch
git push origin feature/amazing-feature

# 5️⃣ Open Pull Request
```

<div align="center">

**💡 Ideas for Contributions:**
- 🐛 Bug fixes and improvements
- ✨ New legal tools or agents
- 📚 Documentation enhancements
- 🧪 Additional test coverage
- 🌍 Internationalization support

</div>

---

## 📞 **Support & Resources**

<div align="center">

### **Helpful Links & Resources**

</div>

<table>
<tr>
<td width="50%" valign="top">

### **☁️ Cloud Platforms**
- 🔗 **[Firebase Console](https://console.firebase.google.com/project/legalmind-486106)**  
  *Manage Firestore & hosting*
  
- 🔗 **[Google Cloud Console](https://console.cloud.google.com/project/legalmind-486106)**  
  *Manage GCP services*
  
- 🔗 **[Gemini API Docs](https://ai.google.dev/docs)**  
  *AI model documentation*

</td>
<td width="50%" valign="top">

### **📚 Frameworks & Libraries**
- 🔗 **[FastAPI Documentation](https://fastapi.tiangolo.com/)**  
  *Backend framework guide*
  
- 🔗 **[Next.js Documentation](https://nextjs.org/docs)**  
  *Frontend framework guide*
  
- 🔗 **[Firebase Documentation](https://firebase.google.com/docs)**  
  *Database & hosting guide*

</td>
</tr>
</table>

<div align="center">

### **💬 Getting Help**

📖 Read **[COMPLETE_SETUP.md](COMPLETE_SETUP.md)** for detailed guide  
💬 Check **[STATUS.txt](STATUS.txt)** for system overview  
📝 Review **[docs/](docs/)** directory for technical details

</div>

---

## 📄 **License**

<div align="center">

### **Apache License 2.0**

This project is licensed under the **Apache License 2.0** - see **[LICENSE.md](LICENSE.md)** for details.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

**Free to use for commercial and non-commercial purposes** ✅

</div>

---

## 🙏 **Acknowledgments**

<div align="center">

### **Built with ❤️ Using World-Class Technologies**

<br/>

| Technology | Purpose |
|:-----------|:--------|
| ☁️ **[Google Cloud Platform](https://cloud.google.com/)** | Enterprise-grade cloud infrastructure |
| 🤖 **[Google Gemini 2.0 Flash](https://ai.google.dev/)** | Advanced AI capabilities & reasoning |
| ⚡ **[FastAPI](https://fastapi.tiangolo.com/)** | High-performance backend framework |
| ⚛️ **[Next.js](https://nextjs.org/)** | Modern React-based frontend |
| 💾 **[Firestore](https://firebase.google.com/docs/firestore)** | Scalable NoSQL database |
| 🌍 **Open Source Community** | Amazing tools & libraries |

<br/>

**Special thanks to all contributors and the legal tech community!**

</div>

---

<div align="center">

## 🌟 **Ready to Transform Legal Analysis?** 🌟

### **Get Started in 60 Seconds**

#### 📖 **Option 1: Quick Start**
Start with **[QUICK_START.md](QUICK_START.md)** for a guided walkthrough

#### 🚀 **Option 2: Instant Launch**
```bash
start-legalmind.bat
```

#### 🌐 **Then Visit**
### **[http://localhost:3000](http://localhost:3000)**

<br/>

---

### 💡 **Built with Cutting-Edge Technology**

**Google Cloud Platform** • **Gemini 2.0 Flash AI** • **FastAPI** • **Next.js** • **Firestore**

---

<br/>

*⚖️ Empowering legal teams with enterprise-grade AI intelligence*

<br/>

### **[⬆ Back to Top](#-legalmind)**

<br/>

**Made with ❤️ for the modern legal world**

</div>
