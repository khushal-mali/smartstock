import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# ==============================================================================
# SMARTSTOCK BCA PROJECT REPORT BUILDER (60-80 PAGES EXCLUDING CODING)
# ==============================================================================

def build_full_report(toc_map=None, lof_map=None, lot_map=None):
    doc = Document()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DIAG_DIR = os.path.join(BASE_DIR, 'diagrams')
    SCR_DIR = os.path.join(BASE_DIR, 'screenshots')
    OUTPUT_FILE = os.path.join(BASE_DIR, 'SmartStock_BCA_Project_Report.docx')

    if toc_map is None:
        toc_map = {}
    if lof_map is None:
        lof_map = {}
    if lot_map is None:
        lot_map = {}

    def get_toc(key, default):
        return str(toc_map.get(key, default))
    def get_lof(key, default):
        return str(lof_map.get(key, default))
    def get_lot(key, default):
        return str(lot_map.get(key, default))

    # XML Formatting Helpers
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def add_page_number_to_run(run):
        fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        r = run._r
        r.append(fldChar1)
        r.append(instrText)
        r.append(fldChar2)
        r.append(fldChar3)

    # --------------------------------------------------------------------------
    # Section 1: Front Matter (Lower Roman Numerals)
    # --------------------------------------------------------------------------
    sec_front = doc.sections[0]
    sec_front.top_margin = Inches(1.0)
    sec_front.bottom_margin = Inches(1.0)
    sec_front.left_margin = Inches(1.5)
    sec_front.right_margin = Inches(1.0)
    sec_front.page_width = Inches(8.27)
    sec_front.page_height = Inches(11.69)
    # Cover page has NO page number
    sec_front.different_first_page_header_footer = True

    sectPr_front = sec_front._sectPr
    pgNumType_front = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
    sectPr_front.append(pgNumType_front)

    # Normal footer for pages after cover page (ii, iii, iv...)
    footer_front = sec_front.footer
    f_p_front = footer_front.paragraphs[0]
    f_p_front.text = ""  # Clean slate
    f_p_front.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run_front = f_p_front.add_run()
    f_run_front.font.name = 'Times New Roman'
    f_run_front.font.size = Pt(10)
    f_run_front.font.color.rgb = RGBColor(100, 116, 139)
    add_page_number_to_run(f_run_front)

    # Global Style Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    # Heading Styles Setup for Word Navigation & Outline
    h1_style = doc.styles['Heading 1']
    h1_style.font.name = 'Times New Roman'
    h1_style.font.size = Pt(14)
    h1_style.font.bold = True
    h1_style.font.color.rgb = RGBColor(15, 23, 42)

    h2_style = doc.styles['Heading 2']
    h2_style.font.name = 'Times New Roman'
    h2_style.font.size = Pt(13)
    h2_style.font.bold = True
    h2_style.font.color.rgb = RGBColor(30, 41, 59)

    h3_style = doc.styles['Heading 3']
    h3_style.font.name = 'Times New Roman'
    h3_style.font.size = Pt(12)
    h3_style.font.bold = True
    h3_style.font.color.rgb = RGBColor(51, 65, 85)

    # Typography Helpers
    def add_chapter_title(text):
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h1(text):
        p = doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_h3(text):
        p = doc.add_paragraph(style='Heading 3')
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_table_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_figure(image_path, caption_text, width=Inches(5.5)):
        if os.path.exists(image_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run()
            run.add_picture(image_path, width=width)
            
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_before = Pt(4)
            cap_p.paragraph_format.space_after = Pt(12)
            c_run = cap_p.add_run(caption_text)
            c_run.font.name = 'Times New Roman'
            c_run.font.size = Pt(10.5)
            c_run.font.bold = True
            c_run.font.color.rgb = RGBColor(71, 85, 105)

    def create_table(headers, data, col_widths, font_size_pt=10.5):
        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
        
        # Header Row
        hdr_row = tbl.rows[0]
        hdr_trPr = hdr_row._tr.get_or_add_trPr()
        hdr_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        hdr_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for i, h_text in enumerate(headers):
            cell = hdr_row.cells[i]
            cell.width = col_widths[i]
            set_cell_background(cell, "1E293B")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(h_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = tbl.rows[r_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(cell_value))
                run.font.name = 'Times New Roman'
                run.font.size = Pt(font_size_pt)
                run.font.color.rgb = RGBColor(30, 41, 59)
                
        # Spacing after table
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)
        return tbl

    def add_code_block(title, code_str):
        add_h3(title)
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_str)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(15, 23, 42)
        
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)

    # ==========================================================================
    # 1. FRONT MATTER
    # ==========================================================================

    # TITLE / COVER PAGE (Precisely proportioned to fit strictly on Page 1)
    p_cov_top = doc.add_paragraph()
    p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_top.paragraph_format.line_spacing = 1.15
    p_cov_top.paragraph_format.space_before = Pt(20)
    p_cov_top.paragraph_format.space_after = Pt(6)
    r1 = p_cov_top.add_run("Project Report\nOn")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(71, 85, 105)

    p_cov_title = doc.add_paragraph()
    p_cov_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_title.paragraph_format.line_spacing = 1.15
    p_cov_title.paragraph_format.space_before = Pt(6)
    p_cov_title.paragraph_format.space_after = Pt(16)
    r2 = p_cov_title.add_run("“SMARTSTOCK – INVENTORY MANAGEMENT SYSTEM”")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(17)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 23, 42)

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_sub.paragraph_format.line_spacing = 1.15
    p_cov_sub.paragraph_format.space_before = Pt(6)
    p_cov_sub.paragraph_format.space_after = Pt(24)
    r3 = p_cov_sub.add_run("Submitted to Uttaranchal University in partial fulfilment of the\nrequirements for the award of the Degree of\n\n")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(11)
    r4 = p_cov_sub.add_run("BACHELOR OF COMPUTER APPLICATIONS\n(BCA – SEMESTER V)")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(13)
    r4.font.bold = True
    r4.font.color.rgb = RGBColor(30, 41, 59)

    p_cov_pers = doc.add_paragraph()
    p_cov_pers.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_pers.paragraph_format.line_spacing = 1.2
    p_cov_pers.paragraph_format.space_before = Pt(12)
    p_cov_pers.paragraph_format.space_after = Pt(28)
    r5 = p_cov_pers.add_run("Submitted by:\n")
    r5.font.name = 'Times New Roman'
    r5.font.size = Pt(11)
    r5.font.bold = True
    r6 = p_cov_pers.add_run("KHUSHAL ASARAM MALI\n(Learner ID: 2413020402)\n\n")
    r6.font.name = 'Times New Roman'
    r6.font.size = Pt(12)
    r6.font.bold = True
    r7 = p_cov_pers.add_run("Under the Guidance of:\n")
    r7.font.name = 'Times New Roman'
    r7.font.size = Pt(11)
    r7.font.bold = True
    r8 = p_cov_pers.add_run("MANISH VERMA\nFull Stack Software Engineer\nThrivedge Edutech Pvt. Ltd.")
    r8.font.name = 'Times New Roman'
    r8.font.size = Pt(12)
    r8.font.bold = True

    p_cov_univ = doc.add_paragraph()
    p_cov_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_univ.paragraph_format.line_spacing = 1.15
    p_cov_univ.paragraph_format.space_before = Pt(16)
    p_cov_univ.paragraph_format.space_after = Pt(0)
    r9 = p_cov_univ.add_run("CENTRE FOR DISTANCE AND ONLINE EDUCATION (CDOE)\nUTTARANCHAL UNIVERSITY, DEHRADUN\nNAAC Grade A+\nAcademic Session 2026")
    r9.font.name = 'Times New Roman'
    r9.font.size = Pt(12)
    r9.font.bold = True
    r9.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # ACKNOWLEDGEMENT
    add_chapter_title("Acknowledgement")
    add_p("I am deeply grateful to all those who have contributed to the successful conceptualization, architecture, implementation, and completion of this project report.")
    add_p("First and foremost, I would like to express my sincere gratitude to my project guide, Manish Verma, Full Stack Software Engineer at Thrivedge Edutech Pvt. Ltd., for his invaluable technical guidance, constructive reviews, and steady encouragement throughout the lifecycle of this project. His deep industry experience in full-stack architecture, relational database modeling, and scalable API design provided invaluable direction in solving complex concurrency challenges and ensuring modern software engineering best practices.")
    add_p("I also extend my heartfelt thanks to the faculty, mentors, and administration at the Centre for Distance and Online Education (CDOE), Uttaranchal University, Dehradun, for establishing a rigorous academic curriculum and providing the technological framework that made this practical endeavor possible.")
    add_p("Finally, I express my sincere appreciation to my family and peers for their continuous moral support, understanding, and motivation throughout the demanding development schedule of SmartStock.")

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(40)
    r = p_sign.add_run("Khushal Asaram Mali\nLearner ID: 2413020402\nBCA Semester - V\nCentre for Distance and Online Education\nUttaranchal University, Dehradun")
    r.font.bold = True

    doc.add_page_break()

    # DECLARATION
    add_chapter_title("Declaration")
    add_p("I, Khushal Asaram Mali, hereby declare that the project entitled “SmartStock – Inventory Management System” submitted by me to Uttaranchal University, Dehradun, in partial fulfillment of the requirements for the award of the Degree of Bachelor of Computer Applications (BCA Semester V), is an authentic and original record of software engineering work carried out by me under the professional guidance of Manish Verma, Full Stack Software Engineer at Thrivedge Edutech Pvt. Ltd.")
    add_p("I confirm that the codebases, architectural designs, relational schemas, automated test suites, and empirical evaluations presented in this report represent my own independent efforts.")
    add_p("I further declare that this work has not been submitted previously, in part or in full, to any other university, institute, or examining body for the award of any degree, diploma, fellowship, or professional title.")

    p_dec_sign = doc.add_paragraph()
    p_dec_sign.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_dec_sign.paragraph_format.space_before = Pt(50)
    r = p_dec_sign.add_run("Student Signature: _____________________\n\n"
                           "Learner Name: Khushal Asaram Mali\n"
                           "Learner ID: 2413020402\n"
                           "Place: Kalyan\n"
                           "Date: 18th November 2026")
    r.font.bold = True

    doc.add_page_break()

    # CERTIFICATE OF ORIGINALITY
    add_chapter_title("Certificate of Originality")
    add_p("This is to certify that the project report entitled “SmartStock – Inventory Management System”, submitted by Khushal Asaram Mali (Learner ID: 2413020402) in partial fulfillment of the requirements for the award of the Degree of Bachelor of Computer Applications (BCA Semester V) to Uttaranchal University, Dehradun, is a bona fide record of original project work carried out under my supervision.")
    add_p("The software architecture, system analysis, relational database schemas, automated test executions, and user interface modules documented herein have been reviewed and verified. To the best of my knowledge, this project work is original and has not been submitted elsewhere for the award of any degree, diploma, or certificate.")

    p_cert_sign = doc.add_paragraph()
    p_cert_sign.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cert_sign.paragraph_format.space_before = Pt(50)
    r = p_cert_sign.add_run("Guide Signature: _____________________\n\n"
                           "Guide Name: Manish Verma\n"
                           "Designation: Full Stack Software Engineer\n"
                           "Organization: Thrivedge Edutech Pvt. Ltd.\n"
                           "Date: 18th November 2026")
    r.font.bold = True

    doc.add_page_break()

    # TABLE OF CONTENTS
    add_chapter_title("Table of Contents")
    toc_data = [
        ("—", "Acknowledgement", "ii"),
        ("—", "Declaration", "iii"),
        ("—", "Certificate of Originality", "iv"),
        ("—", "List of Figures", "x"),
        ("—", "List of Tables", "xii"),
        ("1", "INTRODUCTION", get_toc("CHAPTER 1", 1)),
        ("1.1", "  Background and Industrial Context", get_toc("1.1", 1)),
        ("1.2", "  Problem Statement & Analysis of Existing Systems", get_toc("1.2", 2)),
        ("1.3", "  Comparative Evaluation of Retail Paradigms", get_toc("1.3", 3)),
        ("1.4", "  Proposed System Architecture (SmartStock)", get_toc("1.4", 3)),
        ("1.5", "  Scope and Operational Boundaries", get_toc("1.5", 4)),
        ("1.6", "  Organization of the Project Report", get_toc("1.6", 5)),
        ("2", "PROJECT OBJECTIVES", get_toc("CHAPTER 2", 6)),
        ("2.1", "  Primary Aim & Technical Objectives", get_toc("2.1", 6)),
        ("2.2", "  Functional Objectives", get_toc("2.2", 6)),
        ("2.3", "  Target Beneficiaries & User Personas", get_toc("2.3", 7)),
        ("2.4", "  Objectives to Software Modules Traceability", get_toc("2.4", 7)),
        ("2.5", "  Quantitative System Performance Benchmarks", get_toc("2.5", 8)),
        ("3", "SYSTEM ANALYSIS", get_toc("CHAPTER 3", 9)),
        ("3.1", "  Identification of Operational Need", get_toc("3.1", 9)),
        ("3.2", "  Preliminary Investigation & Retail Workflow Elicitation", get_toc("3.2", 9)),
        ("3.2.1", "    Local Retail Workflow Observations & Bottlenecks", get_toc("3.2.1", 10)),
        ("3.3", "  Multi-Dimensional Feasibility Study", get_toc("3.3", 10)),
        ("3.3.1", "    Technical Feasibility & Framework Trade-Offs", get_toc("3.3.1", 11)),
        ("3.3.2", "    Operational Feasibility & Staff Adoption", get_toc("3.3.2", 11)),
        ("3.3.3", "    Economic Feasibility & Payback Analysis", get_toc("3.3.3", 12)),
        ("3.3.4", "    Schedule & Behavioral Feasibility", get_toc("3.3.4", 12)),
        ("3.4", "  Project Planning & Work Breakdown Structure (WBS)", get_toc("3.4", 12)),
        ("3.5", "  Project Scheduling & Network Analysis", get_toc("3.5", 13)),
        ("3.5.1", "    Gantt Chart Schedule", get_toc("3.5.1", 13)),
        ("3.5.2", "    PERT Network Analysis & Critical Path", get_toc("3.5.2", 14)),
        ("3.6", "  Software Requirement Specification (SRS)", get_toc("3.6", 15)),
        ("3.6.1", "    Functional Requirements Specification", get_toc("3.6.1", 15)),
        ("3.6.2", "    Non-Functional Requirements Specification", get_toc("3.6.2", 17)),
        ("3.6.3", "    Detailed IEEE 830 Use Case Specifications (UC-01 to UC-08)", get_toc("3.6.3", 17)),
        ("3.7", "  System Environment Specifications", get_toc("3.7", 23)),
        ("3.7.1", "    Hardware Infrastructure Specifications", get_toc("3.7.1", 23)),
        ("3.7.2", "    Software Technology Stack & Dependency Rationale", get_toc("3.7.2", 24)),
        ("3.8", "  Visual Data Models & Architectural Diagrams", get_toc("3.8", 24)),
        ("3.8.1", "    Use Case Diagram (Figure 3.3)", get_toc("3.8.1", 24)),
        ("3.8.2", "    Activity Diagram – Sales & Stock Deduction (Figure 3.4)", get_toc("3.8.2", 26)),
        ("3.8.3", "    Sequence Diagram – POS Billing & Concurrency (Figure 3.5)", get_toc("3.8.3", 27)),
        ("3.8.4", "    Domain Class Diagram & Object Model (Figure 3.6)", get_toc("3.8.4", 29)),
        ("3.8.5", "    Entity Relationship Diagram (ERD – 3NF) (Figure 3.7)", get_toc("3.8.5", 31)),
        ("4", "SYSTEM DESIGN", get_toc("CHAPTER 4", 34)),
        ("4.1", "  Modularization Details & Architectural Patterns", get_toc("4.1", 34)),
        ("4.1.1", "    Layered 3-Tier Web Architecture", get_toc("4.1.1", 34)),
        ("4.1.2", "    Enterprise Design Patterns (IoC, DTO, Unit of Work)", get_toc("4.1.2", 34)),
        ("4.1.3", "    Core Subsystem Modules (Modules 1 to 5)", get_toc("4.1.3", 35)),
        ("4.2", "  Database Design & Data Integrity", get_toc("4.2", 35)),
        ("4.2.1", "    Formal Normalization Proofs (UNF to 3NF & BCNF)", get_toc("4.2.1", 36)),
        ("4.2.2", "    Relational Integrity Constraints & Referential Actions", get_toc("4.2.2", 37)),
        ("4.2.3", "    Comprehensive System Data Dictionary (Tables 4.2 to 4.9)", get_toc("4.2.3", 38)),
        ("5", "TESTING & QUALITY ASSURANCE", get_toc("CHAPTER 5", 43)),
        ("5.1", "  Testing Strategy & Methodologies", get_toc("5.1", 43)),
        ("5.2", "  Automated Unit & Integration Test Execution Results", get_toc("5.2", 43)),
        ("5.3", "  Code Coverage Analysis & Metrics Breakdown", get_toc("5.3", 44)),
        ("5.4", "  Comprehensive System Test Execution Matrix (TC-01 to TC-20)", get_toc("5.4", 45)),
        ("6", "SYSTEM SECURITY MEASURES & DEPLOYMENT", get_toc("CHAPTER 6", 48)),
        ("6.1", "  Authentication & Authorization Pipeline (JWT & Bcrypt)", get_toc("6.1", 48)),
        ("6.2", "  Inbound Payload Sanitization & SQL Injection Mitigation", get_toc("6.2", 48)),
        ("6.3", "  ACID Transaction Mechanics & Rollback Handling", get_toc("6.3", 49)),
        ("6.4", "  Deployment Topology & Operating Environment", get_toc("6.4", 49)),
        ("7", "RESULTS, DISCUSSION & COST ESTIMATION", get_toc("CHAPTER 7", 50)),
        ("7.1", "  Operational Impact & Performance Benchmarks", get_toc("7.1", 50)),
        ("7.2", "  Concurrency Analysis & High-Volume Invoice Sequencing", get_toc("7.2", 51)),
        ("7.3", "  Software Cost & Effort Estimation (COCOMO Basic Model)", get_toc("7.3", 52)),
        ("8", "REPORT (SYSTEM OUTPUT & SCREENS)", get_toc("CHAPTER 8", 53)),
        ("8.1", "  Screen Walkthrough & Functional Verification (Figures 8.1 to 8.14)", get_toc("8.1", 53)),
        ("9", "FUTURE SCOPE & ENHANCEMENTS", get_toc("CHAPTER 9", 67)),
        ("9.1", "  Summary of Project Accomplishments", get_toc("9.1", 67)),
        ("9.2", "  Academic Prototype Limitations", get_toc("9.2", 67)),
        ("9.3", "  Future Enhancements Roadmap", get_toc("9.3", 68)),
        ("10", "APPENDICES", get_toc("CHAPTER 10", 69)),
        ("10.1", "  Key Source Code Listings", get_toc("10.1", 69)),
        ("10.2", "  Bibliography & References", get_toc("10.2", 75)),
    ]
    create_table(["S. No", "Chapter / Section Description", "Page No"], toc_data, [Inches(0.8), Inches(4.15), Inches(0.8)])

    doc.add_page_break()

    # LIST OF FIGURES
    add_chapter_title("List of Figures")
    lof_data = [
        ("Figure 3.1", "Project Work Breakdown Schedule (Gantt Chart)", get_lof("Figure 3.1", 13)),
        ("Figure 3.2", "Project Critical Path & Precedence Network (PERT Chart)", get_lof("Figure 3.2", 14)),
        ("Figure 3.3", "System Use Case Diagram with Actor Boundary Partitions", get_lof("Figure 3.3", 25)),
        ("Figure 3.4", "Activity Diagram – Point-of-Sale Billing & Stock Decrement", get_lof("Figure 3.4", 26)),
        ("Figure 3.5", "Sequence Diagram – POS Transaction & Atomic Database Commit", get_lof("Figure 3.5", 28)),
        ("Figure 3.6", "Domain Class Diagram & Object Model Multiplicity", get_lof("Figure 3.6", 30)),
        ("Figure 3.7", "Entity-Relationship Diagram (ERD) with 3NF Relational Mappings", get_lof("Figure 3.7", 32)),
        ("Figure 8.1", "User Authentication & Role-Based Login Screen", get_lof("Figure 8.1", 53)),
        ("Figure 8.2", "Executive Analytics & Operational KPI Dashboard Overview", get_lof("Figure 8.2", 54)),
        ("Figure 8.3", "Master Product Catalog Management Console", get_lof("Figure 8.3", 55)),
        ("Figure 8.4", "Product Creation & SKU Attribute Configuration Modal", get_lof("Figure 8.4", 56)),
        ("Figure 8.5", "Product Taxonomy & Category Management Interface", get_lof("Figure 8.5", 57)),
        ("Figure 8.6", "Vendor & Supplier Profile Directory", get_lof("Figure 8.6", 58)),
        ("Figure 8.7", "Procurement Restocking & Multi-Item Purchase Entry", get_lof("Figure 8.7", 59)),
        ("Figure 8.8", "Point-of-Sale (POS) Multi-Item Checkout Counter", get_lof("Figure 8.8", 60)),
        ("Figure 8.9", "Generated Tax Invoice Modal & Print Dialog", get_lof("Figure 8.9", 61)),
        ("Figure 8.10", "Inventory Stock Valuation & Master Summary Report", get_lof("Figure 8.10", 62)),
        ("Figure 8.11", "Proactive Low-Stock Reorder Alerting Report", get_lof("Figure 8.11", 63)),
        ("Figure 8.12", "Historical Procurement Inflow Audit Log", get_lof("Figure 8.12", 64)),
        ("Figure 8.13", "Historical Sales Revenue Outflow Audit Log", get_lof("Figure 8.13", 65)),
        ("Figure 8.14", "Administrative User Management & RBAC Provisioning Console", get_lof("Figure 8.14", 66)),
    ]
    create_table(["Figure No", "Figure Caption / Description", "Page No"], lof_data, [Inches(1.1), Inches(3.85), Inches(0.8)])

    doc.add_page_break()

    # LIST OF TABLES
    add_chapter_title("List of Tables")
    lot_data = [
        ("Table 1.1", "Organization and Structural Mapping of the Project Report", get_lot("Table 1.1", 5)),
        ("Table 1.2", "Comparative Evaluation of Inventory Management Paradigms", get_lot("Table 1.2", 3)),
        ("Table 2.1", "Project Objectives to Software Modules Traceability Matrix", get_lot("Table 2.1", 7)),
        ("Table 2.2", "Quantitative Operational Success Metrics & KPI Benchmark Targets", get_lot("Table 2.2", 8)),
        ("Table 3.1", "Work Breakdown Structure (WBS) Task Durations and Milestones", get_lot("Table 3.1", 13)),
        ("Table 3.2", "PERT Activity Time Estimates, Variance, and Slack Calculations", get_lot("Table 3.2", 14)),
        ("Table 3.3", "Functional Requirements Specification & Traceability Summary", get_lot("Table 3.3", 16)),
        ("Table 3.4", "Detailed Use Case Specification – UC-01: User Authentication", get_lot("Table 3.4", 17)),
        ("Table 3.5", "Detailed Use Case Specification – UC-02: Product Catalog Management", get_lot("Table 3.5", 18)),
        ("Table 3.6", "Detailed Use Case Specification – UC-03: Category Classification", get_lot("Table 3.6", 19)),
        ("Table 3.7", "Detailed Use Case Specification – UC-04: Supplier Profile Management", get_lot("Table 3.7", 20)),
        ("Table 3.8", "Detailed Use Case Specification – UC-05: Procurement Restocking (Inflow)", get_lot("Table 3.8", 20)),
        ("Table 3.9", "Detailed Use Case Specification – UC-06: POS Checkout & Stock Decrement", get_lot("Table 3.9", 21)),
        ("Table 3.10", "Detailed Use Case Specification – UC-07: Low-Stock Alerting", get_lot("Table 3.10", 22)),
        ("Table 3.11", "Detailed Use Case Specification – UC-08: Financial & Operational Auditing", get_lot("Table 3.11", 22)),
        ("Table 3.12", "Server and Client Hardware Infrastructure Specifications", get_lot("Table 3.12", 23)),
        ("Table 3.13", "Software Technology Stack & Dependency Version Matrix", get_lot("Table 3.13", 24)),
        ("Table 4.1", "Database Functional Dependency & Normalization Transition (1NF to 3NF)", get_lot("Table 4.1", 36)),
        ("Table 4.2", "Data Dictionary – User Entity (users table)", get_lot("Table 4.2", 38)),
        ("Table 4.3", "Data Dictionary – Category Entity (categories table)", get_lot("Table 4.3", 38)),
        ("Table 4.4", "Data Dictionary – Supplier Entity (suppliers table)", get_lot("Table 4.4", 39)),
        ("Table 4.5", "Data Dictionary – Product Entity (products table)", get_lot("Table 4.5", 39)),
        ("Table 4.6", "Data Dictionary – Purchase Entity (purchases table)", get_lot("Table 4.6", 40)),
        ("Table 4.7", "Data Dictionary – PurchaseItem Entity (purchase_items table)", get_lot("Table 4.7", 41)),
        ("Table 4.8", "Data Dictionary – Sale Entity (sales table)", get_lot("Table 4.8", 41)),
        ("Table 4.9", "Data Dictionary – SaleItem Entity (sale_items table)", get_lot("Table 4.9", 42)),
        ("Table 5.1", "Jest Automated Unit & Integration Test Suite Execution Results", get_lot("Table 5.1", 44)),
        ("Table 5.2", "Backend Service Code Coverage Metrics Breakdown", get_lot("Table 5.2", 44)),
        ("Table 5.3", "Comprehensive System Test Execution Matrix (TC-01 through TC-20)", get_lot("Table 5.3", 45)),
        ("Table 7.1", "Projected Operational Improvements vs. Manual Retail Baseline", get_lot("Table 7.1", 50)),
        ("Table 7.2", "Basic COCOMO Software Cost and Effort Estimation Summary", get_lot("Table 7.2", 52)),
    ]
    create_table(["Table No", "Table Title / Description", "Page No"], lot_data, [Inches(1.1), Inches(3.85), Inches(0.8)])

    # ==========================================================================
    # 2. MAIN BODY SECTION BREAK (Arabic Numerals starting at 1)
    # ==========================================================================
    sec_body = doc.add_section()
    sec_body.top_margin = Inches(1.0)
    sec_body.bottom_margin = Inches(1.0)
    sec_body.left_margin = Inches(1.5)
    sec_body.right_margin = Inches(1.0)
    sec_body.page_width = Inches(8.27)
    sec_body.page_height = Inches(11.69)
    sec_body.different_first_page_header_footer = False

    sectPr_body = sec_body._sectPr
    pgNumType_body = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
    sectPr_body.append(pgNumType_body)

    # CRITICAL: Decouple from previous section footer to prevent doubled page numbers!
    sec_body.footer.is_linked_to_previous = False
    footer_body = sec_body.footer
    f_p_body = footer_body.paragraphs[0]
    f_p_body.text = ""  # Clean slate
    f_p_body.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run_body = f_p_body.add_run()
    f_run_body.font.name = 'Times New Roman'
    f_run_body.font.size = Pt(10)
    f_run_body.font.color.rgb = RGBColor(100, 116, 139)
    add_page_number_to_run(f_run_body)

    # ==========================================================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================================================
    add_chapter_title("CHAPTER 1\nINTRODUCTION")

    add_h1("1.1 Background and Industrial Context")
    add_p("In the contemporary commercial ecosystem, retail businesses, supply chains, and warehousing enterprises face stringent operational pressures requiring real-time inventory visibility, rigorous fiscal accountability, and rapid checkout processing. Across developing economic sectors and localized retail environments, small-to-medium retail enterprises (SMEs) represent the vast majority of physical retail distribution. Historically, these enterprises have managed their daily operations through manual paper-based ledger registers or uncoupled, static spreadsheets such as Microsoft Excel.")
    add_p("While manual ledger systems initially provided a negligible financial barrier to entry, their operational sustainability rapidly collapses as catalog complexity and daily transaction velocity expand. In physical retail stores carrying between 200 and 5,000 active Stock Keeping Units (SKUs), manual tracking results in severe structural inefficiencies. Store managers must manually reconcile physical shelf quantities against handwritten purchase and sales receipts at the close of every business day. This process is excessively labor-intensive, taking between one and three hours daily, and introduces substantial human transcription errors.")
    add_p("Furthermore, uncoupled spreadsheets lack multi-user concurrency control. When multiple staff members access or edit inventory tallies simultaneously, dirty reads, overwrites, and formula corruption inevitably occur. Most critically, manual spreadsheets are fundamentally passive; they lack automated event-driven triggers to alert managers when stock falls below critical replenishment levels. Consequently, retailers frequently experience unexpected stockouts of fast-moving consumer goods, directly translating into lost sales revenues, dissatisfied customers, and compromised working capital.")
    add_p("The retail industry has increasingly shifted toward computerized Point-of-Sale (POS) and Enterprise Resource Planning (ERP) frameworks. However, enterprise commercial solutions (such as SAP, Oracle NetSuite, or Microsoft Dynamics) impose prohibitive licensing costs, demanding complex server infrastructures and prolonged consultant onboarding that remain far beyond the capital expenditure thresholds of independent retailers. Therefore, developing an agile, modern, open-source web platform specifically tailored for small-to-medium retailers addresses a critical economic and operational imperative.")
    add_p("SmartStock addresses this exact technological vacuum by delivering a cloud-ready, responsive, type-safe inventory management platform engineered with modern open-source web technologies. By bridging the gap between cumbersome legacy paper ledgers and expensive corporate ERP suites, SmartStock democratizes enterprise-grade inventory governance for local retail entrepreneurs.")

    add_h1("1.2 Problem Statement & Analysis of Existing Systems")
    add_p("A rigorous critical analysis of legacy manual and spreadsheet-based inventory management revealed the following core failure modes that directly threaten retail viability:")
    add_bullet("Absence of Atomic Stock Synchronization: In manual registers, the physical sale of an item is recorded on paper while stock ledgers are updated hours or days later. This systemic temporal disconnect means physical stock and book stock are rarely synchronized, leading to phantom inventory and unverified shrinkages.")
    add_bullet("Human Transcription Errors: Manual entry of multi-digit SKU codes, quantities, and decimal prices introduces arithmetic and transcription errors estimated at 3% to 7% across manual bookkeeping workflows.")
    add_bullet("Vulnerability to Concurrency Anomalies: Shared spreadsheets lack ACID (Atomicity, Consistency, Isolation, Durability) transactional isolation. Simultaneous checkouts of the same product line result in race conditions, overwriting previous sales data and creating negative stock anomalies.")
    add_bullet("Zero Proactive Threshold Alerting: Spreadsheets do not actively notify supervisors when stock depletes to dangerous reorder thresholds. Restocking orders are only initiated reactively after customers discover empty shelves.")
    add_bullet("Inadequate Role Separation & Audit Trails: Paper ledgers and unprotected Excel files offer no cryptographic access control. Any user can alter records without leaving a verifiable audit trail, severely compromising internal store security and accountability.")
    add_p("In addition, traditional manual records prevent managers from calculating true inventory carrying costs and stock turnover ratios. Retailers routinely over-purchase slow-moving product lines while under-purchasing high-demand items, locking up scarce working capital in dead inventory. SmartStock provides a systematic computational solution to these chronic operational bottlenecks.")

    add_h1("1.3 Comparative Evaluation of Retail Paradigms")
    add_p("To contextualize the technical advantages of the proposed SmartStock solution, Table 1.2 presents a comparative evaluation contrasting manual ledgers, generic spreadsheets, proprietary enterprise ERPs, and SmartStock across key operational dimensions.")

    add_table_caption("Table 1.2: Comparative Evaluation of Inventory Management Paradigms")
    eval_matrix_data = [
        ("Deployment Cost", "Negligible (Paper pads)", "Low (Office license)", "Very High (₹5L - ₹50L+)", "Zero (Open-source MIT)"),
        ("ACID Concurrency", "None (Physical bottleneck)", "None (File lock conflicts)", "Yes (Heavyweight RDBMS)", "Yes (PostgreSQL transactions)"),
        ("Checkout Speed", "Slow (Manual calculation)", "Moderate (Lookup delays)", "Fast (Enterprise POS)", "Fast (< 30s POS cart)"),
        ("Threshold Alerting", "None (Visual memory)", "Manual conditional rules", "Yes (Automated triggers)", "Yes (Real-time SQL filters)"),
        ("Audit Integrity", "Poor (Easily altered)", "Poor (Unsigned edits)", "High (Enterprise audit)", "High (JWT & Role logs)"),
        ("Learning Curve", "Immediate", "Low to Moderate", "High (Months of training)", "Very Low (< 30 minutes)"),
    ]
    create_table(["Evaluation Dimension", "Manual Paper Ledgers", "Desktop Spreadsheets", "Proprietary ERP Suites", "SmartStock IMS (Proposed)"], eval_matrix_data, [Inches(1.15), Inches(1.10), Inches(1.10), Inches(1.20), Inches(1.20)])

    add_h1("1.4 Proposed System Architecture (SmartStock)")
    add_p("To eliminate these systemic vulnerabilities, this project conceptualizes, architects, and implements 'SmartStock – Inventory Management System'. SmartStock is engineered as an enterprise-grade, three-tier web application designed specifically to provide high-performance, transactionally secure inventory control and Point-of-Sale (POS) billing for retail operations.")
    add_p("The system architecture decouples the presentation, business logic, and persistence layers into modern, industry-standard frameworks:")
    add_bullet("Presentation Layer: Implemented in Next.js 16 (App Router) and React 19, delivering a highly responsive, component-driven user interface styled with Tailwind CSS v4. The UI incorporates real-time search filtering, dynamic POS cart calculations, and responsive modal dialogs.")
    add_bullet("Application Logic Layer: Built on NestJS 11, a progressive TypeScript framework that enforces robust architectural patterns including Dependency Injection (DI), modular domain separation, and centralized request validation.")
    add_bullet("Data Persistence Layer: Utilizes PostgreSQL 18.1, an enterprise-grade open-source relational database, interfaced through Prisma ORM 6.4.1. Prisma ensures strict compile-time type safety, automated migration management, and parameterized SQL queries that provide complete immunity against SQL injection vulnerabilities.")
    add_p("At the core of SmartStock is an atomic transaction engine that executes all stock-altering workflows inside database transactions. When a sale occurs, the system atomically validates available stock, deducts inventory, creates itemized sale records, and generates a formatted sequential invoice in a single isolated commit, completely preventing stock discrepancies.")

    add_h1("1.5 Scope and Operational Boundaries")
    add_p("The operational boundaries of the SmartStock project are defined as follows:")
    add_bullet("Target Commercial Setting: Independent retail stores, hardware shops, electronics outlets, and departmental stores carrying up to 10,000 active SKUs.")
    add_bullet("Operational Modules Included: Role-based user authentication (Admin, Staff), master product catalog management, category taxonomy, supplier profile directory, inbound procurement restocking, multi-item POS sales checkout with invoice generation, and financial audit reporting.")
    add_bullet("System Boundaries (Exclusions): Multi-branch distributed warehouse logistics, automated optical character recognition (OCR) of supplier paper invoices, and direct programmatic credit card payment gateway settlement (handled externally via cash, POS card swipers, or QR UPI).")

    add_h1("1.6 Organization of the Project Report")
    add_p("This report is structured into ten comprehensive chapters designed in accordance with academic project documentation guidelines:")

    add_table_caption("Table 1.1: Organization and Structural Mapping of the Project Report")
    org_data = [
        ("Chapter 1: Introduction", "Establishes industrial context, problem statement, comparative matrix, and proposed architectural scope."),
        ("Chapter 2: Project Objectives", "Formulates primary engineering aims, functional deliverables, user personas, and KPI benchmarks."),
        ("Chapter 3: System Analysis", "Presents feasibility studies, work breakdown schedules, PERT analysis, SRS requirements, and UML diagrams."),
        ("Chapter 4: System Design", "Details 3-tier architecture, enterprise design patterns, 3NF normalization proofs, and relational data dictionaries."),
        ("Chapter 5: Testing & QA", "Documents Jest automated test execution, code coverage breakdown, and 20 end-to-end system test cases."),
        ("Chapter 6: System Security & Deployment", "Analyzes bcrypt hashing, symmetric JWT authorization, SQL injection prevention, and Docker deployment."),
        ("Chapter 7: Results & Cost Estimation", "Presents operational impact, concurrency race condition analysis, and Basic COCOMO cost calculations."),
        ("Chapter 8: System Output & Screens", "Provides detailed architectural walkthroughs for all 14 authentic application screens."),
        ("Chapter 9: Future Scope & Conclusion", "Summarizes engineering accomplishments, prototype limitations, and commercial roadmap."),
        ("Chapter 10: Appendices", "Contains key TypeScript source code listings and formal academic bibliography."),
    ]
    create_table(["Report Chapter", "Structural Content & Methodological Scope"], org_data, [Inches(1.85), Inches(3.90)])

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 2: PROJECT OBJECTIVES
    # ==========================================================================
    add_chapter_title("CHAPTER 2\nPROJECT OBJECTIVES")

    add_h1("2.1 Primary Aim & Technical Objectives")
    add_p("The primary aim of this project is to conceptualize, engineer, and validate 'SmartStock', a modern, full-stack, type-safe inventory management and point-of-sale system that replaces error-prone manual paper ledgers with automated, transactionally consistent database workflows.")
    add_p("To realize this aim, the following technical objectives were established:")
    add_bullet("Objective 1 (ACID Concurrency Guarantee): Implement an isolated transaction processing pipeline ensuring that inventory increments (restocking) and decrements (POS billing) execute atomically, preventing dirty reads and ghost inventory.")
    add_bullet("Objective 2 (Sub-Second Latency): Architect a high-speed web application achieving average API response times under 500ms on standard local networks, supporting fast search across product catalogs.")
    add_bullet("Objective 3 (Cryptographic Access Governance): Establish strict Role-Based Access Control (RBAC) separating administrative oversight from cashier billing operations via salted bcrypt password hashes and signed JWT bearer tokens.")
    add_bullet("Objective 4 (Compile-Time Type Safety): Enforce complete end-to-end type safety across the database schema, backend services, API interfaces, and React frontend components using TypeScript and Prisma ORM.")

    add_h1("2.2 Functional Objectives")
    add_p("To fulfill operational retail workflows, SmartStock establishes five core functional objectives:")
    add_bullet("Functional Objective 1 (Master Product & Supplier Cataloging): Provide intuitive administrative interfaces to manage product profiles, enforce SKU uniqueness, configure cost/selling prices, assign taxonomic categories, and track supplier contacts.")
    add_bullet("Functional Objective 2 (Restocking & Procurement Management): Implement a structured inbound stock intake engine that logs supplier purchase invoices and automatically updates inventory stock counts.")
    add_bullet("Functional Objective 3 (High-Speed POS Checkout & Billing): Develop an interactive sales counter that enables cashiers to assemble multi-item shopping carts, validates instantaneous stock availability, rejects overselling, and generates formatted invoices.")
    add_bullet("Functional Objective 4 (Proactive Low-Stock Reordering Alerts): Automatically identify depleted product lines whose available quantity is less than or equal to their configured reorder threshold, presenting visual warnings and supplier contacts.")
    add_bullet("Functional Objective 5 (Financial & Operational Auditing): Deliver comprehensive reporting modules that calculate total stock valuation, analyze procurement expenditures, track revenue inflows, and export printable audit logs.")

    add_h1("2.3 Target Beneficiaries & User Personas")
    add_p("The system is specifically engineered to serve three distinct organizational personas within a retail environment:")
    add_bullet("Store Owners / General Managers (Admin Role): Require top-level visibility over gross inventory valuation, low-stock alerts, procurement costs, total sales revenue, and the ability to provision employee user accounts.")
    add_bullet("Cashiers / Sales Associates (Staff Role): Require a clean, frictionless Point-of-Sale interface that accelerates checkout speed, prevents human arithmetic errors, prints clean customer invoices, and blocks stock deficit errors.")
    add_bullet("Warehouse Clerks / Stock Supervisors: Require accurate visibility over current shelf balances, reorder thresholds, and vendor contact directories to streamline supplier purchase orders.")

    add_h1("2.4 Objectives to Software Modules Traceability")
    add_p("To ensure comprehensive verification during system testing, Table 2.1 establishes formal traceability between the project objectives, the software modules implemented, and their respective validation criteria.")

    add_table_caption("Table 2.1: Project Objectives to Software Modules Traceability Matrix")
    obj_trace_data = [
        ("OBJ-01", "ACID Stock Updates", "SalesService, PurchasesService", "prisma.$transaction atomic blocks", "Zero stock anomalies under concurrent checkout"),
        ("OBJ-02", "Sub-Second Latency", "Next.js App Router, NestJS", "Indexed PostgreSQL queries", "API latency < 500ms verified via logging"),
        ("OBJ-03", "RBAC Security", "AuthModule, JwtAuthGuard", "bcrypt hash (10 rounds) + JWT", "Strict 403 Forbidden on unauthorized routes"),
        ("OBJ-04", "Product Cataloging", "ProductsModule, CategoriesModule", "Unique SKU index + DTO validation", "Prevents duplicate SKU and negative pricing"),
        ("OBJ-05", "Procurement Inflow", "PurchasesModule", "Atomic stock increment logic", "Stock accurately increases upon purchase order"),
        ("OBJ-06", "POS Billing & Outflow", "SalesModule, POS Counter UI", "Pre-checkout stock checks", "Prevents stockouts; auto-generates invoice"),
        ("OBJ-07", "Low-Stock Alerts", "ReportsModule, Dashboard UI", "SQL filter (quantity <= reorderLevel)", "Immediate visual badges on low stock"),
        ("OBJ-08", "Financial Auditing", "ReportsModule", "Aggregated SUM() SQL queries", "Accurate valuation and date-filtered exports"),
    ]
    create_table(["Obj ID", "Target Objective", "Implementation Modules", "Technical Mechanism", "Verification Criterion"], obj_trace_data, [Inches(0.7), Inches(1.2), Inches(1.25), Inches(1.25), Inches(1.35)])

    add_h1("2.5 Quantitative System Performance Benchmarks")
    add_p("To establish clear engineering benchmarks for system success, Table 2.2 defines the target quantitative performance thresholds established during requirements definition and verified during testing.")

    add_table_caption("Table 2.2: Quantitative Operational Success Metrics & KPI Benchmark Targets")
    kpi_table_data = [
        ("API Response Latency", "< 500 ms (Local network)", "Indexed PostgreSQL queries & Express HTTP runtime", "Design Target (Sub-500ms response)"),
        ("Checkout Transaction Time", "< 30 seconds per cart checkout", "Client-side stateful POS cart & batch submission", "Design Target (Streamlined workflow)"),
        ("Stock Audit Discrepancies", "0.0% variance (Zero drift)", "prisma.$transaction ACID isolation", "Verified via Automated Unit Tests"),
        ("Authentication Token Expiry", "24.0 Hours from issuance", "Signed via @nestjs/jwt with HS256 secret", "Verified via JwtAuthGuard tests"),
        ("Database Query Concurrency", "Up to 20 pooled connections", "Prisma Client pooled connections", "Verified via pool configuration"),
        ("Unit Test Code Coverage", ">= 80% on critical transaction services (Auth & Sales); >= 70% overall", "Jest automated unit and integration suite", "Verified (Auth 100%, Sales 82.4%, Overall 71.7%)"),
    ]
    create_table(["Performance Dimension", "Target Benchmark Objective", "Implementation Mechanism", "Design Verification Status"], kpi_table_data, [Inches(1.4), Inches(1.45), Inches(1.6), Inches(1.3)])

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 3: SYSTEM ANALYSIS
    # ==========================================================================
    add_chapter_title("CHAPTER 3\nSYSTEM ANALYSIS")

    add_h1("3.1 Identification of Operational Need")
    add_p("The operational need for SmartStock originates from the acute structural friction observed in small-to-medium retail establishments. In physical retail stores carrying hundreds of fast-moving consumer goods (FMCG), hardware tools, or electronic accessories, manual paper-based record-keeping imposes severe operational penalties.")
    add_p("Daily manual audits consume valuable managerial labor, paper purchase receipts are easily misplaced, and arithmetic mistakes during rush-hour sales checkout directly reduce store revenue. Most critically, manual ledgers provide no automated forecasting or threshold alerting. Store supervisors discover that an item is out of stock only when a customer requests it and finds an empty shelf. SmartStock replaces these fragile manual practices with an automated, transactionally consistent software solution.")

    add_h1("3.2 Preliminary Investigation & Retail Workflow Elicitation")
    add_p("To establish realistic system requirements, preliminary investigation focused on analyzing standard point-of-sale and warehousing workflows across retail outlets. The investigation examined order procurement, goods receiving, inventory counting, shelf stocking, retail billing, and cash reconciliation.")

    add_h2("3.2.1 Local Retail Workflow Observations & Bottlenecks")
    add_p("Observations of physical retail store operations highlighted several structural operational bottlenecks:")
    add_bullet("Restocking Lag: Inbound supplier shipments arrive with physical printed paper bills. Store staff manually inspect items and manually write quantities into a physical inward ledger. Hours or days elapse before counts are updated, leading to stock discrepancies.")
    add_bullet("Checkout Bottlenecks: Cashiers calculate item totals, discounts, and tax using tabletop electronic calculators. Hand-keying prices introduces transcription errors and slows down line throughput during peak shopping periods.")
    add_bullet("Phantom Stock: Physical inventory often fails to match written register tallies due to unrecorded damaged goods, theft, or missed entries, leading to customer dissatisfaction.")
    add_bullet("Inaccessible Historical Analytics: Retrieving monthly sales totals or vendor purchase histories requires manually sifting through stacks of paper notebooks, making business performance analysis tedious and slow.")

    add_h1("3.3 Multi-Dimensional Feasibility Study")
    add_p("Prior to architectural modeling, a comprehensive feasibility study was conducted across technical, operational, economic, schedule, and behavioral dimensions.")

    add_h2("3.3.1 Technical Feasibility & Framework Trade-Offs")
    add_p("Technical feasibility evaluated whether the target feature set could be implemented using modern open-source technologies while maintaining low system resource requirements. Key framework decisions included:")
    add_bullet("Backend Architecture: NestJS was selected over raw Express.js because its modular architecture, native TypeScript support, and built-in dependency injection enforce enterprise design patterns and simplify automated unit testing.")
    add_bullet("ORM Selection: Prisma ORM was chosen over TypeORM due to its auto-generated type-safe client, robust schema migration tooling, and intuitive interactive transaction API (`prisma.$transaction`).")
    add_bullet("Database Engine: PostgreSQL was selected over MySQL or MongoDB due to its strict adherence to SQL standards, advanced transaction isolation, reliable B-tree indexing, and proven zero-data-loss durability.")
    add_bullet("Frontend Framework: Next.js 16 (App Router) and React 19 were selected to provide rapid client-side rendering, component reusability, and seamless integration with Tailwind CSS v4.")

    add_h2("3.3.2 Operational Feasibility & Staff Adoption")
    add_p("Operational feasibility evaluated how smoothly non-technical store clerks could transition to the software. The user interface was deliberately designed with high visual affordance, intuitive icons, contrasting status pills, and minimal required keystrokes. Single-click quick-fill buttons were integrated on the login screen to accelerate testing and user onboarding. The POS counter interface mirrors a physical cash register layout, enabling cashiers to complete checkouts with less than thirty minutes of training.")

    add_h2("3.3.3 Economic Feasibility & Payback Analysis")
    add_p("Economic feasibility assessed capital expenditure (CapEx) and operational expenditure (OpEx). Because SmartStock is constructed entirely from permissive open-source software (Node.js, PostgreSQL, Next.js, Prisma, Tailwind CSS), software licensing costs are exactly ₹0. The application runs efficiently on existing retail desktop hardware, eliminating expensive proprietary POS hardware requirements.")
    add_bullet("Projected Operational Return: By eliminating arithmetic checkout errors, reducing daily inventory reconciliation time from two hours to under ten minutes, and preventing lost sales through proactive low-stock alerts, the application delivers substantial projected operational savings for retail owners.")

    add_h2("3.3.4 Schedule & Behavioral Feasibility")
    add_p("Schedule feasibility evaluated whether the full scope of analysis, design, implementation, and testing could be realistically completed within the strict 23-day academic project window allocated from 5th November 2026 to 27th November 2026.")
    add_p("Behavioral feasibility assessed the operational adaptability of retail staff transitioning from paper ledgers to a digital point-of-sale workflow. Simulated operational walkthroughs confirmed that the streamlined barcode search, automated subtotaling, and single-click checkout modal require negligible technical training (< 30 minutes) and minimize manual entry fatigue.")

    add_h1("3.4 Project Planning & Work Breakdown Structure (WBS)")
    add_p("To ensure structured project execution, the development lifecycle was decomposed into five major phases comprising twelve discrete work packages, structured as follows in Table 3.1.")

    add_table_caption("Table 3.1: Work Breakdown Structure (WBS) Task Durations and Milestones")
    wbs_data = [
        ("Phase 1: Analysis", "Task A", "Problem Definition & Requirements Elicitation", "05-Nov-2026", "07-Nov-2026", "3 Days", "Requirements Document"),
        ("Phase 1: Analysis", "Task B", "Feasibility Study & Technology Stack Evaluation", "08-Nov-2026", "09-Nov-2026", "2 Days", "Feasibility Report"),
        ("Phase 2: Design", "Task C", "Database Modeling & 3NF Schema Normalization", "10-Nov-2026", "12-Nov-2026", "3 Days", "Prisma Schema & ERD"),
        ("Phase 2: Design", "Task D", "UML Modeling (Use Case, Activity, Sequence, Class)", "13-Nov-2026", "14-Nov-2026", "2 Days", "Architectural Diagrams"),
        ("Phase 3: Backend", "Task E", "Authentication & Security Module (JWT + bcrypt)", "15-Nov-2026", "16-Nov-2026", "2 Days", "Auth APIs & Guards"),
        ("Phase 3: Backend", "Task F", "Catalog & Restocking Services (Products/Purchases)", "17-Nov-2026", "18-Nov-2026", "2 Days", "Inflow Transaction Engine"),
        ("Phase 3: Backend", "Task G", "Atomic Sales Engine & Dynamic Reporting Services", "19-Nov-2026", "20-Nov-2026", "2 Days", "Outflow Engine & Reports"),
        ("Phase 4: Frontend", "Task H", "Authentication UI, Dashboard & Catalog Components", "21-Nov-2026", "22-Nov-2026", "2 Days", "Next.js Core Views"),
        ("Phase 4: Frontend", "Task I", "Interactive POS Billing Counter & Invoicing Modal", "23-Nov-2026", "24-Nov-2026", "2 Days", "POS Cart & Print Dialog"),
        ("Phase 5: Testing", "Task J", "Automated Jest Unit & Integration Test Suites", "25-Nov-2026", "25-Nov-2026", "1 Day", "Test Execution Reports"),
        ("Phase 5: Testing", "Task K", "End-to-End System Integration & User Acceptance", "26-Nov-2026", "26-Nov-2026", "1 Day", "System Test Matrix"),
        ("Phase 5: Testing", "Task L", "Documentation Finalization & Academic Report Build", "27-Nov-2026", "27-Nov-2026", "1 Day", "Final Project Report"),
    ]
    create_table(["Phase", "Task ID", "Task Description", "Start Date", "End Date", "Duration", "Deliverable Output"], wbs_data, [Inches(0.9), Inches(0.55), Inches(1.7), Inches(0.7), Inches(0.7), Inches(0.5), Inches(0.7)])

    add_h1("3.5 Project Scheduling & Network Analysis")
    add_p("Project scheduling was modeled using both deterministic Gantt scheduling and probabilistic Program Evaluation and Review Technique (PERT) network analysis to identify critical path constraints.")

    add_h2("3.5.1 Gantt Chart Schedule")
    add_p("Figure 3.1 illustrates the chronological Gantt chart schedule depicting task durations, concurrent execution phases, and project milestones across the 23-day timeline.")
    add_figure(os.path.join(DIAG_DIR, '01_gantt_chart.png'), "Figure 3.1: Project Work Breakdown Schedule (Gantt Chart)")

    add_h2("3.5.2 PERT Network Analysis & Critical Path")
    add_p("To determine the minimum project completion time and schedule slack, PERT analysis was applied using three time estimates: Optimistic ($a$), Most Likely ($m$), and Pessimistic ($b$) days. The expected duration is computed as $t_e = (a + 4m + b)/6$, and task variance as $\\sigma^2 = ((b - a)/6)^2$. Table 3.2 details the calculations.")

    add_table_caption("Table 3.2: PERT Activity Time Estimates, Variance, and Slack Calculations")
    pert_data = [
        ("A", "Requirements Elicitation", "—", "2.0", "3.0", "4.0", "3.00", "0.11", "0", "0", "0", "Yes"),
        ("B", "Feasibility Analysis", "A", "1.5", "2.0", "3.0", "2.08", "0.06", "3", "3", "0", "Yes"),
        ("C", "Database Architecture", "B", "2.0", "3.0", "4.0", "3.00", "0.11", "5", "5", "0", "Yes"),
        ("D", "UML System Modeling", "C", "1.5", "2.0", "3.0", "2.08", "0.06", "8", "8", "0", "Yes"),
        ("E", "Security & Auth APIs", "D", "1.5", "2.0", "3.0", "2.08", "0.06", "10", "10", "0", "Yes"),
        ("F", "Catalog & Restocking", "E", "1.5", "2.0", "3.0", "2.08", "0.06", "12", "12", "0", "Yes"),
        ("G", "Sales Engine & Reports", "F", "1.5", "2.0", "3.0", "2.08", "0.06", "14", "14", "0", "Yes"),
        ("H", "Frontend Dashboard", "G", "1.5", "2.0", "3.0", "2.08", "0.06", "16", "16", "0", "Yes"),
        ("I", "POS Billing Counter", "H", "1.5", "2.0", "3.0", "2.08", "0.06", "18", "18", "0", "Yes"),
        ("J", "Automated Jest Testing", "I", "0.8", "1.0", "1.5", "1.05", "0.01", "20", "20", "0", "Yes"),
        ("K", "System Integration Test", "J", "0.8", "1.0", "1.5", "1.05", "0.01", "21", "21", "0", "Yes"),
        ("L", "Final Documentation", "K", "0.8", "1.0", "1.5", "1.05", "0.01", "22", "22", "0", "Yes"),
    ]
    create_table(["Task", "Activity Description", "Pred", "a", "m", "b", "t_e", "Var", "ES", "EF", "Slack", "Crit"], pert_data, [Inches(0.4), Inches(1.35), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.5), Inches(0.45), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.25)], font_size_pt=9.5)

    add_p("Figure 3.2 illustrates the resulting PERT precedence network diagram showing node transitions and the critical path: A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L. The total expected critical path duration is 22.71 days (approximately 23 calendar days).")
    add_figure(os.path.join(DIAG_DIR, '02_pert_chart.png'), "Figure 3.2: Project Critical Path & Precedence Network (PERT Chart)")

    add_h1("3.6 Software Requirement Specification (SRS)")
    add_p("System requirements were specified following the IEEE Std 830-1998 format, categorizing requirements into functional and non-functional specifications.")

    add_h2("3.6.1 Functional Requirements Specification")
    add_p("Functional requirements define the core operational capabilities that the software must provide to end users. Table 3.3 summarizes the primary functional specifications.")

    add_table_caption("Table 3.3: Functional Requirements Specification & Traceability Summary")
    srs_data = [
        ("FR-01", "User Authentication", "The system shall authenticate users via email and password, issuing a signed JWT bearer token upon successful verification.", "High", "UC-01"),
        ("FR-02", "Role Authorization", "The system shall enforce RBAC, restricting user management and financial audit reports strictly to ADMIN users.", "High", "UC-01"),
        ("FR-03", "Product Cataloging", "The system shall enable managers to create, view, update, and delete products with unique SKUs and non-negative pricing.", "High", "UC-02"),
        ("FR-04", "Category Classification", "The system shall organize products into unique taxonomic categories with associated product counters.", "Medium", "UC-03"),
        ("FR-05", "Supplier Directory", "The system shall record supplier profiles including company name, telephone, and email contact info.", "Medium", "UC-04"),
        ("FR-06", "Procurement Restocking", "The system shall record multi-product purchase orders and atomically increment warehouse inventory balances.", "High", "UC-05"),
        ("FR-07", "POS Cart Management", "The system shall provide an interactive sales checkout counter allowing multi-item cart assembly with live subtotaling.", "High", "UC-06"),
        ("FR-08", "Atomic Sales Checkout", "The system shall validate available stock, atomically decrement inventory, and generate an invoice within a single transaction.", "High", "UC-06"),
        ("FR-09", "Low-Stock Alerting", "The system shall identify items where quantity <= reorderLevel, displaying visual warning badges and supplier links.", "High", "UC-07"),
        ("FR-10", "Valuation & Sales Audit", "The system shall aggregate gross stock valuation, date-filtered sales logs, and purchase audit trails.", "High", "UC-08"),
    ]
    create_table(["Req ID", "Requirement Title", "Detailed Functional Description", "Priority", "Use Case"], srs_data, [Inches(0.8), Inches(1.2), Inches(2.35), Inches(0.7), Inches(0.7)])

    add_h2("3.6.2 Non-Functional Requirements Specification")
    add_p("Non-functional requirements specify quality attributes, behavioral constraints, and system performance benchmarks:")
    add_bullet("Performance & Responsiveness: All standard database read queries (product listings, categories, suppliers) shall execute and return JSON payloads in under 500 milliseconds across a local area network.")
    add_bullet("Data Integrity & Concurrency: All inventory modifications shall execute within isolated PostgreSQL transactions under the Read Committed isolation level, ensuring zero stock balance discrepancies.")
    add_bullet("Security & Privacy: Passwords must be cryptographically hashed using bcrypt with 10 salt rounds ($2^{10}$ iterations). Inbound request payloads must be strictly sanitized against SQL injection and cross-site scripting (XSS).")
    add_bullet("Reliability & Availability: The system architecture shall maintain high operational availability (target: 99.5% uptime) with graceful error logging and automatic database connection recovery.")
    add_bullet("Portability & Maintainability: The application shall execute consistently across modern operating systems (Linux, Windows, macOS) using standard Node.js runtimes and containerized PostgreSQL database instances.")

    add_h2("3.6.3 Detailed IEEE 830 Use Case Specifications (UC-01 to UC-08)")
    add_p("To provide rigorous engineering documentation, all eight primary use cases are specified in formal IEEE 830 tabular formats detailing actors, preconditions, triggers, main success flows, alternative flows, and postconditions.")

    # UC-01
    add_table_caption("Table 3.4: Detailed Use Case Specification – UC-01: User Authentication")
    uc01_data = [
        ("Use Case ID", "UC-01: User Authentication & Role Authorization"),
        ("Primary Actor", "Store Employee (Admin or Staff)"),
        ("Preconditions", "User profile exists in database with valid email and bcrypt hashed password."),
        ("Trigger", "User navigates to the login route (/login) and submits email and password."),
        ("Main Success Scenario", "1. User inputs registered email and password.\n2. User clicks 'Sign In'.\n3. Client validates format and sends POST /api/auth/login.\n4. Server queries User entity by email.\n5. Server invokes bcrypt.compare(password, passwordHash).\n6. Server signs JWT bearer token containing id, email, and role.\n7. Server returns HTTP 200 with JWT and user metadata.\n8. Client stores token in localStorage and redirects to Dashboard (/dashboard)."),
        ("Alternative / Error Flows", "4a. Email not found: Server returns HTTP 401 'Invalid credentials'.\n5a. Password mismatch: Server returns HTTP 401 'Invalid credentials'. Client displays red error alert banner without page reload."),
        ("Postconditions", "User session is established with authenticated JWT; role guards enforce route permissions."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc01_data, [Inches(1.5), Inches(4.25)])

    # UC-02
    add_table_caption("Table 3.5: Detailed Use Case Specification – UC-02: Product Catalog Management")
    uc02_data = [
        ("Use Case ID", "UC-02: Master Product Catalog Management"),
        ("Primary Actor", "Store Manager (Admin)"),
        ("Preconditions", "Admin user is logged in with valid JWT possessing Role.ADMIN."),
        ("Trigger", "Admin opens Products page (/products) and clicks 'Add Product' or 'Edit'."),
        ("Main Success Scenario", "1. Admin enters SKU, product name, selling price, cost price, quantity, and reorder level.\n2. Admin selects Category and Supplier from dynamic dropdowns.\n3. Admin clicks 'Save Product'.\n4. Client validates non-negative pricing and dispatches POST /api/products.\n5. NestJS ValidationPipe strips unwhitelisted payload properties.\n6. ProductsService verifies SKU uniqueness.\n7. Prisma inserts record into products table.\n8. Server returns HTTP 201 Created.\n9. Client closes modal and updates product catalog table dynamically."),
        ("Alternative / Error Flows", "6a. Duplicate SKU detected: Server aborts insert, returning HTTP 400 Bad Request 'Product with this SKU already exists'. Client renders input error highlight."),
        ("Postconditions", "New product is persisted in database and immediately searchable in catalog and POS counter."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc02_data, [Inches(1.5), Inches(4.25)])

    # UC-03
    add_table_caption("Table 3.6: Detailed Use Case Specification – UC-03: Category Classification")
    uc03_data = [
        ("Use Case ID", "UC-03: Taxonomic Category Classification"),
        ("Primary Actor", "Store Manager (Admin)"),
        ("Preconditions", "Admin user is logged in with valid JWT possessing Role.ADMIN."),
        ("Trigger", "Admin opens Categories page (/categories) and enters new category title."),
        ("Main Success Scenario", "1. Admin enters category name and optional description.\n2. Admin clicks 'Create Category'.\n3. Client validates non-empty string and sends POST /api/categories.\n4. Server verifies name uniqueness in categories table.\n5. Prisma creates category record.\n6. Server returns HTTP 201 Created.\n7. UI appends new category with an initial count of 0 linked products."),
        ("Alternative / Error Flows", "4a. Duplicate name: Server returns HTTP 400 'Category already exists'.\n7a. Deletion blocked: If products reference categoryId, delete request returns HTTP 400, preventing orphan products."),
        ("Postconditions", "Category is stored and becomes available in product creation dropdown selectors."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc03_data, [Inches(1.5), Inches(4.25)])

    # UC-04
    add_table_caption("Table 3.7: Detailed Use Case Specification – UC-04: Supplier Profile Management")
    uc04_data = [
        ("Use Case ID", "UC-04: Vendor & Supplier Profile Management"),
        ("Primary Actor", "Store Manager (Admin)"),
        ("Preconditions", "Admin user is logged in with valid JWT possessing Role.ADMIN."),
        ("Trigger", "Admin navigates to Suppliers page (/suppliers) and clicks 'Add Supplier'."),
        ("Main Success Scenario", "1. Admin inputs supplier commercial name, phone number, and email address.\n2. Admin clicks 'Register Supplier'.\n3. Client validates email syntax and dispatches POST /api/suppliers.\n4. Server inserts vendor profile into suppliers table.\n5. Server returns HTTP 201 with created supplier object.\n6. UI displays new vendor in directory with active phone and email links."),
        ("Alternative / Error Flows", "3a. Invalid email syntax: Client blocks submission and highlights email field.\n4a. Server error: Returns HTTP 500; client displays toast notification."),
        ("Postconditions", "Supplier profile is stored and linked to restock purchase orders and low-stock alerts."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc04_data, [Inches(1.5), Inches(4.25)])

    # UC-05
    add_table_caption("Table 3.8: Detailed Use Case Specification – UC-05: Procurement Restocking (Inflow)")
    uc05_data = [
        ("Use Case ID", "UC-05: Procurement Restocking & Inbound Stock Inflow"),
        ("Primary Actor", "Store Manager (Admin) or Stock Supervisor"),
        ("Preconditions", "User is authenticated; suppliers and target products exist in database."),
        ("Trigger", "User navigates to Restock page (/purchases) to log inbound delivery."),
        ("Main Success Scenario", "1. User selects supplier from dropdown.\n2. User adds one or more product lines, specifying restock quantity and unit cost price.\n3. Interface calculates item subtotals and grand purchase total dynamically.\n4. User clicks 'Submit Purchase Order'.\n5. Client sends payload to POST /api/purchases.\n6. PurchasesService opens `prisma.$transaction()` block.\n7. Transaction creates Purchase header record with total cost.\n8. Transaction iterates items: inserts PurchaseItem rows and increments Product.quantity.\n9. Transaction commits atomically.\n10. Server returns HTTP 201 Created.\n11. UI clears purchase form, updates inventory counts, and appends to purchase audit log."),
        ("Alternative / Error Flows", "2a. Zero or negative quantity entered: Client blocks submission.\n8a. Database error during insert: Transaction aborts; all changes roll back; stock remains unmodified."),
        ("Postconditions", "Warehouse inventory counts increment atomically; purchase audit trail is recorded."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc05_data, [Inches(1.5), Inches(4.25)])

    # UC-06
    add_table_caption("Table 3.9: Detailed Use Case Specification – UC-06: POS Checkout & Stock Decrement")
    uc06_data = [
        ("Use Case ID", "UC-06: POS Multi-Item Checkout & Stock Outflow"),
        ("Primary Actor", "Cashier (Staff) or Store Manager (Admin)"),
        ("Preconditions", "Cashier is authenticated; products have positive physical shelf stock."),
        ("Trigger", "Customer brings items to billing counter; cashier opens POS Counter (/sales)."),
        ("Main Success Scenario", "1. Cashier searches or selects items from product grid, adding to cart.\n2. System validates that requested quantity <= current available stock.\n3. Cashier selects payment method (Cash, Card, UPI) and enters customer name.\n4. Cashier clicks 'Complete Sale'.\n5. Client sends payload to POST /api/sales.\n6. SalesService begins `prisma.$transaction()`.\n7. Transaction queries current stock for all cart items; verifies availability.\n8. Transaction generates sequential invoice string (e.g. INV-202611-0001).\n9. Transaction creates Sale header and itemized SaleItem records.\n10. Transaction decrements Product.quantity for all purchased items.\n11. Transaction commits atomically.\n12. Server returns HTTP 201 Created with full invoice payload.\n13. Client displays printable tax invoice modal dialog.\n14. Cashier clicks 'Print Invoice' to invoke browser print dialog."),
        ("Alternative / Error Flows", "2a. Cart quantity exceeds stock: UI displays red warning badge and limits quantity.\n7a. Concurrent stock exhaustion: If stock depletes between cart add and checkout submit, transaction throws HTTP 400 'Insufficient stock for product [Name]'. Cart rolls back; cashier notified."),
        ("Postconditions", "Inventory decrements atomically; sequential invoice generated; transaction logged."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc06_data, [Inches(1.5), Inches(4.25)])

    # UC-07
    add_table_caption("Table 3.10: Detailed Use Case Specification – UC-07: Low-Stock Alerting")
    uc07_data = [
        ("Use Case ID", "UC-07: Proactive Low-Stock Reordering Alerting"),
        ("Primary Actor", "Store Manager (Admin) or Stock Supervisor"),
        ("Preconditions", "Products configured with numeric reorderLevel thresholds."),
        ("Trigger", "Inventory decrement causes Product.quantity <= Product.reorderLevel."),
        ("Main Success Scenario", "1. Cashier completes a sale or audit updates shelf counts.\n2. System detects quantity <= reorderLevel via database filter query.\n3. Dashboard renders prominent amber/red low-stock alert badge.\n4. Supervisor clicks alert badge or navigates to Low-Stock Report (/reports/low-stock).\n5. System presents shortage table displaying SKU, current quantity, reorder threshold, shortage deficit, and linked supplier phone and email contacts.\n6. Supervisor clicks supplier contact to initiate replenishment order."),
        ("Alternative / Error Flows", "3a. No products below threshold: Dashboard displays green 'All Products Well Stocked' indicator badge."),
        ("Postconditions", "Depleted inventory is visually flagged with direct supplier contact channels."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc07_data, [Inches(1.5), Inches(4.25)])

    # UC-08
    add_table_caption("Table 3.11: Detailed Use Case Specification – UC-08: Financial & Operational Auditing")
    uc08_data = [
        ("Use Case ID", "UC-08: Financial Valuation & Historical Audit Reporting"),
        ("Primary Actor", "Store Manager (Admin)"),
        ("Preconditions", "Admin is logged in with valid JWT possessing Role.ADMIN."),
        ("Trigger", "Admin navigates to Reports section (/reports/stock, /reports/sales)."),
        ("Main Success Scenario", "1. Admin selects report type: Stock Summary, Purchases Audit, or Sales Audit.\n2. Admin optionally specifies start date and end date filters.\n3. Client dispatches authenticated GET query to ReportsController.\n4. ReportsService executes SQL aggregations (`SUM(quantity * price)`, `SUM(total)`).\n5. Server returns structured JSON with financial totals and itemized arrays.\n6. Client renders metric cards, revenue graphs, and paginated transaction tables.\n7. Admin reviews metrics or prints report via browser print command."),
        ("Alternative / Error Flows", "3a. Staff user attempts access: JwtAuthGuard and RolesGuard return HTTP 403 Forbidden.\n4a. No records in date range: Client displays clean 'No transactions found' state."),
        ("Postconditions", "Manager gains exact visibility over total stock valuation, procurement expenses, and sales revenue."),
    ]
    create_table(["Specification Element", "Detailed Functional Description"], uc08_data, [Inches(1.5), Inches(4.25)])

    add_h1("3.7 System Environment Specifications")
    add_p("The production and testing runtime environments are specified across hardware infrastructure and software technology stacks.")

    add_h2("3.7.1 Hardware Infrastructure Specifications")
    add_p("Table 3.12 outlines the minimum and recommended hardware specifications for server hosting and client POS billing terminals.")

    add_table_caption("Table 3.12: Server and Client Hardware Infrastructure Specifications")
    hw_data = [
        ("Server Processor", "Intel Core i3 (4 Cores, 2.0 GHz) or AMD Ryzen 3", "Intel Core i5 (6 Cores, 3.2 GHz) or AWS EC2 t4g.medium", "Adequate for 100+ req/sec API throughput"),
        ("Server Memory (RAM)", "4 GB DDR4", "8 GB to 16 GB DDR4/DDR5", "Accommodates PostgreSQL buffer pool & Node.js heap"),
        ("Server Storage", "20 GB available SSD space", "50 GB NVMe PCIe M.2 SSD", "Ensures high-speed random I/O for database queries"),
        ("Client Terminal PC", "Intel Celeron / Core 2 Duo, 2 GB RAM", "Intel Core i3, 4 GB RAM, 1080p display", "Renders Next.js React DOM without interface lag"),
        ("POS Peripherals", "Standard QWERTY keyboard, optical mouse", "USB/Wireless 1D/2D Barcode Scanner, 80mm ESC/POS Thermal Printer", "Enables rapid SKU entry and instant receipt printing"),
        ("Network Interface", "100 Mbps Local Ethernet or Wi-Fi (802.11n)", "1 Gbps Gigabit LAN / Wi-Fi 6 (802.11ax)", "Maintains sub-10ms network latency to database"),
    ]
    create_table(["Hardware Component", "Minimum Academic Prototype", "Recommended Enterprise Production", "Functional Engineering Rationale"], hw_data, [Inches(1.25), Inches(1.4), Inches(1.5), Inches(1.6)], font_size_pt=9.5)

    add_h2("3.7.2 Software Technology Stack & Dependency Rationale")
    add_p("Table 3.13 documents the software stack components, runtime versions, and engineering rationale governing tool selection.")

    add_table_caption("Table 3.13: Software Technology Stack & Dependency Version Matrix")
    sw_data = [
        ("Operating System", "Windows 11 / Ubuntu 22.04 LTS", "Cross-Platform", "POSIX compliance and reliable local development"),
        ("Backend Framework", "NestJS v11.0", "Enterprise TypeScript", "Architectural dependency injection and modularity"),
        ("JavaScript Runtime", "Node.js v22.18.0 (v22.x LTS)", "Event-Driven Engine", "Non-blocking asynchronous I/O and broad ecosystem"),
        ("Database Engine", "PostgreSQL v18.1", "Relational RDBMS", "Strict ACID compliance, foreign keys, and MVCC concurrency"),
        ("Object-Relational Mapping", "Prisma ORM v6.4.1", "Type-Safe Data Layer", "Automated schema migrations and compile-time types"),
        ("Frontend Framework", "Next.js v16.0 (App Router)", "React 19 Framework", "Fast client-side hydration and component-level caching"),
        ("CSS Architecture", "Tailwind CSS v4.0", "Utility-First CSS", "Zero runtime overhead and responsive dashboard layouts"),
        ("Language Specification", "TypeScript v5.7", "Static Type System", "Eliminates null/undefined runtime exception classes"),
        ("Cryptographic Hashing", "Bcrypt v5.1", "Key Derivation Function", "Adaptive salted password hashing (10 salt rounds)"),
        ("Token Authentication", "@nestjs/jwt v11.0", "Stateless Security", "Signed JSON Web Tokens with 24h expiration"),
    ]
    create_table(["Software Layer", "Framework & Version", "Technology Classification", "Engineering Rationale"], sw_data, [Inches(1.5), Inches(1.75), Inches(1.0), Inches(1.5)], font_size_pt=9.5)

    add_h1("3.8 Visual Data Models & Architectural Diagrams")
    add_p("To formalize software architecture and data relationships, this section documents seven visual models: Use Case, Activity, Sequence, Domain Class, and 3NF Entity-Relationship Diagrams.")

    add_h2("3.8.1 Use Case Diagram (Figure 3.3)")
    add_p("Figure 3.3 illustrates the global system use case diagram. Two human actors are modeled: Store Manager (Admin) and Cashier (Staff). The diagram defines system boundary lines and highlights role-based permissions.")
    add_figure(os.path.join(DIAG_DIR, '03_use_case_diagram.png'), "Figure 3.3: System Use Case Diagram with Actor Boundary Partitions")
    add_p("Structural Analysis: The use case model establishes clear actor boundaries. Staff users possess operational access to POS sales checkout, inventory availability checks, and receipt printing. Admin users inherit all cashier privileges while exclusively managing user provisioning, master catalog creation, category taxonomies, supplier directories, restocking, and financial audit reports.")

    add_h2("3.8.2 Activity Diagram – Sales & Stock Processing (Figure 3.4)")
    add_p("Figure 3.4 depicts the business workflow activity diagram for POS billing. The flow models the sequence of actions from cart creation through stock availability branching, atomic database transaction execution, and receipt generation.")
    add_figure(os.path.join(DIAG_DIR, '04_activity_diagram.png'), "Figure 3.4: Activity Diagram – Point-of-Sale Billing & Stock Decrement")
    add_p("Process Logic: The activity diagram models decision branches: when a cashier adds items to cart, the system checks whether requested units exceed available shelf quantity. If stock is insufficient, the flow routes to an error node displaying a stock deficit warning. If stock is sufficient, the flow proceeds to payment capture and atomic database commit.")

    add_h2("3.8.3 Sequence Diagram – POS Billing & Concurrency (Figure 3.5)")
    add_p("Figure 3.5 illustrates the chronological sequence of synchronous HTTP requests and database invocations between the Staff User, Next.js Frontend, NestJS SalesController, SalesService, and the PostgreSQL database. The diagram explicitly details the execution boundary of `prisma.$transaction()`, showing how stock decrement and invoice creation execute within an isolated ACID transaction.")
    add_figure(os.path.join(DIAG_DIR, '05_sequence_diagram.png'), "Figure 3.5: Sequence Diagram – POS Transaction & Atomic Database Commit")
    add_p("Interaction Analysis: The sequence diagram highlights the synchronous execution lifecycle: 1. User clicks Complete Sale; 2. POST /api/sales sent with Bearer JWT; 3. JwtAuthGuard decodes and verifies token; 4. SalesController invokes SalesService.create(dto); 5. prisma.$transaction starts; 6. Product quantities queried and verified; 7. Sale and SaleItem records inserted; 8. Product quantities decremented; 9. Transaction commits; 10. HTTP 201 Created returned with complete invoice JSON; 11. Modal dialog rendered with printable receipt.")

    add_h2("3.8.4 Domain Class Diagram & Object Model (Figure 3.6)")
    add_p("Figure 3.6 depicts the Object-Oriented domain model of SmartStock, showing classes, private attributes (-), public service methods (+), and multiplicity associations. Filled composition diamonds highlight strict lifecycle dependencies between Purchase and PurchaseItem (1 to 1..*), and between Sale and SaleItem (1 to 1..*), indicating that child line items cannot exist independently of their parent transactions.")
    add_figure(os.path.join(DIAG_DIR, '06_class_diagram.png'), "Figure 3.6: Domain Class Diagram & Object Model Multiplicity")
    add_p("Object Model Analysis: The domain model illustrates strong encapsulation. Domain services encapsulate business logic and data access, while Data Transfer Objects (DTOs) enforce strict schema boundaries. Compositional associations guarantee that when a sales transaction is purged, all associated item rows are deleted concurrently, preventing orphan records.")

    add_h2("3.8.5 Entity Relationship Diagram (ERD – 3NF) (Figure 3.7)")
    add_p("Figure 3.7 illustrates the complete 3NF normalized Entity-Relationship Diagram comprising eight database tables. Primary keys (PK) and foreign keys (FK) are explicitly mapped across all relationships with cascading delete rules, establishing complete relational integrity.")
    add_figure(os.path.join(DIAG_DIR, '07_er_diagram.png'), "Figure 3.7: Entity-Relationship Diagram (ERD) with 3NF Relational Mappings")
    add_p("Relational Analysis: The ERD captures all eight normalized entities: User, Category, Supplier, Product, Purchase, PurchaseItem, Sale, and SaleItem. All relationships maintain strict 1:N cardinalities. Referential integrity constraints enforce cascading deletions from parent sales and purchases to their respective child items, while protecting referenced product catalog definitions.")

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 4: SYSTEM DESIGN
    # ==========================================================================
    add_chapter_title("CHAPTER 4\nSYSTEM DESIGN")

    add_h1("4.1 Modularization Details & Architectural Patterns")
    add_p("SmartStock is engineered following modern modular architecture principles. The design enforces clear separation of concerns, high internal cohesion, and loose coupling across subsystems.")

    add_h2("4.1.1 Layered 3-Tier Web Architecture")
    add_p("The system architecture is structured across three distinct tiers:")
    add_bullet("Tier 1: Client Presentation Tier (Next.js 16 / React 19): Operates in the end-user's web browser. Employs modern React hooks (useState, useEffect, useContext) for reactive state management. Handles client-side route protection, form validation, and instant DOM updates.")
    add_bullet("Tier 2: Business Logic Application Tier (NestJS 11): Operates as the central API gateway and business processing engine. Implements the Controller-Service-Repository pattern. Controllers map inbound RESTful HTTP routes; Services execute business logic, DTO validation, and transaction boundaries; Guards enforce cryptographic JWT role permissions.")
    add_bullet("Tier 3: Data Persistence Tier (PostgreSQL 18.1 & Prisma ORM): Manages physical database storage, B-tree indexes, foreign key enforcement, and ACID transaction isolation. Prisma Client acts as the type-safe abstraction layer between Node.js and PostgreSQL.")

    add_h2("4.1.2 Enterprise Design Patterns (IoC, DTO, Unit of Work)")
    add_p("SmartStock integrates four established enterprise software design patterns:")
    add_bullet("Inversion of Control (IoC) & Dependency Injection: NestJS utilizes an IoC container that dynamically instantiates and injects service providers (such as PrismaService and JwtService) into controllers and services. This pattern decouples service implementations, simplifies unit test mocking, and guarantees clean singleton lifecycles.")
    add_bullet("Data Transfer Object (DTO) Pattern: All inbound payloads are strongly typed via DTO classes. Combined with NestJS ValidationPipe, DTOs strip unwhitelisted fields, enforce numeric range limits, and convert types before execution reaches business services.")
    add_bullet("Unit of Work Pattern: Prisma's interactive transaction API (`prisma.$transaction(async (tx) => { ... })`) implements the Unit of Work pattern. It tracks all database operations within a business workflow and executes them within a single atomic commit or rollback.")
    add_bullet("Single Responsibility Principle (SRP): Each subsystem module is isolated within its own directory containing dedicated controllers, services, DTOs, and entity definitions, preventing cross-module code tangling.")

    add_h2("4.1.3 Core Subsystem Modules (Modules 1 to 5)")
    add_p("The application architecture is decomposed into five core subsystem modules aligned with the project synopsis:")
    add_bullet("Module 1: User Authentication, Authorization & Administration Subsystem (AuthModule, UsersModule): Governs user credential verification, password hashing via bcrypt (10 rounds of salt), and stateless JWT token signing with symmetric HMAC-SHA256. Enforces Role-Based Access Control (RBAC) across Admin and Staff roles, providing provisioning endpoints to create, update, and manage employee accounts.")
    add_bullet("Module 2: Master Product Catalog & Taxonomy Subsystem (ProductsModule, CategoriesModule): Serves as the central inventory registry and classification engine. Enforces unique SKU constraints, positive pricing validation, category grouping, and high-speed debounced search filtering.")
    add_bullet("Module 3: Supplier Profile & Procurement Restocking Subsystem (SuppliersModule, PurchasesModule): Manages vendor directory profiles and orchestrates inbound stock restocking. Accepts supplier invoices, inserts itemized purchase records, and atomically increments product warehouse inventory inside a database transaction.")
    add_bullet("Module 4: Point-of-Sale (POS) Multi-Item Billing Subsystem (SalesModule): Executes real-time sales checkout counter operations, validates instantaneous stock availability, atomically decrements inventory, prevents overselling, and generates formatted sequential tax invoices.")
    add_bullet("Module 5: Financial Auditing & Analytics Reporting Subsystem (ReportsModule): Aggregates real-time business intelligence, total inventory valuation, date-filtered procurement expense logs, cashier revenue histories, and proactive low-stock threshold alerting.")

    add_h1("4.2 Database Design & Data Integrity")
    add_p("A robust relational database schema is paramount for preventing data redundancy, update anomalies, and inventory inconsistencies.")

    add_h2("4.2.1 Formal Normalization Proofs (UNF to 3NF & BCNF)")
    add_p("The database schema was engineered through a formal normalization progression from an unnormalized state (UNF) to Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF):")
    add_bullet("Unnormalized Form (UNF): The initial operational concept grouped all sales, customer, product, and supplier data into flat, multi-attribute spreadsheets containing repeating item groups.")
    add_bullet("First Normal Form (1NF): Achieved by eliminating repeating groups and ensuring all attribute values are strictly atomic. Each table was assigned a distinct primary key (id autoincrement integer), and individual item rows were separated into child line-item tables.")
    add_bullet("Second Normal Form (2NF): Achieved by ensuring that all non-key attributes are fully functionally dependent on the entire primary key, eliminating partial dependencies. In composite tables such as PurchaseItem and SaleItem, pricing and quantity attributes depend strictly on the composite key (saleId + productId).")
    add_bullet("Third Normal Form (3NF): Achieved by eliminating transitive functional dependencies ($X \\rightarrow Y$ where $Y$ is not a candidate key). Category titles and supplier phone numbers were moved into dedicated Category and Supplier tables, leaving only foreign key references (categoryId, supplierId) in the Product table.")
    add_bullet("Boyce-Codd Normal Form (BCNF): Because every functional dependency $X \\rightarrow Y$ across the entire schema has a determinant $X$ that is a candidate key (or primary key), the schema strictly satisfies Boyce-Codd Normal Form.")

    add_table_caption("Table 4.1: Database Functional Dependency & Normalization Transition (1NF to 3NF)")
    norm_data = [
        ("UNF -> 1NF", "Sales with repeating item rows", "Atomicity achieved; primary key id established", "Eliminated repeating cart arrays in single records"),
        ("1NF -> 2NF", "Partial dependencies on composite keys", "SaleItem and PurchaseItem separated with own PKs", "Eliminated partial dependencies on order headers"),
        ("2NF -> 3NF", "Transitive dependencies (Product -> Category name)", "Extracted Category and Supplier tables with FKs", "Eliminated transitive update and deletion anomalies"),
        ("3NF -> BCNF", "All functional determinants are superkeys", "Every dependency X -> Y has X as candidate key", "Verified zero non-trivial functional anomalies"),
    ]
    create_table(["Normalization Stage", "Initial Relational Anomaly", "Schema Decomposition Solution", "Relational Integrity Result"], norm_data, [Inches(1.1), Inches(1.5), Inches(1.55), Inches(1.6)], font_size_pt=9.5)

    add_h2("4.2.2 Relational Integrity Constraints & Referential Actions")
    add_p("SmartStock establishes strict relational integrity rules across all foreign key relationships:")
    add_bullet("ON DELETE CASCADE: Configured on `PurchaseItem` and `SaleItem` foreign keys referencing parent `Purchase` and `Sale` records. When an order record is deleted, all child item rows are purged automatically, eliminating orphan records.")
    add_bullet("ON DELETE RESTRICT: Configured on `Product` foreign keys referencing `Category` and `Supplier`. The database engine rejects deletion of a category or supplier if active products reference it, preventing catalog corruption.")
    add_bullet("UNIQUE Constraints: Enforced on `User.email`, `Category.name`, `Product.sku`, and `Sale.invoiceNumber` to ensure absolute uniqueness.")

    add_h2("4.2.3 Comprehensive System Data Dictionary (Tables 4.2 to 4.9)")
    add_p("The physical database schema comprises eight tables detailed in the data dictionary tables below:")

    add_table_caption("Table 4.2: Data Dictionary – User Entity (users table)")
    user_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique user primary key"),
        ("name", "String", "VARCHAR(255)", "No", "Full employee display name"),
        ("email", "String", "VARCHAR(255), UNIQUE", "No", "Unique user login email address"),
        ("passwordHash", "String", "VARCHAR(255)", "No", "Cryptographic bcrypt salted password hash"),
        ("role", "Enum (Role)", "DEFAULT 'STAFF'", "No", "RBAC authorization role ('ADMIN' or 'STAFF')"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Timestamp of account registration"),
        ("updatedAt", "DateTime", "AUTO_UPDATE", "No", "Timestamp of most recent profile modification"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], user_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.3: Data Dictionary – Category Entity (categories table)")
    cat_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique category primary key"),
        ("name", "String", "VARCHAR(100), UNIQUE", "No", "Distinct product classification title"),
        ("description", "String", "TEXT", "Yes", "Optional descriptive summary of category scope"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Timestamp of category creation"),
        ("updatedAt", "DateTime", "AUTO_UPDATE", "No", "Timestamp of category update"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], cat_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.4: Data Dictionary – Supplier Entity (suppliers table)")
    sup_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique supplier primary key"),
        ("name", "String", "VARCHAR(255)", "No", "Official commercial name of vendor company"),
        ("contact", "String", "VARCHAR(100)", "Yes", "Telephone or mobile contact number"),
        ("email", "String", "VARCHAR(255)", "Yes", "Official supplier email address for reorder notices"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Timestamp of vendor registration"),
        ("updatedAt", "DateTime", "AUTO_UPDATE", "No", "Timestamp of vendor profile update"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], sup_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.5: Data Dictionary – Product Entity (products table)")
    prod_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique product primary key"),
        ("name", "String", "VARCHAR(255)", "No", "Commercial product display name"),
        ("sku", "String", "VARCHAR(100), UNIQUE", "No", "Stock Keeping Unit code (e.g. ELEC-LOGI-M185)"),
        ("description", "String", "TEXT", "Yes", "Detailed technical or commercial item description"),
        ("price", "Decimal", "DECIMAL(10,2)", "No", "Retail selling price charged per unit at checkout"),
        ("costPrice", "Decimal", "DECIMAL(10,2)", "No", "Wholesale procurement acquisition cost per unit"),
        ("quantity", "Int", "INTEGER, DEFAULT 0", "No", "Current physical inventory shelf count"),
        ("reorderLevel", "Int", "INTEGER, DEFAULT 10", "No", "Threshold level triggering low-stock warning"),
        ("categoryId", "Int", "FK -> Category(id)", "No", "Foreign key linking product to category"),
        ("supplierId", "Int", "FK -> Supplier(id)", "No", "Foreign key linking product to primary vendor"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Timestamp of initial SKU creation"),
        ("updatedAt", "DateTime", "AUTO_UPDATE", "No", "Timestamp of most recent inventory change"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], prod_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.6: Data Dictionary – Purchase Entity (purchases table)")
    purch_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique procurement transaction identifier"),
        ("supplierId", "Int", "FK -> Supplier(id)", "No", "Foreign key identifying vendor supplying stock"),
        ("total", "Decimal", "DECIMAL(10,2)", "No", "Gross financial cost of purchase order"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Date and time procurement was recorded"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], purch_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.7: Data Dictionary – PurchaseItem Entity (purchase_items table)")
    pitem_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique purchase line item identifier"),
        ("purchaseId", "Int", "FK -> Purchase(id), CASCADE", "No", "Parent purchase transaction linkage"),
        ("productId", "Int", "FK -> Product(id)", "No", "Target product being restocked"),
        ("quantity", "Int", "INTEGER", "No", "Number of units received into warehouse"),
        ("costPrice", "Decimal", "DECIMAL(10,2)", "No", "Unit procurement price paid for item"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], pitem_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.8: Data Dictionary – Sale Entity (sales table)")
    sale_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique sales billing transaction identifier"),
        ("invoiceNumber", "String", "VARCHAR(50), UNIQUE", "No", "Sequential invoice string (INV-YYYYMM-XXXX)"),
        ("customerName", "String", "VARCHAR(255)", "Yes", "Optional customer name for tax invoice"),
        ("total", "Decimal", "DECIMAL(10,2)", "No", "Total financial amount charged for checkout"),
        ("paymentMethod", "String", "VARCHAR(50)", "No", "Settlement method ('CASH', 'CARD', 'UPI')"),
        ("userId", "Int", "FK -> User(id)", "No", "Foreign key identifying cashier processing checkout"),
        ("createdAt", "DateTime", "CURRENT_TIMESTAMP", "No", "Date and time transaction was completed"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], sale_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    add_table_caption("Table 4.9: Data Dictionary – SaleItem Entity (sale_items table)")
    sitem_dict_data = [
        ("id", "Int", "PK, Autoincrement", "No", "Unique sales line item identifier"),
        ("saleId", "Int", "FK -> Sale(id), CASCADE", "No", "Parent sales invoice linkage"),
        ("productId", "Int", "FK -> Product(id)", "No", "Product sold at checkout"),
        ("quantity", "Int", "INTEGER", "No", "Quantity of units sold to customer"),
        ("price", "Decimal", "DECIMAL(10,2)", "No", "Unit selling price charged at checkout"),
    ]
    create_table(["Field Name", "Data Type", "Constraints / Indexes", "Nullable", "Functional Description"], sitem_dict_data, [Inches(1.0), Inches(0.75), Inches(1.5), Inches(0.65), Inches(1.85)], font_size_pt=9.5)

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 5: TESTING & QUALITY ASSURANCE
    # ==========================================================================
    add_chapter_title("CHAPTER 5\nTESTING & QUALITY ASSURANCE")

    add_h1("5.1 Testing Strategy & Methodologies")
    add_p("To verify that SmartStock operates reliably under real-world retail workflows, a comprehensive multi-layered testing strategy was implemented encompassing automated unit testing, integration testing, and black-box system validation:")
    add_bullet("Unit Testing: Focused on isolating individual domain services (SalesService, AuthService, ProductsService, ReportsService) using mock repositories to verify business calculations, DTO validations, and exception handling paths.")
    add_bullet("Integration Testing: Evaluated interactions between NestJS controllers, service providers, Prisma ORM, and the PostgreSQL database engine to ensure transactional integrity across multi-entity operations.")
    add_bullet("Black-Box System Testing: Validated end-to-end user workflows against functional requirements from the perspective of both Admin and Staff personas via real browser execution.")

    add_h1("5.2 Automated Unit & Integration Test Execution Results")
    add_p("Automated tests were executed in the Node.js runtime using the Jest test runner. All five test suites containing fifteen automated tests passed successfully with zero failures. Table 5.1 summarizes the execution results.")

    add_table_caption("Table 5.1: Jest Automated Unit & Integration Test Suite Execution Results")
    jest_results_data = [
        ("src/app.controller.spec.ts", "AppController", "1", "1", "0", "0.42 s", "PASSED"),
        ("src/auth/auth.service.spec.ts", "AuthService", "3", "3", "0", "0.68 s", "PASSED"),
        ("src/products/products.service.spec.ts", "ProductsService", "4", "4", "0", "0.55 s", "PASSED"),
        ("src/sales/sales.service.spec.ts", "SalesService", "4", "4", "0", "0.48 s", "PASSED"),
        ("src/reports/reports.service.spec.ts", "ReportsService", "3", "3", "0", "0.43 s", "PASSED"),
        ("Total Aggregated Test Suite", "All 5 Modules", "15", "15", "0", "2.56 s", "ALL PASSED"),
    ]
    create_table(["Test Suite File", "Target Module Under Test", "Tests", "Passed", "Failed", "Duration", "Execution Status"], jest_results_data, [Inches(1.75), Inches(1.2), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.6), Inches(0.7)], font_size_pt=9.5)

    add_h1("5.3 Code Coverage Analysis & Metrics Breakdown")
    add_p("Code coverage analysis was performed using Jest's built-in Istanbul coverage engine (`jest --coverage`). Table 5.2 presents the statement, branch, function, and line coverage metrics measured directly from the live test runner execution.")

    add_table_caption("Table 5.2: Backend Service Code Coverage Metrics Breakdown")
    cov_data = [
        ("src/auth/auth.service.ts", "100.0%", "83.33%", "100.0%", "100.0%", "High (Bcrypt & JWT Verified)"),
        ("src/sales/sales.service.ts", "83.78%", "68.75%", "75.00%", "82.35%", "High (ACID Transaction Verified)"),
        ("src/reports/reports.service.ts", "46.55%", "13.63%", "55.55%", "45.83%", "Moderate (SQL Aggregations Verified)"),
        ("src/products/products.service.ts", "32.00%", "14.00%", "57.14%", "30.23%", "Moderate (CRUD & Search Verified)"),
        ("src/app.service.ts", "100.0%", "100.0%", "100.0%", "100.0%", "High (Health Checks Verified)"),
        ("Tested Core Service Modules", "72.50%", "55.94%", "77.54%", "71.68%", "Partially Meets Target (Core transaction services exceed 80% threshold: AuthService 100%, SalesService 82.4%)"),
    ]
    create_table(["Source File Component", "% Statements", "% Branches", "% Functions", "% Lines", "Quality Assessment"], cov_data, [Inches(1.85), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.65), Inches(1.15)], font_size_pt=9.5)

    add_p("The core transaction engines governing sales stock deduction and credential verification achieved high coverage exceeding the 80% target (100% line coverage for AuthService and 82.35% line coverage for SalesService), confirming that all primary success paths, stock exhaustion exceptions, and authentication failure branches are thoroughly tested. Peripheral reporting and product catalog modules average 45.8% and 30.2% line coverage respectively, bringing overall tested coverage to 71.68% and establishing clear priorities for future test expansion.")

    add_h1("5.4 Comprehensive System Test Execution Matrix (TC-01 to TC-20)")
    add_p("Table 5.3 documents twenty detailed system test cases covering every functional domain, detailing test objectives, inputs, expected behaviors, actual outputs, and execution results.")

    add_table_caption("Table 5.3: Comprehensive System Test Execution Matrix (TC-01 through TC-20)")
    tc_data = [
        ("TC-01", "Auth", "Valid Login", "Valid admin email & password", "JWT token returned; redirect to dashboard", "Token issued; dashboard loaded", "PASS"),
        ("TC-02", "Auth", "Invalid Password", "Correct email, incorrect password", "401 Unauthorized with error message", "401 returned; 'Invalid credentials'", "PASS"),
        ("TC-03", "Auth", "Unregistered User", "Non-existent email address", "401 Unauthorized returned", "401 returned; login rejected", "PASS"),
        ("TC-04", "RBAC", "Staff Route Security", "Staff token requesting /api/users", "403 Forbidden error returned", "403 Forbidden; access blocked", "PASS"),
        ("TC-05", "Product", "Add Valid Product", "SKU: 'PROD-01', Price: 150.00", "Product created with 201 Created", "Product stored in DB; listed in UI", "PASS"),
        ("TC-06", "Product", "Duplicate SKU", "Reuse existing SKU 'PROD-01'", "400 Bad Request ('SKU already exists')", "Duplicate rejected with 400 error", "PASS"),
        ("TC-07", "Product", "Negative Price", "Enter price: -50.00", "Validation error blocks submission", "Client validation blocks submission", "PASS"),
        ("TC-08", "Category", "Add Category", "Category title: 'Stationery'", "Category stored with 201 Created", "Category listed in dropdowns", "PASS"),
        ("TC-09", "Supplier", "Add Supplier", "Name: 'Atlas Traders', Phone", "Supplier recorded successfully", "Supplier profile displayed in list", "PASS"),
        ("TC-10", "Purchase", "Inflow Restock", "Restock 50 units of PROD-01", "Stock incremented by 50 units", "Stock count updated from 10 to 60", "PASS"),
        ("TC-11", "POS", "Single Item Sale", "Sell 2 units of PROD-01", "Stock decremented by 2; Invoice issued", "Stock is 58; Invoice INV-... created", "PASS"),
        ("TC-12", "POS", "Stock Deficit Block", "Attempt sale of 100 units (avail: 58)", "Sale blocked; 400 Insufficient Stock", "Sale rejected; error prompt shown", "PASS"),
        ("TC-13", "POS", "Zero Qty Validation", "Cart item with 0 quantity", "Checkout button disabled", "System blocks zero quantity cart", "PASS"),
        ("TC-14", "POS", "Multi-Item Cart", "Cart with 3 distinct products", "Atomic transaction decrements all 3", "All 3 items decremented; invoice issued", "PASS"),
        ("TC-15", "Alerts", "Low-Stock Badge", "Reduce stock below reorderLevel", "Warning badge shown on Dashboard", "Red low-stock badge displayed", "PASS"),
        ("TC-16", "Reports", "Stock Summary", "Request inventory valuation", "Accurate valuation sum(qty*price)", "Table matches physical product sum", "PASS"),
        ("TC-17", "Reports", "Low-Stock Filter", "Query /api/reports/low-stock", "Only items with qty <= reorderLevel", "Correct filtered low-stock table", "PASS"),
        ("TC-18", "Reports", "Date Filter", "Filter sales by date range", "Returns sales within start/end dates", "Accurately filtered transaction list", "PASS"),
        ("TC-19", "Security", "SQL Injection", "Input ' OR '1'='1 in search field", "Treated as literal string; safe query", "Prisma parameters block injection", "PASS"),
        ("TC-20", "UI", "Invoice Print", "Click 'Print Invoice' in modal", "Browser native print dialog triggered", "Print dialog opens with clean receipt", "PASS"),
    ]
    create_table(["Test ID", "Module", "Test Scenario", "Input Data", "Expected Output", "Actual Result", "Status"], tc_data, [Inches(0.55), Inches(0.6), Inches(1.05), Inches(1.25), Inches(1.15), Inches(0.75), Inches(0.4)], font_size_pt=9.0)

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 6: SYSTEM SECURITY MEASURES & DEPLOYMENT
    # ==========================================================================
    add_chapter_title("CHAPTER 6\nSYSTEM SECURITY MEASURES & DEPLOYMENT")

    add_h1("6.1 Authentication & Authorization Pipeline (JWT & Bcrypt)")
    add_p("Application security is established through a defense-in-depth architecture combining industry-standard cryptographic primitives and strict role guards:")
    add_bullet("Bcrypt Password Hashing: User credentials are never stored in plaintext. Passwords undergo salted one-way hashing using bcrypt with 10 salt rounds ($2^{10} = 1,024$ key expansion iterations). This introduces computational work factors that render offline dictionary and rainbow table attacks infeasible.")
    add_bullet("JSON Web Token (JWT) Bearer Authentication: Upon successful authentication, the server signs a stateless JWT bearer token using symmetric HMAC-SHA256 (HS256) containing the user ID, email, and assigned Role in its cryptographic payload. The token expires in 24 hours, limiting exposure in the event of client-side token interception.")
    add_bullet("Role-Based Access Control (RBAC): Inbound requests pass through NestJS `JwtAuthGuard` and `RolesGuard`. Route handlers annotate permission requirements using the `@Roles(Role.ADMIN)` decorator. If a staff user attempts to access administrative endpoints (such as `/api/users`), the guard immediately halts execution with a 403 Forbidden exception.")

    add_h1("6.2 Inbound Payload Sanitization & SQL Injection Mitigation")
    add_p("To eliminate common web application vulnerabilities (OWASP Top 10), SmartStock enforces strict data validation and query parameterization:")
    add_bullet("Server-Side DTO Validation: All inbound JSON payloads are bound to TypeScript Data Transfer Objects (DTOs) decorated with `class-validator` rules (`@IsString()`, `@IsNotEmpty()`, `@IsPositive()`). NestJS `ValidationPipe` with `{ whitelist: true, forbidNonWhitelisted: true }` automatically strips unexpected or malicious fields before execution reaches service handlers.")
    add_bullet("Prisma ORM SQL Injection Immunity: Prisma completely decouples application code from raw SQL string concatenation. All database operations execute through prepared, parameterized SQL statements generated by the Prisma query engine, guaranteeing absolute immunity against SQL injection attacks.")
    add_bullet("Cross-Origin Resource Sharing (CORS): The NestJS HTTP server configures CORS to restrict incoming requests strictly to the authorized Next.js frontend origin (`http://localhost:3000`), rejecting unauthorized third-party origins.")

    add_h1("6.3 ACID Transaction Mechanics & Rollback Handling")
    add_p("The integrity of retail stock tracking hinges on the strict enforcement of ACID properties during stock-altering operations. SmartStock implements ACID guarantees through Prisma's interactive transaction API (`prisma.$transaction`):")
    add_bullet("Atomicity: In both sales checkout and purchase restocking, parent records and child line-item rows are inserted together with product stock balance adjustments. If any single operation fails (such as a database constraint violation or network interruption), the entire transaction aborts and rolls back completely.")
    add_bullet("Consistency: Invariant constraints—such as non-negative stock counts and valid foreign keys—are maintained continuously. A sale that would cause stock to drop below zero is blocked before the commit occurs.")
    add_bullet("Isolation: The PostgreSQL database engine executes transactions under the Read Committed isolation level, preventing dirty reads and non-repeatable reads during concurrent operations.")
    add_bullet("Durability: Committed transactions are permanently written to PostgreSQL Write-Ahead Logging (WAL) files on non-volatile storage before acknowledgement, guaranteeing data recovery even in the event of an abrupt power loss.")

    add_h1("6.4 Deployment Topology & Operating Environment")
    add_p("The application is architected for modular containerized or bare-metal deployment. In production, the NestJS API server operates as a managed Node.js process behind an Nginx reverse proxy providing TLS/SSL termination. The Next.js frontend is served via Node.js or static CDN edge points, communicating over HTTPS with the backend. PostgreSQL runs as an isolated system service with periodic pg_dump backup automation.")

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 7: RESULTS, DISCUSSION & COST ESTIMATION
    # ==========================================================================
    add_chapter_title("CHAPTER 7\nRESULTS, DISCUSSION & COST ESTIMATION")

    add_h1("7.1 Operational Impact & Performance Benchmarks")
    add_p("The operational impact of deploying SmartStock was evaluated by comparing system performance metrics against established manual retail store baselines. The performance improvements presented in Table 7.1 reflect projected operational design targets and verified technical benchmarks achieved during prototype testing.")

    add_table_caption("Table 7.1: Projected Operational Improvements vs. Manual Retail Baseline")
    perf_data = [
        ("Checkout Transaction Time", "2.5 to 4.0 minutes (Manual ledger/calc)", "15 to 30 seconds (POS multi-item cart)", "Projected ~85% reduction in checkout queue delays"),
        ("Arithmetic Error Rate", "3% to 7% of manual calculations", "0.0% (Automated floating-point math)", "Complete elimination of calculation errors"),
        ("Daily Stock Audit Duration", "60 to 120 minutes daily manual count", "Instantaneous (< 1 second report query)", "Projected >95% reduction in managerial labor"),
        ("Stockout Incident Frequency", "Frequent (Reactive order placement)", "Projected >70% reduction via alerts", "Proactive threshold reorder notifications"),
        ("Audit Trail Accountability", "None (Unprotected paper registers)", "Cryptographic JWT role-stamped logs", "Complete transparency and employee oversight"),
    ]
    create_table(["Operational Performance Metric", "Manual Retail Store Baseline", "SmartStock Software Target", "Observed / Projected Improvement"], perf_data, [Inches(1.45), Inches(1.5), Inches(1.4), Inches(1.4)], font_size_pt=9.5)

    add_h1("7.2 Concurrency Analysis & High-Volume Invoice Sequencing")
    add_p("A critical technical aspect of the sales engine is invoice number generation. In the current academic prototype, invoice identifiers follow the pattern `INV-YYYYMM-XXXX`, computed via `count() + 1` within the transaction:")
    add_p("`const invoiceNumber = `INV-${year}${month}-${String(count + 1).padStart(4, '0')}`;`")
    add_p("Under single-terminal retail operations, this pattern executes reliably without conflict. However, rigorous software engineering analysis reveals that under high-concurrency environments—where multiple cashiers submit checkouts at the exact same millisecond—a race condition could emerge where two simultaneous transactions compute the same `count + 1`, causing one transaction to fail due to the database `UNIQUE` constraint on `Sale.invoiceNumber`.")
    add_p("To eliminate this limitation in multi-terminal production environments, two standard architectural mitigations were formulated:")
    add_bullet("PostgreSQL Sequence Engine: Replacing programmatic count queries with an atomic native database sequence (`CREATE SEQUENCE invoice_seq;`), where `nextval('invoice_seq')` guarantees non-blocking, unique sequential values even under concurrent load.")
    add_bullet("Cryptographic UUID Invoice Identifiers: Appending short random alphanumeric hashes (e.g. `INV-202611-A8F2`) to eliminate concurrency collision risks entirely.")

    add_h1("7.3 Software Cost & Effort Estimation (COCOMO Basic Model)")
    add_p("Software development effort, scheduling, and labor expenditures were calculated using Boehm's Basic COCOMO (Constructive Cost Model) for Organic software projects. In the Organic mode, project parameters are $a_b = 2.4$, $b_b = 1.05$, $c_b = 2.5$, and $d_b = 0.38$.")
    add_p("Codebase Size Analysis: Across 66 project source files (excluding external dependencies and build artifacts), the SmartStock codebase comprises 4,874 total lines of TypeScript and Prisma code (4.874 KLOC effective source lines of code):")
    add_bullet("Backend TypeScript Source (Controllers, Services, DTOs, Prisma Schema): 2,250 LOC")
    add_bullet("Frontend TypeScript/React Source (App Router Views, Context, Components): 2,624 LOC")
    add_bullet("Total Codebase Size = 4,874 LOC = 4.874 KLOC")
    add_p("COCOMO Mathematical Computations:")
    add_bullet("Development Effort: $E = a_b \\times (KLOC)^{b_b} = 2.4 \\times (4.874)^{1.05} \\approx 2.4 \\times 5.2754 = 12.66$ Person-Months")
    add_bullet("Nominal Development Time: $D = c_b \\times (E)^{d_b} = 2.5 \\times (12.66)^{0.38} \\approx 2.5 \\times 2.6247 = 6.56$ Months")
    add_bullet("Average Staffing Size: $SS = E / D = 12.66 / 6.56 \\approx 1.93$ Persons")
    add_bullet("Software Productivity: $P = KLOC / E = 4.874 / 12.66 \\approx 385$ LOC / Person-Month")
    add_p("In the context of this academic BCA project, development was executed under a concentrated 23-day schedule through the utilization of modern component frameworks and rapid prototyping tools. Table 7.2 summarizes the software and hardware cost estimation.")

    add_table_caption("Table 7.2: Basic COCOMO Software Cost and Effort Estimation Summary")
    cocomo_data = [
        ("Development Software Stack", "Node.js, PostgreSQL, Next.js, NestJS, Prisma", "Open-Source (MIT)", "₹0 (Zero License Cost)"),
        ("Integrated Development Environment", "Visual Studio Code, Git, Postman, draw.io", "Community Editions", "₹0 (Free / Open-Source)"),
        ("Server & Client Hardware", "Existing retail desktop PC (Intel i5, 8GB RAM)", "Pre-existing hardware", "₹0 (No new hardware needed)"),
        ("Estimated Commercial Labor Value", "12.66 Person-Months @ ₹30,000/month", "Student academic project", "₹3,79,800 (Equivalent Value)"),
        ("Total Net Capital Expenditure", "Capital out-of-pocket software expenditure", "Permissive open-source", "₹0 Total Out-of-Pocket Cost"),
    ]
    create_table(["Cost Component Description", "Resource Specifications", "Licensing Model", "Fiscal Expenditure / Value"], cocomo_data, [Inches(1.5), Inches(1.55), Inches(1.2), Inches(1.5)], font_size_pt=9.5)

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 8: REPORT (SYSTEM OUTPUT & SCREENS)
    # ==========================================================================
    add_chapter_title("CHAPTER 8\nREPORT (SYSTEM OUTPUT & SCREENS)")

    add_h1("8.1 Screen Walkthrough & Functional Verification (Figures 8.1 to 8.14)")
    add_p("This chapter documents the genuine user interface screens of the SmartStock application, captured directly from the live running prototype in Google Chrome. Each screen is presented with a detailed functional walkthrough of UI components, user interactions, and operational validation behavior.")

    # Screen 8.1
    add_h2("8.1.1 User Authentication Screen (Figure 8.1)")
    add_p("Figure 8.1 shows the user login interface. The screen provides a clean, distraction-free authentication card with email and password inputs, role-based login hint banners, and responsive validation error handling. Submitting valid credentials triggers JWT token issuance and redirects the user to the analytics dashboard.")
    add_figure(os.path.join(SCR_DIR, '01_login_screen.png'), "Figure 8.1: User Authentication & Role-Based Login Screen")
    add_p("Operational Analysis: The authentication form performs pre-flight client-side email format validation before dispatching an HTTP POST request to `/api/auth/login`. In the event of invalid credentials, a red alert banner renders dynamically without requiring a full page reload, maintaining seamless user feedback.")

    # Screen 8.2
    add_h2("8.1.2 Executive Analytics Dashboard Overview (Figure 8.2)")
    add_p("Figure 8.2 depicts the executive analytics dashboard. Four primary KPI summary cards present real-time aggregated metrics: Total Products in catalog, Total Inventory Valuation (sum of quantity * price), Total Sales Revenue, and an active Low Stock Alert badge. A quick actions bar enables immediate navigation to Restock, New Sale, or Add Product workflows.")
    add_figure(os.path.join(SCR_DIR, '02_dashboard_overview.png'), "Figure 8.2: Executive Analytics & Operational KPI Dashboard Overview")
    add_p("Operational Analysis: The dashboard acts as the primary nerve center for store supervisors. Aggregated monetary metrics are formatted using Indian Rupee (INR) currency formatting. The low-stock badge dynamically transitions from emerald green to amber/red when items require urgent supplier replenishment.")

    # Screen 8.3
    add_h2("8.1.3 Master Product Catalog Management Console (Figure 8.3)")
    add_p("Figure 8.3 illustrates the master product catalog table. The interface displays all active inventory items with SKU codes, product names, category badges, supplier associations, unit prices, available stock counts, and reorder levels. Real-time search filters allow cashiers and managers to locate products instantly by SKU or title.")
    add_figure(os.path.join(SCR_DIR, '03_products_catalog.png'), "Figure 8.3: Master Product Catalog Management Console")
    add_p("Operational Analysis: The catalog interface features client-side debounced search filtering. Users can filter inventory across hundreds of items with sub-100ms response times. Visual inventory badges highlight stock availability status: green indicates comfortable buffer stock, while amber badges highlight products nearing replenishment levels.")

    # Screen 8.4
    add_h2("8.1.4 Product Creation & SKU Attribute Configuration Modal (Figure 8.4)")
    add_p("Figure 8.4 displays the 'Add Product' modal dialog. Form fields enforce validation rules for SKU strings, product display names, category dropdown selections, supplier linkages, selling prices, cost prices, initial stock quantities, and minimum reorder thresholds. The modal validates that prices and quantities are strictly non-negative before API transmission.")
    add_figure(os.path.join(SCR_DIR, '03b_add_product_modal.png'), "Figure 8.4: Product Creation & SKU Attribute Configuration Modal")
    add_p("Operational Analysis: The modal utilizes controlled React form inputs. Numeric inputs (Selling Price, Cost Price, Quantity, Reorder Level) reject alphabetic keystrokes. Upon clicking 'Save Product', the form sends an authenticated payload to `POST /api/products`, automatically refreshing the parent catalog view upon successful record insertion.")

    # Screen 8.5
    add_h2("8.1.5 Product Taxonomy & Category Management Interface (Figure 8.5)")
    add_p("Figure 8.5 illustrates the category management console. Store managers can define distinct taxonomic groupings (e.g., Electronics, Accessories, Perishables) with descriptions. The system enforces category name uniqueness and displays the count of active products associated with each category.")
    add_figure(os.path.join(SCR_DIR, '04_categories_management.png'), "Figure 8.5: Product Taxonomy & Category Management Interface")
    add_p("Operational Analysis: Categories provide structural organization for large retail inventories. The interface displays active product counts per category. Foreign key integrity prevents the deletion of categories that currently contain active products, safeguarding catalog consistency.")

    # Screen 8.6
    add_h2("8.1.6 Vendor & Supplier Profile Directory (Figure 8.6)")
    add_p("Figure 8.6 shows the supplier management directory. Vendor profiles record company names, telephone contacts, and email addresses. This directory provides managers with immediate vendor contact details when restocking low-inventory product lines.")
    add_figure(os.path.join(SCR_DIR, '05_suppliers_directory.png'), "Figure 8.6: Vendor & Supplier Profile Directory")
    add_p("Operational Analysis: Vendor profiles centralize external supply chain contacts. When products reach low-stock thresholds, the system cross-references this directory, allowing store clerks to immediately place telephone or email purchase orders with the authorized distributor.")

    # Screen 8.7
    add_h2("8.1.7 Procurement Restocking & Multi-Item Purchase Entry (Figure 8.7)")
    add_p("Figure 8.7 depicts the procurement restocking screen. Users select a vendor supplier and assemble multi-product purchase orders specifying restock quantities and unit cost prices. Submitting the order triggers an atomic database transaction that logs the purchase and automatically increments physical warehouse stock counts.")
    add_figure(os.path.join(SCR_DIR, '06_purchases_restocking.png'), "Figure 8.7: Procurement Restocking & Multi-Item Purchase Entry")
    add_p("Operational Analysis: Restocking is modeled as an atomic inbound workflow. Cashiers or inventory clerks can add multiple product lines in a single session. Upon submission, `prisma.$transaction` creates the purchase header, inserts line items, and increments stock in a single isolated commit.")

    # Screen 8.8
    add_h2("8.1.8 Point-of-Sale (POS) Multi-Item Billing Counter (Figure 8.8)")
    add_p("Figure 8.8 presents the high-speed Point-of-Sale billing counter. Cashiers select items from an interactive product grid or search bar, assembling a dynamic multi-item shopping cart. The interface performs instant stock availability checks, blocking sales with clear alerts if requested quantities exceed available inventory. Payment options (Cash, Card, UPI) and customer names can be configured.")
    add_figure(os.path.join(SCR_DIR, '07_sales_pos_counter.png'), "Figure 8.8: Point-of-Sale (POS) Multi-Item Checkout Counter")
    add_p("Operational Analysis: The POS billing counter is optimized for rapid checkout during peak retail shopping hours. Real-time cart calculations update subtotal and tax amounts dynamically without page reloads. Built-in stock validation blocks checkouts if requested quantities exceed shelf availability.")

    # Screen 8.9
    add_h2("8.1.9 Generated Tax Invoice Modal & Print Dialog (Figure 8.9)")
    add_p("Figure 8.9 illustrates the generated tax invoice modal dialog displayed immediately upon checkout completion. The modal features formatted receipt headers, unique invoice numbers (e.g., INV-202611-0001), itemized rows with unit prices and totals, payment method indicators, and a direct 'Print Invoice' button that invokes the native browser print engine.")
    add_figure(os.path.join(SCR_DIR, '08_sales_invoice_modal.png'), "Figure 8.9: Generated Tax Invoice Modal & Print Dialog")
    add_p("Operational Analysis: The invoice dialog opens automatically upon sales commit. Clicking 'Print Invoice' leverages browser CSS `@media print` rules to strip navigation bars and format the receipt cleanly for 80mm thermal receipt printers or standard A4 invoice sheets.")

    # Screen 8.10
    add_h2("8.1.10 Inventory Stock Valuation & Master Summary Report (Figure 8.10)")
    add_p("Figure 8.10 displays the comprehensive stock summary report. The table presents active stock counts, unit selling prices, unit cost prices, and total monetary inventory valuation calculated on an individual SKU basis and summarized in top-level metric cards.")
    add_figure(os.path.join(SCR_DIR, '09_reports_stock_summary.png'), "Figure 8.10: Inventory Stock Valuation & Master Summary Report")
    add_p("Operational Analysis: The stock valuation report provides accountants and business owners with an exact audit of locked-in working capital. Valuation is calculated dynamically via database queries (`SUM(quantity * price)`), providing instantaneous financial transparency.")

    # Screen 8.11
    add_h2("8.1.11 Proactive Low-Stock Reorder Alerting Report (Figure 8.11)")
    add_p("Figure 8.11 illustrates the low-stock alerting report. The system executes an automated SQL filter isolating all products where current quantity is less than or equal to reorderLevel. Shortage deficits are computed dynamically, and linked supplier phone/email contacts are displayed to expedite restocking orders.")
    add_figure(os.path.join(SCR_DIR, '10_reports_low_stock.png'), "Figure 8.11: Proactive Low-Stock Reorder Alerting Report")
    add_p("Operational Analysis: This report serves as a proactive defense against out-of-stock scenarios. Shortage gaps are highlighted in bold red badges, directly indicating the minimum quantity required to restore inventory to safe operational buffers.")

    # Screen 8.12
    add_h2("8.1.12 Historical Procurement Inflow Audit Log (Figure 8.12)")
    add_p("Figure 8.12 shows the procurement audit report. Store managers can audit all historical purchase transactions, inspecting supplier names, itemized restocked products, total expenditures, and exact timestamps across selectable date ranges.")
    add_figure(os.path.join(SCR_DIR, '10b_reports_purchases.png'), "Figure 8.12: Historical Procurement Inflow Audit Log")
    add_p("Operational Analysis: The procurement log provides a verifiable fiscal audit trail. Managers can expand any historical purchase to inspect the itemized product breakdown, wholesale unit prices paid, and the total financial outflow incurred.")

    # Screen 8.13
    add_h2("8.1.13 Historical Sales Revenue Outflow Audit Log (Figure 8.13)")
    add_p("Figure 8.13 depicts the sales revenue audit log. The report details all historical sales transactions, invoice numbers, customer names, payment modalities, and gross revenues. Managers can filter records by date range to evaluate daily, weekly, or monthly sales performance.")
    add_figure(os.path.join(SCR_DIR, '10c_reports_sales.png'), "Figure 8.13: Historical Sales Revenue Outflow Audit Log")
    add_p("Operational Analysis: The sales audit report aggregates daily revenue figures. Date filtering allows management to assess commercial performance across custom accounting periods and identify high-revenue shopping days.")

    # Screen 8.14
    add_h2("8.1.14 Administrative User Management & RBAC Console (Figure 8.14)")
    add_p("Figure 8.14 illustrates the administrative user management console, accessible exclusively to users with the ADMIN role. Administrators can provision new employee accounts, assign roles (ADMIN or STAFF), update email addresses, and deactivate accounts, maintaining strict internal access governance.")
    add_figure(os.path.join(SCR_DIR, '11_user_management.png'), "Figure 8.14: Administrative User Management & RBAC Provisioning Console")
    add_p("Operational Analysis: Access to this view is protected by NestJS `RolesGuard`. Attempting to load this endpoint using a staff token triggers a 403 Forbidden response. Administrators can onboard new employees, assign operational roles, and reset credentials securely.")

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 9: FUTURE SCOPE & ENHANCEMENTS
    # ==========================================================================
    add_chapter_title("CHAPTER 9\nFUTURE SCOPE & ENHANCEMENTS")

    add_h1("9.1 Summary of Project Accomplishments")
    add_p("The SmartStock project successfully designed, architected, and validated a full-featured, enterprise-grade inventory management and Point-of-Sale web platform. Key accomplishments achieved during this project include:")
    add_bullet("Full-Stack Three-Tier Architecture: Engineered an asynchronous, type-safe web platform utilizing Next.js 16 (App Router), React 19, NestJS 11, Prisma ORM 6, and PostgreSQL 18.1.")
    add_bullet("Guaranteed ACID Stock Integrity: Completely eliminated inventory discrepancies and ghost stock through atomic database transactions governing both procurement inflows and POS checkout outflows.")
    add_bullet("Cryptographic Role-Based Security: Enforced strict role separation (Admin and Staff) using bcrypt salted password hashing (10 rounds) and symmetric HMAC-SHA256 (HS256) JWT bearer token validation.")
    add_bullet("Proactive Replenishment Intelligence: Eliminated manual stock audits through automated low-stock alerting filters linked directly to vendor supplier contact profiles.")
    add_bullet("Comprehensive Test Verification: Achieved 100% pass rates across 15 automated Jest unit/integration tests and validated 20 black-box system test cases with zero defects.")

    add_h1("9.2 Academic Prototype Limitations")
    add_p("As an academic prototype developed within a focused project timeline, the system exhibits several operational limitations:")
    add_bullet("Single-Store Centralized Architecture: SmartStock is designed for single-location retail stores. It does not currently support multi-branch inventory transfers or distributed master-slave database replication.")
    add_bullet("Invoice Concurrency Constraint: The programmatic `count() + 1` invoice generation pattern could experience race conditions under simultaneous multi-terminal checkouts, requiring transition to PostgreSQL native sequences in high-volume production.")
    add_bullet("Lack of Direct Hardware Optical Drivers: Barcode input is currently handled via keyboard wedge emulation rather than direct USB/Bluetooth HID driver integration.")
    add_bullet("Absence of Integrated Payment Gateway: Financial settlements are recorded under Cash, Card, or UPI modalities without direct programmatic API handshakes with banking gateways.")

    add_h1("9.3 Future Enhancements Roadmap")
    add_p("To transition SmartStock from an academic prototype into a commercially deployable enterprise retail product, the following development roadmap is proposed:")
    add_bullet("Hardware Barcode & QR Code Integration: Incorporate WebUSB and WebBluetooth API protocols to enable plug-and-play connectivity with industrial handheld barcode scanners and electronic cash drawers.")
    add_bullet("Multi-Tenant & Multi-Branch Architecture: Expand the relational schema with `Store` and `Warehouse` tenant identifiers, enabling regional retail chains to manage centralized procurement with distributed retail branch inventories.")
    add_bullet("Indian GST e-Invoicing Integration: Connect with the Goods and Services Tax (GST) e-Invoice portal via GSP/ASP APIs for automated Invoice Reference Number (IRN) generation and B2B signed QR code printing.")
    add_bullet("Predictive AI Demand Forecasting: Implement machine learning models (ARIMA / Prophet) to analyze historical sales velocities and seasonality trends, automatically predicting replenishment order quantities and minimizing stockouts.")

    doc.add_page_break()

    # ==========================================================================
    # CHAPTER 10: APPENDICES
    # ==========================================================================
    add_chapter_title("CHAPTER 10\nAPPENDICES")

    add_h1("10.1 Key Source Code Listings")
    add_p("This appendix documents key TypeScript source code listings and Prisma schema definitions from the SmartStock implementation, showcasing relational data modeling, atomic ACID transactions, and cryptographic authentication.")

    # Listing 10.1: Prisma Schema
    prisma_code = """// backend/prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role {
  ADMIN
  STAFF
}

model User {
  id           Int      @id @default(autoincrement())
  email        String   @unique
  passwordHash String
  name         String
  role         Role     @default(STAFF)
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
  sales        Sale[]

  @@map("users")
}

model Category {
  id          Int       @id @default(autoincrement())
  name        String    @unique
  description String?
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  products    Product[]

  @@map("categories")
}

model Supplier {
  id        Int        @id @default(autoincrement())
  name      String
  contact   String?
  email     String?
  createdAt DateTime   @default(now())
  updatedAt DateTime   @updatedAt
  products  Product[]
  purchases Purchase[]

  @@map("suppliers")
}

model Product {
  id            Int            @id @default(autoincrement())
  name          String
  sku           String         @unique
  description   String?
  price         Decimal        @db.Decimal(10, 2)
  costPrice     Decimal        @db.Decimal(10, 2)
  quantity      Int            @default(0)
  reorderLevel  Int            @default(10)
  categoryId    Int
  supplierId    Int
  createdAt     DateTime       @default(now())
  updatedAt     DateTime       @updatedAt
  category      Category       @relation(fields: [categoryId], references: [id])
  supplier      Supplier       @relation(fields: [supplierId], references: [id])
  purchaseItems PurchaseItem[]
  saleItems     SaleItem[]

  @@map("products")
}

model Purchase {
  id         Int            @id @default(autoincrement())
  supplierId Int
  total      Decimal        @db.Decimal(10, 2)
  createdAt  DateTime       @default(now())
  supplier   Supplier       @relation(fields: [supplierId], references: [id])
  items      PurchaseItem[]

  @@map("purchases")
}

model PurchaseItem {
  id         Int      @id @default(autoincrement())
  purchaseId Int
  productId  Int
  quantity   Int
  costPrice  Decimal  @db.Decimal(10, 2)
  purchase   Purchase @relation(fields: [purchaseId], references: [id], onDelete: Cascade)
  product    Product  @relation(fields: [productId], references: [id])

  @@map("purchase_items")
}

model Sale {
  id            Int        @id @default(autoincrement())
  invoiceNumber String     @unique
  customerName  String?
  total         Decimal    @db.Decimal(10, 2)
  paymentMethod String     @default("CASH")
  userId        Int
  createdAt     DateTime   @default(now())
  user          User       @relation(fields: [userId], references: [id])
  items         SaleItem[]

  @@map("sales")
}

model SaleItem {
  id        Int     @id @default(autoincrement())
  saleId    Int
  productId Int
  quantity  Int
  price     Decimal @db.Decimal(10, 2)
  sale      Sale    @relation(fields: [saleId], references: [id], onDelete: Cascade)
  product   Product @relation(fields: [productId], references: [id])

  @@map("sale_items")
}"""
    add_code_block("Listing 10.1: Relational Database Schema Specification (schema.prisma)", prisma_code)

    # Listing 10.2: Sales Transaction Engine
    sales_code = """// backend/src/sales/sales.service.ts
import { Injectable, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSaleDto } from './dto/create-sale.dto';

@Injectable()
export class SalesService {
  constructor(private prisma: PrismaService) {}

  async create(createSaleDto: CreateSaleDto, userId: number) {
    const { items, customerName, paymentMethod } = createSaleDto;

    return this.prisma.$transaction(async (tx) => {
      let grandTotal = 0;

      // 1. Validate instantaneous stock availability for all items
      for (const item of items) {
        const product = await tx.product.findUnique({
          where: { id: item.productId },
        });

        if (!product) {
          throw new BadRequestException(`Product with ID ${item.productId} not found`);
        }

        if (product.quantity < item.quantity) {
          throw new BadRequestException(
            `Insufficient stock for "${product.name}". Available: ${product.quantity}, Requested: ${item.quantity}`
          );
        }

        grandTotal += Number(product.price) * item.quantity;
      }

      // 2. Generate formatted sequential invoice string
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const count = await tx.sale.count();
      const invoiceNumber = `INV-${year}${month}-${String(count + 1).padStart(4, '0')}`;

      // 3. Atomically create Sale header record
      const sale = await tx.sale.create({
        data: {
          invoiceNumber,
          customerName: customerName || 'Walk-in Customer',
          paymentMethod: paymentMethod || 'CASH',
          total: grandTotal,
          userId,
        },
      });

      // 4. Atomically insert line items and decrement product inventory
      for (const item of items) {
        const product = await tx.product.findUnique({
          where: { id: item.productId },
        });

        await tx.saleItem.create({
          data: {
            saleId: sale.id,
            productId: item.productId,
            quantity: item.quantity,
            price: product.price,
          },
        });

        await tx.product.update({
          where: { id: item.productId },
          data: {
            quantity: {
              decrement: item.quantity,
            },
          },
        });
      }

      // 5. Return committed transaction payload
      return tx.sale.findUnique({
        where: { id: sale.id },
        include: {
          items: {
            include: { product: true },
          },
          user: {
            select: { id: true, name: true, email: true },
          },
        },
      });
    });
  }
}"""
    add_code_block("Listing 10.2: Atomic Sales Transaction Engine (sales.service.ts)", sales_code)

    # Listing 10.3: Authentication Service
    auth_code = """// backend/src/auth/auth.service.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../prisma/prisma.service';
import { LoginDto } from './dto/login.dto';
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async login(loginDto: LoginDto) {
    const user = await this.prisma.user.findUnique({
      where: { email: loginDto.email },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // Verify salted hash with bcrypt
    const isMatch = await bcrypt.compare(loginDto.password, user.passwordHash);
    if (!isMatch) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // Sign symmetric HMAC-SHA256 JWT bearer token
    const payload = { sub: user.id, email: user.email, role: user.role };
    const accessToken = this.jwtService.sign(payload);

    return {
      accessToken,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
    };
  }
}"""
    add_code_block("Listing 10.3: Authentication Service with Bcrypt Verification (auth.service.ts)", auth_code)

    doc.add_page_break()

    # 10.2 Bibliography
    add_h1("10.2 Bibliography & References")

    add_p("Official Technical Documentation:")
    add_bullet("Next.js Documentation. Vercel Inc. Available: https://nextjs.org/docs [Accessed: Nov 2026].")
    add_bullet("NestJS Framework Documentation. Kamil Mysliwiec. Available: https://docs.nestjs.com [Accessed: Nov 2026].")
    add_bullet("PostgreSQL 18 Database Documentation. PostgreSQL Global Development Group. Available: https://www.postgresql.org/docs/ [Accessed: Nov 2026].")
    add_bullet("Prisma ORM Technical Reference. Prisma Data Inc. Available: https://www.prisma.io/docs [Accessed: Nov 2026].")
    add_bullet("React 19 Documentation. Meta Platforms Inc. Available: https://react.dev [Accessed: Nov 2026].")
    add_bullet("Tailwind CSS v4 Documentation. Tailwind Labs Inc. Available: https://tailwindcss.com/docs [Accessed: Nov 2026].")
    add_bullet("TypeScript Language Specification. Microsoft Corporation. Available: https://www.typescriptlang.org/docs/ [Accessed: Nov 2026].")

    add_p("Academic Standards & Curriculum Guidelines:")
    add_bullet("IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications. IEEE Computer Society, 1998.")
    add_bullet("BCA Project Report Guidelines. Centre for Distance and Online Education (CDOE), Uttaranchal University, Dehradun, 2026.")

    doc.save(OUTPUT_FILE)
    return OUTPUT_FILE

if __name__ == '__main__':
    build_full_report()
    print("SUCCESS: Full report built!")
