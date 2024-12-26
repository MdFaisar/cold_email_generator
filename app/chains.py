import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
# For streamlit secret key
groq_api_key = os.environ["groq_api_key"]

headers ={ 
   "authorization": st.secrets["groq_api_key"]
}

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("groq_api_key"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_jobs(self, page_data):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your job is to extract the job postings and return them in JSON format containing
            the following keys: "role", "experience", "skills", and "description".
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': page_data})

        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
            return json_res if isinstance(json_res, list) else [json_res]
        except OutputParserException:
            raise OutputParserException("Content too big. Unable to parse jobs.")

    def write_mail(self, job_description, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Faisar, a software developer at Zoho. Zoho is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools.
            Over my experience, I have empowered numerous enterprises with tailored solutions, fostering scalability,
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of zoho 
            in fulfilling their needs. First start by saying or introducing my name(Faisar) note: I am a AI software Engineer
            Also, add the most relevant ones from the following links to showcase Zoho portfolio: {link_list}
            Remember you are Zoho, BDE at Zoho.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job_description), "link_list": links})
        return res.content
