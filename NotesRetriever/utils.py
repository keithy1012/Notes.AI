import os 
import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TEMP = 0.3

def match_directory(input, base_path="../notes"):
    directories_list = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            full_path = os.path.join(root, d)
            rel_path = os.path.relpath(full_path, base_path)
            directories_list.append(f"../notes/{rel_path.replace(os.sep, '/')}/")
    
    directories = "\n".join(sorted(directories_list)) if directories_list else "(No existing subdirectories)"
    

    prompt = f"""
    Given the following user request for a subdirectory retrieval, decide which subdirectory to retrieve. If there are no appropriate subdirectories, return a message saying that there is no relevant subdirectory notes.

    User Request:
    {input}

    Current Notes Directory:
    {directories}

    Your answer should be a valid path under 'notes/', like:
        ../notes/Math/Calculus/
        ../notes/Biology/Botany/
        ../notes/CS/Machine_Learning/
    Respond with only the valid subdirectory file path and nothing else. If there is no relevant subdirectory, return "N/A".
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're an intelligent file retriever. Based on the user request, return the most relevant existing subdirectory under the base ../notes/ folder."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMP,
    )
    path = response.choices[0].message.content.strip()
    return path