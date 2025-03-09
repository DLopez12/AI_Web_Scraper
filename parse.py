import asyncio
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


model = OllamaLLM(model="llama3.1")

async def parse_chunk(chain, chunk, parse_description, i): # Parse the chunk of content
    response = await chain.ainvoke({"dom_content": chunk, "parse_description": parse_description}) # await the response from the chain
    print(f"Parsed batch {i}") # Print the batch number
    return response # Return the response
                  
async def parse_with_ollama(dom_chunks, parse_description): # Parse the content using Ollama
    prompt = ChatPromptTemplate.from_template(template)  # Create a prompt using the template
    chain = prompt | model  # Chain the prompt and the model

    tasks = [parse_chunk(chain, chunk, parse_description, i) for i, chunk in enumerate(dom_chunks, start=1)] # Create a list of tasks
    parsed_results = await asyncio.gather(*tasks)  # Gather the results from the tasks

    return "\n".join(parsed_results) # Return the parsed results as a single string