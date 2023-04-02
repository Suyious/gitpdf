import os
import sys
import argparse
import shutil
from fpdf import FPDF
from git import Repo


class PDF(FPDF):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # self.set_auto_page_break(True)
    self.alias_nb_pages()
    self.add_font('JetBrains Mono', '', os.path.join(os.getcwd(), '../fonts/JetBrains Mono Regular Nerd Font Complete.ttf'), uni=True)
    self.set_font('JetBrains Mono', '', 8)
    self.filename = ''

  def set_filename(self, filename):
    self.filename = filename

  def header(self):
    self.set_font('JetBrains Mono', 'U', 8)
    self.cell(0, 10, self.filename, 0, 0, 'L')
    self.ln(10)
    # self.line(10, self.tMargin + 16, self.w - 10, self.tMargin + 16)

  def footer(self):
    self.set_y(-15)
    page_num = f'Page {self.page_no()} of {{nb}}'
    self.cell(0, 10, page_num, 0, 0, 'C')

def main():
  parser = argparse.ArgumentParser(prog="gitpdf", description="Convert a GitHub repository to a PDF")
  parser.add_argument("github_repo_url", type=str, help="GitHub repository URL")
  parser.add_argument(
    "--output", "-o", type=str, default="output.pdf", help="Output file name"
  )
  args = parser.parse_args()

  tmp_dir = "tmp_repo"
  try:
    Repo.clone_from(args.github_repo_url, tmp_dir)
  except Exception as e:
    print("[ERROR] Could not clone git repository. Make sure the url is valid.")
    print("[EXITING]")
    raise e
    sys.exit()

  os.chdir(tmp_dir)
  shutil.rmtree(".git")

  pdf = PDF()
  for dirpath, dirname, filenames in os.walk(os.curdir):
    for filename in filenames:
      filepath = os.path.join(dirpath, filename)
      pdf.set_filename(filepath)
      print("[PRINTING]", filepath)
      with open(filepath, "r") as f:
        pdf.add_page()
        try:
          pdf.multi_cell(0, 4, f.read().expandtabs(2), border=0)
        except UnicodeDecodeError:
          print("[ERROR] Skipping file", filepath)
        pdf.ln()

  print("[LOG] Preparing Output")
  os.chdir('..')
  pdf.output(args.output, 'F')
  print("[DELETING]", tmp_dir)
  shutil.rmtree(tmp_dir)

if __name__ == "__main__":
  main()
