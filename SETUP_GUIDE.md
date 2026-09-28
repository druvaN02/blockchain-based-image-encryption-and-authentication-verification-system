# 🚀 Complete Setup Guide - BlockVision

Step-by-step guide to set up and run the BlockVision Image Verification System.

## 📋 Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] Git installed
- [ ] MetaMask browser extension installed
- [ ] Ganache installed (Desktop or CLI)

## 🔧 Step 1: Install Required Software

### Install Python
Download from: https://www.python.org/downloads/
```bash
python --version  # Should show 3.8+
```

### Install Node.js
Download from: https://nodejs.org/
```bash
node --version  # Should show 16+
npm --version
```

### Install Ganache
**Option A: Ganache Desktop (Recommended for beginners)**
Download from: https://trufflesuite.com/ganache/

**Option B: Ganache CLI**
```bash
npm install -g ganache
```

### Install MetaMask
Add to your browser: https://metamask.io/

## 📦 Step 2: Project Setup

### 1. Navigate to Project Directory
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain
```

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

If you encounter issues, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
```bash
cd ..\blockchain
npm install
```

## ⚙️ Step 3: Configure Environment

### 1. Create Required Directories
The backend needs these folders:
```bash
cd ..\backend
mkdir uploads encrypted keys
```

### 2. Configure Environment Variables
The `.env` file is already created. You'll update it after deploying the contract.

## 🔗 Step 4: Setup Blockchain

### 1. Start Ganache

**If using Ganache Desktop:**
1. Open Ganache
2. Click "Quickstart"
3. Note the RPC Server (usually `http://127.0.0.1:7545`)
4. Note the first account's private key

**If using Ganache CLI:**
```bash
ganache-cli
```
Keep this terminal window open!

### 2. Configure MetaMask

1. Open MetaMask
2. Click network dropdown → "Add Network"
3. Add custom network:
   - **Network Name**: Ganache Local
   - **RPC URL**: `http://127.0.0.1:7545`
   - **Chain ID**: `5777` (or `1337` for Ganache CLI)
   - **Currency Symbol**: ETH

4. Import an account:
   - Click account icon → Import Account
   - Paste private key from Ganache
   - You should see 100 ETH balance

### 3. Compile Smart Contract
```bash
cd blockchain
npx hardhat compile
```

Expected output:
```
Compiled 1 Solidity file successfully
```

### 4. Deploy Smart Contract
```bash
npx hardhat run scripts/deploy.js --network ganache
```

Expected output:
```
🚀 Starting deployment...
📝 Deploying ImageVerification contract...
✅ ImageVerification deployed to: 0x...
📍 Network: ganache
⛽ Gas used: ...
✅ Contract address and ABI saved
```

**Important**: Copy the contract address from the output!

### 5. Update .env File
Open `.env` file and update:
```env
CONTRACT_ADDRESS=0xYOUR_CONTRACT_ADDRESS_HERE
PRIVATE_KEY=YOUR_PRIVATE_KEY_FROM_GANACHE
```

## 🚀 Step 5: Run the Application

### 1. Start Flask Backend
Open a new terminal:
```bash
cd backend
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### 2. Open Application
Open your browser and navigate to:
```
http://localhost:5000
```

You should see the BlockVision homepage!

## ✅ Step 6: Test the System

### Test 1: Upload and Register an Image

1. Go to Upload page
2. Click or drag an image
3. Click "Upload & Generate Hash"
4. Wait for hash generation
5. Click "Register on Blockchain"
6. Approve transaction in MetaMask
7. Wait for confirmation
8. Download certificate

### Test 2: Verify an Image

1. Go to Verify page
2. Upload the same image
3. Click "Verify Image"
4. Should show "✓ Verified & Authentic"

### Test 3: View History

1. Go to History page
2. Should see your registered image
3. Click "View" for details
4. Export to CSV

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Cannot connect to Ganache"
**Solution:**
- Ensure Ganache is running
- Check RPC URL matches in `.env`
- Try restarting Ganache

### Issue: MetaMask transaction fails
**Solution:**
- Reset MetaMask account (Settings → Advanced → Reset Account)
- Check you have enough ETH
- Ensure contract address is correct in `.env`

### Issue: "Contract not found"
**Solution:**
- Verify contract is deployed: `npx hardhat run scripts/deploy.js --network ganache`
- Copy new contract address to `.env`
- Restart Flask server

### Issue: Image upload fails
**Solution:**
- Check file size (max 16MB)
- Check file format (PNG, JPG, JPEG, GIF, BMP, WEBP)
- Ensure `uploads` folder exists

### Issue: Port 5000 already in use
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py
app.run(port=5001)
```

## 🔄 Restarting the System

Every time you restart:

1. **Start Ganache** (if not already running)
2. **Start Flask Backend**:
   ```bash
   cd backend
   python app.py
   ```
3. **Open Browser**: http://localhost:5000

**Note**: If you restart Ganache, you'll need to redeploy the contract!

## 🌐 Deploy to Testnet (Advanced)

### 1. Get Sepolia Test ETH
- Visit: https://sepoliafaucet.com/
- Enter your MetaMask address
- Wait for ETH to arrive

### 2. Get Infura API Key
- Sign up at: https://infura.io/
- Create new project
- Copy Project ID

### 3. Update .env
```env
ETHEREUM_NODE_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
NETWORK_ID=11155111
PRIVATE_KEY=YOUR_METAMASK_PRIVATE_KEY
```

### 4. Deploy to Sepolia
```bash
cd blockchain
npx hardhat run scripts/deploy.js --network sepolia
```

### 5. Verify on Etherscan
Contract will be automatically verified. View at:
```
https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS
```

## 📚 Additional Resources

- **Solidity Documentation**: https://docs.soliditylang.org/
- **Web3.py Documentation**: https://web3py.readthedocs.io/
- **Hardhat Documentation**: https://hardhat.org/docs
- **MetaMask Documentation**: https://docs.metamask.io/
- **Flask Documentation**: https://flask.palletsprojects.com/

## 🎉 Success!

If you've completed all steps, you now have a fully functional blockchain image verification system!

### What You Can Do:
- ✅ Upload and register images on blockchain
- ✅ Verify image authenticity
- ✅ Encrypt images with AES-256
- ✅ Track registration history
- ✅ Export data to CSV
- ✅ Generate certificates

### Next Steps:
1. Customize the UI colors and branding
2. Add user authentication
3. Implement batch upload
4. Add email notifications
5. Deploy to production

## 💡 Tips

- **Backup**: Save your private keys and contract addresses
- **Testing**: Test on local blockchain before deploying to testnet
- **Gas**: Monitor gas prices when deploying to mainnet
- **Security**: Never share private keys or commit them to git

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Check GitHub issues
4. Ensure all prerequisites are installed
5. Try redeploying the contract

---

**Happy Verifying! 🔐**
