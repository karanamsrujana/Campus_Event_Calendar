async function loadReports(){
 const r=await fetch('/api/reports/attendance');const data=await r.json();
 const registered=data.reduce((a,x)=>a+x.registered,0),attended=data.reduce((a,x)=>a+x.attended,0);
 const rate=registered?((attended/registered)*100).toFixed(1):0;
 document.getElementById('reportCards').innerHTML=`<div class="stat"><strong>${registered}</strong><span class="muted">Total registrations</span></div><div class="stat"><strong>${attended}</strong><span class="muted">Total attendees</span></div><div class="stat"><strong>${rate}%</strong><span class="muted">Overall attendance</span></div>`;
 document.getElementById('reportBody').innerHTML=data.map(x=>`<tr><td><strong>${escapeHtml(x.event_name)}</strong><br><small class="muted">${escapeHtml(x.category)}</small></td><td>${x.registered}</td><td>${x.attended}</td><td>${x.attendance_percentage}%<div class="progress"><i style="width:${Math.min(x.attendance_percentage,100)}%"></i></div></td></tr>`).join('');
 new Chart(document.getElementById('attendanceChart'),{type:'bar',data:{labels:data.map(x=>x.event_name),datasets:[{label:'Registered',data:data.map(x=>x.registered)},{label:'Attended',data:data.map(x=>x.attended)}]},options:{responsive:true,maintainAspectRatio:false}});
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
