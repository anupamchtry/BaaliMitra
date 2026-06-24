// forum.js - lightweight forum client with category and location filters
// expects endpoints:
// GET  /api/forum/posts
// POST /api/forum/posts  (multipart/form-data: title, body, category, district, image)

const postListEl = document.getElementById('postList');
const postModal = document.getElementById('postModal');
const createBtn = document.getElementById('createBtn');
const closeModalBtn = document.getElementById('closeModal');
const postForm = document.getElementById('postForm');
const postTitle = document.getElementById('postTitle');
const postBody = document.getElementById('postBody');
const postImage = document.getElementById('postImage');
const postCategory = document.getElementById('postCategory');
const postDistrict = document.getElementById('postDistrict');
const imagePreview = document.getElementById('imagePreview');
const toast = document.getElementById('toast');
const searchInput = document.getElementById('searchInput');
const filterCategory = document.getElementById('filterCategory');
const filterLocation = document.getElementById('filterLocation');

let postsCache = [];
let currentFilters = {
  search: '',
  category: '',
  location: ''
};

function showToast(msg, ms = 3000){
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(()=> toast.classList.add('hidden'), ms);
}

async function loadPosts(){
  try{
    postListEl.innerHTML = '<div class="empty">Loading posts…</div>';
    const res = await fetch('/api/forum/posts');
    if(!res.ok) throw new Error('Failed to load posts');
    const data = await res.json();
    postsCache = data.posts || [];
    applyFilters();
    showToast(`Loaded ${postsCache.length} posts`, 1500);
  }catch(e){
    console.error(e);
    postListEl.innerHTML = '<div class="empty">Failed to load posts</div>';
    showToast('Unable to load forum posts',2000);
  }
}

function applyFilters() {
  const filtered = postsCache.filter(post => {
    // Search filter
    if (currentFilters.search) {
      const searchText = (post.title + ' ' + post.body + ' ' + post.category).toLowerCase();
      if (!searchText.includes(currentFilters.search.toLowerCase())) {
        return false;
      }
    }
    
    // Category filter
    if (currentFilters.category && post.category !== currentFilters.category) {
      return false;
    }
    
    // Location filter
    if (currentFilters.location && post.district !== currentFilters.location) {
      return false;
    }
    
    return true;
  });
  
  renderList(filtered);
  updateFilterStatus();
}

function updateFilterStatus() {
  // Remove existing filter status
  const existingStatus = document.querySelector('.filter-status');
  if (existingStatus) {
    existingStatus.remove();
  }
  
  // Create new filter status if any filters are active
  const activeFilters = [];
  if (currentFilters.search) activeFilters.push({type: 'search', value: currentFilters.search});
  if (currentFilters.category) activeFilters.push({type: 'category', value: currentFilters.category});
  if (currentFilters.location) activeFilters.push({type: 'location', value: currentFilters.location});
  
  if (activeFilters.length > 0) {
    const statusDiv = document.createElement('div');
    statusDiv.className = 'filter-status';
    
    activeFilters.forEach(filter => {
      const tag = document.createElement('div');
      tag.className = 'filter-tag';
      tag.innerHTML = `
        ${filter.type}: ${filter.value}
        <span class="remove" onclick="removeFilter('${filter.type}')">&times;</span>
      `;
      statusDiv.appendChild(tag);
    });
    
    postListEl.parentNode.insertBefore(statusDiv, postListEl);
  }
}

window.removeFilter = function(type) {
  switch(type) {
    case 'search':
      currentFilters.search = '';
      searchInput.value = '';
      break;
    case 'category':
      currentFilters.category = '';
      filterCategory.value = '';
      break;
    case 'location':
      currentFilters.location = '';
      filterLocation.value = '';
      break;
  }
  applyFilters();
}

