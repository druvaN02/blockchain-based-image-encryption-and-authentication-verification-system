# System Architecture & Design

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      USER (Browser)                          │
│                   http://127.0.0.1:5000                      │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ HTTP/HTTPS
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                  FRONTEND (HTML/CSS/JS)                      │
│  ┌────────────┬─────────────┬─────────────┬──────────────┐  │
│  │ index.html │ upload.html │ verify.html │ history.html │  │
│  └────────────┴─────────────┴─────────────┴──────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           JavaScript (API calls, UI logic)             │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ AJAX/Fetch API
                        │
┌───────────────────────▼──────────────────────────────────────┐
│              FLASK BACKEND (Python 3.11+)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app.py (Main Application)                           │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  Routes:                                             │   │
│  │  - /api/upload    → upload.py                        │   │
│  │  - /api/register  → upload.py                        │   │
│  │  - /api/verify    → verify.py                        │   │
│  │  - /api/history   → history.py                       │   │
│  │  - /api/stats     → history.py                       │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  Utils:                                              │   │
│  │  - blockchain.py  (Web3 interaction)                 │   │
│  │  - encryption.py  (AES-256 encryption)               │   │
│  │  - image_handler.py (SHA-256, validation)            │   │
│  │  - cleanup.py     (Auto-deletion)                    │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ Web3.py
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                 BLOCKCHAIN LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Smart Contract (Solidity 0.8.19)                 │   │
│  │                                                       │   │
│  │  contract ImageVerification {                        │   │
│  │    mapping(hash => ImageRecord) images;              │   │
│  │    function registerImage()                          │   │
│  │    function verifyImage()                            │   │
│  │    function getImageDetails()                        │   │
│  │  }                                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Ethereum Network (Ganache Local / Sepolia Testnet)  │   │
│  │  - Blocks: Immutable ledger                          │   │
│  │  - Accounts: Wallet addresses                        │   │
│  │  - Transactions: State changes                       │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                    FILE STORAGE                              │
│  ┌────────────┬─────────────────┬────────────────────────┐  │
│  │ uploads/   │  encrypted/     │  keys/                 │  │
│  │ (images)   │  (encrypted)    │  (encryption keys)     │  │
│  └────────────┴─────────────────┴────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Frontend Layer

**Purpose:** User interaction and visualization

**Components:**
```
frontend/
├── HTML Pages (Structure)
│   ├── index.html     - Landing page
│   ├── upload.html    - Image upload interface
│   ├── verify.html    - Verification interface
│   └── history.html   - History dashboard
│
├── CSS (Styling)
│   ├── style.css      - Global styles
│   ├── upload.css     - Upload page styles
│   ├── verify.css     - Verify page styles
│   └── history.css    - History page styles
│
└── JavaScript (Logic)
    ├── main.js        - Utils, API wrapper
    ├── upload.js      - Upload page logic
    ├── verify.js      - Verify page logic
    └── history.js     - History page logic
```

**Key Functions:**
- Form handling
- File validation (client-side)
- API communication
- PDF certificate generation
- Real-time updates

---

### 2. Backend Layer

**Purpose:** Business logic and blockchain interaction

**Architecture:**
```python
Flask Application
├── app.py (Entry point)
│   ├── Routes registration
│   ├── CORS configuration
│   ├── Auto-cleanup on startup
│   └── Error handlers
│
├── config.py (Configuration)
│   ├── Environment variables
│   ├── Blockchain settings
│   └── Application settings
│
├── Routes (Blueprints)
│   ├── upload.py
│   │   ├── POST /api/upload
│   │   └── POST /api/register
│   ├── verify.py
│   │   ├── POST /api/verify
│   │   └── POST /api/verify-hash
│   └── history.py
│       ├── GET /api/history/:address
│       ├── GET /api/stats
│       └── GET /api/all-images
│
└── Utils (Helper modules)
    ├── blockchain.py
    │   ├── connect_to_network()
    │   ├── register_image()
    │   ├── verify_image()
    │   └── get_image_details()
    ├── encryption.py
    │   ├── generate_key()
    │   ├── encrypt_file()
    │   └── decrypt_file()
    ├── image_handler.py
    │   ├── validate_image()
    │   ├── calculate_hash()
    │   └── get_image_info()
    └── cleanup.py
        └── cleanup_old_files()
```

