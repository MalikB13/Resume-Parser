from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

TAGS = {
    "Contact": ["Contact", "Coordonnées"],
    "Top Skills": ["Top Skills", "Principales compétences"],
    "Certifications": ["Certifications"],
    "Honors-Awards": ["Honors-Awards"],
    "Publications": ["Publications"],
    "Summary": ["Summary"],
    "Languages": ["Languages"],
    "Experience": ["Experience", "Expérience"],
    "Education": ["Education", "Formation"],
}

ALL_TAGS = [item for sublist in TAGS.values() for item in sublist]

WEIRD = [
    "\u00b7",
    "\xa0",
    "\uf0da",
    "\x0c",
    "• ",
    "* ",
    "(LinkedIn)",
    " (LinkedIn)",
    "\uf0a7",
    "(Mobile)",
    "-       ",
    "●",
]


def extract_pdf(fname):
    imagewriter = None
    caching = True
    laparams = LAParams()
    retstr = io.StringIO()
    rsrcmgr = PDFResourceManager(caching=caching)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams, imagewriter=imagewriter)
    data = []

    with open(fname, "rb") as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, caching=caching, check_extractable=True):
            interpreter.process_page(page)
            data = retstr.getvalue()

    for i in WEIRD:
        data = data.replace(i, "")

    result_list = data.split("\n")
    return result_list


def get_contact(result_list, i):
    contact = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            contact.append(result_list[j].strip())
        else:
            return contact, j + 1


def get_skills(result_list, i):
    skills = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            skills.append(result_list[j].strip())
        else:
            return skills, j + 1


def get_certifications(result_list, i):
    certifications = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            certifications.append(result_list[j].strip())
        else:
            return certifications, j + 1


def get_honors(result_list, i):
    honors = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            honors.append(result_list[j].strip())
        else:
            return honors, j + 1


def get_summary(result_list, i):
    summary = []
    summ = ""
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            summ += result_list[j].strip() + " "
        else:
            summary.append(summ.strip())
            return summary, j + 1


def get_languages(result_list, i):
    languages = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            languages.append(result_list[j].strip())
        else:
            return languages, j + 1


def get_experiences(result_list, i):
    experiences = []
    for j in range(i + 1, len(result_list)):
        if len(result_list[j]) == 0:
            continue
        elif "Page" in result_list[j]:
            continue
        elif result_list[j] not in ALL_TAGS:
            experiences.append(result_list[j].strip())
        else:
            return experiences, j + 1


def get_many(result_list):
    skills, languages, summary, certifications, honors, contact, experiences = [], [], [], [], [], [], []
    res = {}

    for i in range(len(result_list)):
        if result_list[i] in TAGS["Contact"]:
            contact, i = get_contact(result_list, i)
        if result_list[i] in TAGS["Top Skills"]:
            skills, i = get_skills(result_list, i)
        if result_list[i] in TAGS["Certifications"]:
            certifications, i = get_certifications(result_list, i)
        if result_list[i] in TAGS["Honors-Awards"]:
            honors, i = get_honors(result_list, i)
        if result_list[i] in TAGS["Summary"]:
            summary, i = get_summary(result_list, i)
        if result_list[i] in TAGS["Languages"]:
            languages, i = get_languages(result_list, i)
        if result_list[i] in TAGS["Experience"]:
            experiences, i = get_experiences(result_list, i)

    res = {
        "contact": contact,
        "skills": skills,
        "languages": languages,
        "certifications": certifications,
        "honors": honors,
        "summary": summary,
        "experiences": experiences,
    }

    return res
