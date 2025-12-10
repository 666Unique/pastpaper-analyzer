import os
import pdfplumber
import re

# Directory containing the downloaded files
download_dir = "downloads"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def find_keyword_context(text, keywords):
    """Find contexts around keywords in the text."""
    contexts = []
    lower_text = text.lower()

    for keyword in keywords:
        pos = 0
        occurrences = 0
        while pos < len(text) and occurrences < 5:  # limit per file per keyword
            pos = lower_text.find(keyword, pos)
            if pos == -1:
                break
            # Get context around the keyword
            start_context = max(0, pos - 200)
            end_context = min(len(text), pos + len(keyword) + 200)
            context = text[start_context:end_context].strip()
            contexts.append({
                'keyword': keyword,
                'context': context
            })
            pos += len(keyword)
            occurrences += 1

    return contexts

def main():
    cache = {}  # To cache extracted text per file to speed up repeated searches

    while True:
        # Get keywords from user
        keywords_input = input("Enter keywords separated by commas (or 'quit' to exit) (e.g., algorithm, binary, hash): ").strip()
        if keywords_input.lower() == 'quit':
            print("Exiting.")
            break

        keywords = [kw.strip().lower() for kw in keywords_input.split(',') if kw.strip()]

        if not keywords:
            print("No keywords entered. Try again.")
            continue

        print(f"Searching for keywords: {', '.join(keywords)}")

        # Collect matching contexts
        matching_contexts = []

        for root, dirs, files in os.walk(download_dir):
            for file in files:
                if file.lower().endswith('.pdf') and 'qp' in file.lower():  # Focus on question papers
                    pdf_path = os.path.join(root, file)
                    period = os.path.basename(root)

                    if pdf_path not in cache:
                        print(f"Processing {file} from {period}...")
                        text = extract_text_from_pdf(pdf_path)
                        cache[pdf_path] = text
                    else:
                        text = cache[pdf_path]

                    if not text:
                        continue

                    contexts = find_keyword_context(text, keywords)

                    for ctx in contexts:
                        matching_contexts.append({
                            'file': file,
                            'period': period,
                            'keyword': ctx['keyword'],
                            'context': ctx['context']
                        })

        # Display results
        if not matching_contexts:
            print("No contexts found matching the keywords.")
        else:
            print(f"\nFound {len(matching_contexts)} matching context(s):\n")

            for mc in matching_contexts:
                print(f"Period: {mc['period']}")
                print(f"File: {mc['file']}")
                print(f"Keyword: {mc['keyword']}")
                context_preview = mc['context'][:500] + ("..." if len(mc['context']) > 500 else "")
                context_preview = context_preview.encode('ascii', 'replace').decode('ascii')
                print(f"Context: {context_preview}")
                print("-" * 80)

        print("\n" + "="*100 + "\n")

if __name__ == "__main__":
    main()
