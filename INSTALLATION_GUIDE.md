# Installation Guide - BlockVision Project

## Prerequisites (Install These First)

### 1. Node.js (v18+)
- Download: https://nodejs.org/
- Install LTS version
- Verify: `node --version`

### 2. Python (3.11+)
- Download: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH"
- Verify: `python --version`

### 3. Ganache
- Download: https://trufflesuite.com/ganache/
- Install and keep open

---

## Step-by-Step Installation

### Step 1: Install Backend Dependencies
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain\backend
pip install -r requirements.txt
```

### Step 2: Install Blockchain Tools
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain\blockchain
npm install
```

### Step 3: Setup Ganache
1. Open Ganache
2. Click "QUICKSTART"
3. Copy first account's private key (click key icon 🔑)

### Step 4: Configure Environment
1. Open `.env` file in root folder
2. Update these values:
```
PRIVATE_KEY=<paste_private_key_from_ganache>
CONTRACT_ADDRESS=<will_update_after_deployment>
```

### Step 5: Deploy Smart Contract
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain\blockchain
npx hardhat run scripts/deploy.js --network ganache
```

Copy the contract address from output and update `.env` file.

### Step 6: Start Flask Server
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain\backend
python app.py
```

### Step 7: Open Browser
Navigate to: http://127.0.0.1:5000

---

## Quick Commands Summary

```bash
# Start Ganache (GUI application)
# Then in terminal:

# Terminal 1 - Flask Server
cd C:\Users\manoj\OneDrive\Desktop\blockchain\backend
python app.py

# Keep this running!
```

Open browser: http://127.0.0.1:5000
