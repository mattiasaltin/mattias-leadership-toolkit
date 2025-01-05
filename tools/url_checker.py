"""URL verification tool that checks titles and content against expected values.

This module provides functionality to verify URLs by comparing their page titles
with expected values, handling various platform-specific formats and common suffixes.
"""

import re
import json
import os
import glob
from typing import Dict, List
from rapidfuzz import fuzz  # Use rapidfuzz for better performance
import streamlit as st
import requests
from bs4 import BeautifulSoup


def fetch_page_title(url: str) -> str:
    """Fetches the page title from the given URL."""
    st.write(f"Fetching title for URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No title found'
        st.write(f"Found title: {title}")
        return title
    except requests.RequestException as err:
        st.write(f"Error fetching title: {err}")
        return f"Error fetching title: {err}"
    except AttributeError:
        st.write("No title found in page")
        return "No title found in page"


def normalise_title(title: str) -> str:
    """Normalises titles by removing extra spaces, case sensitivity, and punctuation."""
    title = title.lower().strip()
    title = re.sub(r"[^\w\s]", "", title)  # Remove punctuation
    return title


def clean_title(title: str) -> str:
    """Remove common website suffixes from titles."""
    common_suffixes = [
        " - YouTube",
        " | Goodreads",
        " | Amazon",
        " | LinkedIn",
        " | Medium"
    ]
    cleaned = title
    for suffix in common_suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    return cleaned.strip()


def platform_specific_clean(title: str, url: str) -> str:
    """Cleans titles based on platform-specific quirks."""
    if "goodreads.com" in url:
        return title.replace(" | Goodreads", "").strip()
    if "youtube.com" in url:
        return title.replace(" - YouTube", "").strip()
    return title


def should_skip(actual_title: str, expected_title: str) -> bool:
    """Check if a record should be skipped due to common suffix differences."""
    suffixes_to_ignore = [
        "\u2022 GOTO 2017",
        "\u2022 GOTO 2018",
        "\u2022 GOTO 2019",
        "\u2022 GOTO 2020",
    ]
    for suffix in suffixes_to_ignore:
        if actual_title.endswith(suffix):
            cleaned_actual = actual_title[: -len(suffix)].strip()
            if normalise_title(cleaned_actual) == normalise_title(expected_title):
                return True
    return False


def fuzzy_match(title1: str, title2: str, threshold: int = 85) -> bool:
    """Check if two titles match with a certain similarity threshold."""
    score = fuzz.ratio(title1, title2)
    st.write(f"Fuzzy match score: {score}")
    return score >= threshold


def extract_links_from_md(file_path: str) -> List[Dict]:
    """Extracts links and their descriptions from a markdown file."""
    links = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
        for line in content:
            # Match markdown links
            match = re.search(r'\[(.*?)\]\((https?://.*?)\)', line)
            if match:
                text = match.group(1)
                url = match.group(2)
                description = line.strip()
                links.append({'text': text, 'url': url, 'description': description})
    return links


def verify_links(links: List[Dict], file_path: str, filter_status: int = None) -> List[Dict]:
    """Verifies each link's status and content relevance."""
    st.write(f"Starting verification of {len(links)} links in {file_path}")
    verification_results = []
    
    # Add retry settings
    session = requests.Session()
    session.mount('https://', requests.adapters.HTTPAdapter(
        max_retries=3,
        pool_connections=10,
        pool_maxsize=10
    ))

    for i, link in enumerate(links, 1):
        try:
            url = link['url']
            expected_title = normalise_title(link['text'])
            expected_description = link['description']
            
            st.write(f"Processing link {i}/{len(links)}: {url}")
            
            try:
                response = session.head(url, allow_redirects=True, timeout=30)
                status_code = response.status_code
            except (requests.RequestException, requests.ConnectionError) as err:
                st.warning(f"Network error for {url}: {err}")
                verification_results.append({
                    'file': file_path,
                    'url': url,
                    'status_code': 'Network Error',
                    'expected_title': expected_title,
                    'actual_title': 'Could not access site',
                    'title_matches': False,
                    'description': expected_description
                })
                continue

            st.write(f"Checking URL status: {url}")
            if status_code == 200:
                actual_title = fetch_page_title(url)
                actual_title = platform_specific_clean(actual_title, url)
                cleaned_actual = clean_title(actual_title)
                cleaned_actual = normalise_title(cleaned_actual)

                # Check for skipping
                if should_skip(cleaned_actual, expected_title):
                    st.write("Skipped record due to ignorable suffix difference")
                    continue

                # Title match logic
                title_matches = (
                    expected_title == cleaned_actual or fuzzy_match(expected_title, cleaned_actual)
                )
                if not title_matches and fuzz.ratio(expected_description, cleaned_actual) >= 85:
                    st.write("Title did not match, but description matched.")
                    title_matches = True

                st.write(f"Expected: '{expected_title}'")
                st.write(f"Found (cleaned): '{cleaned_actual}'")
                st.write(f"Title match: {title_matches}")
            else:
                actual_title = 'N/A'
                title_matches = False
                st.write("Skipping title check due to non-200 status")
        except requests.RequestException as err:
            st.write(f"Request error: {err}")
            status_code = 'Error'
            actual_title = str(err)
            title_matches = False

        if filter_status is None or status_code != filter_status:
            verification_results.append({
                'file': file_path,
                'url': url,
                'status_code': status_code,
                'expected_title': expected_title,
                'actual_title': actual_title,
                'title_matches': title_matches,
                'description': expected_description
            })

    st.write("Link verification completed")
    return verification_results


def find_md_files(root_folder: str) -> List[str]:
    """Find all .md files in the given root folder and its subfolders."""
    md_files = glob.glob(os.path.join(root_folder, '**', '*.md'), recursive=True)
    return md_files


st.set_page_config(page_title="Check URLs", page_icon=":tada:", layout="wide")

with st.sidebar:
    st.title("Check URLs")
    root_folder = st.text_input("Enter root folder path:")
    filter_status = st.selectbox("Filter out responses with status code:", [None, 200, 404, 500])
    process = st.button("Process")

if root_folder and process:
    md_files = find_md_files(root_folder)
    st.write(f"Found {len(md_files)} markdown files.")
    all_results = []
    for md_file in md_files:
        st.write(f"Processing file: {md_file}")
        links = extract_links_from_md(md_file)
        link_results = verify_links(links, md_file, filter_status)
        all_results.extend(link_results)

    # Convert results to table format
    table_data = []
    for result in all_results:
        table_data.append({
            "File": result['file'],
            "URL": result['url'],
            "Status": result['status_code'],
            "Expected Title": result['expected_title'],
            "Actual Title": result['actual_title'],
            "Title Match": "✅" if result['title_matches'] else "❌",
            "Description": result['description']
        })
    st.write("### Results Table")
    st.dataframe(table_data)

    # Add JSON export button
    st.download_button(
        label="Download Results as JSON",
        data=json.dumps(all_results, indent=2),
        file_name="url_check_results.json",
        mime="application/json"
    )
