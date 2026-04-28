# this file handles cleaning up the raw text extracted from the PDF
import re
from src.GlobalSettings import UrlPattern, EmailPattern, EmojiPattern, BulletPattern


def Sanitize(RawText):
    """
    takes raw messy text from a PDF and cleans it up
    removes URLs, emails, emojis, bullets, and extra whitespace
    returns a clean string ready for NLP processing
    """

    CleanText = RawText
    
    CleanText = UrlPattern.sub("", CleanText)
    CleanText = EmailPattern.sub("", CleanText)
    CleanText = EmojiPattern.sub("", CleanText)
    CleanText = BulletPattern.sub("", CleanText)
    CleanText = re.sub(r'[^\x00-\x7F]+', ' ', CleanText)
    CleanText = re.sub(r'\s+', ' ', CleanText)
    CleanText = CleanText.strip()

    print(f"The text has been cleaned successfully  went from {len(RawText)} chars to {len(CleanText)} chars")

    return CleanText