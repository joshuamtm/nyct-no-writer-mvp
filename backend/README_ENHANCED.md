# NYCT No-Writer Enhanced Backend

## Overview
This enhanced version of the NYCT No-Writer backend includes:
- ✅ Real PDF/Word text extraction
- ✅ OpenAI/Anthropic AI integration
- ✅ Intelligent proposal analysis
- ✅ AI-powered memo generation
- ✅ Database metrics tracking
- ✅ Production-ready error handling

## Quick Start

### 1. Run Setup Script
```bash
cd backend
./setup_enhanced.sh
```

### 2. Configure API Keys
Edit `.env` file with your API keys:
```env
# Choose one AI provider
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Set provider (openai or anthropic)
LLM_PROVIDER=openai
```

### 3. Run Enhanced Backend
```bash
source venv/bin/activate
python main_enhanced.py
```

## Features Comparison

| Feature | Original (main.py) | Enhanced (main_enhanced.py) |
|---------|-------------------|---------------------------|
| PDF Text Extraction | Mock | ✅ Real (pypdf + pdfplumber) |
| Word Doc Extraction | Mock | ✅ Real (python-docx) |
| Proposal Analysis | Mock | ✅ AI-powered extraction |
| Memo Generation | Template | ✅ AI-generated (GPT-4/Claude) |
| Metrics Tracking | Hardcoded | ✅ Database (SQLite/PostgreSQL) |
| Error Handling | Basic | ✅ Comprehensive with fallbacks |

## API Endpoints

### 1. Upload Document
```bash
POST /upload
```
- Accepts PDF and Word documents
- Extracts text using multiple methods
- Returns cleaned, structured text

### 2. Analyze Proposal
```bash
POST /analyze
```
- AI extracts 15+ key elements:
  - Organization details
  - Grant amount
  - Project description
  - Target population
  - Budget information
  - Timeline & deliverables
  - And more...

### 3. Generate Decline
```bash
POST /generate
```
- Generates NYCT-formatted internal memo (150-200 words)
- Creates professional external letter
- Uses AI for context-aware content

### 4. Get Metrics
```bash
GET /metrics?days=30
```
- Real-time usage statistics
- Daily activity tracking
- Error monitoring
- Performance metrics

## Configuration Options

### Environment Variables
```env
# AI Configuration
LLM_PROVIDER=openai              # or anthropic
OPENAI_MODEL=gpt-4-turbo-preview # or gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-opus-20240229

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# CORS Settings
CORS_ORIGINS=http://localhost:5173,https://your-domain.com

# Feature Flags
ENABLE_METRICS=True
DEBUG=True
```

### Using Different AI Models

#### OpenAI Models
- `gpt-4-turbo-preview` - Best quality, slower
- `gpt-3.5-turbo` - Faster, lower cost
- `gpt-4` - Standard GPT-4

#### Anthropic Models
- `claude-3-opus-20240229` - Best quality
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fastest

## Testing the Enhanced Features

### Test Text Extraction
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@test-proposal.pdf"
```

### Test AI Analysis
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "proposal_hash": "abc123",
    "text_content": "Full proposal text here...",
    "filename": "test.pdf"
  }'
```

### Test Memo Generation
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "reason_code": "project_capability",
    "specific_reasons": "Lacks clear implementation plan",
    "proposal_summary": {
      "organizationName": "Test Org",
      "grantAmount": "$100,000",
      "projectDescription": "Community program"
    }
  }'
```

## Database Setup (Optional)

### SQLite (Default)
No setup needed - automatically created as `metrics.db`

### PostgreSQL
1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE nyct_nowriter;
```
3. Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/nyct_nowriter
```

## Deployment Considerations

### For Production
1. **API Keys Security**: Use environment variables, never commit keys
2. **Database**: Switch from SQLite to PostgreSQL
3. **Rate Limiting**: Implement API rate limits
4. **Authentication**: Add user authentication
5. **Monitoring**: Set up error tracking (Sentry, etc.)
6. **Caching**: Add Redis for response caching

### Azure Deployment
```bash
# Build container
docker build -t nyct-backend .

# Deploy to Azure Container Instances
az container create \
  --resource-group nyct-rg \
  --name nyct-backend \
  --image nyct-backend \
  --ports 8000 \
  --environment-variables \
    OPENAI_API_KEY=$OPENAI_API_KEY \
    DATABASE_URL=$DATABASE_URL
```

## Troubleshooting

### No API Keys Error
- The app will still run but use template-based generation
- Add keys to `.env` for full AI functionality

### PDF Extraction Issues
- The system tries multiple extraction methods
- Falls back gracefully if one method fails
- Check logs for specific errors

### Database Connection Issues
- Defaults to SQLite if PostgreSQL unavailable
- Check DATABASE_URL format
- Ensure database server is running

### Memory Issues with Large Files
- Files are limited to 10MB
- Text is truncated to 8000 tokens for AI processing
- Consider chunking for larger documents

## Performance Optimization

### Caching Responses
```python
# Add to main_enhanced.py
from functools import lru_cache

@lru_cache(maxsize=100)
async def cached_analysis(text_hash: str):
    # Cache frequent analyses
    pass
```

### Async Processing
All operations are async-ready for better performance under load.

### Token Optimization
- Text is intelligently truncated to stay within token limits
- Uses tiktoken for accurate token counting

## Support

For issues or questions:
1. Check logs: `tail -f backend.log`
2. Enable debug mode: `DEBUG=True` in `.env`
3. Review error metrics: `GET /metrics`

## Next Steps

1. **Add Authentication**: Implement Azure AD integration
2. **Enhanced Metrics**: Add Grafana dashboard
3. **Batch Processing**: Support multiple file uploads
4. **Export Formats**: Add PDF/Word export for memos
5. **Template Management**: Allow custom memo templates