# 🚀 Making NYCT No-Writer Fully Functional - Step-by-Step Guide

## Overview
Your app currently works but uses mock (fake) data. To make it fully functional with real AI, you need to:
1. Get an AI API key (free tier available)
2. Deploy the backend to a cloud service
3. Connect everything together

## Option 1: Quick Setup with Render (Recommended - FREE)

### Step 1: Get an OpenAI API Key
1. Go to https://platform.openai.com/signup
2. Create a free account (you get $5 free credits)
3. Click your profile icon → "View API keys"
4. Click "Create new secret key"
5. Copy the key that starts with `sk-...` and save it somewhere safe

### Step 2: Deploy Backend to Render
1. Go to https://render.com and click "Get Started for Free"
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: `joshuamtm/nyct-no-writer-mvp`
5. Fill in these settings:
   - **Name**: `nyct-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main_enhanced.py`
6. Choose "Free" plan
7. Click "Create Web Service"

### Step 3: Add Your API Key to Render
1. In Render dashboard, go to your service
2. Click "Environment" in the left menu
3. Add these environment variables:
   - Click "Add Environment Variable"
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI key from Step 1
   - Click "Add Environment Variable" again
   - **Key**: `CORS_ORIGINS`
   - **Value**: `https://nyct-no-writer-mvp.netlify.app`
4. Click "Save Changes"
5. The service will restart automatically

### Step 4: Update Your Frontend on Netlify
1. Copy your Render backend URL (looks like: `https://nyct-backend.onrender.com`)
2. Go to https://app.netlify.com
3. Click on your `nyct-no-writer-mvp` site
4. Go to "Site configuration" → "Environment variables"
5. Click "Add a variable"
   - **Key**: `VITE_API_URL`
   - **Value**: Your Render URL from step 1 (e.g., `https://nyct-backend.onrender.com`)
6. Click "Create variable"
7. Go to "Deploys" → "Trigger deploy" → "Deploy site"

### Step 5: Test Your App
1. Wait 2-3 minutes for everything to deploy
2. Visit https://nyct-no-writer-mvp.netlify.app
3. Upload a proposal document
4. The app should now:
   - Extract real text from PDFs
   - Analyze proposals using AI
   - Generate intelligent decline memos

---

## Option 2: Using Replit (Easiest - No GitHub Required)

### Step 1: Get OpenAI API Key
(Same as Option 1, Step 1)

### Step 2: Deploy to Replit
1. Go to https://replit.com
2. Sign up for free account
3. Click "Create Repl" → "Import from GitHub"
4. Paste: `https://github.com/joshuamtm/nyct-no-writer-mvp`
5. Click "Import from GitHub"
6. When imported, click "Secrets" (lock icon)
7. Add your secrets:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI key
8. In the Shell, type:
   ```
   cd backend
   pip install -r requirements.txt
   python main_enhanced.py
   ```
9. Click "Run"
10. Copy the URL that appears (like `https://nyct-backend.username.repl.co`)

### Step 3: Update Netlify
(Same as Option 1, Step 4, but use your Replit URL)

---

## Option 3: Advanced - Using Supabase Edge Functions (FREE)

### Step 1: Set up Supabase
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Create new project:
   - **Name**: `nyct-nowriter`
   - **Database Password**: Create a strong password
   - **Region**: Choose closest to you
5. Wait for project to set up (2-3 minutes)

### Step 2: Deploy Functions
1. In Supabase dashboard, click "Edge Functions"
2. Click "Create new function"
3. I'll provide you with ready-to-use functions (contact me for the code)

---

## 💰 Cost Breakdown

### Render (Recommended)
- **Backend Hosting**: FREE (with 750 hours/month)
- **OpenAI API**: ~$0.01 per proposal analyzed
- **Total Monthly Cost**: ~$5-10 for moderate use

### Replit
- **Hosting**: FREE (always on with Hacker plan $7/month)
- **OpenAI API**: Same as above
- **Total**: $0-7/month

### Supabase
- **Everything**: FREE for up to 500MB database
- **OpenAI API**: Same as above
- **Total**: ~$5-10/month

---

## 🆘 Troubleshooting

### "API Key Invalid" Error
- Make sure you copied the entire key including `sk-`
- Check there are no extra spaces
- Try generating a new key

### "CORS Error" in Browser
- Make sure you added your Netlify URL to CORS_ORIGINS
- The URL should include `https://`
- Try adding both with and without trailing slash

### Backend Not Responding
- On Render: Check the "Logs" tab for errors
- On Replit: Check the Console output
- Make sure all environment variables are set

### Still Using Mock Data
- Verify VITE_API_URL is set in Netlify
- Redeploy the Netlify site after adding the variable
- Clear your browser cache

---

## 📧 Need Help?

If you get stuck:
1. Take a screenshot of any error messages
2. Note which step you're on
3. Check the service logs (Render/Replit dashboard → Logs)

The app will still work without API keys - it just uses template responses instead of AI.

---

## 🎯 Quick Checklist

- [ ] Got OpenAI API key
- [ ] Deployed backend to Render/Replit
- [ ] Added API key to backend environment
- [ ] Added backend URL to Netlify
- [ ] Redeployed Netlify site
- [ ] Tested with a real document

Once all checked, your app is fully functional with real AI! 🎉