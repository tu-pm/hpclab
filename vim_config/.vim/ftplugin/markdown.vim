setlocal  tabstop=4
setlocal  shiftwidth=4

" Convert LATEX to SVG
python3 << EOL
import vim, sys, re
from io import StringIO
import urllib.parse


def get_latex_block_():
  tex_range = []
  for i, line in enumerate(vim.current.buffer):
    cnt = line.count('$$')
    if (cnt == 1):
      tex_range.append(i+1)
      if (len(tex_range) == 2):
        break
    elif (cnt >= 2):
      tex_range.append(i+1)
      tex_range.append(i+1)
      break
  if len(tex_range) < 2:
    raise StopIteration
  return (tex_range[0], tex_range[1])

def ConvertLatex():
  while True:
    try:
      start, end = get_latex_block_()
      block = vim.current.buffer.range(start, end)
      regex = re.compile(r'\$\$(.*?)\$\$', re.MULTILINE|re.DOTALL)
      latex = '\n'.join(block)

      match = regex.search(latex)
      latex_content = match.string[match.start()+2:match.end()-2].strip()
      latex_encoded = urllib.parse.quote(latex_content)
      
      tag = '<img align="center" src="https://tex.s2cms.ru/svg/{}"/>'.format(latex_encoded)

      latex = regex.sub(tag, latex, count=1)
      block[:] = latex.split('\n')
    
    except StopIteration:
      break

def ConvertLatexBlock():
  while True:
    try:
      start, end = get_latex_block_()
      block = vim.current.buffer.range(start, end)
      regex = re.compile(r'\$\$(.*?)\$\$', re.MULTILINE|re.DOTALL)
      latex = '\n'.join(block)

      match = regex.search(latex)
      latex_content = match.string[match.start()+2:match.end()-2].strip()
      latex_encoded = urllib.parse.quote(latex_content)
      
      tag = '<img align="center" src="https://tex.s2cms.ru/svg/{}"/>'.format(latex_encoded)
      tag = '<p align="center" style="text-align: center">{}</p>'.format(tag)

      latex = regex.sub(tag, latex, count=1)
      block[:] = latex.split('\n')
    
    except StopIteration:
      break

EOL

command! -range Tex python3 ConvertLatex()
command! -range Texb python3 ConvertLatexBlock()
vnoremap <f5> :Tex<CR>
vnoremap <f6> :Texb<CR>


