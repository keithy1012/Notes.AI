import argparse
from generate_notes import NotesGenerator
from Extractor import Extractor
import os
class Generator:
    def __init__(self, file_path, output_path = "notes.md", instruction = "Instructions", latex=False):
        self.file_path = file_path
        self.output_path = output_path
        self.instruction = instruction
        self.latex = latex

    def run(self):
        self.main(self.file_path, self.output_path, self.instruction)

    def main(self, file_path, output_file_name, user_instruction):
        extractor = Extractor(file_path)
        print(f"📂 Extracting content from: {file_path}")
        # Breaks down a powerpoint into slides
        chunks = extractor.extract_content()
        generator = NotesGenerator(chunks, user_instruction)

        all_notes = []

        for chunk in chunks:
            note = generator.process_chunk(chunk)
            all_notes.append(f"### {chunk['section']}\n{note}\n")
            
        summary_title = generator.generate_title(all_notes)
        summary_overview = generator.generate_summary(all_notes)

        if self.latex:
            processed_notes = []
            for note_chunk in all_notes:
                updated_chunk = generator.replace_latex_with_images(note = note_chunk)
                processed_notes.append(updated_chunk)
            all_notes = processed_notes

        # Generates a suggested output directory based on the title and summary overview. 
        suggested_dir = generator.generate_directory(summary_title, summary_overview)

        output_path = os.path.join(suggested_dir, output_file_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated Notes For {summary_title}\n\n")
            f.write(f"## Summary Overview: {summary_overview}\n")
            f.write("\n\n".join(all_notes))
        print(f"✅ Notes saved to: {output_path}")

'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert documents into AI-generated notes.")
    parser.add_argument("file_path", help="Path to input file (.pptx, .pdf, .txt, etc.)")
    parser.add_argument("--output", default="notes.md", help="Output markdown file")
    parser.add_argument("--instruction", help="Instruction for note generation", required=False)
    parser.add_argument("--latex", action="store_true", help="Output notes as LaTeX file")

    args = parser.parse_args()

    if not args.instruction:
        args.instruction = input("Enter instruction for the note generation: ")

    main(args.file_path, args.output, args.instruction)
'''