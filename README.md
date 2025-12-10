# PDF Question Analyzer

A Python tool for searching and analyzing past exam papers (specifically CAIE Computer Science 9618 question papers) to find questions or contexts related to specific keywords or phrases.

## Features

- **Interactive Search**: Enter keywords or phrases to search across all downloaded question papers in the `downloads` directory.
- **Phrase Support**: Supports both single words and multi-word phrases (e.g., "operating system", "digital cameras").
- **Organization**: Groups results by exam period and file name.
- **Caching**: Caches extracted text for faster subsequent searches.
- **Comprehensive Results**: Displays context around each keyword match for better understanding.

## Prerequisites

- Python 3.x
- `pdfplumber` library for PDF text extraction

Install dependencies:
```
pip install pdfplumber
```

## Usage

1. Ensure you have downloaded past papers using a compatible downloader (files organized in `downloads/<period>/` directories).
2. Run the analyzer:
   ```
   python pdf_analyzer.py
   ```
3. Enter keywords separated by commas (e.g., `algorithm, binary, operating system`).
4. Review the results showing period, file, keyword, and context snippet.
5. Repeat searches or enter `quit` to exit.

## Directory Structure

```
downloads/
├── 2021 May June/
│   ├── 9618_s21_qp_11.pdf
│   ├── ...
├── 2021 Oct Nov/
├── ...
└── 2025 May June/
    ├── 9618_s25_qp_11.pdf
    ├── ...
```

## Output Example

```
Searching for keywords: operating system, binary

Found 5 matching context(s):

Period: 2022 Oct Nov
File: 9618_w22_qp_13.pdf
Keyword: operating system
Context: ...the operating system is the software that manages computer hardware and software resources... ...

------------------------------------------------------------

Period: 2021 May June
File: 9618_s21_qp_11.pdf
Keyword: binary
Context: ...binary search algorithm works by... ...

------------------------------------------------------------
```

## How It Works

1. **Text Extraction**: Uses `pdfplumber` to extract text from PDF question papers.
2. **Keyword Matching**: Searches for exact keyword/phrase matches in the extracted text.
3. **Context Retrieval**: Provides a 400-character context window around each match.
4. **Caching**: Stores extracted text to avoid reprocessing on subsequent searches.

## Notes

- Focuses on question papers (files containing 'qp' in the filename).
- Handles PDFs with text content; may not work on heavily imaged/scanned documents.
- Supports ASCII-compatible encoding for display.

## Related

- `downloader.py`: Tool for downloading the past papers (https://github.com/[username]/pastpaper-downloader)
