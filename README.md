# Resume Ranking API

AI-powered resume ranking system using Sentence-BERT for semantic matching.

## Features

- Semantic similarity matching using Sentence-BERT
- Skills extraction and matching
- Experience level analysis
- Support for PDF and DOCX files
- Two upload methods: direct file upload or base64 encoding

## Installation

```bash
cd resume-ml
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Start the API

```bash
python app.py
```

Server runs at: `http://localhost:5000`

### API Endpoints

#### 1. File Upload (Recommended)

**POST** `/rank_resumes_upload`

Upload PDF/DOCX files directly using multipart/form-data.

**Parameters:**

- `job_description` (text) - Job description (min 50 chars)
- `resumes` (file) - PDF/DOCX files
- `top_k` (text, optional) - Number of top results (default: 10)

**Example (Postman):**

1. Select POST method
2. URL: `http://localhost:5000/rank_resumes_upload`
3. Body → form-data
4. Add `job_description` (Text)
5. Add `resumes` (File) - select your PDF/DOCX files
6. Send

#### 2. Base64 Upload

**POST** `/rank_resumes`

Send base64-encoded files in JSON format.

**Request Body:**

```json
{
  "job_description": "Your job description here",
  "resumes": [
    {
      "file_base64": "base64_encoded_content",
      "file_type": "pdf"
    }
  ],
  "top_k": 10
}
```

#### 3. Health Check

**GET** `/health`

#### 4. API Info

**GET** `/info`

## Response Format

```json
{
  "success": true,
  "total_resumes_processed": 2,
  "ranked_resumes": [
    {
      "index": 0,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "123-456-7890",
      "skills": ["Python", "React", "Node.js"],
      "years_of_experience": 5.0,
      "education": ["Bachelor", "Computer Science"],
      "match_score": 85.5,
      "matched_skills": ["Python", "React"],
      "score_breakdown": {
        "semantic_similarity": 78.5,
        "skills_match": 66.7,
        "experience_match": 100.0
      }
    }
  ]
}
```

## Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx)

## Requirements

- Python 3.13+
- Flask
- PyTorch
- Transformers
- Sentence-Transformers
- pdfplumber
- python-docx
- scikit-learn

## License

MIT
