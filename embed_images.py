"""
Usage:
  1. Put all your success story images in a folder named 'success_images/'
  2. Run:  python embed_images.py
  3. Share the generated 'index.html' anywhere — all images are embedded inside it.

Supported formats: .jpg, .jpeg, .png, .webp, .gif
"""

import base64, os, mimetypes

SCRIPT_DIR = r'E:\education-academy'
IMAGES_DIR = os.path.join(SCRIPT_DIR, 'success_images')
INDEX_FILE = os.path.join(SCRIPT_DIR, 'index.html')

# ─── Step 1: Read all images from success_images/ ───
if not os.path.isdir(IMAGES_DIR):
    print(f'ERROR: Folder not found: {IMAGES_DIR}')
    print('Create it and put your images inside, then run again.')
    exit(1)

image_exts = {'.jpg','.jpeg','.png','.webp','.gif'}
image_files = sorted(
    f for f in os.listdir(IMAGES_DIR)
    if os.path.splitext(f)[1].lower() in image_exts
)

if not image_files:
    print(f'ERROR: No images found in {IMAGES_DIR}')
    print(f'Place .jpg, .png, .webp, or .gif files in that folder.')
    exit(1)

print(f'Found {len(image_files)} image(s):')
gallery_html = ''
for fname in image_files:
    fpath = os.path.join(IMAGES_DIR, fname)
    ext = os.path.splitext(fname)[1].lower()
    mime_map = {'.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.gif':'image/gif'}
    mime = mime_map.get(ext, 'image/jpeg')
    with open(fpath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    size_kb = len(b64) * 3 // 4 // 1024
    print(f'  {fname}  ({size_kb} KB)')
    gallery_html += f'      <img src="data:{mime};base64,{b64}" alt="{fname}" class="gallery-img reveal" loading="lazy">\n'

# ─── Step 2: Read current index.html ───
with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── Step 3: Replace the success stories section ───
old_section_start = '<!-- Success Stories -->'
old_section_end = '<!-- Contact -->'

# Find the old success stories section
start_idx = html.find(old_section_start)
end_idx = html.find(old_section_end)
if start_idx == -1 or end_idx == -1:
    print('ERROR: Could not find Success Stories section in index.html')
    exit(1)

new_section = f'''<!-- Success Stories -->
<section id="stories">
  <div class="container">
    <span class="section-label reveal">Success Stories</span>
    <h2 class="section-title reveal">Our Achievements</h2>
    <p class="section-desc reveal">A glimpse of our students who have achieved remarkable success in their academic and professional journeys.</p>
    <div class="gallery-grid">
{gallery_html}    </div>
    <div class="success-text reveal" style="margin-top:40px;text-align:center">
      <h3>Transforming Lives Through Education</h3>
      <p style="max-width:700px;margin:0 auto;color:var(--muted);font-size:15px;line-height:1.8">Year after year, Education Academy students achieve remarkable success in competitive exams across Pakistan. From CSS and PMS to provincial public service commissions, our students consistently rank among the top candidates. We take pride in having helped hundreds of students from Khairpur Mirs and across Sindh secure government jobs, win scholarships, and gain admission to prestigious universities.</p>
      <a href="https://wa.me/923079833016" target="_blank" class="btn btn-whatsapp" style="margin-top:16px">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Join Our Success
      </a>
    </div>
  </div>
</section>

<!-- Contact -->'''

html = html[:start_idx] + new_section + html[end_idx:]

# ─── Step 4: Add gallery CSS if not present ───
gallery_css = '\n.gallery-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px}\n.gallery-img{width:100%;border-radius:var(--radius);border:2px solid var(--border);object-fit:cover;aspect-ratio:4/3;transition:transform .4s,border-color .4s}\n.gallery-img:hover{transform:scale(1.03);border-color:var(--accent)}'

if '.gallery-grid' not in html:
    # Insert after the .success-grid styles
    insert_marker = '.success-img'
    insert_idx = html.find(insert_marker)
    if insert_idx != -1:
        line_end = html.find('\n', insert_idx)
        html = html[:line_end+1] + gallery_css[1:] + html[line_end+1:]

# ─── Step 5: Write back ───
with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone! index.html updated with {len(image_files)} embedded images ({len(html)} bytes)')
print('Share index.html anywhere — it works standalone on Android, PC, etc.')
