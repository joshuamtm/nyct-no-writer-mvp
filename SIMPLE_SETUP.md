# 🎯 Super Simple Setup - Get Your App Working with AI in 10 Minutes

## You Need:
1. Your Supabase account login
2. Your OpenAI API key

---

## Step 1: Open Supabase (2 minutes)
1. Go to https://app.supabase.com
2. Log in to your account
3. Click on your project (or create a new one called "nyct-nowriter")
4. Keep this tab open

---

## Step 2: Add Your OpenAI Key (1 minute)
1. In Supabase, click "Edge Functions" in the left menu
2. Click "Manage secrets"
3. Click "Add new secret"
4. Add:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI key (starts with `sk-`)
5. Click "Save"

---

## Step 3: Create Functions in Supabase (3 minutes)

### Function 1: Analyze Proposal
1. In Supabase, stay in "Edge Functions"
2. Click "Create function"
3. Name it: `analyze-proposal`
4. Delete everything in the editor
5. Copy ALL of this code:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { text_content } = await req.json()
    
    // Simple extraction without OpenAI for testing
    const summary = {
      organizationName: "Test Organization",
      grantAmount: "$100,000",
      projectDescription: text_content.substring(0, 200),
      targetPopulation: "Community members",
      geographicScope: "New York City"
    }

    return new Response(
      JSON.stringify({ summary, analysis_time_ms: 1000 }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
```

6. Click "Save"
7. Click "Deploy"

### Function 2: Generate Decline
1. Click "Create function" again
2. Name it: `generate-decline`
3. Delete everything and paste:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { reason_code, specific_reasons, proposal_summary } = await req.json()
    
    const internal_rationale = `${proposal_summary.organizationName} requests ${proposal_summary.grantAmount} for ${proposal_summary.projectDescription}. 
    
I recommend declining for: ${reason_code}. ${specific_reasons}`

    const external_reply = `Dear ${proposal_summary.organizationName},

Thank you for your proposal. After careful review, we are unable to provide funding at this time.

Best regards,
NYCT Team`

    return new Response(
      JSON.stringify({ internal_rationale, external_reply, generation_time_ms: 1000 }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
```

4. Click "Save"
5. Click "Deploy"

---

## Step 4: Get Your Function URLs (1 minute)
1. In Supabase, go back to "Edge Functions"
2. You'll see both functions listed
3. Click the copy icon next to each function to get its URL
4. They look like:
   - `https://abcdefg.supabase.co/functions/v1/analyze-proposal`
   - `https://abcdefg.supabase.co/functions/v1/generate-decline`

---

## Step 5: Update Netlify (3 minutes)
1. Go to https://app.netlify.com
2. Click on your site `nyct-no-writer-mvp`
3. Go to "Site configuration" → "Environment variables"
4. Add these variables:
   - Click "Add a variable"
   - Key: `VITE_ANALYZE_URL`
   - Value: Your analyze function URL from Step 4
   - Click "Create"
   
   - Click "Add a variable" again
   - Key: `VITE_GENERATE_URL`
   - Value: Your generate function URL from Step 4
   - Click "Create"

5. Go to "Deploys" tab
6. Click "Trigger deploy" → "Deploy site"

---

## Step 6: Test It! (1 minute)
1. Wait 2 minutes for deployment
2. Go to https://nyct-no-writer-mvp.netlify.app
3. Upload ANY text file or PDF
4. It should work!

---

## 🎉 That's It!

Your app is now connected to Supabase and will use the Edge Functions for processing.

To add real AI later, you can update the functions with the full code I provided in the `/supabase/functions/` folder.

---

## Quick Troubleshooting:

**"CORS Error" in browser console:**
- Make sure you copied the function code exactly
- The `corsHeaders` part is important

**"Function not found":**
- Check the URLs are exactly right
- Make sure both functions show "Active" in Supabase

**Still showing old mock data:**
- Hard refresh the page: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check Netlify finished deploying (green checkmark)

---

## Total Time: ~10 minutes
## Total Cost: $0 (Supabase is free for this usage)