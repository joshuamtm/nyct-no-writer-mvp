import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import OpenAI from "https://deno.land/x/openai@v4.24.0/mod.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

const reasonDescriptions = {
  "project_capability": "Project Capability Problems",
  "general_operating": "General Operating Support",
  "higher_merit": "Other Projects Higher Merit",
  "outside_guidelines": "Outside Approved Guidelines",
  "incomplete_proposal": "Incomplete Proposal",
  "geographic_scope": "Geographic Scope Limitation",
  "strategic_mismatch": "Strategic Priority Mismatch",
  "sustainability": "Sustainability Concerns"
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { reason_code, specific_reasons, proposal_summary } = await req.json()
    
    // Initialize OpenAI
    const openai = new OpenAI({
      apiKey: Deno.env.get('OPENAI_API_KEY'),
    })

    // Generate NYCT-formatted internal memo
    const memoPrompt = `
    Write a concise internal memo for The New York Community Trust board in EXACTLY this format:
    
    [Organization name], founded in [year], [mission/description]. This [grant amount] request is to support [project description]. [Add 1-2 relevant details about scope, budget, or population served].
    
    I recommend this request be declined for ${reasonDescriptions[reason_code]?.toLowerCase() || 'the specified reason'}. ${specific_reasons}
    
    Rationale: ${reasonDescriptions[reason_code] || 'Decline Reason'}
    
    Requirements:
    - Total length: 150-200 words
    - Factual, objective tone
    - No subjective assessments
    - Include specific grant amount
    - Clear decline reason
    
    Proposal Summary:
    ${JSON.stringify(proposal_summary, null, 2)}
    `

    const memoCompletion = await openai.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content: "You are a grant officer writing internal memos for a foundation board. Be concise and factual."
        },
        {
          role: "user",
          content: memoPrompt
        }
      ],
      temperature: 0.3,
      max_tokens: 300
    })

    const internalMemo = memoCompletion.choices[0].message.content

    // Generate external letter
    const letterPrompt = `
    Write a professional, empathetic decline letter for a grant application from ${proposal_summary.organizationName || 'the organization'}.
    
    Requirements:
    - Professional and respectful tone
    - Thank them for their application
    - Acknowledge their important work
    - Indicate the decision without specific reasons
    - Encourage future applications
    - Keep it concise (150-200 words)
    
    Do not mention specific decline reasons or internal rationale.
    `

    const letterCompletion = await openai.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content: "You are writing on behalf of The New York Community Trust. Be professional and empathetic."
        },
        {
          role: "user",
          content: letterPrompt
        }
      ],
      temperature: 0.4,
      max_tokens: 300
    })

    const externalLetter = letterCompletion.choices[0].message.content

    return new Response(
      JSON.stringify({
        internal_rationale: internalMemo,
        external_reply: externalLetter,
        generation_time_ms: 3000
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    )
  } catch (error) {
    console.error('Error:', error)
    
    // Fallback to template
    const { proposal_summary, reason_code, specific_reasons } = await req.json()
    
    const fallbackMemo = `${proposal_summary.organizationName || 'The organization'} requests ${proposal_summary.grantAmount || 'funding'} to support ${proposal_summary.projectDescription || 'their project'}.

I recommend this request be declined for ${reasonDescriptions[reason_code]?.toLowerCase() || 'the specified reason'}. ${specific_reasons}

Rationale: ${reasonDescriptions[reason_code] || 'Decline Reason'}`

    const fallbackLetter = `Dear ${proposal_summary.organizationName || 'Applicant'},

Thank you for your proposal submission to The New York Community Trust. We appreciate your organization's dedication to serving the community.

After careful review, we have determined that we will not be able to provide funding for this request at this time. While we recognize your important work, this proposal does not align with our current funding priorities.

We encourage you to review our updated guidelines and consider applying for future opportunities.

Best regards,
NYCT Program Team`

    return new Response(
      JSON.stringify({
        internal_rationale: fallbackMemo,
        external_reply: fallbackLetter,
        generation_time_ms: 1000
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    )
  }
})