# 🌐 Web Scraper & AI Summarizer

A powerful Python tool that scrapes websites, extracts key information, and generates concise AI-powered summaries using Groq's Llama model.

## ✨ Features

- **Intelligent Web Scraping** - Extracts clean text content from web pages
- **Multi-Page Crawling** - Follows and analyzes related sub-pages
- **AI-Powered Summarization** - Uses Groq's Llama3-70b for high-quality summaries
- **Content Refinement** - Combines multiple summaries into cohesive output
- **Privacy Focused** - Local processing with your own API keys

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper-summarizer.git
    
2. Navigate inside the web-scrapper-summarizer folder:
   ```bash
   cd web-scraper-summarizer
    
3.Install the requirements:
  ```bash
   pip install -r requirements.txt
    
4.Create a .env file in the same folder web-scrapper-summarizer using these commands:
  ```bash
     touch .env
    
  -(content of .env file):
    GROQ_API_KEY=your_actual_key_here
    
5.Finally run the webSrcapper.py using :
  ```bash
    python run webScrapper.py
    
6. Enter the desired link of the website and hit "enter"
## 🎉 Hurray! You've Got the Data!

##Limitations:
1.Dynamic Website Content
❌ Doesn't work with: javascript rendered content
2.Anti-Scraping Protections
🛑 May fail when:
-Websites block bots (Cloudflare, Distil Networks)
-Rate-limiting is triggered 
