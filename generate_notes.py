import openai
from dotenv import load_dotenv
import os
import uuid 
import matplotlib as plt
import re
from pathlib import Path
LATEX_INLINE = re.compile(r"\$(.+?)\$")
LATEX_BLOCK = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

class NotesGenerator:
    def __init__(self, notes_chunks = None, user_instruction = ""):
        load_dotenv()
        self.notes = notes_chunks
        self.instruction = user_instruction
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.TEMP = 0.3

    def generate_prompt(self, chunk):
        return f"""
    [User Instruction]: {self.instruction}

    [{chunk['section']} Content]:
    {chunk['content']}

    Please turn this into notes based on the above instructions.
    """

    def generate_note(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert note-taking assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.TEMP,
        )

        return response.choices[0].message.content.strip()

    def process_chunk(self, chunk): 
        prompt = self.generate_prompt(chunk)
        note = self.generate_note(prompt)

        return note
    
    def generate_title(self, note_chunks):
        combined_notes = "\n\n".join(note_chunks)
        prompt = f"""
    Given the following notes generated from a presentation, create a short, informative title (max 10 words) that summarizes what this presentation is about.

    Notes:
    {combined_notes}

    Respond with only the title and nothing else.
    """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise academic summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.TEMP,
        )
        return response.choices[0].message.content.strip()

    def generate_summary(self, note_chunks):
        combined_notes = "\n\n".join(note_chunks)
        prompt = f"""
    Given the following notes generated from a presentation, create a short, informative summary (1-2 sentences) that summarizes what this presentation is about.

    Notes:
    {combined_notes}

    Respond with only the summary sentences and nothing else.
    """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise academic summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.TEMP,
        )
        return response.choices[0].message.content.strip()

    def render_latex_to_image(self, latex_str, out_dir="latex_images"):
        os.makedirs(out_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(out_dir, filename)

        fig, ax = plt.subplots(figsize=(0.01, 0.01))
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=16, ha='center', va='center')
        plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        return filepath
    
    def replace_latex_with_images(self, note, out_dir="latex_images"):
        def repl_inline(match):
            latex = match.group(1)
            img_path = self.render_latex_to_image(latex, out_dir)
            return f"![formula]({img_path})"

        note = LATEX_INLINE.sub(repl_inline, note)
        note = LATEX_BLOCK.sub(repl_inline, note)
        return note

    def generate_directory(self, title, summary, base_path = "notes"):
        directories_list = []
        for root, dirs, _ in os.walk(base_path):
            for d in dirs:
                full_path = os.path.join(root, d)
                rel_path = os.path.relpath(full_path, base_path)
                directories_list.append(f"notes/{rel_path.replace(os.sep, '/')}/")
    
        directories = "\n".join(sorted(directories_list)) if directories_list else "(No existing subdirectories)"
    
        prompt = f"""
    Given the following title and summary generated from a presentation, decide which subdirectory to place this notesheet. If there are no approrpiate subdirectorys, create a new one in the appropriate location.

    Title:
    {title}

    Summary: 
    {summary}

    Current Notes Directory:
    {directories}

    Your answer should be a valid path under 'notes/', like:
        notes/Math/Calculus/
        notes/Biology/Botany/
        notes/CS/Machine_Learning/
    Respond with only the valid subdirectory file path and nothing else.
    """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an intelligent file organizer. Based on the summary and content, suggest a clean subdirectory path under the base Notes/ folder."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.TEMP,
        )
        path = response.choices[0].message.content.strip()
        Path(path).mkdir(parents=True, exist_ok=True)
        return path