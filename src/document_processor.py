import pymupdf


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        pages.append({
            "text": text,
            "page": page_number
        })

    document.close()

    return pages