import sys
import os
import re
import markdown

def slugify(text):
    base = re.sub(r'\s+', '-', text.strip().lower())
    base = re.sub(r'[^\w\-]', '', base)
    return base

def generate_toc_and_add_ids(html):
    # 見出しの正規表現パターン
    pattern = re.compile(r'<h([1-6])>(.*?)</h\1>')
    headings = pattern.findall(html)

    id_map = {}
    heading_data = []

    def make_unique_id(base):
        count = 1
        unique_id = base
        while unique_id in id_map:
            unique_id = f"{base}-{count}"
            count += 1
        id_map[unique_id] = True
        return unique_id

    def add_ids_to_html(match):
        level, title = match.groups()
        base_id = slugify(title)
        unique_id = make_unique_id(base_id)
        heading_data.append((int(level), title, unique_id))
        return f'<h{level} id="{unique_id}">{title}</h{level}>'

    # HTML中の見出しタグにIDを追加
    html_with_ids = pattern.sub(add_ids_to_html, html)

    # スタイル付きTOCのHTMLを構築
    toc_lines = ['<div style="text-align:left;padding:10px;border-color:#cccccc;border-width:2px;border-style:solid;width:90%;background:#ffffff;">\n']
    toc_lines.append('<br /><b>目次</b><br />\n')

    prev_level = 0

    for level, title, hid in heading_data:
        if level > prev_level:
            for _ in range(level - prev_level):
                toc_lines.append('<ul>\n')
        elif level < prev_level:
            for _ in range(prev_level - level):
                toc_lines.append('</ul>\n')
        toc_lines.append(f'<li><a href="#{hid}">{title}</a><br /></li>\n')
        prev_level = level

    for _ in range(prev_level):
        toc_lines.append('</ul>\n')
    toc_lines.append('</div>\n')

    toc_html = ''.join(toc_lines)
    return toc_html + html_with_ids

def convert_md_file(md_path):
    if not os.path.isfile(md_path) or not md_path.endswith('.md'):
        print("指定されたファイルが存在しないか、.mdファイルではありません")
        sys.exit(1)

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    final_html = generate_toc_and_add_ids(html)

    html_path = os.path.splitext(md_path)[0] + '.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f'変換完了: {html_path}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("使い方: python convert_md.py <markdownファイルパス>")
        sys.exit(1)

    convert_md_file(sys.argv[1])
