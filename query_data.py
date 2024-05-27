from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
import dotenv

dotenv.load_dotenv()

_template = """Given the following blog posts about what was done each day in an internship program, create a general internship report with three main sections: activities executed, methodologies applied and conclusion. No need for timestamps.

Blog posts:
{blog_posts}
Internship report:"""
prompt = PromptTemplate.from_template(_template)

with open("vectorstore.pkl", "r") as f:
    vectorstore = f.read()

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)
llm_chain = LLMChain(llm=llm, prompt=prompt)

response = llm_chain.run(vectorstore)
with open("report.md", "w") as r:
    r.write(response)
