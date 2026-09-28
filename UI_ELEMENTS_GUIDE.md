# UI Elements Guide - What Everything Means

## Quick Reference for All Pages

---

## 📤 Upload Page

### What You See and What It Means:

| Element | What It Is | What It Does |
|---------|-----------|--------------|
| **Drag & Drop Area** | File upload zone | Click or drag image to upload |
| **Enable AES-256 Encryption** | Checkbox | Encrypts image with military-grade security |
| **Upload & Generate Hash** | Button | Calculates unique fingerprint of image |
| **Hash Display** | Text field | Shows 64-character SHA-256 hash |
| **Image Preview** | Thumbnail | Shows your uploaded image |
| **Register on Blockchain** | Button | Stores hash permanently on blockchain |
| **Download Certificate** | Button | Creates PDF proof of registration |

### Enable AES-256 Encryption - Detailed

**What is AES-256?**
- Advanced Encryption Standard with 256-bit key
- Same encryption used by military and governments
- Makes image unreadable without decryption key

**When to Enable:**
- ✅ Sensitive documents
- ✅ Private photos
- ✅ Confidential images
- ✅ Medical records
- ❌ Public images (not needed)

**How It Works:**
1. You check the box
2. System generates random 256-bit key
3. Image encrypted before storage
4. Key stored separately
5. Image remains encrypted on server
6. Blockchain only has hash (not encrypted image)

**Security Level:**
- 2^256 possible keys
- Would take billions of years to crack
- Quantum-resistant (currently)

**Important Notes:**
- Hash is calculated BEFORE encryption
- Encryption happens during storage
- Blockchain verification still works
- Can decrypt later if needed

---

## ✅ Verify Page

### Two Verification Methods:

#### Method 1: Upload Image
| Element | What It Does |
|---------|-------------|
| **Upload Image Tab** | Select to verify by uploading file |
| **Drag & Drop Area** | Upload image to check |
| **Verify Image Button** | Checks blockchain for this image |

#### Method 2: Verify by Hash
| Element | What It Does |
|---------|-------------|
| **Verify by Hash Tab** | Select to verify without uploading |
| **Hash Input Field** | Paste 64-character hash |
| **Verify Hash Button** | Checks blockchain for this hash |

### Verification Results:

#### If Image is VERIFIED (Registered):

**Green Badge: ✓ VERIFIED**

You'll see:
- **Owner Address:** Who registered it
  - Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5`
  - Meaning: Ethereum wallet address of registrant
  
- **Registration Date:** When it was registered
  - Example: "January 15, 2024 at 3:45 PM"
  - Meaning: Exact blockchain timestamp
  
- **Filename:** Original filename
  - Example: "vacation_photo.jpg"
  - Meaning: Name given during upload
  
- **Image Hash:** Complete hash
  - Example: "bdf8e2cfdd743df040698e0b61ecc57e..."
  - Meaning: Unique fingerprint
  
- **Transaction Hash:** Blockchain transaction ID
  - Example: "0x3f7a9c2b1e8d4f5c6a3b2e1d..."
  - Meaning: Proof on blockchain (clickable link)
  
- **Block Number:** Which block
  - Example: "Block #12345"
  - Meaning: Permanent location in blockchain

#### If Image is NOT VERIFIED:

**Red Badge: ✗ NOT VERIFIED**

You'll see:
- **Status:** "This image is not registered"
- **Meaning:** No matching hash found on blockchain
- **Possible Reasons:**
  1. Never uploaded/registered
  2. Image was modified (different hash)
  3. Different file (even if looks similar)
- **Suggestion:** "Register this image to prove authenticity"
- **Action Button:** Quick link to upload page

---

## 📊 History Page

### Top Statistics Cards:

#### Card 1: Total Images
```
📊 Total Images
    156
```
**What it shows:** Total number of ALL images registered by anyone on blockchain

**Why it matters:** Shows overall system usage

**Updates:** Every 30 seconds (auto-refresh)

#### Card 2: Your Images  
```
👤 Your Images
    12
```
**What it shows:** Number of images YOU registered

**How it counts:** 
- Filters by your Ethereum address
- If using backend wallet: shows all (same account)
- If using MetaMask: shows only yours

**Why it matters:** Track your own registrations

#### Card 3: Network Status
```
🟢 Network Status
    Connected
```
**Possible Status:**
- 🟢 **Connected** (Green): Blockchain is accessible, everything working
- 🔴 **Disconnected** (Red): Cannot reach blockchain, check Ganache

**Why it matters:** Know if system is working properly

**Auto-check:** Updates every 30 seconds

#### Card 4: Contract Address
```
📜 Contract Address
    0x32482b3BA7A6aCc376931778DFe38B08FCE8bFb4
    [Copy]
