from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed('<center><table border=0 width=80%><tr><td align=left><B><a name = "CS241"></a>CS 241 LAB,LEC,TST,TUT 0.50</b></td><td align=right>Course ID: 004378</td></tr><tr><td colspan=2><b>Foundations of Sequential Programs</B></td></tr><tr><td colspan=2>The relationship between high-level languages and the computer architecture that underlies their implementation, including basic machine architecture, assemblers, specification and translation of programming languages, linkers and loaders, block-structured languages, parameter passing mechanisms, and comparison of programming languages. </td></tr><tr><td colspan=2><i>[Note: Enrolment is restricted; see Note 1 above. Lab is not scheduled and students are expected to find time in open hours to complete their work. CS 251 is a recommended corequisite. Offered: F,W,S]</i></td></tr><tr><td colspan=2><i> </i></td></tr><tr><td colspan=2><i>Prereq: CS 246 or (CS 138 and enrolled in Software Engineering); Computer Science students only.</i></td></tr><tr><td colspan=2><i> Antireq: CS 230</i></td></tr><p></table></center><Br><P><center><table border=0 width=80%><tr><td align=left><B><a name = "CS245"></a>CS 245 LEC,TST,TUT 0.50</b></td><td align=right>Course ID: 011405</td></tr><tr><td colspan=2><b>Logic and Computation</B></td></tr><tr><td colspan=2>Propositional and predicate logic. Soundness and completeness and theirimplications. Unprovability of formulae in certain systems. Undecidability of problems in computation, including the halting problem. Reasoning about programs. Correctness proofs for both recursive and iterative program constructions. </td></tr><tr><td colspan=2><i>[Note: Enrolment is restricted; see Note 1 above. Offered: F,W,S]</i></td></tr><tr><td colspan=2><i> </i></td></tr><tr><td colspan=2><i>Prereq: (One of CS 136, 138, 146), MATH 135; Honours Mathematics students only.</i></td></tr><tr><td colspan=2><i> Antireq: PMATH 330, SE 212</i></td></tr><p></table></center><Br><P>'
)
