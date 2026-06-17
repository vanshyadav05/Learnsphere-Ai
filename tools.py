from ddgs import DDGS

def search_web(query):

    if not query.strip():
        return "No search query given."

    results_text = ""

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=5
        )

        for result in results:
            title = result.get("title", "")
            body = result.get("body", "")
            link = result.get("href", "")

            results_text += f"Title: {title}\n"
            results_text += f"Info: {body}\n"
            results_text += f"Link: {link}\n\n"

    return results_text