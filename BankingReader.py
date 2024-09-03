import re
from pdfreader import PDFDocument, SimplePDFViewer

fd = open(input("Enter File Location:" ), "rb")
viewer = SimplePDFViewer(fd)
doc = PDFDocument(fd)

# renders the whole document and saves it as a large string that can be checked with regex
def extract_pdf_text():
    full_text = ""

    all_pages = [p for p in doc.pages()]

    for page in range(len(all_pages)):
        viewer.navigate(page + 1)
        viewer.render()
        for str in viewer.canvas.strings:
            full_text += str
    
    return full_text

# checks the entire text with regex to find matches of U.S.C. or C.F.R. codes and returns a set (unique matches)
def matching(checkText):
    usc_pattern = re.compile(r'(\d+\s+U\.S\.C\.\s+§\s+\d+(\s*\(\w+\))*(?:\s*(?:and|or|,)\s*\(\w+\))*)')
    cfr_pattern = re.compile(r'\d+\s+C\.F\.R\.\s(?:Part|§)\s\d+(?:\.\d*)?\s*(?:or|and\s+Part\s+\d+)?\s*\d+')
    usc_codes = []
    cfr_codes = []
    final_result = ""
    if checkText:
        usc_matches = usc_pattern.findall(checkText)
        usc_codes.extend(usc_matches)
        cfr_matches = cfr_pattern.findall(checkText)
        cfr_codes.extend(cfr_matches)
    for a in range(len(usc_codes)):
        usc_codes[a] = usc_codes[a][0]
    for b in set(usc_codes).union(set(cfr_codes)):
        final_result += b
        final_result += "; "
    return(final_result)

# checks the entire text with regex to find if the word 'fiduciary' is located within the text and returns a response
def fiduciaryMentioned(checkText):
    fiduciaryPattern = re.compile(r'(\bfiduciary\b)')
    fiduciaryMentions = []
    if checkText:
        fiduciaryMatches = fiduciaryPattern.findall(checkText, re.IGNORECASE)
        fiduciaryMentions.extend(fiduciaryMatches)
    if len(fiduciaryMentions) > 0:
        return "Fiduciary IS mentioned"
    else:
        return "Fiduciary IS NOT mentioned"

print(matching(extract_pdf_text()))
print(fiduciaryMentioned(extract_pdf_text()))

