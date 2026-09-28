# Technologies Used - Explained Simply

## What We Used & Why

### Frontend (What User Sees)

#### 1. **HTML5**
- **What:** Markup language for web pages
- **Why:** Standard for creating web structure
- **Used For:** Page layout, forms, content structure

#### 2. **CSS3**  
- **What:** Styling language
- **Why:** Make the website look beautiful
- **Used For:** Colors, animations, responsive design

#### 3. **JavaScript (Vanilla)**
- **What:** Programming language for web
- **Why:** Make pages interactive
- **Used For:** Button clicks, form validation, API calls

#### 4. **jsPDF**
- **What:** JavaScript library
- **Why:** Generate PDF certificates
- **Used For:** Creating downloadable certificates

---

### Backend (Server Side)

#### 1. **Python 3.11**
- **What:** Programming language
- **Why:** Easy to learn, powerful for blockchain
- **Used For:** Server logic, blockchain interaction

#### 2. **Flask Framework**
- **What:** Web framework for Python
- **Why:** Lightweight, simple to use
- **Used For:** API endpoints, routing, server logic

#### 3. **Web3.py**
- **What:** Python library for Ethereum
- **Why:** Interact with blockchain from Python
- **Used For:** Send transactions, read blockchain data

#### 4. **Pillow (PIL)**
- **What:** Image processing library
- **Why:** Validate and process images
- **Used For:** Check image format, get dimensions

#### 5. **Cryptography Library**
- **What:** Security library
- **Why:** Implement encryption
- **Used For:** AES-256 encryption, key generation

---

### Blockchain Technologies

#### 1. **Ethereum**
- **What:** Blockchain platform
- **Why:** Most popular smart contract platform
- **Used For:** Store immutable records

#### 2. **Solidity**
- **What:** Smart contract language
- **Why:** Only language for Ethereum contracts
- **Used For:** Write blockchain logic

#### 3. **Hardhat**
- **What:** Development environment
- **Why:** Best tool for Ethereum development
- **Used For:** Compile, deploy, test contracts

#### 4. **Ganache**
- **What:** Local blockchain
- **Why:** Test without real money
- **Used For:** Development and testing

#### 5. **Ethers.js**
- **What:** Ethereum library
- **Why:** Modern, well-maintained
- **Used For:** Deploy smart contracts

---

### Security & Cryptography

#### 1. **SHA-256**
- **What:** Hashing algorithm
- **Why:** Creates unique fingerprint
- **Used For:** Generate image hash
- **Example:** 
  - Input: image.jpg
  - Output: bdf8e2cfdd743df040698...

#### 2. **AES-256**
- **What:** Encryption algorithm
- **Why:** Military-grade security
- **Used For:** Optional image encryption
- **Key Size:** 256 bits = 2^256 possible keys

#### 3. **PBKDF2HMAC**
- **What:** Key derivation function
- **Why:** Secure password-to-key conversion
- **Used For:** Generate encryption keys

---

## Why These Specific Choices?

### Frontend: Why Vanilla JS instead of React?
✅ **Simpler to understand**  
✅ **No build tools needed**  
✅ **Faster to learn**  
✅ **Perfect for this project size**

### Backend: Why Flask instead of Django?
✅ **Lightweight and simple**  
✅ **Easy to customize**  
✅ **Perfect for APIs**  
✅ **No unnecessary features**

### Blockchain: Why Ethereum?
✅ **Most widely used**  
✅ **Best documentation**  
✅ **Large community**  
✅ **Proven security**

### Hashing: Why SHA-256?
✅ **Industry standard**  
✅ **Used by Bitcoin**  
✅ **Collision-resistant**  
✅ **Fast computation**

### Encryption: Why AES-256?
✅ **NSA-approved**  
✅ **Unbreakable (currently)**  
✅ **Fast and efficient**  
✅ **Widely supported**

---

## How They Work Together

```
User uploads image
   ↓
JavaScript sends to Flask server  
   ↓
Python calculates SHA-256 hash
   ↓
Web3.py sends to Ethereum blockchain
   ↓
Smart Contract stores record
   ↓
Transaction confirmed
   ↓
Certificate generated (jsPDF)
   ↓
User downloads certificate
```

---

## For Research Paper

### Technical Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Presentation** | HTML/CSS/JS | User Interface |
| **Application** | Python/Flask | Business Logic |
| **Blockchain** | Ethereum/Solidity | Immutable Storage |
| **Security** | SHA-256, AES-256 | Cryptography |
| **Development** | Hardhat, Ganache | Testing & Deployment |

### Key Algorithms

1. **SHA-256 Hashing**
   - Input: Image file (any size)
   - Output: 64-character hexadecimal hash
   - Time Complexity: O(n) where n = file size
   - Security: 256-bit security level

2. **AES-256 Encryption**
   - Mode: CBC (Cipher Block Chaining)
   - Key Size: 256 bits
   - Block Size: 128 bits
   - Security: Quantum-resistant (currently)

3. **PBKDF2HMAC**
   - Iterations: 100,000
   - Hash Function: SHA-256
   - Purpose: Key derivation from password
   - Salt: Randomly generated 16 bytes

---

## Dependencies List

### Backend (Python)
```
Flask==2.3.3
Flask-CORS==4.0.0
web3==6.11.1
cryptography==41.0.4
Pillow==10.0.1
python-dotenv==1.0.0
eth-account==0.9.0
hexbytes==0.3.1
requests==2.31.0
```

### Blockchain (Node.js)
```
@nomicfoundation/hardhat-toolbox
hardhat
ethers
dotenv
@openzeppelin/contracts
```

### Frontend (CDN)
```
jsPDF (via CDN)
```
