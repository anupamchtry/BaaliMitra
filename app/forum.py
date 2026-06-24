from flask import Blueprint, render_template, current_app, request, jsonify, url_for
import os, json, time
from pathlib import Path
from werkzeug.utils import secure_filename

forum_bp = Blueprint('forum', __name__, template_folder='../templates', static_folder='../static')

BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = BASE_DIR / 'database' / 'forum.json'
UPLOAD_DIR = BASE_DIR / 'static' / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_db_lock = None

def _read_db():
    try:
        if not DB_PATH.exists():
            DB_PATH.write_text("[]", encoding="utf-8")
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def _write_db(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@forum_bp.route('/forum')
def forum_page():
    # supply districts list for the template
    posts = _read_db()
    districts = sorted(list({p.get('district') for p in posts if p.get('district')}))
    # include some default districts if none
    if not districts:
        districts = ["Varanasi","Lucknow","Kanpur","Agra","Meerut","Delhi","Mumbai","Kolkata"]
    return render_template('forum.html', districts=districts)

@forum_bp.route('/api/forum/posts', methods=['GET'])
def get_posts():
    posts = _read_db()
    # return newest first
    posts_sorted = sorted(posts, key=lambda p: p.get('created_ts', 0), reverse=True)
    # attach full static URLs for images
    for p in posts_sorted:
        if p.get('image'):
            p['image'] = url_for('static', filename='uploads/' + os.path.basename(p['image']), _external=False)
    return jsonify({"posts": posts_sorted})

@forum_bp.route('/api/forum/posts', methods=['POST'])
def create_post():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    category = request.form.get('category', 'General')
    district = request.form.get('district', '')
    if not title or not body:
        return jsonify({"error":"title and body required"}), 400

    image_path = ''
    if 'image' in request.files:
        f = request.files['image']
        if f and f.filename:
            filename = secure_filename(f.filename)
            ts = int(time.time())
            filename = f"{ts}_{filename}"
            dest = UPLOAD_DIR / filename
            f.save(str(dest))
            image_path = str(dest)

    posts = _read_db()
    new_id = (max([p.get('id',0) for p in posts]) + 1) if posts else 1
    post = {
        "id": new_id,
        "title": title,
        "body": body,
        "category": category,
        "district": district,
        "image": image_path,
        "created": time.strftime("%Y-%m-%d %H:%M"),
        "created_ts": int(time.time()),
        "answers": 0,
        "upvotes": 0
    }
    posts.append(post)
    _write_db(posts)
    # return post with image URL normalized
    if post['image']:
        post['image'] = url_for('static', filename='uploads/' + os.path.basename(post['image']), _external=False)
    return jsonify({"ok": True, "post": post}), 201