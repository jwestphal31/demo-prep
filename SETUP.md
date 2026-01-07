# Setup Guide for Web Search Integration

The Demo Prep Tool uses Google Custom Search API to gather comprehensive company information. Follow these steps to enable web search functionality.

## Prerequisites

- Google Cloud account (free tier available)
- Python 3.7+ installed

## Step 1: Set Up Google Custom Search API

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing (required for API access, but free tier is generous)

### 1.2 Enable Custom Search API

1. In the Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Custom Search API"
3. Click on it and press **Enable**

### 1.3 Create API Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **API Key**
3. Copy the API key (you'll need this for `GOOGLE_API_KEY`)
4. (Recommended) Click **Restrict Key** and limit it to Custom Search API only

## Step 2: Create a Custom Search Engine

### 2.1 Set Up Search Engine

1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click **Add** or **Get Started**
3. Configure your search engine:
   - **Sites to search**: Select "Search the entire web"
   - **Name**: "Demo Prep Research" (or any name)
   - **Language**: English (or your preference)
4. Click **Create**

### 2.2 Get Search Engine ID

1. In the Programmable Search Engine console, click on your search engine
2. In the **Overview** section, you'll see **Search engine ID**
3. Copy this ID (you'll need this for `GOOGLE_SEARCH_ENGINE_ID`)

### 2.3 Configure Search Settings (Optional)

1. Go to **Edit search engine** > **Setup**
2. Enable **Search the entire web**: ON
3. Enable **Image search**: OFF (not needed)
4. Save changes

## Step 3: Configure Environment Variables

### Option 1: Using .env file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_actual_search_engine_id_here
   ```

3. Install python-dotenv (if not already installed):
   ```bash
   pip3 install python-dotenv
   ```

4. Load environment variables before running:
   ```bash
   export $(cat .env | xargs) && python3 demo_prep.py example.com
   ```

### Option 2: Export directly (Quick Test)

```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"

python3 demo_prep.py example.com
```

### Option 3: Add to shell profile (Permanent)

Add to `~/.bashrc`, `~/.zshrc`, or similar:

```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"
```

Then reload: `source ~/.bashrc` (or `~/.zshrc`)

## Step 4: Verify Setup

Test the tool with a company:

```bash
python3 demo_prep.py anthropic.com
```

You should see:
- ✓ Web search enabled
- ✓ Found LinkedIn, Crunchbase, tech stack, security tools

If you see warnings about missing credentials, double-check your environment variables.

## API Usage & Costs

### Google Custom Search API Limits

- **Free tier**: 100 queries per day
- **Paid**: $5 per 1,000 additional queries
- Each company research uses approximately 15-20 queries

### Optimizing API Usage

- The tool is designed to make targeted searches
- Results are not cached by default (implement caching if needed)
- Consider batching research for multiple companies

## Troubleshooting

### "Web search disabled" message

- Verify environment variables are set: `echo $GOOGLE_API_KEY`
- Check that variables are exported before running the script
- Ensure no extra spaces or quotes in the values

### "Search error: 403"

- API key might be restricted - check API key restrictions in Cloud Console
- Make sure Custom Search API is enabled
- Verify billing is enabled on your Google Cloud project

### "Search error: 429" (Rate Limit)

- You've hit the daily quota (100 free searches)
- Wait 24 hours or upgrade to paid tier
- Consider implementing caching to reduce API calls

### No results found

- Search engine might not be configured to search entire web
- Try different company names or domains
- Check that Search Engine ID is correct

## Security Best Practices

1. **Never commit API keys to git**
   - `.env` is in `.gitignore`
   - Use environment variables or secret management

2. **Restrict API key**
   - Limit to Custom Search API only
   - Add application restrictions if possible

3. **Monitor usage**
   - Check Cloud Console regularly for unexpected usage
   - Set up billing alerts

## Next Steps

Once web search is configured, you can:

1. Research multiple companies efficiently
2. Export results to markdown
3. (Coming soon) Export to Google Docs
4. (Coming soon) Integrate with local battle card knowledge base

## Support

If you encounter issues:
1. Check the [Google Custom Search API docs](https://developers.google.com/custom-search/v1/overview)
2. Verify your Cloud Console configuration
3. Open an issue in the project repository
