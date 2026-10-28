async function loadEvents(){
 const r=await fetch('/api/events');const events=await r.json();const grid=document.getElementById('eventGrid');
 grid.innerHTML=events.map(e=>`<article class="event-card"><span class="tag">${escapeHtml(e.category)}</span><h3>${escapeHtml(e.title)}</h3>
 <div class="event-meta">📅 ${formatDate(e.start_time)}<br>📍 ${escapeHtml(e.venue)}<br>👥 ${e.rsvp_count}/${e.capacity} registered</div>
 <button class="button" onclick='showRsvp(${JSON.stringify(e)})'>RSVP</button></article>`).join('');
}
function showRsvp(e){
 document.getElementById('eventModalContent').innerHTML=`<span class="tag">${escapeHtml(e.category)}</span><h2>${escapeHtml(e.title)}</h2><p class="muted">${formatDate(e.start_time)} · ${escapeHtml(e.venue)}</p>
 <p>${escapeHtml(e.description)}</p><form onsubmit="submitEventRsvp(event,${e.id})"><div class="form-grid">
 <div class="field"><label>Name</label><input name="student_name" required></div><div class="field"><label>Student ID</label><input name="student_id" required></div>
 <div class="field full"><label>Email</label><input type="email" name="student_email" required></div></div><div class="form-actions"><button class="button">Confirm RSVP</button></div></form><div id="eventRsvpMessage"></div>`;
 document.getElementById('eventModal').classList.remove('hidden');
}
async function submitEventRsvp(ev,id){ev.preventDefault();const data=Object.fromEntries(new FormData(ev.target));
 const r=await fetch(`/api/events/${id}/rsvp`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const d=await r.json();
 const b=document.getElementById('eventRsvpMessage');b.className='notice '+(r.ok?'success':'');b.textContent=d.message||d.error;if(r.ok) loadEvents();
}
function showCreate(){document.getElementById('eventModalContent').innerHTML=`<h2>Create Event</h2><form onsubmit="createEvent(event)"><div class="form-grid">
<div class="field full"><label>Title</label><input name="title" required></div><div class="field"><label>Category</label><select name="category"><option>Workshop</option><option>Hackathon</option><option>Seminar</option><option>Cultural</option><option>Sports</option><option>Other</option></select></div><div class="field"><label>Venue</label><input name="venue" value="Campus"></div>
<div class="field"><label>Start</label><input type="datetime-local" name="start_time" required></div><div class="field"><label>End</label><input type="datetime-local" name="end_time" required></div><div class="field"><label>Capacity</label><input type="number" name="capacity" value="100" min="1"></div>
<div class="field full"><label>Description</label><textarea name="description"></textarea></div></div><div class="form-actions"><button class="button">Create Event</button></div></form>`;document.getElementById('eventModal').classList.remove('hidden')}
async function createEvent(ev){ev.preventDefault();const data=Object.fromEntries(new FormData(ev.target));const r=await fetch('/api/events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(r.ok){closeEventModal();loadEvents()}else alert((await r.json()).error)}
function closeEventModal(){document.getElementById('eventModal').classList.add('hidden')}
function formatDate(s){return new Date(s).toLocaleString([], {dateStyle:'medium',timeStyle:'short'})}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
async function loadHomeStats(){const r=await fetch('/api/events');if(!r.ok)return;const e=await r.json();const total=e.reduce((a,x)=>a+x.rsvp_count,0);document.getElementById('homeStats').innerHTML=`<div class="stat"><strong>${e.length}</strong><span class="muted">Upcoming events</span></div><div class="stat"><strong>${total}</strong><span class="muted">Confirmed RSVPs</span></div><div class="stat"><strong>${e.reduce((a,x)=>a+x.capacity,0)}</strong><span class="muted">Total capacity</span></div>`}
