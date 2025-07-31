# Capstone-Project - capstone-webapp: Multi-Agent Orchestration Project

Welcome! This repository demonstrates a cloud-deployable multi-agent system using Semantic Kernel, Azure Container Apps, and a simple HTML/JS interface.

---

## Quickstart: Build Your Own Lab Practice

### Step 1: Clone This Repository
```bash
git clone https://github.com/M10vir/capstone-webapp.git
cd capstone-webapp
```

### Step 2: Set Up Python Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Project Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Azure Developer CLI
```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

### Step 5: Authenticate with Azure
```bash
az login
az account set --subscription "<your-subscription-id>"
```

### Step 6: Provision & Deploy the App
```bash
azd up
```
This will:
* Create a resource group
* Provision Azure Container Registry and Container Apps
* Deploy the web interface and backend
* Output a live public endpoint

### Step 7: Validate Your Endpoint
```bash
curl -I https://<your-endpoint>.azurecontainerapps.io/
```
Or visit the URL in your browser to verify functionality.

### Step 8: Customize Agent Behavior
Explore and modify configuration files under /src, /agents, or /config. You can:
* Add new personas
* Adjust orchestration logic
* Tune approval workflows

### Step 9: (Optional) Trigger Git-Based Automation
If included, run:
```bash
./push_to_github.sh
```
Make sure your Git credentials are configured properly.

### Step 10: Extend Your Lab (Optional)
* Try customizing or adding features:
* Include additional agent roles (e.g. QA, Compliance)
* Integrate Azure OpenAI for smarter responses
* Add monitoring, logging, or a health check endpoint


