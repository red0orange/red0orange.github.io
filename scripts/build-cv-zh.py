#!/usr/bin/env python3
"""Build the one-page Chinese resume from curated text and shared publication metadata.

Dependencies: reportlab, PyYAML, pypdf. Uses macOS Heiti SC fonts, embedded in the PDF.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import re
import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/黄德豪_中文简历_一页版.pdf'
DRAFT = ROOT / 'tmp/pdfs/cv-zh-draft.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
DRAFT.parent.mkdir(parents=True, exist_ok=True)
papers = {p['id']: p for p in yaml.safe_load((ROOT / '_data/publications.yml').read_text())}
profile = yaml.safe_load((ROOT / '_data/profile.yml').read_text())
pdfmetrics.registerFont(TTFont('Heiti', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('HeitiBold', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold', italic='Arial', boldItalic='ArialBold')
pdfmetrics.registerFontFamily('Heiti', normal='Heiti', bold='HeitiBold', italic='Heiti', boldItalic='HeitiBold')
W, H = A4
MARGIN = 45
WIDTH = W - 2 * MARGIN
INK = '#28353F'
ACCENT = '#365568'
MUTED = '#64717C'
LINK = '#365568'
cv = canvas.Canvas(str(DRAFT), pagesize=A4, pageCompression=1)
cv.setTitle('黄德豪 - 中文简历（一页版）')
cv.setAuthor('黄德豪 / Dehao Huang')
cv.setSubject('机器人操作与抓取、机器人学习、VLA 后训练与部署')
# Small mirrored corner marks, entirely outside the text area.
# The page and header backgrounds remain white.
for x, corner_y, sx, sy in [(18, H-18, 1, -1), (W-18, H-18, -1, -1),
                           (18, 18, 1, 1), (W-18, 18, -1, 1)]:
    cv.saveState()
    cv.translate(x, corner_y)
    cv.scale(sx, sy)
    cv.setStrokeColor(HexColor('#BECFD9'))
    cv.setLineWidth(.65)
    outer = cv.beginPath()
    outer.moveTo(0, 24)
    outer.lineTo(0, 0)
    outer.lineTo(24, 0)
    cv.drawPath(outer, stroke=1, fill=0)
    cv.setStrokeColor(HexColor('#DEE7EC'))
    cv.setLineWidth(.5)
    inner = cv.beginPath()
    inner.moveTo(6, 18)
    inner.lineTo(6, 6)
    inner.lineTo(18, 6)
    cv.drawPath(inner, stroke=1, fill=0)
    cv.setFillColor(HexColor('#94ADBB'))
    cv.rect(-1.2, -1.2, 2.4, 2.4, stroke=0, fill=1)
    cv.restoreState()
y = H - 43
blocks = []


def mixed_fonts(text, bold=False):
    # Keep all wording intact, with a conventional Latin font for acronyms and dates.
    depth = int(bold)
    parts = []
    for part in re.split(r'(<[^>]+>)', text):
        if part.startswith('<'):
            if part.lower() in ('<b>', '<strong>'):
                depth += 1
            elif part.lower() in ('</b>', '</strong>'):
                depth -= 1
            parts.append(part)
        else:
            font = 'ArialBold' if depth else 'Arial'
            parts.append(re.sub(r'[A-Za-z0-9][A-Za-z0-9 .,/+%():;|_-]*',
                                lambda match: f'<font name="{font}">{match.group(0)}</font>', part))
    return ''.join(parts)


def p(text, x, top, width, size=10.5, leading=15.2, color=INK, bold=False, align=0):
    style = ParagraphStyle('cv', fontName='HeitiBold' if bold else 'Heiti', fontSize=size,
                           leading=leading, textColor=HexColor(color), wordWrap='CJK',
                           alignment=align, splitLongWords=False, allowWidows=0, allowOrphans=0)
    para = Paragraph(mixed_fonts(text, bold), style)
    _, height = para.wrap(width, H)
    para.drawOn(cv, x, top - height)
    blocks.append((text, x, top-height, width, height))
    return height


def line(text, size=10.5, leading=15.2, color=INK, after=0):
    global y
    y -= p(text, MARGIN, y, WIDTH, size=size, leading=leading, color=color)
    y -= after


def row(left, right='', size=10.5, after=0, right_width=165):
    global y
    left_width = WIDTH-right_width-12 if right else WIDTH
    lh = p(left, MARGIN, y, left_width, size=size, leading=15.2, bold=True)
    rh = p(right, W-MARGIN-right_width, y, right_width, size=9.5, leading=15.2, color=MUTED, align=2) if right else 0
    y -= max(lh, rh) + after


def section(title, note=''):
    global y
    y -= 13
    p(title, MARGIN, y, 100, size=11.7, leading=16, color=ACCENT, bold=True)
    if note:
        p(note, MARGIN+100, y-1, WIDTH-100, size=9.1, leading=15, color=MUTED, align=2)
    y -= 18
    cv.setStrokeColor(HexColor('#D8DFE4'))
    cv.setLineWidth(.4)
    cv.line(MARGIN, y+2, W-MARGIN, y+2)
    cv.setStrokeColor(HexColor(ACCENT))
    cv.setLineWidth(1.1)
    cv.line(MARGIN, y+2, MARGIN+22, y+2)
    y -= 5


def link(url, label, color=LINK):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="{color}">{escape(label)}</link>'

# Header: compact text on white.
p('黄德豪', MARGIN, y, 110, size=22, leading=28, color=ACCENT, bold=True)
p('Dehao Huang', MARGIN+82, y-8, 130, size=10.5, leading=16, color=MUTED)
p('博士研究生 · 机器人操作与抓取', W-MARGIN-210, y-8, 210, size=10.2, leading=16, color=MUTED, align=2)
y -= 36
line('南方科技大学 / 北京中关村学院（联合培养）', size=10.5, leading=15, color=MUTED, after=4)
contact = '  |  '.join([
    link('mailto:huangdehao919@gmail.com','huangdehao919@gmail.com'),
    link('https://red0orange.github.io/','red0orange.github.io'),
    link(profile['scholar'],'Google Scholar'),
    link('https://github.com/red0orange','GitHub'),
])
line(contact, size=9.4, leading=13)

section('研究方向')
line('研究机器人操作与抓取，重点减少操作策略（如 VLA）后训练与部署中的人工干预；探索 DAgger、强化学习（RL）与智能体（Agentic）方法。', size=10.4, leading=15.5)

section('教育经历')
row('南方科技大学 / 北京中关村学院', '2024.09 - 2027.06（预计）')
line('智能制造与机器人 · 博士（联合培养）　导师：'+link('https://sustech.edu.cn/zh/faculties/zhanghong.html','张宏')+'、'+link('https://www.bza.edu.cn/faculty/4b6e5ed12ce4492da61c808b9d48a44a','汪跃'), after=6)
row('南方科技大学', '2022.08 - 2024.06')
line('电子科学与技术 · 硕士　导师：张宏', after=6)
row('华南师范大学', '2018.08 - 2022.06')
line('信息工程 · 学士　GPA：3.86 / 5.0')

section('代表研究成果')
selected = [
    ('erlt', 'eRLT：面向 VLA 的高效强化学习', '跨层路由动作相关 token，提升在线学习效率；相同交互预算下，USB 插接末段成功率由 50% 提升至 90%。'),
    ('vlaconf', 'VLAConf：VLA 任务成功置信度校准', '利用冻结的 VLA 表征估计任务成功概率，为选择性专家介入提供依据。'),
    ('hgdiffuser', 'HGDiffuser：人类引导的抓取扩散模型', '将人类示范约束融入扩散采样，直接生成面向任务的六自由度抓取。'),
    ('rearrangement', '基于多视角融合的高效物体重排', '融合多视角观测，使杂乱桌面物体布局匹配单张目标图像。'),
    ('easy-iil', 'Easy-IIL：降低交互模仿学习的人工负担', '由辅助专家承担主要交互与数据采集，将人工干预集中在关键状态。'),
    ('cocoreviewbench', 'CoCoReviewBench：AI 审稿质量评测', '基于 3,900 篇论文，从反馈完整性与正确性两个维度评价 AI 审稿。'),
]
for idx, (paper_id, title, summary) in enumerate(selected):
    paper = papers[paper_id]
    role = '第一作者' if paper['authors'][0]=='Dehao Huang' else '合作作者'
    venue = f"{paper['venue']} {paper['year']}" + ('（预印本）' if paper['status']=='preprint' else '')
    row(link(paper['paper'], title, INK), f'{role} · {venue}', size=10.5, right_width=181)
    line(summary, size=10.1, leading=14.8, color='#505E69', after=6 if idx<len(selected)-1 else 0)

section('实习与开源')
row('商汤科技（元萝卜机器人） · 算法实习生', '2024', right_width=60)
line('参与自研移动操作机器人的算法开发与部署。', after=4)
line('<b>'+link('https://github.com/RLinf/RLinf','RLinf')+'</b>：参与 VLA 训练与评估相关的强化学习基础设施开发。', after=2)
line('<b>'+link('https://github.com/liyiteng/AlohaMini','AlohaMini')+'</b>：参与开源低成本移动操作平台开发。')

section('技能')
line('<b>编程与工具：</b>Python、C/C++；PyTorch、ROS、RLinf、LeRobot、Git、LaTeX。')
line('<b>语言：</b>中文（母语），英语（CET-6）。')

section('荣誉奖励')
line('中关村学院首届学术研究之星（2026）；美国大学生数学建模竞赛 M 奖（2021）。', size=10.0, leading=14.5)
line('RoboMaster 全国二等奖（2020）；全国大学生智能汽车竞赛三等奖（2020）。', size=10.0, leading=14.5)

if y < 39:
    raise RuntimeError(f'Content too long: bottom={y:.1f}pt; must keep at least 39pt.')
cv.showPage()
cv.save()
reader=PdfReader(DRAFT)
assert len(reader.pages)==1, 'The Chinese resume must be exactly one page.'
text=reader.pages[0].extract_text()
assert all(word in text for word in ['黄德豪','研究方向','教育经历','代表研究成果','实习与开源','荣誉奖励','eRLT','VLAConf'])
OUT.write_bytes(DRAFT.read_bytes())
print(f'Created {OUT}')
print(f'Pages: 1; content bottom: {y:.1f} pt; font sizes: 10-10.5 pt body / 11.7 pt section titles.')
