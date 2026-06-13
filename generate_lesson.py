from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── colours ──────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0d1b2a")
ACCENT      = colors.HexColor("#00b4d8")
LIGHT_GRAY  = colors.HexColor("#f5f7fb")
MID_GRAY    = colors.HexColor("#e0e4ef")
CODE_BG     = colors.HexColor("#1e2d3d")
CODE_FG     = colors.HexColor("#cdd9e5")
WHITE       = colors.white
BLACK       = colors.HexColor("#222222")
STEP_BADGE  = colors.HexColor("#00b4d8")

W, H = A4
MARGIN = 18 * mm

# ── styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S("cover_title",
    fontName="Helvetica-Bold", fontSize=36, textColor=WHITE,
    leading=44, alignment=TA_CENTER, spaceAfter=6)

cover_sub = S("cover_sub",
    fontName="Helvetica", fontSize=16, textColor=ACCENT,
    leading=22, alignment=TA_CENTER, spaceAfter=4)

cover_meta = S("cover_meta",
    fontName="Helvetica", fontSize=12, textColor=MID_GRAY,
    leading=18, alignment=TA_CENTER)

h1 = S("h1", fontName="Helvetica-Bold", fontSize=22,
        textColor=DARK_BLUE, spaceBefore=14, spaceAfter=8, leading=28)

h2 = S("h2", fontName="Helvetica-Bold", fontSize=16,
        textColor=DARK_BLUE, spaceBefore=10, spaceAfter=6, leading=22)

h3 = S("h3", fontName="Helvetica-Bold", fontSize=13,
        textColor=ACCENT, spaceBefore=8, spaceAfter=4, leading=18)

body = S("body", fontName="Helvetica", fontSize=10.5,
          textColor=BLACK, leading=16, spaceAfter=6, alignment=TA_JUSTIFY)

bullet = S("bullet", fontName="Helvetica", fontSize=10.5,
            textColor=BLACK, leading=16, spaceAfter=4,
            leftIndent=14, firstLineIndent=-10)

code_style = S("code_style",
    fontName="Courier", fontSize=9, textColor=CODE_FG,
    leading=13, backColor=CODE_BG,
    leftIndent=10, rightIndent=10,
    spaceBefore=4, spaceAfter=4)

tip_style = S("tip_style",
    fontName="Helvetica", fontSize=10, textColor=DARK_BLUE,
    leading=15, backColor=colors.HexColor("#e0f7fd"),
    leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=4,
    borderPadding=(6, 6, 6, 6))

label_style = S("label_style",
    fontName="Helvetica-Bold", fontSize=10, textColor=WHITE,
    leading=14, backColor=ACCENT,
    leftIndent=8, spaceBefore=2, spaceAfter=2)

note_style = S("note_style",
    fontName="Helvetica-Oblique", fontSize=9.5,
    textColor=colors.HexColor("#555555"), leading=14, spaceAfter=4)

# ── helpers ───────────────────────────────────────────────────────────────────
def HR():
    return HRFlowable(width="100%", thickness=1,
                      color=MID_GRAY, spaceAfter=8, spaceBefore=6)

def SP(h=6):
    return Spacer(1, h)

def code_block(lines):
    items = []
    for line in lines:
        items.append(Paragraph(line.replace(" ", "&nbsp;").replace("<","&lt;").replace(">","&gt;"), code_style))
    return items

def tip(text):
    return Paragraph(f"💡 <b>Tip:</b> {text}", tip_style)

def note(text):
    return Paragraph(f"<i>{text}</i>", note_style)

def step_header(num, title):
    return [
        SP(4),
        Paragraph(f"STEP {num}", label_style),
        Paragraph(title, h2),
    ]

def task_box(items):
    rows = [[Paragraph(f"✅ {i}", bullet)] for i in items]
    t = Table(rows, colWidths=[W - 2*MARGIN - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#f0fdf4")),
        ("BOX",        (0,0),(-1,-1), 0.5, colors.HexColor("#86efac")),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    return t

# ── document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(Path(__file__).with_name("NISAB_CSS_Lesson.pdf")),
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=MARGIN,
)

story = []

# ═══════════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════════
cover_bg = Table(
    [[Paragraph("NIFES NISAB 2.0", cover_title)],
     [Paragraph("CSS Practical Lesson", cover_sub)],
     [SP(4)],
     [Paragraph("From Plain HTML to a Fully Styled Website", cover_meta)],
     [SP(8)],
     [Paragraph("A Step-by-Step Guide for Beginners", cover_meta)],
     [SP(20)],
     [Paragraph("📘 &nbsp; Instructor Edition", cover_meta)],
    ],
    colWidths=[W - 2*MARGIN],
)
cover_bg.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,-1), DARK_BLUE),
    ("TOPPADDING",    (0,0),(-1,-1), 18),
    ("BOTTOMPADDING", (0,0),(-1,-1), 18),
    ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ("RIGHTPADDING",  (0,0),(-1,-1), 20),
    ("ROUNDEDCORNERS", [8]),
]))
story += [cover_bg, PageBreak()]

