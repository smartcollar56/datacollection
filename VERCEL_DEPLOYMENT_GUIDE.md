# Vercel Deployment Guide

## Issues Fixed

The deployment errors were caused by:
1. ❌ **Wrong file path in vercel.json** - Was pointing to `app.py` instead of `api/app.py`
2. ❌ **Missing index.py** - Vercel expects `api/index.py` as the entry point
3. ❌ **File serving issues** - `send_file()` with relative paths didn't work in serverless environment
4. ❌ **Missing error handling** - No graceful handling for missing environment variables
5. ❌ **Favicon errors** - Returning 500 instead of 204 for missing favicon

## What Was Changed

### 1. Created `api/index.py`
- Entry point for Vercel deployment
- Imports and exposes the Flask app

### 2. Updated `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### 3. Fixed File Serving in `api/app.py`
- Added `serve_html_file()` helper function
- Uses absolute paths based on `__file__` location
- Fallback to reading file content directly if `send_file()` fails
- Better error handling and logging

### 4. Improved Supabase Initialization
- No longer crashes if environment variables are missing
- Returns helpful warning messages
- Gracefully handles missing credentials

### 5. Added `.vercelignore`
- Excludes unnecessary files from deployment
- Reduces deployment size

## Deployment Steps

### Step 1: Configure Environment Variables in Vercel

Go to your Vercel project dashboard:
1. Navigate to **Settings** > **Environment Variables**
2. Add the following variables:
   - `SUPABASE_URL` = your Supabase project URL
   - `SUPABASE_ANON_KEY` = your Supabase anonymous key
   - `SUPABASE_BUCKET` = `datacollection` (or your bucket name)

### Step 2: Deploy to Vercel

```bash
# If you haven't installed Vercel CLI
npm i -g vercel

# Deploy
vercel

# Or deploy to production
vercel --prod
```

Or simply push to your GitHub repository if you have automatic deployments enabled.

### Step 3: Verify Deployment

After deployment, test these endpoints:
- `https://your-app.vercel.app/` - Should show login page
- `https://your-app.vercel.app/login` - POST endpoint for authentication
- `https://your-app.vercel.app/data` - GET sensor data
- `https://your-app.vercel.app/upload` - POST sensor data

## Troubleshooting

### Still getting 500 errors?

1. **Check Vercel logs**: Go to your project > Deployments > Click on deployment > Runtime Logs
2. **Verify environment variables are set** in Vercel dashboard
3. **Check file permissions**: Ensure HTML files and favicon are committed to git

### Environment Variables Not Working?

- Make sure you've set them in Vercel dashboard (not just in `.env` file)
- Redeploy after setting environment variables
- Check variable names are exactly: `SUPABASE_URL` and `SUPABASE_ANON_KEY`

### HTML Pages Not Loading?

- Check that `login.html` and `dashboard.html` are in the project root
- Verify they're committed to git (not in `.gitignore`)
- Check Vercel build logs to see if files are included

### Favicon Errors?

- These are now handled gracefully (returns 204 No Content)
- Won't cause 500 errors anymore
- You can add a favicon later to `public/favicon.ico`

## Testing Locally

To test the app locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
echo "SUPABASE_URL=your_url_here" > .env
echo "SUPABASE_ANON_KEY=your_key_here" >> .env
echo "SUPABASE_BUCKET=datacollection" >> .env

# Run the app
cd api
python app.py
```

Note: The commented-out `if __name__ == "__main__"` section in `app.py` can be uncommented for local testing.

## Success Indicators

✅ All routes return 200 (or 204 for favicon)
✅ Login page loads successfully
✅ Dashboard page loads successfully
✅ API endpoints work correctly
✅ No 500 errors in logs

## Next Steps

After successful deployment:
1. Test the login functionality
2. Test data upload from your IoT device
3. Verify data appears on the dashboard
4. Set up custom domain (optional)
5. Enable production mode

## Support

If you still face issues:
1. Check Vercel runtime logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure all files are committed to your repository
4. Try redeploying after making changes

