import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}
    corpus_len = len(corpus)
    num_links = len(corpus[page])
    if num_links == 0:
        for key in corpus.keys():
            result[key] = 1 / corpus_len
    else:
        for key in corpus.keys():
            if key in corpus[page]:
                result[key] = damping_factor / \
                    num_links + (1.0 - damping_factor) / corpus_len
            else:
                result[key] = (1.0 - damping_factor) / corpus_len
    return result



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    for key in corpus.keys():
        result[key] = 0.0
    for i in range(0, n):
        if i == 0:
            current_page = list(corpus)[random.randint(0, len(corpus) - 1)]
            result[current_page] += 1.0
        else:
            transit_dict = transition_model(
                corpus, current_page, damping_factor)
            rand_num = random.uniform(0.0, 1.0)
            total = 0.0
            for key in transit_dict.keys():
                total += transit_dict[key]
                if total >= rand_num:
                    current_page = key
                    result[current_page] += 1.0
                    break
    normalizer = SAMPLES
    for key in result.keys():
        result[key] = result[key] / normalizer

    return result
            

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_len = len(corpus) + 0.0
    result = {}
    result_old = {}
    for key in corpus.keys():
        result[key] = 1 / corpus_len
        result_old[key] = 1 / corpus_len
        if len(corpus[key]) == 0:
            corpus[key] = set(corpus.keys())
    n = 0
    p = 0.0
    summation = 0.0
    while n < 1:
        n = 0
        for key in corpus.keys():
            summation = 0.0
            p = (1.0 - damping_factor) / corpus_len
            for key2 in corpus.keys():
                if key == key2 or key not in corpus[key2]:
                    continue
                else:
                    num_links = len(corpus[key2]) + 0.0
                    summation += (result_old[key2] / num_links)
            summation = damping_factor * summation
            p += summation
            result[key] = p
        for key in result.keys():
            if abs(result[key] - result_old[key]) < 0.001:
                n = n + 1
            result_old[key] = result[key]

    normalizer = sum(result.values())
    for key in result.keys():
        result[key] = result[key] / normalizer
    return result


if __name__ == "__main__":
    main()
