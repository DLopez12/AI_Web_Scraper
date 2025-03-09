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

def solve_captcha_with_ai(image):
    """Uses Ollama AI to solve CAPTCHA from an image."""
    prompt = "What text do you see in this CAPTCHA image?"
    
    response = model.invoke({"image": image, "prompt": prompt})
    
    if response:
        print(f"CAPTCHA Solved: {response}")
        return response.strip()
    
    return None  # Return None if AI couldn't solve it

async def parse_chunk(prompt, chunk, parse_description, i):
    # Format the input using the prompt template
    formatted_input = prompt.format(dom_content=chunk, parse_description=parse_description)
    
    # Invoke the model with the formatted input
    response = await model.ainvoke(formatted_input)
    
    print(f"Parsed batch {i}")
    return response

async def parse_with_ollama(dom_chunks, parse_description):
    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create tasks for each chunk
    tasks = [parse_chunk(prompt, chunk, parse_description, i) for i, chunk in enumerate(dom_chunks, start=1)]
    
    # Gather results from all tasks
    parsed_results = await asyncio.gather(*tasks)
    
    # Join the results into a single string
    return "\n".join(parsed_results)