Adobe Hackathon Round 1B – Persona-Driven Document Intelligence
Overview
This project processes multiple PDFs related to a given persona and job-to-be-done, extracts the most relevant sections, and provides a structured JSON output including:

Metadata

Extracted Sections

Refined Subsection Analysis

Folder Structure
pgsql
Copy
Edit
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                        # South of France guides
│   ├── challenge1b_input.json       # Input configuration
│   └── challenge1b_output.json      # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
└── README.md
Approach
1. Input Parsing
Read persona and job-to-be-done from challenge1b_input.json.

Load all PDFs from the respective PDFs/ folder.

2. Chunk Extraction
Use PyMuPDF (fitz) to extract page-level text blocks.

Filter out tiny or irrelevant text fragments.

3. Semantic Ranking
Model: sentence-transformers/all-MiniLM-L6-v2 (fast, CPU-friendly).

Combine persona + job into a query:

arduino
Copy
Edit
"{persona}. Task: {job}"
Compute embeddings for:

Query

All text chunks

Rank chunks by cosine similarity using sentence-transformers.

4. Diversity Control
Take top 20 chunks by score.

Apply max-2-per-document constraint to avoid dominance by one file.

Keep top 10 after filtering.

(Optional Future Step: Use MMR for smarter diversity control).

5. Subsection Analysis
For each top section:

Split into smaller chunks (≈300 characters, sentence-based).

Rank again by semantic similarity.

Keep top-3 refined chunks per section.

6. JSON Output
Metadata: Input files, persona, job, timestamp.

Extracted Sections: Document name, title, page number, importance rank.

Section title = first meaningful non-bullet line.

Subsection Analysis: Grouped refined chunks with scores.

Why This Approach
✅ Lightweight & CPU-friendly
✅ Works offline (model <200MB)
✅ Semantic relevance + diversity boost
✅ Output aligns with Adobe’s expected JSON format

How to Run
Run the script for all collections:

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
Sample Output (Collection 1)
json
Copy
Edit
{
  "metadata": {
    "input_documents": [
      "South of France - Cities.pdf",
      "South of France - Cuisine.pdf",
      "South of France - History.pdf"
    ],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-28T20:36:01"
  },
  "extracted_sections": [
    {
      "document": "South of France - Things to Do.pdf",
      "section_title": "Coastal Adventures",
      "importance_rank": 1,
      "page_number": 2
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Things to Do.pdf",
      "page_number": 2,
      "refined_chunks": [
        {
          "refined_text": "The South of France is renowned for its beautiful coastline...",
          "score": 0.45
        }
      ]
    }
  ]
}
Future Improvements
✅ Implement MMR (Maximal Marginal Relevance) for better diversity.

✅ Add LLM-based summarization for more natural summaries.

✅ Create a visual dashboard for interactive review.

Author: Riddhi Sharma
Hackathon: Adobe India – Understand Your Document (Round 1B)