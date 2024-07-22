from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAI

api_key = 'AIzaSyAemuKyW8j93M2OyoZK7A_voHoThxSxprU'
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)


def checking(uploaded_file,job):

    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        
        
        resume=text

        prompt=f"""check strictly whether the given details: {job} \n matches with the following resume or not {resume} in 50 words """
        if (len(text)==0):
            string="Upload a valid file"
            return string
        else:
            result=llm.invoke(prompt)
            return result
        