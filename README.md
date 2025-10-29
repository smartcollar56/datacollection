# Farm Health Dashboard - Cloud-Native IoT Platform

A real-time farm health monitoring system with **100% cloud-based data storage** using Supabase Storage. No local CSV dependencies - fully deployable on Render or any cloud platform.

## 🌟 Features

✅ **Fully Cloud-Native** - All data stored in Supabase Storage (no local files needed)  
✅ **Real-Time Dashboard** - Live updates every 5 seconds  
✅ **Multi-Device Tracking** - Monitor multiple cow collar devices  
✅ **24-Hour Timeline** - Visualize full day activity patterns  
✅ **Date Filtering** - View historical data by date  
✅ **Beautiful UI** - Glassmorphism design with Chart.js visualizations  
✅ **Production Ready** - Deploy to Render without any file system dependencies  

## 🏗️ Architecture

```
IoT Devices → POST /upload → Flask API → Supabase Storage (CSV append)
                                              ↓
Dashboard → GET /data → Flask API → Supabase Storage (CSV download) → Display
```

**Key Points:**
- ☁️ All data reads from **Supabase Storage**
- 📝 All uploads **append to cloud CSV** (never overwrites)
- 🚀 No local file system needed (perfect for cloud deployment)
- 💾 Data persists even if server restarts

## 📦 Installation

### 1. Clone Repository
```bash
git clone <your-repo>
cd DataCollectionApp
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create `.env` file:
```env
SUPABASE_URL=https://frjzpymkqgemlzvkqarl.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_BUCKET=datacollection
```

### 4. Configure Supabase Storage
In Supabase Dashboard:
1. Go to **Storage** → Create bucket `datacollection`
2. Set bucket to **Public** or configure RLS policies:
   - Allow INSERT for authenticated/anon
   - Allow SELECT for authenticated/anon
   - Allow UPDATE for authenticated/anon

## 🚀 Running the Application

### Start Server
```bash
python app.py
```

Server runs on `http://localhost:5000`

### Generate Sample Data (Optional)
Generate 5 days of realistic test data for 6 devices:
```bash
python generate_sample_data.py
```

This creates **1,728 data points** (48 readings/day/device × 6 devices × 6 days)

### Test Single Upload
```bash
python test_single_upload.py
```

## 📊 API Endpoints

### `POST /upload`
Upload sensor data from IoT device.

**Request:**
```json
{
  "device_id": "cow_device_01",
  "temperature": 38.5,
  "gyroscope": {
    "x": 1.2,
    "y": 0.3,
    "z": -0.1
  },
  "timestamp": "2025-10-29T10:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Data uploaded to cloud"
}
```

### `GET /data`
Retrieve all sensor data from Supabase Storage.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2025-10-29T10:30:00",
      "device_id": "cow_device_01",
      "temperature": 38.5,
      "gyro_x": 1.2,
      "gyro_y": 0.3,
      "gyro_z": -0.1
    }
  ],
  "source": "supabase"
}
```

### `POST /login`
Authenticate device (minimal validation).

**Request:**
```json
{
  "device_id": "cow_device_01",
  "password": "any_password"
}
```

## 🎨 Dashboard Features

### 1. **Temperature Chart**
- Line chart showing temperature trends per device
- X-axis: Time
- Y-axis: Temperature (°C)
- Multiple devices shown with different colors

### 2. **Movement Chart (24-Hour Timeline)**
- Bar chart showing animal movement patterns
- X-axis: **00:00 to 23:59** (full 24-hour day)
- Y-axis: Movement (m/s² from gyroscope X-axis)
- Hourly averages with gaps for missing data
- Tooltip shows: "No data recorded" for inactive hours

### 3. **Filters**
- **Device Filter:** Select specific device or "All Devices"
- **Date Filter:** Select "Today" or any historical date
- **No Data Message:** Shows warning when device not registered on selected date

### 4. **Stats Cards**
- Average Temperature (per device)
- Average Movement (per device)
- Active Devices count
- Total Readings count

### 5. **Data Table**
- Shows latest 20 readings
- All sensor values with timestamps

## 🌐 Deployment on Render

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Create Render Web Service
1. Go to [Render Dashboard](https://render.com)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name:** farm-health-dashboard
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

### 3. Add Environment Variables
In Render settings, add:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_BUCKET`

### 4. Deploy
Click **Create Web Service** - Done! 🚀

## 📁 Project Structure

```
DataCollectionApp/
├── app.py                      # Flask backend (cloud-only)
├── dashboard.html              # Main dashboard with Chart.js
├── login.html                  # Login page
├── generate_sample_data.py     # Generate 5 days of test data
├── test_single_upload.py       # Test single upload
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
└── README.md                   # This file
```

## 🔧 Technical Details

### Data Storage
- **Format:** CSV stored in Supabase Storage
- **Structure:** `timestamp,device_id,temperature,gyro_x,gyro_y,gyro_z`
- **Append Logic:** Download → Append Row → Re-upload (atomic)
- **No Local Files:** Everything in cloud
- **Self-Healing:** If CSV doesn't exist, first upload creates it automatically
- **Graceful Handling:** Dashboard shows "No data uploaded yet" instead of errors when CSV is empty/missing

### Sample Data Characteristics
- **Devices:** 6 cow collars (`cow_device_01` through `cow_device_06`)
- **Time Range:** 5 days (120 hours)
- **Frequency:** Every 30 minutes (48 readings/day/device)
- **Temperature:** 37.8-39.2°C (realistic cow body temp)
- **Movement Patterns:**
  - **Night (00:00-05:00):** Low activity (0.0-0.3 m/s²)
  - **Morning (06:00-07:00):** Waking up (0.3-1.2 m/s²)
  - **Day (07:00-19:00):** Active grazing (1.5-3.5 m/s²)
  - **Evening (19:00-22:00):** Resting (0.5-1.5 m/s²)
  - **Night Prep (22:00-00:00):** Settling down (0.2-0.8 m/s²)

### Chart.js Configuration
- **Type:** Line (temperature), Bar (movement)
- **Time Scale:** Chart.js time adapter
- **Height:** 800px (highly readable)
- **Responsive:** Adapts to screen size
- **Tooltips:** Show exact values and time ranges

## 🐛 Troubleshooting

### "Could not read from Supabase" Error
- Check `.env` file has correct credentials
- Verify Supabase bucket exists and is public
- Check Supabase RLS policies allow read/write

### No Data Showing on Dashboard
- Run `python generate_sample_data.py` to populate data
- Check Flask console for "✓ Successfully read X rows from Supabase Storage"
- Verify network connection to Supabase

### Upload Failing
- Check device_id is not empty
- Verify temperature and gyroscope values are numbers
- Ensure timestamp is ISO 8601 format
- Check Supabase Storage write permissions

## 📝 License

MIT License - Feel free to use for your farm or IoT project!

## 🙏 Credits

Built with:
- Flask (Python web framework)
- Supabase (Cloud storage)
- Chart.js (Data visualization)
- HTML/CSS/JavaScript (Frontend)

---

**Ready for production deployment!** 🚀🐄📊
