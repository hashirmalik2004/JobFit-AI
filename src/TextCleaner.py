# TextCleaner.py
# this file handles cleaning up the raw text extracted from the PDF
# PDFs often contain messy elements like URLs, emails, emojis, and formatting artifacts

import re  # built-in Python module for regular expressions (pattern matching)

# importing pre-defined regex patterns from your GlobalSettings file
# these patterns are used to detect and remove unwanted text
from src.GlobalSettings import UrlPattern, EmailPattern, EmojiPattern, BulletPattern


def Sanitize(RawText):
    """
    takes raw messy text from a PDF and cleans it up
    removes URLs, emails, emojis, bullets, and extra whitespace
    returns a clean string ready for NLP processing
    """

    # start with the original text
    CleanText = RawText
    
    # remove URLs (like https://example.com)
    CleanText = UrlPattern.sub("", CleanText)

    # remove email addresses (like name@email.com)
    CleanText = EmailPattern.sub("", CleanText)

    # remove emojis (😀🔥🚀 etc.)
    CleanText = EmojiPattern.sub("", CleanText)

    # remove bullet points or special list symbols (•, -, etc.)
    CleanText = BulletPattern.sub("", CleanText)

    # remove non-ASCII characters (anything outside basic English characters)
    # replaces them with a space instead of deleting completely to avoid word merging
    CleanText = re.sub(r'[^\x00-\x7F]+', ' ', CleanText)

    # replace multiple spaces, tabs, or newlines with a single space
    CleanText = re.sub(r'\s+', ' ', CleanText)

    # remove leading and trailing whitespace
    CleanText = CleanText.strip()

    # print how much text was cleaned (before vs after length)
    print(f"The text has been cleaned successfully , went from {len(RawText)} chars to {len(CleanText)} chars")

    # return the cleaned text
    return CleanText