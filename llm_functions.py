from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd


def summary(gmap_id, data, api_key):
    print('here')
    doc = data['gmap_id' == gmap_id]
    print(doc)
    query = doc['name'] + ' ' + doc['doc_information']
    print(query)

    llm = ChatOpenAI(openai_api_key=api_key, temperature=0, model_name="gpt-3.5-turbo-1106")

    prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY: """

    llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))
    summary = llm_chain.run({"text": query})
    print(summary)
    return summary
    

