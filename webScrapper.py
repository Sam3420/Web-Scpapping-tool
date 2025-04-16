from bs4 import BeautifulSoup
import requests

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import getpass
import os


if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("GROQ_API_KEY")

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text() for p in paragraphs)
        return text[:3000]  
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def extract_suburls(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = "/".join(url.split("/")[:3])
        anchors = soup.find_all('a', href=True)
        links = []

        excluded_urls = [
            "https://www.myscheme.gov.in/terms-conditions",
        ]

        for a in anchors:
            href = a['href']
            
           
            if href.startswith("http"):
                full_url = href
            elif href.startswith("/"):
                full_url = base_url + href
            else:
                continue  
                
           
            if full_url not in excluded_urls:
                links.append(full_url)

        return list(set(links))[:6]  
    except Exception as e:
        print(f"Error fetching sub-URLs from {url}: {e}")
        return []

# Load LLM (make sure you have your groq api key in the .env file )
llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.environ["GROQ_API_KEY"], 
    model_name="llama3-70b-8192"
)

# Prompt to summarize a page
summarizer_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
You are an AI assistant. From the content provided fetch and format the key takeaways from the content of the webiste:
{content}
NOTE: IGNORE CONTENT OF ADVERITISEMENT AND PRIVACY POLICY OF THE WEBSITE , STRICTLY STICK TO THE INFORMATION useful for the user.
"""
)
summarizer_chain = LLMChain(prompt=summarizer_prompt, llm=llm)

# Prompt to combine and refine multiple summaries
combine_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
You are an ai assistant use the data combined data and format is all :
{content}
NOTE: IGNORE CONTENT OF ADVERITISEMENT AND PRIVACY POLICY OF THE WEBSITE , STRICTLY STICK TO THE INFORMATION useful for the user
"""
)
refiner_chain = LLMChain(prompt=combine_prompt, llm=llm)



def run_scraper_and_summarizer(start_url):
    print(f"\n Scraping: {start_url}")
    main_text = scrape_website(start_url)
    main_summary = summarizer_chain.run({"content": main_text})

    all_summaries = [{"url": start_url, "summary": main_summary}]
    anchor_links = extract_suburls(start_url)

    for link in anchor_links:
        print(f"\n➡️ Following link: {link}")
        page_text = scrape_website(link)
        if page_text:
            summary = summarizer_chain.run({"content": page_text})
            all_summaries.append({"url": link, "summary": summary})

    for i, r in enumerate(all_summaries):
        print(f"\nSummary {i+1} from {r['url']}:\n{r['summary']}")

    combined = "\n\n".join([s["summary"] for s in all_summaries])
    refined_summary = refiner_chain.run({"content": combined})
    

    print("\n Final Refined Summary:\n")
    print(refined_summary)

# Example Usage
if __name__ == "__main__":
    url = input("enter the link of website you want to scrape: ")  
    run_scraper_and_summarizer(url)
