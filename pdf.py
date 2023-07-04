import os
from fpdf import FPDF

class PDF(FPDF):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # self.set_auto_page_break(True)
    # self.alias_nb_pages()
    self.add_font('JetBrains Mono', '', os.path.join(os.getcwd(), '../fonts/JetBrains Mono Regular Nerd Font Complete.ttf'), uni=True)
    self.set_font('JetBrains Mono', '', 8)
    self.filename = ''
    self.footerleft = ''
    self.footerright = ''
    self.pageoffset = 0

  def set_filename(self, filename):
    self.filename = filename

  def set_pageoffset(self, pageoffset):
    if(pageoffset):
      self.pageoffset = pageoffset

  def set_footer_text(self, **kwargs):
    left = kwargs.get('left', '')
    right = kwargs.get('right', '')
    if(left):
      self.footerleft = left
    if(right):
      self.footerright = right

  def header(self):
    self.set_font('JetBrains Mono', 'U', 8)
    self.cell(0, 10, self.filename, 0, 0, 'L')
    self.ln(10)
    # self.line(10, self.tMargin + 16, self.w - 10, self.tMargin + 16)

  def footer(self):
    self.set_y(-15)
    # page_num = f'Page {self.page_no() + int(self.pageoffset)} of {{nb}}'
    page_num = f'{self.page_no() + int(self.pageoffset)}'
    page_width = self.w - 2 * self.l_margin
    if self.footerleft:
      self.cell(page_width / 3, 10, self.footerleft, 0, 0, 'L')
    self.cell(page_width / 3, 10, page_num, 0, 0, 'C')
    if self.footerright:
      self.cell(page_width / 3, 10, self.footerright, 0, 0, 'R')
