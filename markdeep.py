from typing import List
from planning import Student


UTF8_HEADER = """<meta charset="utf-8">"""
MARKDEEP_FOOTER = """<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://casual-effects.com/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>"""

FIRSTNAME_HEADER = " Vorname "
LASTNAME_HEADER = " Nachname "
MATRIKEL_HEADER = " Matrikel "
SIGN_HEADER = " Unterschrift "


def generate_student_list(students: List[Student]) -> str:
    firstname_length = max([len(s.firstname) for s in students] + [len(FIRSTNAME_HEADER)])
    lastname_length = max([len(s.lastname) for s in students] + [len(LASTNAME_HEADER)])
    matrikel_length = max([len(str(s.matrikel)) for s in students] + [len(MATRIKEL_HEADER)])
    sign_length = len(SIGN_HEADER)

    def generate_line(fname, lname, mnr, sign, pad=" "):
        return "|%s|%s|%s|%s|" % (str(fname).rjust(firstname_length, pad),
                                  str(lname).rjust(lastname_length, pad),
                                  str(mnr).rjust(matrikel_length, pad),
                                  sign.rjust(sign_length, pad))

    table_header = generate_line(FIRSTNAME_HEADER, LASTNAME_HEADER, MATRIKEL_HEADER, SIGN_HEADER)
    table_header += "\n" + generate_line("", "", "", "", "-")

    body = "\n".join([generate_line(s.firstname, s.lastname, s.matrikel, "") for s in students])

    return "%s\n%s" % (table_header, body)


class MarkdeepDocument(object):
    def __init__(self):
        self.contents = []

    def append(self, content):
        self.contents.append(content)

    def render(self):
        content = "".join([str(c) for c in self.contents])
        return "%s\n%s\n%s" % (UTF8_HEADER, content, MARKDEEP_FOOTER)

    def to_file(self, file):
        with open(file, "w") as fh:
            fh.write(self.render())
