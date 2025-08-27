# 🔑 API Key Configuration Guide for Insight Foundry

## Overview
Your Insight Foundry platform supports both OpenAI and Anthropic APIs with built-in configuration management, connection testing, and automatic fallback between providers.

## Step 1: Get Your OpenAI API Key 🤖

### 1.1 Create OpenAI Account
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** in the sidebar

### 1.2 Generate API Key
1. Click **"Create new secret key"**
2. Give it a descriptive name like "Insight Foundry Research"
3. **IMPORTANT**: Copy the key immediately - you won't see it again!
4. The key format looks like: `sk-proj-...` (starts with sk-proj or sk-)

### 1.3 Add Credits
1. Go to **Billing** → **Payment methods**
2. Add a payment method
3. Add at least $5-10 in credits for testing
4. Set up usage limits to control costs

**Cost Estimate**: GPT-4o-mini costs ~$0.15 per 1M input tokens, so analyzing research papers will cost just a few cents each.

---

## Step 2: Get Your Anthropic API Key 🧠

### 2.1 Create Anthropic Account
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to **API Keys**

### 2.2 Generate API Key
1. Click **"Create Key"**
2. Name it "Insight Foundry Research"
3. Copy the key immediately - format: `sk-ant-api03-...`

### 2.3 Add Credits
1. Go to **Billing** and add credits
2. Claude 3 Haiku is very cost-effective (~$0.25 per 1M input tokens)
3. Start with $10-20 for extensive testing

---

## Step 3: Configure Keys in Your Platform ⚙️

### 3.1 Access API Configuration
Your platform has a built-in API configuration interface:

1. **Log in** to your Insight Foundry platform
2. Click the **user avatar** in the top-right corner
3. Select **"API Configuration"** from the dropdown menu
4. Or look for a **Settings/Gear icon** in the interface

### 3.2 Enter Your Keys
In the API Configuration dialog:

```
┌─ API Configuration ─────────────────┐
│                                     │
│ OpenAI Configuration                │
│ ├─ API Key: [sk-proj-your-key...]   │
│ ├─ Model: gpt-4o-mini (recommended) │
│ └─ Test Connection [✓]              │
│                                     │
│ Anthropic Configuration             │
│ ├─ API Key: [sk-ant-api03-your...]  │
│ ├─ Model: claude-3-haiku-20240307   │
│ └─ Test Connection [✓]              │
│                                     │
│ Provider Priority                   │
│ ├─ Primary: OpenAI                  │
│ └─ Fallback: Anthropic              │
│                                     │
│ [Save Configuration]                │
└─────────────────────────────────────┘
```

### 3.3 Test Your Connections
1. After entering each API key, click **"Test Connection"**
2. You should see green checkmarks ✅ if successful
3. If you see errors, double-check your keys and billing

---

## Step 4: Platform Features with Your Keys 🚀

Once configured, you can use:

### 4.1 Document Analysis
- Upload PDF research papers
- Get AI-powered summaries with evidence levels
- Extract key findings and clinical implications
- Statistical significance analysis

### 4.2 AI Chat Assistant
- Ask questions about your uploaded papers
- Context-aware responses using your research
- Compare findings across multiple papers
- Get explanations of complex concepts

### 4.3 Slide Generation
- Create presentations from your research
- AI generates structured slides with key points
- Export as PowerPoint or PDF
- Professional formatting with citations

### 4.4 Smart Library
- Automatic categorization by medical specialty
- Evidence-level sorting (Level I-V)
- Search across all your papers
- Citation management

---

## Step 5: Cost Management & Best Practices 💰

### 5.1 Built-in Rate Limiting
Your platform includes:
- **20 requests per minute** limit to prevent runaway costs
- **Automatic retries** with exponential backoff
- **Usage warnings** when approaching limits

### 5.2 Cost Optimization Tips
1. **Start with OpenAI** (usually cheaper for most tasks)
2. **Use Anthropic as fallback** (higher quality for complex analysis)
3. **Monitor usage** in your provider dashboards
4. **Set billing alerts** at $10, $25, $50 thresholds

### 5.3 Expected Costs
- **Research Paper Analysis**: $0.10-0.50 per paper
- **Chat Conversations**: $0.05-0.20 per conversation
- **Slide Generation**: $0.20-0.80 per presentation
- **Monthly Usage** (heavy research): $20-50

---

## Step 6: Troubleshooting 🔧

### Common Issues:

**"API Key Invalid"**
- Double-check the key was copied correctly
- Ensure no extra spaces or characters
- Verify the key hasn't expired

**"Insufficient Credits"**
- Add billing method to your provider account
- Purchase credits ($10 minimum recommended)
- Check billing dashboard for current balance

**"Rate Limit Exceeded"**
- Wait 60 seconds and try again
- The platform automatically handles this
- Consider upgrading to higher tier if needed

**"Model Not Available"**
- Stick with recommended models:
  - OpenAI: `gpt-4o-mini`
  - Anthropic: `claude-3-haiku-20240307`

### Getting Help:
1. Check the **API Configuration** dialog for connection status
2. Review error messages in the platform
3. Check provider status pages for outages
4. Verify billing and usage limits

---

## Step 7: Security Best Practices 🔒

### 7.1 API Key Security
- **Never share** your API keys publicly
- **Don't commit** keys to code repositories
- **Rotate keys** every few months
- **Use separate keys** for different projects

### 7.2 Platform Security
- Your keys are stored in **browser localStorage** only
- **No server-side storage** of your credentials
- **Connection testing** is done client-side
- **Automatic key validation** before each request

---

## Ready to Start! 🎉

Once your API keys are configured:

1. **Test the connection** - should see green checkmarks
2. **Upload a research paper** - try a PDF from PubMed
3. **Run AI analysis** - see the magic happen
4. **Chat with your research** - ask questions about findings
5. **Generate slides** - create a presentation

Your Insight Foundry platform is now powered by real AI and ready for serious research work!

---

## Quick Reference 📋

**OpenAI Dashboard**: https://platform.openai.com/usage
**Anthropic Console**: https://console.anthropic.com/
**Your Platform**: https://medresearch-ai-d86c1d5d.scout.site

**Test Credentials**: admin / admin@1234$

**Support Models**:
- OpenAI: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
- Anthropic: claude-3-haiku-20240307, claude-3-sonnet-20240229