# 🚀 Setup Guide: Making NYCT No-Writer Fully Functional with Supabase

## What You'll Need
- ✅ Your Supabase account (you have this)
- ✅ Your OpenAI API key (you have this)
- ⏱️ About 15 minutes

---

## Step 1: Install Supabase CLI (5 minutes)

### On Mac:
1. Open Terminal (find it in Applications → Utilities)
2. Copy and paste this command:
```bash
brew install supabase/tap/supabase
```
3. Press Enter and wait for it to install

### On Windows:
1. Download from: https://github.com/supabase/cli/releases
2. Download the `.exe` file for Windows
3. Run the installer

---

## Step 2: Set Up Your Supabase Project (3 minutes)

1. Open Terminal/Command Prompt
2. Navigate to your project folder:
```bash
cd /Users/joshua/nyct-no-writer-mvp
```

3. Login to Supabase:
```bash
supabase login
```
(This will open your browser - click "Generate token" and paste it back)

4. Link to your Supabase project:
```bash
supabase link --project-ref [your-project-id]
```

To find your project ID:
- Go to https://app.supabase.com
- Click your project
- Go to Settings → General
- Copy the "Reference ID" (looks like: `abcdefghijklmnop`)

---

## Step 3: Deploy the Functions (3 minutes)

1. In Terminal, make sure you're in the project folder:
```bash
cd /Users/joshua/nyct-no-writer-mvp
```

2. Deploy the analyze function:
```bash
supabase functions deploy analyze-proposal
```

3. Deploy the generate function:
```bash
supabase functions deploy generate-decline
```

---

## Step 4: Add Your OpenAI API Key (2 minutes)

1. In Terminal, run:
```bash
supabase secrets set OPENAI_API_KEY="sk-your-actual-openai-key-here"
```

Replace `sk-your-actual-openai-key-here` with your real OpenAI API key.

---

## Step 5: Get Your Function URLs (1 minute)

1. Go to https://app.supabase.com
2. Click your project
3. Click "Edge Functions" in the left menu
4. You'll see your two functions listed
5. Click on each function to see its URL

Your URLs will look like:
- `https://abcdefghijklmnop.supabase.co/functions/v1/analyze-proposal`
- `https://abcdefghijklmnop.supabase.co/functions/v1/generate-decline`

**Save these URLs - you'll need them next!**

---

## Step 6: Update Your Frontend Code (2 minutes)

1. Open the file: `/Users/joshua/nyct-no-writer-mvp/frontend/src/App.tsx`
2. Find line 50 (approximately) that says:
```javascript
const response = await fetch(`${API_URL}/analyze`, {
```

3. Replace it with:
```javascript
const response = await fetch('YOUR-ANALYZE-FUNCTION-URL', {
```

4. Find line 169 (approximately) in the same file
5. Look for the generate function call and update similarly

6. Save the file

---

## Step 7: Deploy to Netlify (2 minutes)

1. In Terminal, run:
```bash
cd /Users/joshua/nyct-no-writer-mvp
git add .
git commit -m "Connect Supabase Edge Functions"
git push
```

2. Go to https://app.netlify.com
3. Your site will automatically redeploy

---

## Step 8: Test It! 🎉

1. Wait 2-3 minutes for deployment
2. Go to https://nyct-no-writer-mvp.netlify.app
3. Upload a PDF proposal
4. You should see:
   - Real text extraction
   - AI-powered analysis
   - Intelligent memo generation

---

## 🔧 Troubleshooting

### "Unauthorized" Error
- Check your OpenAI API key is correct
- Make sure you included the `sk-` part
- Try setting the secret again

### Functions Not Found
- Make sure you deployed both functions
- Check the URLs are exactly correct
- Look for typos in the function names

### Still Getting Mock Data
- Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check the browser console for errors (F12 → Console tab)
- Make sure you saved the App.tsx file after editing

---

## 📊 Checking Your Usage

### OpenAI Usage:
- Go to https://platform.openai.com/usage
- You'll see how much you've used

### Supabase Usage:
- Go to your Supabase dashboard
- Click "Edge Functions" → "Logs"
- You can see all function calls

---

## 💰 Costs

- **Supabase Edge Functions**: FREE (2 million requests/month)
- **OpenAI API**: 
  - ~$0.01 per proposal analyzed
  - ~$0.01 per memo generated
  - Total: ~$0.02 per complete workflow

Example: Processing 100 proposals per month = ~$2

---

## ✅ Final Checklist

- [ ] Installed Supabase CLI
- [ ] Linked to your Supabase project
- [ ] Deployed both Edge Functions
- [ ] Added OpenAI API key as secret
- [ ] Updated frontend with function URLs
- [ ] Pushed changes to GitHub
- [ ] Site redeployed on Netlify
- [ ] Tested with a real document

---

## 🎯 Quick Test

Once everything is set up, try this:
1. Upload any PDF with text
2. You should see extracted information within 5 seconds
3. Add a decline reason
4. Click generate
5. You should get a professional memo in 3-5 seconds

If this works, you're all set! 🎉

---

## Need Help?

If something doesn't work:
1. Check the Supabase Function logs:
   - Go to Supabase dashboard
   - Click "Edge Functions"
   - Click "Logs"
   - Look for error messages

2. Check browser console:
   - Press F12 in your browser
   - Click "Console" tab
   - Look for red error messages

Common issues are usually:
- Typo in the API key
- Wrong function URL
- Forgot to deploy functions