---

### 3. Blockchain Layer

**Smart Contract Structure:**

```solidity
contract ImageVerification {
    // Data Structures
    struct ImageRecord {
        string imageHash;      // SHA-256 hash
        address owner;         // Owner's Ethereum address
        uint256 timestamp;     // Registration time
        string fileName;       // Original filename
        bool exists;          // Existence flag
    }
    
    // Storage
    mapping(string => ImageRecord) private images;
    string[] private imageHashes;
    mapping(address => string[]) private userImages;
    
    // Events
    event ImageRegistered(...);
    event ImageVerified(...);
    
    // Functions
    function registerImage() public returns (bool)
    function verifyImage() public returns (...)
    function getImageDetails() public view returns (...)
    function isImageRegistered() public view returns (bool)
    function getUserImages() public view returns (...)
    function getTotalImages() public view returns (uint256)
}
```

**Gas Optimization:**
- Use `mapping` for O(1) lookups
- Use `memory` instead of `storage` where possible
- Minimize `SSTORE` operations
- Use events for logging (cheaper than storage)

---

## Data Flow Diagrams

### 1. Image Upload & Registration Flow

```
User
  │
  ├─1. Select Image File
  │
  ▼
Frontend (JavaScript)
  │
  ├─2. Validate File (type, size)
  │
  ├─3. Create FormData
  │
  ├─4. POST /api/upload
  │
  ▼
Backend (Flask)
  │
  ├─5. Receive file
  │
  ├─6. Validate file (server-side)
  │
  ├─7. Save file temporarily
  │
  ├─8. Calculate SHA-256 hash
  │
  ├─9. Rename file (hash + extension)
  │
  ├─10. (Optional) Encrypt file
  │
  ├─11. Return hash to frontend
  │
  ▼
Frontend
  │
  ├─12. Display hash
  │
  ├─13. User clicks "Register"
  │
  ├─14. POST /api/register
  │
  ▼
Backend
  │
  ├─15. Create transaction
  │
  ├─16. Sign with private key
  │
  ├─17. Send to blockchain
  │
  ▼
Ethereum Blockchain
  │
  ├─18. Execute smart contract
  │
  ├─19. Store record
  │
  ├─20. Emit event
  │
  ├─21. Return transaction hash
  │
  ▼
Backend
  │
  ├─22. Wait for confirmation
  │
  ├─23. Return success + details
  │
  ▼
Frontend
  │
  ├─24. Show success message
  │
  └─25. Offer certificate download
```

### 2. Image Verification Flow

```
User
  │
  ├─1. Upload image to verify
  │
  ▼
Frontend
  │
  ├─2. POST /api/verify (with image)
  │
  ▼
Backend
  │
  ├─3. Receive image
  │
  ├─4. Calculate SHA-256 hash
  │
  ├─5. Query blockchain (read-only)
  │
  ▼
Blockchain
  │
  ├─6. Look up hash in mapping
  │
  ├─7. Return record if exists
  │
  ▼
Backend
  │
  ├─8. Parse blockchain response
  │
  ├─9. Format data
  │
  ├─10. Return to frontend
  │
  ▼
Frontend
  │
  ├─11. Display result
  │     - Authentic: Show owner, date
  │     - Not found: Show "Not registered"
  │
  └─12. User sees result
```

---

## Security Architecture

### 1. Defense in Depth

```
Layer 1: Frontend Validation
├── File type checking (JS)
├── File size limits (JS)
└── HTTPS (in production)

Layer 2: Backend Validation
├── File type verification (Python)
├── File size enforcement
├── Image validation (PIL)
└── Input sanitization

Layer 3: Cryptography
├── SHA-256 hashing
├── AES-256 encryption
├── PBKDF2HMAC key derivation
└── Secure random number generation

Layer 4: Blockchain Security
├── Smart contract validation
├── Transaction signing
├── Gas limit checks
└── Immutable storage

Layer 5: Infrastructure
├── CORS protection
├── Environment variables
├── File permissions
└── Auto-cleanup
```

