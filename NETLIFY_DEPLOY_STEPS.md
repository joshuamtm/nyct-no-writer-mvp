# 🔄 How to Redeploy Your Site on Netlify

## Method 1: From the Deploys Tab (Most Common)
1. Go to https://app.netlify.com
2. Click on your site `nyct-no-writer-mvp`
3. Click **"Deploys"** tab at the top
4. Look for one of these options:
   - **"Retry deploy"** button → Click **"Clear cache and retry deploy"**
   - OR a button that says **"Trigger deploy"** with a dropdown arrow
   - OR three dots menu (**...**) → **"Clear cache and deploy site"**

## Method 2: From Site Overview
1. On your site's main page in Netlify
2. Look for a **"Production deploys"** section
3. Click the dropdown arrow next to the deploy status
4. Select **"Clear cache and deploy site"**

## Method 3: Automatic Deploy (Easiest!)
Since your site is connected to GitHub, you can also:
1. Make a small change to any file
2. Push to GitHub
3. Netlify will automatically redeploy

Quick way to trigger this:
```bash
cd /Users/joshua/nyct-no-writer-mvp
echo " " >> README.md
git add .
git commit -m "Trigger Netlify redeploy"
git push
```

## Method 4: Direct Link
Try this direct link to your deploys:
https://app.netlify.com/sites/nyct-no-writer-mvp/deploys

Then look for **"Trigger deploy"** or **"Retry deploy"** button.

---

## 🎯 What You're Looking For:

The button might say any of these:
- **"Trigger deploy"**
- **"Retry deploy"** 
- **"Redeploy site"**
- **"Clear cache and deploy site"** (this is best - clears old environment variables)

---

## 📸 Visual Guide:

The deploy button is usually:
- In the **Deploys** tab at the top
- OR in a dropdown menu (look for ▼ or ...)
- OR as a button near your latest deploy entry

---

## ✅ How to Know It Worked:

1. After clicking deploy, you'll see:
   - **"Deploy in progress"** message
   - A yellow/building status indicator
   - Progress logs showing

2. Wait 1-3 minutes until you see:
   - **"Published"** status
   - Green checkmark ✓
   - Timestamp of completion

3. Your environment variables are now active!

---

## 🔧 If You Can't Find the Deploy Button:

**Alternative: Just push any change to GitHub**

I can do this for you right now by running:
```bash
git commit --allow-empty -m "Redeploy with new environment variables"
git push
```

This creates an empty commit that triggers a redeploy without changing any files.

---

## 💡 Quick Check:

After your site redeploys:
1. Go to https://nyct-no-writer-mvp.netlify.app
2. Open browser console (F12 → Console tab)
3. Upload a test file
4. You should see the Supabase functions being called

---

Let me know if you need me to trigger the redeploy for you through GitHub!