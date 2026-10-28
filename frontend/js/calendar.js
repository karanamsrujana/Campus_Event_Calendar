let calendarEvents=[];
async function loadCalendar(){
 const res=await fetch('/api/events'); calendarEvents=await res.json();
 const el=document.getElementById('calendar');
 const calendar=new FullCalendar.Calendar(el,{initialView:'dayGridMonth',height:'auto',events:calendarEvents.map(e=>({id:e.id,title:e.title,start:e.start_time,end:e.end_time,extendedProps:e})),eventClick:info=>showEvent(info.event.extendedProps)});
 calendar.render();
}
function showEvent(e){
 document.getElementById('eventDetails').innerHTML=`<span class="tag">${e.category}</span><h2>${escapeHtml(e.title)}</h2>
 <p class="muted">${formatDate(e.start_time)} · ${escapeHtml(e.venue)}</p><p>${escapeHtml(e.description)}</p>
 <p><strong>${e.rsvp_count}</strong> / ${e.capacity} seats reserved</p>
 <form onsubmit="submitRsvp(event,${e.id})"><div class="form-grid">
 <div class="field"><label>Name</label><input name="student_name" required></div>
 <div class="field"><label>Student ID</label><input name="student_id" required></div>
 <div class="field full"><label>Email</label><input type="email" name="student_email" required></div></div>
 <div class="form-actions"><button class="button">Confirm RSVP</button></div></form>
 <div id="rsvpMessage"></div>`;
 document.getElementById('modal').classList.remove('hidden');
}
async function submitRsvp(ev,id){
 ev.preventDefault();const data=Object.fromEntries(new FormData(ev.target));
 const r=await fetch(`/api/events/${id}/rsvp`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
 const d=await r.json();const box=document.getElementById('rsvpMessage');
 box.className='notice '+(r.ok?'success':'');box.textContent=d.message||d.error;
}
function closeModal(){document.getElementById('modal').classList.add('hidden')}
function formatDate(s){return new Date(s).toLocaleString([], {dateStyle:'medium',timeStyle:'short'})}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
loadCalendar();
