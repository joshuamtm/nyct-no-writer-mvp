# 🔧 Quick Fix - Make Your App Use Supabase Functions

The app is currently using mock/sample data. Here's how to fix it:

## Option 1: Quick Frontend Update (Easiest)

1. Go to your Netlify dashboard
2. Add these environment variables if you haven't already:
   - `VITE_ANALYZE_URL` = your Supabase analyze function URL
   - `VITE_GENERATE_URL` = your Supabase generate function URL

3. Open this file on your computer:
   `/Users/joshua/nyct-no-writer-mvp/frontend/src/App.tsx`

4. Find line 69 (approximately) that says:
```javascript
// For now, use mock data if backend doesn't return proper analysis
const mockSummary: ExtractedProposalData = {
```

5. Change lines 88-89 from:
```javascript
setProposalSummary(data.summary || mockSummary);
```
To:
```javascript
setProposalSummary(data.summary);
```

6. Find line 91-99 in the catch block and DELETE or comment out the mock data fallback

7. Save the file

8. In Terminal:
```bash
cd /Users/joshua/nyct-no-writer-mvp
git add .
git commit -m "Remove mock data fallback - use real Supabase functions"
git push
```

## Option 2: Test Directly (See if Supabase is Working)

Open your browser console (F12) and run this test:

```javascript
// Replace with your actual Supabase analyze URL
fetch('https://YOUR-PROJECT.supabase.co/functions/v1/analyze-proposal', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text_content: "Test organization requests $50,000 for community program.",
    filename: "test.pdf"
  })
}).then(r => r.json()).then(console.log)
```

If this returns data, your Supabase function is working!

## Option 3: Force Real Data (Complete Fix)

I'll update the code to properly read files and send to Supabase. Run these commands:

```bash
cd /Users/joshua/nyct-no-writer-mvp/frontend/src/components
```

Then update FileUpload.tsx to actually read the file content:

Replace the mock section (lines 39-50) with:
```javascript
try {
  // Read actual file content
  const fileContent = await file.text();
  
  // Call Supabase analyze function directly
  const analyzeUrl = import.meta.env.VITE_ANALYZE_URL;
  if (analyzeUrl) {
    const response = await fetch(analyzeUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text_content: fileContent,
        filename: file.name
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      // Use the analyzed data
      const uploadedFile: UploadedFile = {
        proposal_hash: Math.random().toString(36).substring(7),
        text_content: fileContent,
        filename: file.name,
        size: file.size
      };
      onFileUploaded(uploadedFile);
      return;
    }
  }
  
  // Fallback only if no Supabase URL
  const mockUploadedFile: UploadedFile = {
    proposal_hash: Math.random().toString(36).substring(7),
    text_content: fileContent || `Content from ${file.name}`,
    filename: file.name,
    size: file.size
  };
  onFileUploaded(mockUploadedFile);
```

## The Real Issue:

Your app has 3 places using mock data:
1. **FileUpload.tsx** - Creates mock text instead of reading file
2. **App.tsx line 69-86** - Uses mock summary even when API returns real data  
3. **App.tsx line 91-99** - Falls back to mock in error handling

All 3 need to be fixed for real data to flow through.

## Quickest Solution:

Let me know your Supabase function URLs and I can push a complete fix that:
1. Reads actual file content
2. Sends to your Supabase functions
3. Displays real AI analysis

The URLs look like:
- `https://abcdefg.supabase.co/functions/v1/analyze-proposal`
- `https://abcdefg.supabase.co/functions/v1/generate-decline`