from fpdf import FPDF
from datetime import datetime


def clean_text(text):
    """Remove or replace all non-latin-1 characters"""
    replacements = {
        '\u2014': '-',   
        '\u2013': '-',  
        '\u2018': "'",  
        '\u2019': "'",   
        '\u201c': '"',  
        '\u201d': '"',  
        '\u2022': '-',   
        '\u25cf': '-',   
        '\u2026': '...',
        '\u00e9': 'e',   
        '\u00e8': 'e',  
        '\u00ea': 'e',   
        '\u00fc': 'u',   
        '\u00f6': 'o', 
        '\u00e4': 'a',   
        '\u2019': "'",
        '\u2764': '<3',  
        '\u00b0': ' degrees',
        '\u20b9': 'Rs', 
        '**': '',       
        '__': '',       
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Final safety — encode to latin-1, replacing anything remaining
    return text.encode('latin-1', errors='replace').decode('latin-1')


class DashboardPDF(FPDF):
    def header(self):
        self.set_fill_color(37, 99, 235)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 25, 'Social Media Analytics Report', align='C', ln=True)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10,
            clean_text(f'Generated on {datetime.now().strftime("%d %b %Y %I:%M %p")} | ArivuPro Analytics Dashboard'),
            align='C')


def generate_pdf_report(profiles, insights):
    pdf = DashboardPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Date ──────────────────────────────────────────
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(120, 120, 120)
    pdf.ln(5)
    pdf.cell(0, 8,
        clean_text(f'Report Date: {datetime.now().strftime("%d %B %Y")}'),
        ln=True)
    pdf.ln(3)

    # ── Profile Cards ─────────────────────────────────
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 10, 'Profile Overview', ln=True)
    pdf.set_draw_color(37, 99, 235)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    for profile in profiles:
        is_main = profile.get('type') == 'main'

        if is_main:
            pdf.set_fill_color(239, 246, 255)
        else:
            pdf.set_fill_color(249, 250, 251)

        pdf.set_draw_color(200, 200, 200)
        pdf.rect(10, pdf.get_y(), 190, 32, 'FD')

        y = pdf.get_y() + 5

        # Username
        pdf.set_xy(15, y)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(30, 30, 30)
        label = '[YOUR PROFILE]' if is_main else '[COMPETITOR]'
        pdf.cell(0, 6,
            clean_text(f"@{profile['username']}  {label}"),
            ln=True)

        # Stats
        pdf.set_xy(15, pdf.get_y() + 1)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(80, 80, 80)
        stats = clean_text(
            f"Followers: {profile.get('followers', 0):,}   |   "
            f"Engagement: {profile.get('engagement_rate', 0)}%   |   "
            f"Posts: {profile.get('total_posts', 0)}   |   "
            f"Posts/Day: {profile.get('posting_frequency', 0)}   |   "
            f"Top Content: {profile.get('top_content_type', 'N/A')}"
        )
        pdf.cell(0, 6, stats, ln=True)

        # Bio
        pdf.set_xy(15, pdf.get_y() + 1)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(120, 120, 120)
        bio = clean_text(profile.get('bio', '')[:90])
        pdf.cell(0, 5, bio, ln=True)

        pdf.ln(6)

    # ── Comparison Table ──────────────────────────────
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 10, 'Engagement Comparison', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    # Table header
    pdf.set_fill_color(37, 99, 235)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    col_widths = [50, 35, 35, 35, 35]
    headers = ['Username', 'Followers', 'Engagement%', 'Avg Likes', 'Posts/Day']
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1, fill=True, align='C')
    pdf.ln()

    # Table rows
    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', '', 9)
    for i, profile in enumerate(profiles):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        row = [
            clean_text(f"@{profile.get('username', '')}"),
            f"{profile.get('followers', 0):,}",
            f"{profile.get('engagement_rate', 0)}%",
            f"{profile.get('avg_likes', 0)}",
            f"{profile.get('posting_frequency', 0)}"
        ]
        for j, val in enumerate(row):
            pdf.cell(col_widths[j], 7, val, border=1, fill=fill, align='C')
        pdf.ln()

    # ── AI Insights ───────────────────────────────────
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 10, 'AI-Generated Insights (Powered by Gemini)', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    # Write insights line by line
    for line in insights.split('\n'):
        line = clean_text(line.strip())
        if not line:
            pdf.ln(2)
            continue

        if line.endswith(':') or line.isupper():
            # Section heading
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(37, 99, 235)
            pdf.ln(2)
            pdf.cell(0, 7, line, ln=True)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(40, 40, 40)
        else:
            pdf.multi_cell(0, 6, line)

    output_path = 'report.pdf'
    pdf.output(output_path)
    return output_path
