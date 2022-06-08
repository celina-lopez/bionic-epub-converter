import os
import tempfile
from pathlib import Path
from . import converter

def cleanup(path):
  os.remove(path)

async def convert(file):
  contents = await file.read()
  tmpdirname = tempfile.mkdtemp()
  temp_dir = Path(tmpdirname)
  file_name = temp_dir / "test.epub"
  book_file_name = temp_dir / "bionic_test.epub"
  tmp_file = open(file_name, 'wb')
  tmp_file.write(contents)
  tmp_file.close()
  converter.create_bionic_book(file_name, book_file_name)
  cleanup(file_name)
  return book_file_name