# ═══════════════════════════════════════════════════════════
#  TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════
story += [Paragraph("Table of Contents", h1), HR()]
toc = [
    ("Introduction",                         "How CSS works & linking a stylesheet"),
    ("Step 1 – The Finished Design",          "See where we're going first"),
    ("Step 2 – Assigning Classes & IDs",      "Mark up the HTML so CSS can target it"),
    ("Step 3 – CSS Reset & Body",             "Remove browser defaults"),
    ("Step 4 – Navbar",                       "Flex layout, colours, links"),
    ("Step 5 – Buttons",                      "Shared styles & hover states"),
    ("Step 6 – Hero Section",                 "Background image, overlay, grid"),
    ("Step 7 – About Section",                "Padding, text alignment, max-width"),
    ("Step 8 – Tracks / Cards",               "CSS Grid, card shadows & hover"),
    ("Step 9 – Benefits Section",             "Contrast background, list style"),
    ("Step 10 – Footer",                      "Dark footer, three-column grid"),
    ("Step 11 – Responsive Design",           "@media queries"),
    ("Cheat Sheet",                           "Quick-reference of every property used"),
]
toc_data = [[Paragraph(f"<b>{t}</b>", body), Paragraph(d, note_style)] for t,d in toc]
toc_table = Table(toc_data, colWidths=[68*mm, W - 2*MARGIN - 68*mm])
toc_table.setStyle(TableStyle([
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LINEBELOW",     (0,0),(-1,-1), 0.5, MID_GRAY),
]))
story += [toc_table, PageBreak()]

# ═══════════════════════════════════════════════════════════
#  INTRODUCTION
# ═══════════════════════════════════════════════════════════
story += [Paragraph("Introduction", h1), HR()]
story += [
    Paragraph("What Is CSS?", h2),
    Paragraph(
        "CSS stands for <b>Cascading Style Sheets</b>. While HTML gives a page its "
        "<i>structure</i> (headings, paragraphs, buttons), CSS controls how everything "
        "<i>looks</i> — colours, fonts, spacing, layout, and animations.", body),
    Paragraph(
        "Think of HTML as the skeleton of a building and CSS as the paint, "
        "furniture, and lighting.", body),
    SP(4),

    Paragraph("How CSS Is Linked to HTML", h2),
    Paragraph(
        "We connect a CSS file to our HTML using a &lt;link&gt; tag inside &lt;head&gt;:", body),
    *code_block([
        '&lt;head&gt;',
        '  &lt;link rel="stylesheet" href="style.css"&gt;',
        '&lt;/head&gt;',
    ]),
    note("Both files must be in the same folder."),
    SP(4),

    Paragraph("Three Ways to Apply CSS", h2),
    Paragraph("• <b>Inline</b> — style attribute directly on a tag (not recommended for big projects)", bullet),
    Paragraph("• <b>Internal</b> — &lt;style&gt; tag inside &lt;head&gt; (useful for quick tests)", bullet),
    Paragraph("• <b>External</b> — a separate .css file linked to HTML <b>(best practice — what we use)</b>", bullet),
    SP(4),

    Paragraph("The CSS Syntax", h2),
    *code_block([
        "selector {",
        "    property: value;",
        "}",
    ]),
    Paragraph(
        "The <b>selector</b> targets an HTML element. The <b>property</b> is what you want to change. "
        "The <b>value</b> is what you change it to.", body),
    tip("Every declaration ends with a semicolon (;). Forgetting it is the #1 beginner mistake!"),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 1 – FINISHED DESIGN
# ═══════════════════════════════════════════════════════════
story += step_header(1, "See the Finished Design First")
story += [
    Paragraph(
        "Before writing a single line of CSS, always look at what you are building. "
        "This gives you a mental map and helps you plan which elements need styling.", body),
    Paragraph("The NISAB 2.0 finished page has:", h3),
    Paragraph("• A dark navy navbar with a logo, links, and a teal button", bullet),
    Paragraph("• A full-width hero section with a background image and dark overlay", bullet),
    Paragraph("• A centred About section on a light background", bullet),
    Paragraph("• Six skill cards arranged in a 3-column grid", bullet),
    Paragraph("• A dark Benefits section with a bulleted list", bullet),
    Paragraph("• A 3-column dark footer", bullet),
    SP(4),
    Paragraph("Colour Palette", h3),
]

palette_data = [
    [Paragraph("<b>Name</b>", body), Paragraph("<b>Hex Code</b>", body), Paragraph("<b>Used For</b>", body)],
    [Paragraph("Dark Navy",  body), Paragraph("#0d1b2a", body), Paragraph("Navbar, Benefits bg, Footer bg", body)],
    [Paragraph("Teal Accent", body), Paragraph("#00b4d8", body), Paragraph("Buttons, hover links, accents", body)],
    [Paragraph("Light Gray", body), Paragraph("#f5f7fb", body), Paragraph("Page background", body)],
    [Paragraph("White",      body), Paragraph("#ffffff", body), Paragraph("Cards, text on dark bg", body)],
    [Paragraph("Dark Text",  body), Paragraph("#222222", body), Paragraph("Body text", body)],
]
palette_table = Table(palette_data, colWidths=[38*mm, 38*mm, W - 2*MARGIN - 76*mm])
palette_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",  (0,0),(-1,0), WHITE),
    ("FONTNAME",   (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",       (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
]))
story += [palette_table, SP(8),
    tip("Save this colour palette. You will use these exact hex codes throughout the lesson."),
    PageBreak()]

