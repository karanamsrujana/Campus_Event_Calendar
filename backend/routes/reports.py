from flask import Blueprint, jsonify, Response
from ..database import get_db
from ..services.csv_export import rows_to_csv

reports_bp = Blueprint("reports", __name__, url_prefix="/api/reports")

@reports_bp.get("/attendance")
def attendance_report():
    conn = get_db()
    rows = conn.execute("""
        SELECT e.id AS event_id, e.title AS event_name, e.category,
               e.start_time, e.capacity,
               COUNT(DISTINCT r.id) AS registered,
               COUNT(DISTINCT CASE WHEN a.attended=1 THEN a.id END) AS attended
        FROM events e
        LEFT JOIN rsvps r ON r.event_id=e.id AND r.status='confirmed'
        LEFT JOIN attendance a ON a.event_id=e.id
        GROUP BY e.id
        ORDER BY e.start_time
    """).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["attendance_percentage"] = round(
            (d["attended"] / d["registered"] * 100), 2
        ) if d["registered"] else 0
        result.append(d)
    conn.close()
    return jsonify(result)

@reports_bp.get("/rsvp")
def rsvp_report():
    conn = get_db()
    rows = conn.execute("""
        SELECT e.id AS event_id, e.title AS event_name,
               COUNT(r.id) AS registered, e.capacity
        FROM events e
        LEFT JOIN rsvps r ON r.event_id=e.id AND r.status='confirmed'
        GROUP BY e.id ORDER BY e.start_time
    """).fetchall()
    result = [dict(r) for r in rows]
    conn.close()
    return jsonify(result)

@reports_bp.get("/attendance/csv")
def attendance_csv():
    conn = get_db()
    rows = conn.execute("""
        SELECT e.id AS event_id, e.title AS event_name, e.category,
               e.start_time, e.capacity,
               COUNT(DISTINCT r.id) AS registered,
               COUNT(DISTINCT CASE WHEN a.attended=1 THEN a.id END) AS attended
        FROM events e
        LEFT JOIN rsvps r ON r.event_id=e.id AND r.status='confirmed'
        LEFT JOIN attendance a ON a.event_id=e.id
        GROUP BY e.id ORDER BY e.start_time
    """).fetchall()
    data=[]
    for r in rows:
        d=dict(r)
        d["attendance_percentage"] = round(d["attended"]/d["registered"]*100,2) if d["registered"] else 0
        data.append(d)
    conn.close()
    return Response(rows_to_csv(data), mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=attendance_summary.csv"})

@reports_bp.get("/rsvp/csv")
def rsvp_csv():
    conn = get_db()
    rows = conn.execute("""
        SELECT e.id AS event_id, e.title AS event_name,
               r.student_name, r.student_email, r.student_id, r.status
        FROM rsvps r JOIN events e ON e.id=r.event_id
        ORDER BY e.start_time, r.student_name
    """).fetchall()
    data=[dict(r) for r in rows]
    conn.close()
    return Response(rows_to_csv(data), mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=rsvp_list.csv"})

@reports_bp.get("/events/<int:event_id>/attendees")
def event_attendees(event_id):
    conn = get_db()
    rows = conn.execute("""
        SELECT r.student_name, r.student_email, r.student_id,
               COALESCE(a.attended,0) AS attended
        FROM rsvps r
        LEFT JOIN attendance a ON a.event_id=r.event_id AND a.student_email=r.student_email
        WHERE r.event_id=? ORDER BY r.student_name
    """,(event_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])
