# How to Run BlockVision - Simple Guide

## Every Time You Want to Run the Project:

### Step 1: Start Ganache
1. Open Ganache application
2. Click "QUICKSTART"
3. Keep it running

### Step 2: Start Flask Server
1. Open Command Prompt
2. Run:
```bash
cd C:\Users\manoj\OneDrive\Desktop\blockchain\backend
python app.py
```
3. Wait until you see: "Running on http://127.0.0.1:5000"
4. Keep this terminal window open

### Step 3: Open Browser
1. Open any web browser
2. Go to: http://127.0.0.1:5000
3. You're ready to use the application!

---

## What You Can Do:

### Upload & Register Image
1. Click "Upload" in navigation
2. Select/drag an image
3. Click "Upload & Generate Hash"
4. Click "Register on Blockchain"
5. Download certificate (optional)

### Verify Image
1. Click "Verify" in navigation
2. Upload image to verify
3. Click "Verify Image"
4. See if it's registered

### View History
1. Click "History" in navigation
2. See all registered images
3. View thumbnails and details

---

## Stopping the Project:

1. Close browser
2. In Command Prompt with Flask server:
   - Press `Ctrl + C`
3. Close Ganache application

---

## Troubleshooting:

**"Failed to fetch" error?**
- Make sure Flask server is running
- Make sure Ganache is running

**"Cannot connect to blockchain"?**
- Open Ganache and click QUICKSTART
- Check if `.env` has correct private key

**Page not loading?**
- Make sure you're at http://127.0.0.1:5000
- Not http://localhost:5000 (they're different!)