# ═══════════════════════════════════════════════════════════
#  STEP 2 – ASSIGNING CLASSES & IDs
# ═══════════════════════════════════════════════════════════
story += step_header(2, "Assigning Classes and IDs to the HTML")
story += [
    Paragraph("Why Do We Need Classes and IDs?", h2),
    Paragraph(
        "CSS needs a way to <i>target</i> specific elements. Without classes or IDs, "
        "writing <b>h2 { color: red }</b> would turn <i>every</i> h2 on the page red. "
        "Classes and IDs let us be precise.", body),
    SP(4),

    Paragraph("Classes vs IDs — The Rule", h2),
]

diff_data = [
    [Paragraph("<b>Feature</b>", body), Paragraph("<b>Class (.name)</b>", body), Paragraph("<b>ID (#name)</b>", body)],
    [Paragraph("Usage",    body), Paragraph("Many elements can share it", body), Paragraph("Only ONE element per page", body)],
    [Paragraph("HTML syntax", body), Paragraph('class="navbar"', body), Paragraph('id="hero"', body)],
    [Paragraph("CSS syntax", body), Paragraph(".navbar { }", body), Paragraph("#hero { }", body)],
    [Paragraph("Best for", body), Paragraph("Reusable styles (cards, buttons)", body), Paragraph("Unique sections (used rarely in CSS)", body)],
]
diff_table = Table(diff_data, colWidths=[32*mm, 68*mm, W - 2*MARGIN - 100*mm])
diff_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",  (0,0),(-1,0), WHITE),
    ("FONTNAME",   (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",       (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("VALIGN",     (0,0),(-1,-1), "TOP"),
]))
story += [diff_table, SP(10)]

story += [Paragraph("Your Task: Add These Classes to the HTML", h3)]

classes_data = [
    [Paragraph("<b>HTML Element</b>", body), Paragraph("<b>Add This Class</b>", body), Paragraph("<b>Why</b>", body)],
    [Paragraph("&lt;header&gt;",         body), Paragraph('class="navbar"',          body), Paragraph("Styles the top navigation bar",    body)],
    [Paragraph("&lt;nav&gt;",            body), Paragraph('class="nav-container"',   body), Paragraph("Controls flex layout inside nav",  body)],
    [Paragraph("&lt;h1&gt; (logo)",      body), Paragraph('class="logo"',            body), Paragraph("White text styling for the logo",  body)],
    [Paragraph("&lt;ul&gt; (nav links)", body), Paragraph('class="nav-links"',       body), Paragraph("Horizontal flex list with gaps",   body)],
    [Paragraph("Navbar &lt;button&gt;",  body), Paragraph('class="btn"',             body), Paragraph("Reusable teal button style",       body)],
    [Paragraph("1st &lt;section&gt;",    body), Paragraph('class="hero"',            body), Paragraph("Full-width hero image section",    body)],
    [Paragraph("Buttons div in hero",    body), Paragraph('class="hero-buttons"',    body), Paragraph("Flex row for two buttons",         body)],
    [Paragraph("Features div in hero",   body), Paragraph('class="hero-features"',   body), Paragraph("4-column grid of feature badges",  body)],
    [Paragraph("Learn More button",      body), Paragraph('class="btn-outline"',     body), Paragraph("Ghost/outline button variant",     body)],
    [Paragraph("2nd &lt;section&gt;",    body), Paragraph('class="about"',           body), Paragraph("Centred about section",           body)],
    [Paragraph("3rd &lt;section&gt;",    body), Paragraph('class="tracks"',          body), Paragraph("Skill tracks section",            body)],
    [Paragraph("Wrapper div in tracks",  body), Paragraph('class="track-container"', body), Paragraph("3-column CSS grid container",     body)],
    [Paragraph("Each skill div",         body), Paragraph('class="card"',            body), Paragraph("White card with shadow & hover",  body)],
    [Paragraph("4th &lt;section&gt;",    body), Paragraph('class="benefits"',        body), Paragraph("Dark benefits section",          body)],
    [Paragraph("&lt;footer&gt;",         body), Paragraph('class="footer"',          body), Paragraph("Dark footer background",         body)],
    [Paragraph("Footer columns div",     body), Paragraph('class="footer-grid"',     body), Paragraph("3-column grid in footer",        body)],
    [Paragraph("Copyright &lt;p&gt;",    body), Paragraph('class="copyright"',       body), Paragraph("Centred copyright line",         body)],
]
ct = Table(classes_data, colWidths=[44*mm, 44*mm, W - 2*MARGIN - 88*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ("FONTSIZE",       (0,1),(-1,-1), 9.5),
]))
story += [ct, SP(8)]
story += [
    Paragraph("How to Add a Class — Example", h3),
    Paragraph("Before (raw HTML):", note_style),
    *code_block(["&lt;header&gt;"]),
    Paragraph("After (with class):", note_style),
    *code_block(['&lt;header class="navbar"&gt;']),
    SP(4),
    tip("Use only lowercase letters and hyphens in class names. Never use spaces — that creates two classes."),
    SP(4),
    task_box([
        "Open your raw HTML file",
        "Add every class from the table above",
        "Save the file — it won't look different yet. That's normal!",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 3 – RESET & BODY
# ═══════════════════════════════════════════════════════════
story += step_header(3, "CSS Reset & Body Styles")
story += [
    Paragraph("Why We Need a Reset", h2),
    Paragraph(
        "Every browser (Chrome, Firefox, Safari) applies its own default margin and "
        "padding to elements. This causes pages to look slightly different in each browser. "
        "A CSS reset removes all of these defaults so we start from a clean slate.", body),
    SP(4),
    Paragraph("Create your style.css file and type this first:", h3),
    *code_block([
        "/* RESET */",
        "* {",
        "    margin: 0;",
        "    padding: 0;",
        "    box-sizing: border-box;",
        "}",
    ]),
    SP(4),
    Paragraph("Breaking It Down", h3),
]

reset_data = [
    [Paragraph("<b>Property</b>", body),  Paragraph("<b>Value</b>", body), Paragraph("<b>What It Does</b>", body)],
    [Paragraph("*",               body),  Paragraph("(selector)",   body), Paragraph("Targets EVERY element on the page", body)],
    [Paragraph("margin",          body),  Paragraph("0",            body), Paragraph("Removes all default outer spacing", body)],
    [Paragraph("padding",         body),  Paragraph("0",            body), Paragraph("Removes all default inner spacing", body)],
    [Paragraph("box-sizing",      body),  Paragraph("border-box",   body), Paragraph("Padding is included inside the element's total width", body)],
]
rt = Table(reset_data, colWidths=[34*mm, 30*mm, W - 2*MARGIN - 64*mm])
rt.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "TOP"),
]))
story += [rt, SP(10)]

