import os
import re
import requests
import time

# ============================================================
# SETTINGS
# ============================================================

nb_pages = 5

# Number of papers per page
results_per_page = 10

# Search query
search_query = "machine learning"

# Folder where all PDFs will be saved
DOWNLOAD_FOLDER = "pdf_files"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ============================================================
# SESSION
# ============================================================

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


# ============================================================
# DOWNLOAD PDF
# ============================================================

def download_file(pdf_url, filename):

    filepath = os.path.join(
        DOWNLOAD_FOLDER,
        filename
    )

    response = session.get(
        pdf_url,
        timeout=60,
        allow_redirects=True
    )

    response.raise_for_status()

    # Check that we actually received a PDF
    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if (
        "pdf" not in content_type
        and not response.url.lower().endswith(".pdf")
    ):
        print(
            f"Not a PDF: {response.url}"
        )
        return None

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath


# ============================================================
# CREATE SAFE FILENAME
# ============================================================

def clean_filename(title):

    # Use the title as filename
    filename = title

    # Remove characters that are illegal in filenames
    filename = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename
    )

    # Remove extra spaces
    filename = re.sub(
        r"\s+",
        " ",
        filename
    ).strip()

    # Limit filename length
    filename = filename[:180]

    if not filename:
        filename = "paper"

    filename += ".pdf"

    return filename


# ============================================================
# SEARCH CROSSREF
# ============================================================

for n_page in range(1, nb_pages + 1):

    # Calculate offset
    offset = (n_page - 1) * results_per_page

    url = "https://api.crossref.org/v1/works"

    params = {
        "query": search_query,
        "rows": results_per_page,
        "offset": offset,

        # Ask Crossref to return useful fields
        "select": (
            "DOI,title,author,published,"
            "URL,link,type"
        ),

        # Identify ourselves to Crossref
        # Replace with your email if you want
        "mailto": "your_email@example.com"
    }

    print()
    print("=" * 70)
    print(f"HTTP GET: {url}")
    print(f"PAGE: {n_page}")
    print(f"QUERY: {search_query}")
    print("=" * 70)

    try:

        response = session.get(
            url,
            params=params,
            timeout=30
        )

        print(
            f"HTTP status: {response.status_code}"
        )

        response.raise_for_status()

        # Crossref returns JSON
        data = response.json()

        # Get the actual search results
        papers = data["message"]["items"]

        print(
            f"Papers found: {len(papers)}"
        )

        # ====================================================
        # PROCESS EACH PAPER
        # ====================================================

        for paper_number, paper in enumerate(
            papers,
            start=1
        ):

            print()
            print(
                f"Paper {paper_number}"
            )

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            titles = paper.get(
                "title",
                []
            )

            if titles:
                title = titles[0]
            else:
                title = (
                    f"paper_page_{n_page}_"
                    f"{paper_number}"
                )

            print(f"Title: {title}")

            # ------------------------------------------------
            # DOI
            # ------------------------------------------------

            doi = paper.get(
                "DOI"
            )

            print(
                f"DOI: {doi}"
            )

            # ------------------------------------------------
            # PUBLISHED DATE
            # ------------------------------------------------

            published = paper.get(
                "published",
                {}
            )

            date_parts = published.get(
                "date-parts",
                []
            )

            if date_parts:

                publication_date = (
                    "-".join(
                        str(x)
                        for x in date_parts[0]
                    )
                )

            else:

                publication_date = "Unknown"

            print(
                f"Published: {publication_date}"
            )

            # ------------------------------------------------
            # FIND FULL-TEXT / PDF LINKS
            # ------------------------------------------------

            links = paper.get(
                "link",
                []
            )

            pdf_url = None

            for link in links:

                link_url = link.get(
                    "URL"
                )

                content_type = link.get(
                    "content-type",
                    ""
                ).lower()

                if not link_url:
                    continue

                # Prefer actual PDF links
                if (
                    "pdf" in content_type
                    or ".pdf" in link_url.lower()
                ):

                    pdf_url = link_url
                    break

            # ------------------------------------------------
            # NO PDF
            # ------------------------------------------------

            if not pdf_url:

                print(
                    "No PDF/full-text link found."
                )

                continue

            # ------------------------------------------------
            # PDF FOUND
            # ------------------------------------------------

            print(
                f"PDF URL: {pdf_url}"
            )

            # ------------------------------------------------
            # CREATE FILENAME
            # ------------------------------------------------

            filename = clean_filename(
                title
            )

            # ------------------------------------------------
            # PREVENT OVERWRITING
            # ------------------------------------------------

            filepath = os.path.join(
                DOWNLOAD_FOLDER,
                filename
            )

            if os.path.exists(filepath):

                name, extension = (
                    os.path.splitext(filename)
                )

                counter = 1

                while os.path.exists(filepath):

                    new_filename = (
                        f"{name}_{counter}"
                        f"{extension}"
                    )

                    filepath = os.path.join(
                        DOWNLOAD_FOLDER,
                        new_filename
                    )

                    counter += 1

                filename = new_filename

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            try:

                saved_file = download_file(
                    pdf_url,
                    filename
                )

                if saved_file:

                    print(
                        f"Saved: {saved_file}"
                    )

            except requests.RequestException as e:

                print(
                    f"PDF download failed: {e}"
                )

            # Be polite to Crossref / publisher
            time.sleep(1)

    except requests.RequestException as e:

        print(
            f"Crossref request failed: {e}"
        )

    except ValueError as e:

        print(
            f"JSON parsing failed: {e}"
        )


# ============================================================
# FINISHED
# ============================================================

print()
print("=" * 70)
print("DONE!")
print("=" * 70)

print(
    "PDFs are saved in:"
)

print(
    os.path.abspath(
        DOWNLOAD_FOLDER
    )
)
