from typing import List
import planning


UTF8_HEADER = """<meta charset="utf-8">"""
SLIDES = """<link rel="stylesheet" href="https://casual-effects.com/markdeep/latest/slides.css?"><script>markdeepOptions={tocStyle:'none'}</script>"""
MARKDEEP_FOOTER = """<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://casual-effects.com/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>"""
ROWS_PER_PAGE = 30


FIRSTNAME_HEADER = " Vorname "
LASTNAME_HEADER = " Nachname "
MATRIKEL_HEADER = " Matrikel "
SIGN_HEADER = "      Unterschrift      "
COMMENT_HEADER = "      Anmerkung       "


def generate_room_signs():
    pass


def generate_student_list(students: List[planning.Student]) -> str:
    firstname_length = max([len(s.firstname) for s in students] + [len(FIRSTNAME_HEADER)])
    lastname_length = max([len(s.lastname) for s in students] + [len(LASTNAME_HEADER)])
    matrikel_length = max([len(str(s.matrikel)) for s in students] + [len(MATRIKEL_HEADER)])
    sign_length = len(SIGN_HEADER)
    comment_length = len(COMMENT_HEADER)

    def generate_row(fname, lname, mnr, sign, comment, pad=" "):
        return "|%s|%s|%s|%s|%s|" % (str(fname).rjust(firstname_length, pad),
                                     str(lname).rjust(lastname_length, pad),
                                     str(mnr).rjust(matrikel_length, pad),
                                     str(sign).rjust(sign_length, pad),
                                     str(comment).rjust(comment_length, pad))

    table_header = generate_row(FIRSTNAME_HEADER, LASTNAME_HEADER, MATRIKEL_HEADER, SIGN_HEADER, COMMENT_HEADER)
    table_header += "\n" + generate_row("", "", "", "", "", "-")

    body = "\n".join([generate_row(s.firstname, s.lastname, s.matrikel, "", "") for s in students])

    return "%s\n%s" % (table_header, body)


class MarkdeepDocument(object):
    def __init__(self, slides=False):
        self.contents = []
        self.footer = SLIDES + MARKDEEP_FOOTER if slides else MARKDEEP_FOOTER

    def append(self, content):
        self.contents.append(content)

    def render(self):
        content = "".join([str(c) for c in self.contents])
        return "%s\n%s\n%s" % (UTF8_HEADER, content, self.footer)

    def to_file(self, file):
        with open(file, "w") as fh:
            fh.write(self.render())
