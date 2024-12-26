import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

headers ={ 
   "authorization": st.secrets["groq_api_key"]
}

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Email Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-46057")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load data from the URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Process the portfolio
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            # Generate emails
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job.get('description', ''), links)
                st.markdown(f"### Generated Email for Job: {job.get('role', 'Unknown')}")
                st.code(email, language='markdown')

        except Exception as e:
            # Handle errors gracefully and provide feedback in Streamlit
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
