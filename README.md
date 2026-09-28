# 🔐 BlockVision - Blockchain Image Verification System

A complete blockchain-based image verification system that allows users to register images on the Ethereum blockchain and verify their authenticity. Features include SHA-256 hashing, AES-256 encryption, and immutable blockchain storage.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Solidity](https://img.shields.io/badge/solidity-0.8.19-orange.svg)
![Ethereum](https://img.shields.io/badge/ethereum-blockchain-purple.svg)

## 🌟 Features

### For Image Owners
- ✅ Upload images and generate cryptographic proof of ownership
- ✅ Immutable blockchain record with timestamp
- ✅ AES-256 encryption for secure storage
- ✅ Certificate of authenticity generation
- ✅ Transaction history tracking

### For Verifiers
- ✅ Upload images to check authenticity
- ✅ Compare against blockchain records
- ✅ Detect image tampering
- ✅ View original owner and registration details
- ✅ Verify by hash without uploading files

### Core Technologies
- **Backend**: Python 3.8+, Flask, Web3.py
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Blockchain**: Solidity 0.8.19, Ethereum
- **Security**: SHA-256 hashing, AES-256 encryption
- **Smart Contracts**: Truffle/Hardhat deployment

## 📁 Project Structure

```
blockchain-image-verification/
├── backend/
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration settings
│   ├── requirements.txt            # Python dependencies
│   ├── contracts/
│   │   ├── ImageVerification.sol   # Smart contract
│   │   └── compiled/               # Compiled contracts
│   ├── utils/
│   │   ├── blockchain.py           # Blockchain interaction
│   │   ├── encryption.py           # AES encryption
│   │   ├── hashing.py              # SHA-256 hashing
│   │   └── image_handler.py        # Image processing
│   └── routes/
│       ├── upload.py               # Upload endpoints
│       ├── verify.py               # Verification endpoints
│       └── history.py              # History endpoints
├── frontend/
│   ├── index.html                  # Landing page
│   ├── upload.html                 # Upload interface
│   ├── verify.html                 # Verification interface
│   ├── history.html                # Transaction history
│   ├── css/                        # Stylesheets
│   └── js/                         # JavaScript files
├── blockchain/
│   ├── truffle-config.js           # Truffle configuration
│   ├── hardhat.config.js           # Hardhat configuration
│   ├── scripts/deploy.js           # Deployment script
│   ├── migrations/                 # Migration files
│   └── test/                       # Smart contract tests
└── .env                            # Environment variables
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Ganache** (for local blockchain)
- **MetaMask** browser extension
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/blockchain-image-verification.git
cd blockchain-image-verification
```

2. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
cd ../blockchain
npm install
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Configuration

Edit the `.env` file:

```env
# Blockchain Configuration
ETHEREUM_NODE_URL=http://127.0.0.1:7545
CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS_HERE
PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
NETWORK_ID=5777

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
```

### Deploy Smart Contract

#### Using Hardhat (Recommended)

1. **Start local blockchain (Ganache)**
```bash
ganache-cli
# Or use Ganache GUI
```

2. **Compile contracts**
```bash
cd blockchain
npx hardhat compile
```

3. **Deploy to local network**
```bash
npx hardhat run scripts/deploy.js --network ganache
```

4. **Copy contract address from output and update `.env`**

#### Using Truffle

```bash
cd blockchain
truffle compile
truffle migrate --network ganache
```

### Run the Application

1. **Start Flask backend**
```bash
cd backend
python app.py
```

2. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Upload and Register an Image

1. Navigate to the **Upload** page
2. Drag and drop an image or click to browse
3. (Optional) Enable AES-256 encryption
4. Click **Upload & Generate Hash**
5. Click **Register on Blockchain**
6. Confirm the transaction in MetaMask
7. Download your certificate of authenticity

### 2. Verify an Image

#### Method 1: Upload Image
1. Navigate to the **Verify** page
2. Select "Upload Image" tab
3. Upload the image you want to verify
4. Click **Verify Image**
5. View verification results

#### Method 2: Verify by Hash
1. Navigate to the **Verify** page
2. Select "Verify by Hash" tab
3. Paste the SHA-256 hash
4. Click **Verify Hash**
5. View verification results

### 3. View History

1. Navigate to the **History** page
2. View all registered images
3. Filter by "All", "My Images", or "Recent"
4. Search by hash, filename, or address
5. Click "View" for detailed information
6. Export data to CSV

## 🧪 Testing

### Smart Contract Tests

```bash
cd blockchain
npx hardhat test
```

Expected output:
```
  ImageVerification
    ✓ Should deploy successfully
    ✓ Should register an image successfully
    ✓ Should not register duplicate image hash
    ✓ Should verify registered image
    ✓ Should track user's registered images
```

### Manual Testing

1. **Test Image Upload**
   - Upload various image formats (PNG, JPG, GIF)
   - Test file size limits (max 16MB)
   - Verify hash generation

2. **Test Blockchain Registration**
   - Register images on local blockchain
   - Verify transaction success
   - Check gas usage

3. **Test Verification**
   - Verify registered images
   - Test with modified images
   - Verify tampering detection

## 🌐 Deployment

### Deploy to Sepolia Testnet

1. **Get Sepolia ETH**
   - Use a faucet: https://sepoliafaucet.com/

2. **Update `.env`**
```env
ETHEREUM_NODE_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
NETWORK_ID=11155111
```

3. **Deploy contract**
```bash
cd blockchain
npx hardhat run scripts/deploy.js --network sepolia
```

4. **Verify on Etherscan** (automatic in deploy script)

### Deploy Backend (Production)

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```bash
docker build -t blockvision-backend .
docker run -p 5000:5000 blockvision-backend
```

## 🔒 Security Considerations

1. **Private Keys**: Never commit private keys to version control
2. **Environment Variables**: Use `.env` files and keep them secure
3. **HTTPS**: Always use HTTPS in production
4. **Input Validation**: All inputs are validated on backend
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Encryption Keys**: Store encryption keys securely
7. **Access Control**: Implement proper authentication

## 📊 API Documentation

### Upload Endpoints

#### POST `/api/upload`
Upload an image and generate hash.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` (file), `encrypt` (boolean)

**Response:**
```json
{
  "success": true,
  "image_hash": "abc123...",
  "filename": "image.jpg",
  "file_size": 1234567,
  "dimensions": "1920x1080",
  "format": "JPEG"
}
```

#### POST `/api/register`
Register image hash on blockchain.

**Request:**
```json
{
  "image_hash": "abc123...",
  "filename": "image.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "transaction_hash": "0x...",
  "block_number": 12345,
  "gas_used": 123456
}
```

### Verify Endpoints

#### POST `/api/verify`
Verify image authenticity.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` (file)

**Response:**
```json
{
  "success": true,
  "verified": true,
  "authentic": true,
  "owner": "0x...",
  "timestamp": 1234567890,
  "registration_date": "2024-01-01T00:00:00"
}
```

#### POST `/api/verify-hash`
Verify by hash only.

**Request:**
```json
{
  "image_hash": "abc123..."
}
```

### History Endpoints

#### GET `/api/history/:address`
Get user's registered images.

#### GET `/api/stats`
Get blockchain statistics.

#### GET `/api/all-images?page=1&per_page=20`
Get all registered images (paginated).

## 🛠️ Troubleshooting

### Common Issues

**Problem**: Contract deployment fails
- **Solution**: Ensure Ganache is running and you have sufficient ETH

**Problem**: MetaMask not connecting
- **Solution**: Add localhost network to MetaMask (RPC: http://127.0.0.1:7545, Chain ID: 5777)

**Problem**: Image upload fails
- **Solution**: Check file size (max 16MB) and format (PNG, JPG, JPEG, GIF, BMP, WEBP)

**Problem**: Transaction fails
- **Solution**: Check gas limit and account balance

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Ethereum blockchain technology
- Web3.py library
- Flask framework
- OpenZeppelin contracts
- MetaMask wallet

---

**Made with ❤️ by BlockVision Team**
