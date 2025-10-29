# Vercel Deployment Guide

This guide explains how to deploy your Flask app to Vercel and fix the "Failed to fetch" CORS errors.

## Changes Made

### 1. **Fixed `dashboard.html`** ✅
- Changed `API_BASE` from `'http://localhost:5000'` to `''` (empty string)
- Now uses relative paths like `/data` and `/upload` which work on both local and deployed environments

### 2. **Enhanced Flask CORS Configuration** ✅
- Updated `app.py` to explicitly allow all origins and methods
- Added proper headers support for `Content-Type`

### 3. **Created `vercel.json`** ✅
- Configured Flask as a serverless function
- Set up proper routing for all endpoints
- Added environment variable placeholders

## Deployment Steps

### Step 1: Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Set Environment Variables in Vercel

You need to add your Supabase credentials to Vercel. You can do this in two ways:

#### Option A: Via Vercel Dashboard (Recommended)
1. Go to https://vercel.com/dashboard
2. Select your project (or create new one)
3. Go to **Settings** → **Environment Variables**
4. Add these variables:
   - `SUPABASE_URL` = your_supabase_url
   - `SUPABASE_ANON_KEY` = your_supabase_anon_key
   - `SUPABASE_BUCKET` = datacollection (or your bucket name)

#### Option B: Via CLI
```bash
vercel env add SUPABASE_URL
# Enter your Supabase URL when prompted

vercel env add SUPABASE_ANON_KEY
# Enter your Supabase anon key when prompted

vercel env add SUPABASE_BUCKET
# Enter: datacollection
```

### Step 4: Deploy to Vercel
```bash
# From your project root directory
vercel --prod
```

Or for testing deployment first:
```bash
vercel
```

### Step 5: Test Your Deployment

After deployment, Vercel will give you a URL like: `https://your-app.vercel.app`

Test these endpoints:
1. **Homepage (Login)**: `https://your-app.vercel.app/`
2. **Dashboard**: `https://your-app.vercel.app/dashboard.html`
3. **API Data**: `https://your-app.vercel.app/data`
4. **API Upload**: `https://your-app.vercel.app/upload` (POST)

### Step 6: Verify CORS is Working

Open your dashboard in the browser and check the console:
- ✅ **No "Failed to fetch" errors**
- ✅ **No CORS errors**
- ✅ **Data loads successfully**

## Testing Locally After Changes

To test locally with the new relative path configuration:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
echo "SUPABASE_URL=your_url" > .env
echo "SUPABASE_ANON_KEY=your_key" >> .env
echo "SUPABASE_BUCKET=datacollection" >> .env

# Run the app
python app.py
```

Visit: `http://localhost:5000`

## Troubleshooting

### Issue: "Failed to fetch" errors
**Solution**: Ensure CORS is enabled in Flask (already done in `app.py`)

### Issue: 404 errors for static files
**Solution**: Ensure `dashboard.html` and `login.html` are in the root directory

### Issue: Environment variables not found
**Solution**: 
- Check `.env` file exists locally
- Check environment variables are set in Vercel dashboard
- Redeploy after adding env vars: `vercel --prod`

### Issue: Supabase connection fails
**Solution**: Verify your Supabase credentials are correct in environment variables

## Continuous Deployment

Link your GitHub repository to Vercel for automatic deployments:

1. Push your code to GitHub
2. Go to Vercel Dashboard
3. Click **"Import Project"**
4. Select your GitHub repository
5. Vercel will auto-deploy on every push to main branch

## Summary of Files Changed

- ✅ `dashboard.html` - Fixed API_BASE to use relative paths
- ✅ `app.py` - Enhanced CORS configuration
- ✅ `vercel.json` - Created Vercel configuration
- ✅ `DEPLOYMENT.md` - This deployment guide

## Expected Behavior

**Before Fix:**
- ❌ Console error: `TypeError: Failed to fetch`
- ❌ Dashboard doesn't load data
- ❌ Upload fails

**After Fix:**
- ✅ No console errors
- ✅ Dashboard loads data successfully
- ✅ All fetch requests work on Vercel
- ✅ CORS enabled for all endpoints
- ✅ Works on both localhost and deployed URL

## Need Help?

If you encounter any issues:
1. Check browser console for errors
2. Check Vercel deployment logs: `vercel logs`
3. Verify all environment variables are set correctly
4. Ensure `requirements.txt` includes all dependencies

