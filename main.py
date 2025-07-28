from extractor.loader import load_pdfs
from extractor.persona_parser import load_persona
from extractor.section_ranker import rank_sections
from extractor.summarizer import refine_subsections
from extractor.formatter import save_output

from datetime import datetime
from collections import defaultdict
import os

def main():
    base_dir = "Challenge_1b"
    collections = ["Collection 1", "Collection 2", "Collection 3"]

    for collection in collections:
        collection_path = os.path.join(base_dir, collection)
        pdf_dir = os.path.join(collection_path, "PDFs")
        persona_path = os.path.join(collection_path, "challenge1b_input.json")
        output_path = os.path.join(collection_path, "challenge1b_output.json")

        if not os.path.exists(pdf_dir) or not os.path.exists(persona_path):
            print(f"⚠️ Skipping missing {collection_path}")
            continue

        print(f"🔍 Processing {collection}...")

        # Step 1: Load PDFs
        documents = load_pdfs(pdf_dir)

        # Step 2: Load Persona Info
        persona = load_persona(persona_path)
        persona_role = persona["persona"]
        persona_task = persona["job_to_be_done"]

        # Step 3: Extract and Rank Sections (MMR + heading boost)
        ranked_sections = rank_sections(pdf_dir, persona_role, persona_task, top_k=10)

        # Step 4: Refine Subsections
        refined_sections = refine_subsections(ranked_sections, persona=persona_role, job=persona_task, top_k=3)

        # Step 5: Metadata
        metadata = {
            "input_documents": [doc["name"] for doc in documents],
            "persona": persona_role,
            "job_to_be_done": persona_task,
            "processing_timestamp": datetime.now().isoformat()
        }

        # Step 6: Build extracted_sections
        extracted_sections = []
        for i, sec in enumerate(ranked_sections, 1):
            # Use heading if available, else fallback to first line
            section_title = sec.heading if sec.heading else \
                (sec.text.strip().split("\n")[0][:80])
            extracted_sections.append({
                "document": sec.document,
                "section_title": section_title[:80],
                "importance_rank": i,
                "page_number": sec.page_number
            })

        # Step 7: Group refined subsections by (doc, page)
        grouped_subs = defaultdict(list)
        for r in refined_sections:
            grouped_subs[(r["document"], r["page_number"])].append({
                "refined_text": r["refined_text"],
                "score": r["score"]
            })

        subsection_analysis = []
        for (doc, page), subs in grouped_subs.items():
            subsection_analysis.append({
                "document": doc,
                "page_number": page,
                "refined_chunks": subs
            })

        # Step 8: Save Output
        save_output(metadata, extracted_sections, subsection_analysis, output_path)
        print(f"✅ Output saved to {output_path}")

if __name__ == "__main__":
    main()