function renderList(list){
  postListEl.innerHTML = '';
  if(!list || list.length===0){
    const emptyMsg = currentFilters.search || currentFilters.category || currentFilters.location 
      ? 'No posts match your filters. Try adjusting your search criteria.'
      : 'No posts yet — be the first to ask!';
    postListEl.innerHTML = `<div class="empty">${emptyMsg}</div>`;
    return;
  }
  
  list.forEach(p=>{
    const card = document.createElement('article');
    card.className = 'post-card';
    card.innerHTML = `
      <div class="post-media">${p.image?`<img loading="lazy" src="${p.image}" alt="Post image">`:'<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#999;font-size:2rem">📷</div>'}</div>
      <div class="post-body">
        <div class="post-title">${escapeHtml(p.title)}</div>
        <div class="post-meta">
          <span><i class="fas fa-tag"></i> ${escapeHtml(p.category)}</span>
          <span><i class="fas fa-map-marker-alt"></i> ${escapeHtml(p.district || 'Unknown')}</span>
          <span><i class="fas fa-clock"></i> ${escapeHtml(p.created)}</span>
        </div>
        <div class="post-actions">
          <button class="small-btn" data-id="${p.id}" onclick="openPost(${p.id})">
            <i class="fas fa-eye"></i> View
          </button>
          <button class="small-btn" onclick="quickReply(${p.id})">
            <i class="fas fa-reply"></i> Reply
          </button>
        </div>
      </div>
    `;
    postListEl.appendChild(card);
  });
}

function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' })[c]); }

window.openPost = function(id){
  const p = postsCache.find(x=>x.id===id);
  if(!p) return;
  const detail = document.getElementById('detailContent');
  detail.innerHTML = `
    <div class="post-header">
      <h3>${escapeHtml(p.title)}</h3>
      <div class="post-meta" style="margin-bottom: 16px;">
        <span><i class="fas fa-tag"></i> ${escapeHtml(p.category)}</span>
        <span><i class="fas fa-map-marker-alt"></i> ${escapeHtml(p.district||'Unknown')}</span>
        <span><i class="fas fa-clock"></i> ${escapeHtml(p.created)}</span>
      </div>
    </div>
    <div class="post-content">
      <p style="line-height: 1.6; margin-bottom: 16px;">${escapeHtml(p.body)}</p>
      ${p.image?`<img src="${p.image}" style="max-width:100%;border-radius:8px;margin:10px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)" alt="Post image">`:''}
    </div>
    <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
    <div class="post-actions-detail">
      <h4 style="margin-bottom: 16px;"><i class="fas fa-comments"></i> Responses</h4>
      <div id="responses" style="margin-bottom: 20px;">
        <div style="padding: 20px; text-align: center; color: #666; font-style: italic;">
          No responses yet. Be the first to help!
        </div>
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <button class="primary" onclick="quickReply(${p.id})">
          <i class="fas fa-reply"></i> Answer Question
        </button>
        <button class="secondary" onclick="upvotePost(${p.id})">
          <i class="fas fa-thumbs-up"></i> Helpful (${p.upvotes || 0})
        </button>
        <button class="secondary" onclick="reportPost(${p.id})">
          <i class="fas fa-flag"></i> Report
        </button>
      </div>
    </div>
  `;
  const drawer = document.getElementById('detailDrawer');
  drawer.classList.add('open');
  drawer.setAttribute('aria-hidden','false');
}

window.quickReply = function(postId) {
  showToast('Quick reply feature coming soon! Full comment system needs backend implementation.', 3000);
}

window.upvotePost = function(postId) {
  // Optimistically update the UI
  const post = postsCache.find(p => p.id === postId);
  if (post) {
    post.upvotes = (post.upvotes || 0) + 1;
    applyFilters(); // Re-render to show updated count
    showToast('Thanks for your feedback!', 2000);
  }
  // TODO: Send to backend: POST /api/forum/posts/:id/upvote
}

document.getElementById('closeDetail')?.addEventListener('click', ()=> {
  document.getElementById('detailDrawer').classList.remove('open');
  document.getElementById('detailDrawer').setAttribute('aria-hidden','true');
});