```
**What it shows:** Your smart contract's Ethereum address

**Format:** 0x + 40 hexadecimal characters

**Why it matters:**
- Transparency: Anyone can verify the contract
- Etherscan: View on blockchain explorer
- Audit: Check contract code
- Trust: Proves which contract you're using

**Copy Button:** Click to copy full address

**Use it for:**
- Adding to MetaMask
- Viewing on Etherscan
- Sharing with others
- Documentation

---

### Search & Filter Section:

#### Search Bar
```
🔍 Search by hash, filename, or owner...
```
**What you can search:**
- Image hash (partial or full)
- Filename (e.g., "photo.jpg")
- Owner address (full or partial)

**Examples:**
- `bdf8e2c` → Finds hashes starting with this
- `vacation` → Finds files with "vacation" in name
- `0x742d` → Finds owners with this address

**Features:**
- Real-time: Updates as you type
- Case-insensitive: Capital or lowercase both work
- Partial match: Don't need full text

#### Filter Dropdown
```
Filter: [All Images ▼]
```
**Options:**
- **All Images:** Shows every registered image
- **My Images:** Only images YOU registered
- **Recent:** Last 24 hours only

**Use:**
- Find your images quickly
- See latest registrations
- Manage your uploads

---

### Images Table Columns Explained:

#### Column 1: Image
- **Shows:** 60x60 pixel thumbnail
- **Purpose:** Visual identification
- **After 30 days:** Shows "No Image" placeholder
- **Note:** File deleted but record remains

#### Column 2: Image Hash
- **Shows:** First 16 characters + "..."
- **Full hash on hover:** Move mouse over to see complete hash
- **Copy:** Click to copy full hash
- **Example:** `bdf8e2cfdd743df...`

#### Column 3: Filename
- **Shows:** Original filename
- **Example:** `vacation_photo.jpg`
- **Purpose:** Easy recognition
- **Editable:** No (stored permanently)

#### Column 4: Owner
- **Shows:** Shortened address (e.g., `0x742d...bEb5`)
- **Full address on hover:** Move mouse to see complete
- **Format:** First 6 + last 4 characters
- **Copy:** Click to copy full address

#### Column 5: Registered
- **Shows:** When registered
- **Format:** 
  - Recent: "2 hours ago", "3 days ago"
  - Old: "Jan 15, 2024"
- **Tooltip:** Exact date and time on hover

#### Column 6: Actions
- **View Button:** Opens popup with full details
- **Copy Button:** Copies hash to clipboard

---

### Pagination Controls:

```
< Previous  [1] [2] [3] ... [10]  Next >
```

**What it does:** Navigate through pages

**Settings:**
- 20 images per page
- Click numbers to jump to page
- Previous/Next for sequential browsing

**Total Pages:** Shown at bottom

---

### Loading & Empty States:

#### Loading Spinner
```
⏳ Loading...
```
**When shown:** Fetching data from blockchain
**Duration:** Usually 2-3 seconds
**Meaning:** Please wait

#### Empty State
```
📷 No images found
   Upload your first image!
```
**When shown:** No images match your search/filter
**Action:** Click to go to upload page

---

## 📱 Common UI Patterns

### Buttons:

| Button Color | Meaning | Example |
|-------------|---------|---------|
| **Blue/Purple** | Primary action | "Upload", "Register", "Verify" |
| **Green** | Success/Verified | "Download Certificate" |
| **Gray** | Secondary | "Copy", "View" |
| **Red** | Error/Delete | (Not used currently) |

### Status Indicators:

| Indicator | Meaning |
|-----------|---------|
| 🟢 Green | Success, Connected, Verified |
| 🔴 Red | Error, Disconnected, Not Found |
| 🟡 Yellow | Warning, Processing |
| ⏳ Spinner | Loading, Please Wait |

### Badges:

| Badge | Meaning |
|-------|---------|
| ✓ VERIFIED | Image is registered |
| ✗ NOT VERIFIED | Image not found |
| 🔒 ENCRYPTED | Image is encrypted |
| 📜 CERTIFICATE | Certificate available |

---

## 💡 Tips for Your Friend

### Understanding Addresses:
**Ethereum Address:** Like a bank account number for crypto
- Format: `0x` + 40 characters
- Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5`
- **Owner Address:** Who registered the image
- **Contract Address:** Where the smart contract lives

### Understanding Hashes:
**SHA-256 Hash:** Like a fingerprint for your image
- Format: 64 hexadecimal characters
- Example: `bdf8e2cfdd743df040698e0b61ecc57e...`
- **Unique:** Each image has different hash
- **Deterministic:** Same image = always same hash
- **Changed:** Even 1 pixel different = completely different hash

### Understanding Blockchain Terms:
- **Transaction:** An action on blockchain (registering image)
- **Block:** Container that stores transactions
- **Block Number:** Which block contains your transaction
- **Gas:** Fee to run transaction (like postage stamp)
- **Network:** Which blockchain (Ganache local / Ethereum mainnet)

### Understanding Status:
- **Connected:** Green = Everything working
- **Disconnected:** Red = Problem, check Ganache
- **Verified:** Green = Image is registered
- **Not Verified:** Red = Image not found

---

## 🎯 Quick Actions Guide

### To Register an Image:
1. Go to Upload page
2. Drag/drop or click to select image
3. (Optional) Check "Enable AES-256 Encryption"
4. Click "Upload & Generate Hash"
5. Wait for hash to appear
6. Click "Register on Blockchain"
7. Wait for confirmation (~10-15 seconds)
8. Click "Download Certificate"

### To Verify an Image:
1. Go to Verify page
2. **Option A:** Upload image under "Upload Image" tab
3. **Option B:** Paste hash under "Verify by Hash" tab
4. Click "Verify Image" or "Verify Hash"
5. See results instantly

### To View History:
1. Go to History page
2. See all registered images
3. Use search to find specific image
4. Click "View" for details
5. Click "Copy" to copy hash

---

## 📝 For Report/Documentation

When explaining UI elements in your report:

**Include:**
- Screenshots of each page
- Labels pointing to elements
- Explanations of what each does
- Why each element is important

**Example Description:**
"The History page displays a Statistics Dashboard with four key metrics: Total Images (showing overall system usage), Your Images (personal registrations), Network Status (blockchain connectivity), and Contract Address (smart contract location). This provides users with comprehensive system information at a glance."

---

**All UI elements now explained! Your friend will understand every part of the interface!** 🎉