### 2. Threat Model

| Threat | Mitigation |
|--------|-----------|
| Malicious file upload | File type validation, size limits |
| SQL Injection | No SQL database (blockchain) |
| XSS | Input sanitization, CSP headers |
| CSRF | CORS configuration |
| Man-in-the-middle | HTTPS (production) |
| Private key theft | .env file, not in code |
| 51% Attack | Use established networks |
| Smart contract bugs | Audited, tested code |

---

## Database Schema (Blockchain)

### ImageRecord Structure

```
ImageRecord {
    imageHash:  string    (primary key, indexed)
    owner:      address   (indexed)
    timestamp:  uint256   
    fileName:   string    
    exists:     bool      
}
```

### Mappings

```
images: mapping(string => ImageRecord)
├── Key: imageHash
└── Value: ImageRecord struct

userImages: mapping(address => string[])
├── Key: user address
└── Value: array of image hashes

imageHashes: string[]
└── Array of all registered hashes
```

### Indexes

```
Indexed Fields:
├── imageHash (for fast lookup)
└── owner (for filtering by owner)
```

---

## API Endpoints

### Upload Endpoints

```
POST /api/upload
├── Body: multipart/form-data (image file)
├── Response: {success, image_hash, filename, ...}
└── Purpose: Upload image and generate hash

POST /api/register
├── Body: {image_hash, filename}
├── Response: {success, transaction_hash, block_number, ...}
└── Purpose: Register hash on blockchain
```

### Verify Endpoints

```
POST /api/verify
├── Body: multipart/form-data (image file)
├── Response: {verified, authentic, owner, timestamp, ...}
└── Purpose: Verify image authenticity

POST /api/verify-hash
├── Body: {image_hash}
├── Response: {verified, authentic, owner, timestamp, ...}
└── Purpose: Verify by hash only
```

### History Endpoints

```
GET /api/stats
├── Response: {connected, total_images, contract_address, ...}
└── Purpose: Get blockchain statistics

GET /api/all-images?page=1&per_page=20
├── Response: {images: [...], total, page, total_pages}
└── Purpose: Get paginated image list

GET /api/image/<hash>
├── Response: Image file
└── Purpose: Serve image by hash
```

---

## Deployment Architecture

### Development Environment

```
Local Machine
├── Ganache (Local blockchain)
├── Flask Development Server
└── Browser (Frontend)
```

### Production Environment

```
┌─────────────────┐
│   Cloudflare    │ CDN & SSL
└────────┬────────┘
         │
┌────────▼────────┐
│   Nginx/Apache  │ Reverse Proxy
└────────┬────────┘
         │
┌────────▼────────┐
│   Gunicorn      │ WSGI Server
└────────┬────────┘
         │
┌────────▼────────┐
│   Flask App     │ Application
└────────┬────────┘
         │
┌────────▼────────┐
│   Ethereum      │ Mainnet/Testnet
└─────────────────┘
```

---

## Performance Considerations

### Optimization Strategies

1. **Caching:**
   - Browser caching for static files
   - In-memory caching for blockchain data
   
2. **Lazy Loading:**
   - Paginated history
   - Image thumbnails on-demand

3. **Async Operations:**
   - Non-blocking blockchain calls
   - Background file cleanup

4. **Gas Optimization:**
   - Efficient data structures
   - Minimal storage operations
   - Batch operations (future)

---

## Scalability Plan

### Current Limitations
- Single server
- Local file storage
- Ethereum mainnet costs

### Future Scalability
1. **Horizontal Scaling:** Multiple Flask instances
2. **IPFS Storage:** Decentralized file storage
3. **Layer 2:** Polygon, Optimism for lower costs
4. **CDN:** Global content delivery
5. **Load Balancer:** Distribute traffic

---

**This architecture ensures security, scalability, and maintainability!**
