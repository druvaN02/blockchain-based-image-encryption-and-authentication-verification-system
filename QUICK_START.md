# ⚡ Quick Start - BlockVision

Get up and running in 5 minutes!

## Prerequisites
- Python 3.8+
- Node.js 16+
- Ganache (running)
- MetaMask

## Installation

```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Install Node.js dependencies
cd ../blockchain
npm install

# 3. Compile and deploy contract
npx hardhat compile
npx hardhat run scripts/deploy.js --network ganache

# 4. Copy contract address and update .env
# Edit .env file with CONTRACT_ADDRESS and PRIVATE_KEY

# 5. Start Flask server
cd ../backend
python app.py

# 6. Open browser
# Navigate to http://localhost:5000
```

## Configure MetaMask

1. Add network: `http://127.0.0.1:7545`, Chain ID: `5777`
2. Import account with Ganache private key
3. You're ready!

## Test It

1. **Upload** an image → Register on blockchain
2. **Verify** the same image → See it's verified
3. **History** → View all registered images

## Need Help?

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

---

**That's it! Start securing your images! 🚀**
