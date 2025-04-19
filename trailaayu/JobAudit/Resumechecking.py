from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
# from langchain.llms import GooglePalm
# from langchain_google_genai import GoogleGenerativeAI
import re

# api_key = 'AIzaSyAemuKyW8j93M2OyoZK7A_voHoThxSxprU'
# api_key="AIzaSyDN6NgNARrwBROwynH2j7qRh5XtWnJJuZw"
# llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)
# from langchain_community.llms import Ollama
# llm=Ollama(model="llama3")
from google import genai

client = genai.Client(api_key="AIzaSyDfr-6fEAouStvTRk6iEao9kwdKrU6GkPk")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)


def refined(text):
    text=text.lower()
    text=text.replace("\n","")
    text=re.sub(' +', ' ', text)
    text=re.findall(r'(?:skills|skill)([\s\S]*)', text)

    print(text)
    if(len(text)!=0):
        return text[0]
    return ""
    # text=text[0]
    # return text
    

    # return ""
    # text=text[0]
    # return text

def checking(uploaded_file,job,option):

    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        text= re.sub(r'\s*(?=@)|(?<=@)\s*', '', text)
        pattern='[a-zA-Z0-9|_.]+@[a-z|\s]+.[a-z]+'
        prompt=""
        email=re.findall(pattern,text,flags=re.IGNORECASE)

        if email:
            email=email[0]
        else:
            email=None
        # email1=email1[0]
        print("hi" ,email)
        
        resume=refined(text)
        if option=="emails":
            prompt=f"""check strictly whether the given details: {job} \n matches with the following resume or not {resume}  if yes then just say yes"""
        else:
            prompt=f"""check strictly whether the given details: {job} \n matches with the following resume or not {resume} if yes then just say yes"""
        if (len(text)==0):
            return "none"
        else:
            result = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            result=result.text
            # result=llm.invoke(prompt)
            # print(".......................///.",type(result),"......................................")

            if (re.search(r'\byes\b', result,flags=re.IGNORECASE)):
                return email
            else:
                return None

            # return result
        