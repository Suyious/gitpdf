import os
import shutil
from io import BytesIO
from flask import Flask, request, make_response, send_file
from git import Repo
from git.exc import GitCommandError

from pdf import PDF

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route("/")
def index():
  return '''
    <form method="post">
      <p>Git Repository URL: <input type="text" name="git_url"></p>
      <p><input type="submit" value="Submit"></p>
    </form>
  '''

@app.route("/", methods=["POST"])
def generate():
  git_url = request.form.get('git_url')
  if not git_url:
    return "<p>Please provide Github URL</p>"

  tmp_dir = "tmp_repo"
  if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
  try:
    Repo.clone_from(git_url, tmp_dir)
  except GitCommandError as a:
    raise a
    return "<p>Could not clone git repository. Give Valid url.</p>"
  except Exception as e:
    raise e

  os.chdir(tmp_dir)
  shutil.rmtree(".git")

  pdf = PDF()
  for dirpath, dirname, filenames in os.walk(os.curdir):
    for filename in filenames:
      filepath = os.path.join(dirpath, filename)
      pdf.set_filename(filepath)
      with open(filepath, "r") as f:
        pdf.add_page()
        try:
          pdf.multi_cell(0, 4, f.read().expandtabs(2), border=0)
        except UnicodeDecodeError:
          print("[ERROR] Skipping file", filepath)
        pdf.ln()

  buffer = BytesIO()
  buffer.write(pdf.output(dest = "S").encode('latin-1'))
  buffer.seek(0)
  response = send_file(buffer, as_attachment=True, download_name=f'{git_url.split("/")[-1]}.pdf', mimetype="application/pdf")

  os.chdir('..')
  shutil.rmtree(tmp_dir)
  return response

if __name__ == '__main__':
  app.run(debug=True)
