import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

class Chains:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key =groq_api_key, model_name = "llama-3.1-70b-versatile")
    
    def get_job_detail(self,page_data):
        try:
            prompt_extract = PromptTemplate.from_template(
                    """
                    ### SCRAPED TEXT FROM WEBSITE:
                    {page_data}
                    ### INSTRUCTION:
                    The scraped text is from the career's page of a website.
                    Your job is to extract the job postings and return them in JSON format containing the 
                    following keys: `role`, `experience`, `skills` and `description`.
                    Only return the valid JSON.
                    ### VALID JSON (NO PREAMBLE):    
                    """
            )
            parser = JsonOutputParser()
            chain_extract = prompt_extract | self.llm | parser
            job_deatil = chain_extract.invoke(input={'page_data':page_data})
            
            return job_deatil
        
        except Exception as e:
            print(e)
            
    def get_email(self,job_detail,cv):
        try:
            prompt = PromptTemplate.from_template(
                        """
                        ### JOB DESCRIPTION:
                        {job_description}

                        ### CLIENT PORTFOLIO:
                        {client_cv}

                        ### INSTRUCTION:
                        - Craft a professional email tailored to the job description and the client's portfolio.
                        - Highlight the client's most relevant skills, experiences, and achievements for the role.
                        - Use a formal and engaging tone.
                        - Structure the email as follows:
                            1. Opening: Address the recipient and express enthusiasm for the role.
                            2. Body: Connect the client's qualifications to the job description.
                            3. Closing: Reiterate interest and include a call-to-action for further discussion.
                        - End the email with the client's contact information (name, mobile number, LinkedIn link, and GitHub link).
                        - Avoid providing a preamble; directly begin with the email content.

                        ### EMAIL (NO PREAMBLE):
                        """
                        )

            chain_email = prompt | self.llm
            email = chain_email.invoke({"job_description":str(job_detail),"client_cv":cv})
            
            return email.content
        
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))