from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
import dotenv

dotenv.load_dotenv()

def create_report_from_blog():
    _template = """Given the following blog posts about what was done each day in an internship program, create a general internship report with three main sections: activities executed, methodologies applied and conclusion. No need for timestamps.

    Blog posts:
    {blog_posts}
    Internship report:"""
    prompt = PromptTemplate.from_template(_template)

    with open("blog_posts.pkl", "r") as f:
        blog_posts = f.read()

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    response = llm_chain.run(blog_posts)
    return response

def create_report_from_reports():
    _template = """Given the following reports from an internship program, create a general report with three main sections: activities executed, methodologies applied and conclusion.

    Reports:
    {reports}
    General report:"""
    prompt = PromptTemplate.from_template(_template)

    with open("reports.pkl", "r") as f:
        vectorstore = f.read()

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    response = llm_chain.run(vectorstore)
    return response

def save_report(response):
    with open("report.md", "w") as r:
        r.write(response)