story += [
    Paragraph("Body Styles", h2),
    Paragraph("Now add the body block right after the reset:", body),
    *code_block([
        "/* BODY */",
        "body {",
        "    font-family: Arial, Helvetica, sans-serif;",
        "    line-height: 1.6;",
        "    background: #f5f7fb;",
        "    color: #222;",
        "}",
    ]),
    SP(4),
    Paragraph("• <b>font-family</b>: Sets the font for the whole page. We list backups in case Arial isn't available.", bullet),
    Paragraph("• <b>line-height: 1.6</b>: Adds vertical breathing room between lines of text.", bullet),
    Paragraph("• <b>background: #f5f7fb</b>: Very light blue-grey page background.", bullet),
    Paragraph("• <b>color: #222</b>: Near-black default text colour.", bullet),
    SP(6),
    tip("font-family, background, and color set on body are <i>inherited</i> by all child elements — you don't need to repeat them everywhere."),
    SP(4),
    task_box([
        "Create an empty file called style.css in the same folder as your HTML",
        "Add the reset block",
        "Add the body block",
        "Save and open your HTML in a browser — the font should change",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 4 – NAVBAR
# ═══════════════════════════════════════════════════════════
story += step_header(4, "Styling the Navbar")
story += [
    Paragraph("Concept: Flexbox", h2),
    Paragraph(
        "Flexbox is a CSS layout tool that arranges items in a row (or column). "
        "Setting <b>display: flex</b> on a container turns its direct children into "
        "flex items that can be aligned, spaced, and sized together.", body),
    SP(4),
    Paragraph("Add this to style.css:", h3),
    *code_block([
        "/* NAVBAR */",
        ".navbar {",
        "    background: #0d1b2a;",
        "    padding: 20px 8%;",
        "}",
        "",
        ".nav-container {",
        "    display: flex;",
        "    justify-content: space-between;",
        "    align-items: center;",
        "}",
        "",
        ".logo {",
        "    color: white;",
        "}",
        "",
        ".nav-links {",
        "    display: flex;",
        "    gap: 25px;",
        "    list-style: none;",
        "}",
        "",
        ".nav-links a {",
        "    text-decoration: none;",
        "    color: white;",
        "    font-size: 14px;",
        "}",
        "",
        ".nav-links a:hover {",
        "    color: #00b4d8;",
        "}",
    ]),
    SP(6),
    Paragraph("Property Glossary for This Step", h3),
]

nav_data = [
    [Paragraph("<b>Property</b>", body),    Paragraph("<b>Value Used</b>",      body), Paragraph("<b>What It Does</b>", body)],
    [Paragraph("background",       body),    Paragraph("#0d1b2a",                body), Paragraph("Dark navy background on the navbar",             body)],
    [Paragraph("padding",          body),    Paragraph("20px 8%",                body), Paragraph("20px top/bottom, 8% left/right — creates breathing room", body)],
    [Paragraph("display",          body),    Paragraph("flex",                   body), Paragraph("Enables flexbox on .nav-container",              body)],
    [Paragraph("justify-content",  body),    Paragraph("space-between",          body), Paragraph("Pushes logo left, links centre, button right",   body)],
    [Paragraph("align-items",      body),    Paragraph("center",                 body), Paragraph("Vertically centres all items",                   body)],
    [Paragraph("gap",              body),    Paragraph("25px",                   body), Paragraph("Space between each nav link",                   body)],
    [Paragraph("list-style",       body),    Paragraph("none",                   body), Paragraph("Removes the bullet points from the &lt;ul&gt;", body)],
    [Paragraph("text-decoration",  body),    Paragraph("none",                   body), Paragraph("Removes the underline from &lt;a&gt; tags",     body)],
    [Paragraph(":hover",           body),    Paragraph("(pseudo-class)",         body), Paragraph("Applies styles when the user mouses over",      body)],
]
nt = Table(nav_data, colWidths=[38*mm, 32*mm, W - 2*MARGIN - 70*mm])
nt.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ("FONTSIZE",       (0,1),(-1,-1), 9.5),
]))
story += [nt, SP(6),
    tip("justify-content controls the MAIN axis (horizontal by default). align-items controls the CROSS axis (vertical)."),
    SP(4),
    task_box([
        "Add all navbar styles to style.css",
        "Save and refresh — your navbar should be dark with a teal hover on links",
        "Try changing justify-content to flex-start and see what happens",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 5 – BUTTONS
# ═══════════════════════════════════════════════════════════
story += step_header(5, "Styling the Buttons")
story += [
    Paragraph(
        "We have two button types: a filled teal <b>.btn</b> and a transparent "
        "<b>.btn-outline</b>. Both share the same padding and border-radius, only the "
        "background and border differ. This is the power of reusable classes.", body),
    SP(4),
    *code_block([
        "/* BUTTONS */",
        ".btn {",
        "    background: #00b4d8;",
        "    color: white;",
        "    border: none;",
        "    padding: 12px 20px;",
        "    border-radius: 5px;",
        "    cursor: pointer;",
        "}",
        "",
        ".btn:hover {",
        "    background: #0096c7;",
        "}",
        "",
        ".btn-outline {",
        "    background: transparent;",
        "    border: 2px solid white;",
        "    color: white;",
        "    padding: 12px 20px;",
        "    border-radius: 5px;",
        "    cursor: pointer;",
        "}",
    ]),
    SP(6),
    Paragraph("New Properties", h3),
    Paragraph("• <b>border: none</b> — removes the default grey border browsers add to buttons", bullet),
    Paragraph("• <b>border-radius: 5px</b> — rounds the corners slightly", bullet),
    Paragraph("• <b>cursor: pointer</b> — shows the hand cursor when hovering, signalling it's clickable", bullet),
    Paragraph("• <b>background: transparent</b> — makes the button see-through (shows the hero image behind)", bullet),
    SP(6),
    Paragraph("Understanding Padding Shorthand", h3),
    Paragraph("padding: 12px 20px means:", body),
    Paragraph("• First value (12px) = top &amp; bottom padding", bullet),
    Paragraph("• Second value (20px) = left &amp; right padding", bullet),
    SP(4),
    tip("You can use padding: 12px 20px 12px 20px (top, right, bottom, left — clockwise) for full control."),
    SP(4),
    task_box([
        "Add both button styles",
        "Hover over the Register Now button — it should darken slightly",
        "Notice how both buttons share the same padding but look different",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 6 – HERO
# ═══════════════════════════════════════════════════════════
story += step_header(6, "Styling the Hero Section")
story += [
    Paragraph("Concept: Background Images & Overlays", h2),
    Paragraph(
        "A background image alone can make text hard to read. We fix this by adding "
        "a dark semi-transparent overlay using a CSS gradient layered on top of the image.", body),
    SP(4),
    *code_block([
        "/* HERO */",
        ".hero {",
        "    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),",
        "    url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f');",
        "    background-size: cover;",
        "    background-position: center;",
        "    color: white;",
        "    text-align: center;",
        "    padding: 120px 10%;",
        "}",
        "",
        ".hero h2 {",
        "    font-size: 55px;",
        "    margin-bottom: 20px;",
        "}",
        "",
        ".hero p {",
        "    max-width: 700px;",
        "    margin: auto;",
        "    margin-bottom: 30px;",
        "}",
        "",
        ".hero-buttons {",
        "    display: flex;",
        "    justify-content: center;",
        "    gap: 20px;",
        "    margin-bottom: 40px;",
        "}",
        "",
        ".hero-features {",
        "    display: grid;",
        "    grid-template-columns: repeat(4, 1fr);",
        "    gap: 20px;",
        "}",
        "",
        ".hero-features div {",
        "    background: rgba(255,255,255,0.1);",
        "    padding: 20px;",
        "    border-radius: 10px;",
        "}",
    ]),
    SP(6),
    Paragraph("Key Concepts Explained", h3),
    Paragraph(
        "<b>linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6))</b> — creates a dark "
        "overlay. rgba(0,0,0,0.6) is black at 60% opacity. Placing it before the URL "
        "layers it on top of the image.", body),
    Paragraph(
        "<b>background-size: cover</b> — stretches the image to fill the entire section "
        "without leaving gaps.", body),
    Paragraph(
        "<b>max-width: 700px; margin: auto</b> — limits the paragraph width to 700px "
        "and centres it horizontally.", body),
    Paragraph(
        "<b>grid-template-columns: repeat(4, 1fr)</b> — creates 4 equal columns. "
        "<b>1fr</b> means 'one fraction of available space'.", body),
    Paragraph(
        "<b>rgba(255,255,255,0.1)</b> — white at 10% opacity, creating a frosted "
        "glass look on the feature badges.", body),
    SP(4),
    tip("repeat(4, 1fr) is shorthand for 1fr 1fr 1fr 1fr — saves typing and is easier to change."),
    SP(4),
    task_box([
        "Add all hero styles",
        "Refresh — you should see the background image with a dark overlay",
        "Try changing the 0.6 in rgba to 0.2 to see a lighter overlay",
        "Change repeat(4, 1fr) to repeat(2, 1fr) and see the layout shift",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 7 – ABOUT
# ═══════════════════════════════════════════════════════════
story += step_header(7, "Styling the About Section")
story += [
    Paragraph(
        "The About section is simple — it uses padding, centred text, and a font-size "
        "on the heading. This step reinforces spacing concepts.", body),
    SP(4),
    *code_block([
        "/* ABOUT */",
        ".about {",
        "    padding: 80px 10%;",
        "    text-align: center;",
        "}",
        "",
        ".about h2 {",
        "    margin-bottom: 20px;",
        "    font-size: 40px;",
        "}",
    ]),
    SP(6),
    Paragraph("The Box Model", h2),
    Paragraph(
        "Every HTML element is a rectangular box made of four layers from inside out:", body),
]

box_data = [
    [Paragraph("<b>Layer</b>", body), Paragraph("<b>Property</b>", body), Paragraph("<b>Description</b>", body)],
    [Paragraph("Content",  body), Paragraph("width / height", body), Paragraph("The actual text or image",          body)],
    [Paragraph("Padding",  body), Paragraph("padding",        body), Paragraph("Space inside the border",           body)],
    [Paragraph("Border",   body), Paragraph("border",         body), Paragraph("The visible outline around the box", body)],
    [Paragraph("Margin",   body), Paragraph("margin",         body), Paragraph("Space outside the border",          body)],
]
bt = Table(box_data, colWidths=[32*mm, 36*mm, W - 2*MARGIN - 68*mm])
bt.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
]))
story += [bt, SP(6),
    tip("Use your browser's DevTools (F12 → Elements) to see the Box Model visually for any element."),
    SP(4),
    task_box([
        "Add the About section styles",
        "Try changing padding: 80px 10% to padding: 20px 10% — notice how squashed it becomes",
        "Restore it to 80px when done",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 8 – TRACKS / CARDS
# ═══════════════════════════════════════════════════════════
story += step_header(8, "Skill Track Cards — CSS Grid & Hover Effects")
story += [
    Paragraph("Concept: CSS Grid", h2),
    Paragraph(
        "CSS Grid is a two-dimensional layout system. Unlike Flexbox (one row or column), "
        "Grid lets you define both rows and columns. We use it here to create a "
        "3-column layout of skill cards.", body),
    SP(4),
    *code_block([
        "/* TRACKS */",
        ".tracks {",
        "    padding: 80px 10%;",
        "}",
        "",
        ".tracks h2 {",
        "    text-align: center;",
        "    margin-bottom: 50px;",
        "    font-size: 40px;",
        "}",
        "",
        ".track-container {",
        "    display: grid;",
        "    grid-template-columns: repeat(3, 1fr);",
        "    gap: 25px;",
        "}",
        "",
        ".card {",
        "    background: white;",
        "    padding: 30px;",
        "    border-radius: 10px;",
        "    box-shadow: 0 5px 15px rgba(0,0,0,0.1);",
        "    transition: 0.3s;",
        "}",
        "",
        ".card:hover {",
        "    transform: translateY(-10px);",
        "}",
    ]),
    SP(6),
    Paragraph("Understanding box-shadow", h3),
    Paragraph(
        "box-shadow: 0 5px 15px rgba(0,0,0,0.1) has four parts:", body),
    Paragraph("• <b>0</b> — horizontal offset (no shadow to the left or right)", bullet),
    Paragraph("• <b>5px</b> — vertical offset (shadow 5px below the card)", bullet),
    Paragraph("• <b>15px</b> — blur radius (how soft/blurry the shadow is)", bullet),
    Paragraph("• <b>rgba(0,0,0,0.1)</b> — black at 10% opacity (very subtle)", bullet),
    SP(6),
    Paragraph("Understanding transition & transform", h3),
    Paragraph(
        "<b>transition: 0.3s</b> tells the browser to animate any property change over "
        "0.3 seconds. Without it, the hover effect would be instant and jarring.", body),
    Paragraph(
        "<b>transform: translateY(-10px)</b> moves the card 10px <i>upward</i> on hover, "
        "creating a 'lift' effect. Negative Y = up.", body),
    SP(4),
    tip("transition must be on the base element (.card), not on .card:hover, so it also animates back smoothly when you mouse out."),
    SP(4),
    task_box([
        "Add all track and card styles",
        "Hover over a card — it should lift upward",
        "Try box-shadow: 0 10px 30px rgba(0,180,216,0.3) for a teal glow",
        "Try translateY(-20px) for a more dramatic lift",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 9 – BENEFITS
# ═══════════════════════════════════════════════════════════
story += step_header(9, "Benefits Section — Dark Background & Lists")
story += [
    Paragraph(
        "The Benefits section uses the same dark navy as the navbar to create "
        "visual contrast against the light sections around it.", body),
    SP(4),
    *code_block([
        "/* BENEFITS */",
        ".benefits {",
        "    background: #0d1b2a;",
        "    color: white;",
        "    padding: 80px 10%;",
        "}",
        "",
        ".benefits h2 {",
        "    margin-bottom: 20px;",
        "}",
        "",
        ".benefits ul {",
        "    padding-left: 20px;",
        "}",
    ]),
    SP(6),
    Paragraph("Alternating Dark & Light Sections", h3),
    Paragraph(
        "Good web design uses alternating light and dark sections to create visual rhythm. "
        "Looking at our page so far:", body),
    Paragraph("• Navbar — Dark", bullet),
    Paragraph("• Hero — Dark (image overlay)", bullet),
    Paragraph("• About — Light (#f5f7fb)", bullet),
    Paragraph("• Tracks — Light (#f5f7fb)", bullet),
    Paragraph("• Benefits — Dark (#0d1b2a) ← this step", bullet),
    Paragraph("• Footer — Dark (#111)", bullet),
    SP(4),
    tip("Inheriting color: white on .benefits means all text inside it (including li items) becomes white automatically."),
    SP(4),
    task_box([
        "Add the benefits styles",
        "Notice how color: white on the parent automatically colours the list items",
        "Try removing padding-left: 20px to see the bullets disappear off-screen",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 10 – FOOTER
# ═══════════════════════════════════════════════════════════
story += step_header(10, "Styling the Footer")
story += [
    Paragraph(
        "The footer uses a three-column grid layout with a very dark background. "
        "This is the same grid concept as the track cards, just with different content.", body),
    SP(4),
    *code_block([
        "/* FOOTER */",
        ".footer {",
        "    background: #111;",
        "    color: white;",
        "    padding: 60px 10%;",
        "}",
        "",
        ".footer-grid {",
        "    display: grid;",
        "    grid-template-columns: repeat(3, 1fr);",
        "    gap: 40px;",
        "}",
        "",
        ".copyright {",
        "    margin-top: 40px;",
        "    text-align: center;",
        "}",
    ]),
    SP(6),
    Paragraph("Flexbox vs Grid — When to Use Which?", h3),
]

fvg_data = [
    [Paragraph("<b>Use Flexbox when…</b>", body),       Paragraph("<b>Use Grid when…</b>", body)],
    [Paragraph("Layout is one-dimensional (row OR column)", body), Paragraph("Layout is two-dimensional (rows AND columns)", body)],
    [Paragraph("Items should size themselves naturally",   body), Paragraph("You need precise column/row control",          body)],
    [Paragraph("Navbar, button groups, hero buttons",      body), Paragraph("Cards, footer columns, feature grids",        body)],
]
fvg = Table(fvg_data, colWidths=[(W - 2*MARGIN)/2, (W - 2*MARGIN)/2])
fvg.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "TOP"),
]))
story += [fvg, SP(6),
    tip("gap works identically in both Flexbox and Grid — it sets the space between items."),
    SP(4),
    task_box([
        "Add all footer styles",
        "Your page is now fully styled on desktop!",
        "Try changing repeat(3, 1fr) to repeat(2, 1fr) to see two columns",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  STEP 11 – RESPONSIVE
# ═══════════════════════════════════════════════════════════
story += step_header(11, "Responsive Design — @media Queries")
story += [
    Paragraph("What Is Responsive Design?", h2),
    Paragraph(
        "Responsive design means the page looks good on all screen sizes — desktop, tablet, "
        "and mobile. CSS media queries let you apply different styles below certain widths.", body),
    SP(4),
    Paragraph("Syntax of a Media Query", h3),
    *code_block([
        "@media (max-width: 900px) {",
        "    /* Styles inside here ONLY apply when",
        "       the screen is 900px wide or less */",
        "}",
    ]),
    SP(4),
    Paragraph("Add This at the Very End of style.css", h3),
    *code_block([
        "/* RESPONSIVE */",
        "@media (max-width: 900px) {",
        "",
        "    .nav-container {",
        "        flex-direction: column;",
        "        gap: 20px;",
        "    }",
        "",
        "    .nav-links {",
        "        flex-wrap: wrap;",
        "        justify-content: center;",
        "    }",
        "",
        "    .hero h2 {",
        "        font-size: 38px;",
        "    }",
        "",
        "    .hero-features {",
        "        grid-template-columns: 1fr 1fr;",
        "    }",
        "",
        "    .track-container {",
        "        grid-template-columns: 1fr;",
        "    }",
        "",
        "    .footer-grid {",
        "        grid-template-columns: 1fr;",
        "    }",
        "}",
    ]),
    SP(6),
    Paragraph("What Each Rule Does", h3),
    Paragraph("• <b>flex-direction: column</b> — stacks the logo, links, and button vertically on small screens", bullet),
    Paragraph("• <b>flex-wrap: wrap</b> — allows nav links to wrap to a second line if needed", bullet),
    Paragraph("• <b>font-size: 38px</b> — reduces the hero heading so it doesn't overflow on mobile", bullet),
    Paragraph("• <b>1fr 1fr</b> — changes feature grid to 2 columns instead of 4", bullet),
    Paragraph("• <b>1fr</b> — changes cards and footer to a single column for easy scrolling", bullet),
    SP(4),
    tip("Test your responsive styles by resizing the browser window or pressing F12 → Toggle Device Toolbar in Chrome."),
    SP(4),
    task_box([
        "Add the media query block",
        "Open DevTools (F12) and click the mobile icon",
        "Select iPhone SE or similar — the layout should stack",
        "Congratulations! Your page is now fully styled and responsive 🎉",
    ]),
    PageBreak()
]

# ═══════════════════════════════════════════════════════════
#  CHEAT SHEET
# ═══════════════════════════════════════════════════════════
story += [Paragraph("CSS Cheat Sheet — All Properties Used", h1), HR()]

cheat = [
    [Paragraph("<b>Property</b>", body), Paragraph("<b>Example Value</b>", body), Paragraph("<b>What It Does</b>", body)],
    [Paragraph("background",          body), Paragraph("#0d1b2a",                    body), Paragraph("Sets background colour or image",            body)],
    [Paragraph("color",               body), Paragraph("white",                      body), Paragraph("Sets text colour",                          body)],
    [Paragraph("font-family",         body), Paragraph("Arial, sans-serif",          body), Paragraph("Sets the font",                             body)],
    [Paragraph("font-size",           body), Paragraph("55px",                       body), Paragraph("Sets text size",                            body)],
    [Paragraph("line-height",         body), Paragraph("1.6",                        body), Paragraph("Spacing between lines",                     body)],
    [Paragraph("padding",             body), Paragraph("20px 8%",                    body), Paragraph("Space inside element",                      body)],
    [Paragraph("margin",              body), Paragraph("0 auto",                     body), Paragraph("Space outside element / centering",         body)],
    [Paragraph("border",              body), Paragraph("2px solid white",            body), Paragraph("Border around element",                     body)],
    [Paragraph("border-radius",       body), Paragraph("10px",                       body), Paragraph("Rounds corners",                            body)],
    [Paragraph("border-none",         body), Paragraph("none",                       body), Paragraph("Removes border",                            body)],
    [Paragraph("display",             body), Paragraph("flex / grid",                body), Paragraph("Enables Flexbox or Grid",                   body)],
    [Paragraph("justify-content",     body), Paragraph("space-between / center",     body), Paragraph("Aligns items on main axis",                 body)],
    [Paragraph("align-items",         body), Paragraph("center",                     body), Paragraph("Aligns items on cross axis",                body)],
    [Paragraph("gap",                 body), Paragraph("25px",                       body), Paragraph("Space between flex/grid items",             body)],
    [Paragraph("flex-direction",      body), Paragraph("column",                     body), Paragraph("Stacks flex items vertically",              body)],
    [Paragraph("flex-wrap",           body), Paragraph("wrap",                       body), Paragraph("Allows flex items to wrap",                 body)],
    [Paragraph("grid-template-cols",  body), Paragraph("repeat(3, 1fr)",             body), Paragraph("Defines grid columns",                      body)],
    [Paragraph("list-style",          body), Paragraph("none",                       body), Paragraph("Removes bullet points",                     body)],
    [Paragraph("text-decoration",     body), Paragraph("none",                       body), Paragraph("Removes underline from links",              body)],
    [Paragraph("text-align",          body), Paragraph("center",                     body), Paragraph("Aligns text horizontally",                  body)],
    [Paragraph("max-width",           body), Paragraph("700px",                      body), Paragraph("Limits element's maximum width",            body)],
    [Paragraph("box-shadow",          body), Paragraph("0 5px 15px rgba(0,0,0,.1)", body), Paragraph("Adds shadow under element",                body)],
    [Paragraph("transition",          body), Paragraph("0.3s",                       body), Paragraph("Animates property changes",                 body)],
    [Paragraph("transform",           body), Paragraph("translateY(-10px)",          body), Paragraph("Moves/rotates/scales element",              body)],
    [Paragraph("cursor",              body), Paragraph("pointer",                    body), Paragraph("Shows hand cursor on hover",                body)],
    [Paragraph("background-size",     body), Paragraph("cover",                      body), Paragraph("Stretches image to fill element",           body)],
    [Paragraph("background-position", body), Paragraph("center",                     body), Paragraph("Positions background image",               body)],
    [Paragraph("@media",              body), Paragraph("(max-width: 900px)",         body), Paragraph("Applies styles at certain screen sizes",    body)],
    [Paragraph(":hover",              body), Paragraph("(pseudo-class)",             body), Paragraph("Styles applied on mouse hover",             body)],
    [Paragraph("rgba()",              body), Paragraph("rgba(0,0,0,0.6)",            body), Paragraph("Colour with opacity (0=transparent, 1=solid)", body)],
]
ct2 = Table(cheat, colWidths=[40*mm, 48*mm, W - 2*MARGIN - 88*mm])
ct2.setStyle(TableStyle([
    ("BACKGROUND",     (0,0),(-1,0), DARK_BLUE),
    ("TEXTCOLOR",      (0,0),(-1,0), WHITE),
    ("FONTNAME",       (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1),(-1,-1), [LIGHT_GRAY, WHITE]),
    ("GRID",           (0,0),(-1,-1), 0.5, MID_GRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 4),
    ("LEFTPADDING",    (0,0),(-1,-1), 6),
    ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ("FONTSIZE",       (0,1),(-1,-1), 9),
]))
story += [ct2, SP(10)]

# Final note
final = Table(
    [[Paragraph(
        "🎓 <b>Well done!</b> You have gone from a completely unstyled HTML page to a "
        "fully designed, responsive website using real CSS techniques used by professional "
        "developers every day. Keep experimenting — try changing colours, font sizes, "
        "and layouts to make the design your own.", body
    )]],
    colWidths=[W - 2*MARGIN]
)
final.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#e0f7fd")),
    ("BOX",        (0,0),(-1,-1), 1, ACCENT),
    ("TOPPADDING",    (0,0),(-1,-1), 12),
    ("BOTTOMPADDING", (0,0),(-1,-1), 12),
    ("LEFTPADDING",   (0,0),(-1,-1), 14),
    ("RIGHTPADDING",  (0,0),(-1,-1), 14),
]))
story += [final]

# ── build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print("Done!")