Approach Explanation – Adobe Hackathon Round 1B
Persona-Driven Document Intelligence
adobe_r1b/
├── input/                      # Folder to store 3–10 input PDFs
├── output/                     # Folder where final JSON output will be saved
├── main.py                     # Main pipeline to run extraction + prioritization
├── extractor/                  # Modular logic
│   ├── __init__.py
│   ├── loader.py               # Load + parse PDFs (PyMuPDF/pdfplumber)
│   ├── persona_parser.py       # Parse persona & job-to-be-done
│   ├── section_ranker.py       # Rank sections based on semantic relevance
│   ├── summarizer.py           # Refine subsection text
│   └── formatter.py            # Create final output JSON
├── models/                     # Store MiniLM model or SentenceTransformer wrapper
│   └── embedder.py
├── approach_explanation.md     # Required: Explain your methodology (300–500 words)
├── requirements.txt
├── Dockerfile
└── README.md

Problem Statement
Given:

3 Collections of PDFs (Travel Planning, Adobe Acrobat Learning, Recipe Collection)

An input JSON with:

persona

job_to_be_done

Goal:

Identify top relevant sections across multiple PDFs

Extract fine-grained subsections

Output a structured JSON with:

Metadata

Ranked sections (titles, pages)

Subsection-level summaries

Design Principles
Lightweight: CPU-only, ≤200MB model, <60s runtime per collection.

Accurate: Leverage semantic similarity, not keyword search.

Structured Output: Matches Adobe challenge format.

Pipeline Overview
Step 1: Load Persona & PDFs
Parse challenge1b_input.json:

json
Copy
Edit
{
  "persona": "Travel Planner",
  "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends."
}
Load PDFs from respective Collection/PDFs/ folder using PyMuPDF.

Step 2: Extract Text Chunks
Use fitz (PyMuPDF) → page.get_text("blocks") for block-level text.

Clean text:

Remove empty strings

Filter blocks shorter than 50 chars (junk)

Create Chunk objects:

python
Copy
Edit
Chunk(document="file.pdf", page_number=2, text="Actual content")
Step 3: Semantic Relevance Scoring
Embedding Model: sentence-transformers/all-MiniLM-L6-v2

Size: ~90MB

CPU inference ~0.2s per 1,000 tokens

Combine persona + job → query:

arduino
Copy
Edit
"{persona}. Task: {job}"
Compute embeddings:

Query embedding

All chunks embeddings

Use cosine similarity → score each chunk.

Sort chunks by score.

Step 4: Diversity Boost
Problem: Without control, one PDF dominates (e.g., “Tips and Tricks” in Collection 1).
Solution:

Take top 20 ranked chunks.

Apply max-2-per-document rule.

Keep final top 10 for extracted sections.

(Optional Future Step: MMR for embedding-level diversity).

Step 5: Subsection Refinement
For each top section:

Split text into smaller sentences/chunks (~300 chars) using regex.

Rank each subsection by cosine similarity with query.

Keep top 3 subsections per section.

Output format:

json
Copy
Edit
{
  "document": "file.pdf",
  "page_number": 8,
  "refined_chunks": [
    { "refined_text": "...", "score": 0.43 }
  ]
}
Step 6: Output Formatting
Metadata:

Input PDFs

Persona & Job

Timestamp

Extracted Sections:

Title = first meaningful non-bullet line or first text line.

Rank by importance.

Subsection Analysis:

Group by document + page.

Final JSON:

json
Copy
Edit
{
  "metadata": {...},
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
Sample Workflow
bash
Copy
Edit
python main.py
Outputs:

bash
Copy
Edit
Collection 1/challenge1b_output.json
Collection 2/challenge1b_output.json
Collection 3/challenge1b_output.json
Strengths
✅ CPU-optimized
✅ Semantic-driven, persona-aware
✅ Matches Adobe JSON format
✅ Multi-collection automation

Future Enhancements
MMR (Maximal Marginal Relevance) for better diversity.

LLM-based summarization for natural, concise summaries.

Visualization dashboard for interactive review.

Author: Riddhi Sharma
Hackathon: Adobe India – Understand Your Document (Round 1B)