function reportPost(id){
  if (confirm('Are you sure you want to report this post? Our moderation team will review it.')) {
    showToast('Post reported. Our team will review it shortly.',2000);
    // TODO: POST /api/forum/posts/:id/report
  }
}

/* Modal open/close */
createBtn?.addEventListener('click', ()=> {
  postModal.classList.remove('hidden');
  postTitle.focus();
});
closeModalBtn?.addEventListener('click', ()=> postModal.classList.add('hidden'));
document.addEventListener('click', (e)=> {
  if(e.target === postModal) postModal.classList.add('hidden');
});

/* image preview */
postImage?.addEventListener('change', ()=> {
  const f = postImage.files[0];
  if(!f){ imagePreview.classList.add('hidden'); imagePreview.innerHTML=''; return; }
  const url = URL.createObjectURL(f);
  imagePreview.classList.remove('hidden');
  imagePreview.innerHTML = `<img src="${url}" alt="preview" style="max-width: 200px; border-radius: 8px;" />`;
});

/* submit */
postForm?.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const title = postTitle.value.trim();
  const body = postBody.value.trim();
  if(!title || !body){ 
    showToast('Please add both a title and description for your question',2500); 
    return; 
  }

  const submitBtn = document.getElementById('submitPostBtn');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = 'Posting...';
  submitBtn.disabled = true;

  const fd = new FormData();
  fd.append('title', title);
  fd.append('body', body);
  fd.append('category', postCategory.value);
  fd.append('district', postDistrict.value || '');
  if(postImage.files && postImage.files[0]) fd.append('image', postImage.files[0]);

  try{
    const res = await fetch('/api/forum/posts', { method:'POST', body: fd });
    if(!res.ok) throw new Error('Failed to post');
    const data = await res.json();
    
    // Add to cache and re-render
    postsCache.unshift(data.post);
    applyFilters();
    
    // Reset form and close modal
    postModal.classList.add('hidden');
    postForm.reset();
    imagePreview.classList.add('hidden');
    imagePreview.innerHTML = '';
    
    showToast('Your question has been posted successfully!',2500);
  }catch(e){
    console.error(e);
    showToast('Failed to post your question. Please try again.',2500);
  } finally {
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  }
});

/* Filter event listeners */
searchInput?.addEventListener('input', (e)=>{
  currentFilters.search = e.target.value.trim();
  applyFilters();
});

filterCategory?.addEventListener('change', (e) => {
  currentFilters.category = e.target.value;
  applyFilters();
});

filterLocation?.addEventListener('change', (e) => {
  currentFilters.location = e.target.value;
  applyFilters();
});

/* Draft saving functionality */
document.getElementById('saveDraftBtn')?.addEventListener('click', () => {
  const draft = {
    title: postTitle.value,
    body: postBody.value,
    category: postCategory.value,
    district: postDistrict.value,
    timestamp: Date.now()
  };
  
  localStorage.setItem('baalimitra_forum_draft', JSON.stringify(draft));
  showToast('Draft saved locally', 1500);
});

/* Load draft on modal open */
createBtn?.addEventListener('click', () => {
  try {
    const draftStr = localStorage.getItem('baalimitra_forum_draft');
    if (draftStr) {
      const draft = JSON.parse(draftStr);
      const draftAge = Date.now() - draft.timestamp;
      
      // Only restore if draft is less than 24 hours old
      if (draftAge < 24 * 60 * 60 * 1000) {
        postTitle.value = draft.title || '';
        postBody.value = draft.body || '';
        postCategory.value = draft.category || 'General';
        postDistrict.value = draft.district || '';
        
        if (draft.title || draft.body) {
          showToast('Previous draft restored', 1500);
        }
      }
    }
  } catch (e) {
    console.error('Failed to load draft:', e);
  }
});

/* Initial load */
loadPosts();

// Clear draft after successful post
postForm?.addEventListener('submit', () => {
  setTimeout(() => {
    localStorage.removeItem('baalimitra_forum_draft');
  }, 1000);
});