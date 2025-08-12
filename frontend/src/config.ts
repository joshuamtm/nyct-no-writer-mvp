// API Configuration

// Option 1: Use environment variables (set in Netlify dashboard)
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const ANALYZE_URL = import.meta.env.VITE_ANALYZE_URL || `${API_URL}/analyze`;
export const GENERATE_URL = import.meta.env.VITE_GENERATE_URL || `${API_URL}/generate`;

// Option 2: Hardcode your Supabase URLs here (replace with your actual URLs)
// export const ANALYZE_URL = 'https://your-project-id.supabase.co/functions/v1/analyze-proposal';
// export const GENERATE_URL = 'https://your-project-id.supabase.co/functions/v1/generate-decline';