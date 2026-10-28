from flask import Blueprint, jsonify, request
from ..database import get_db
from ..models import event_with_counts

rsvp_bp = Blueprint("rsvp", __name__, url_prefix="/api/events")

@rsvp_bp.post("/<int:event_id>/rsvp")
def create_rsvp(event_id):
    data = request.get_json(silent=True) or {}
    required = ["student_name", "student_email", "student_id"]
    missing = [x for x in required if not data.get(x)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_db()
    event = event_with_counts(conn, event_id)
    if not event:
        conn.close()
        return jsonify({"error": "Event not found"}), 404
    if event["rsvp_count"] >= event["capacity"]:
        conn.close()
        return jsonify({"error": "This event is full"}), 409

    try:
        conn.execute("""INSERT INTO rsvps(event_id, student_name, student_email, student_id)
                        VALUES (?, ?, ?, ?)""",
                     (event_id, data["student_name"].strip(),
                      data["student_email"].strip().lower(), data["student_id"].strip()))
        conn.commit()
    except Exception as exc:
        conn.close()
        if "UNIQUE" in str(exc).upper():
            return jsonify({"error": "This email has already RSVP'd for the event"}), 409
        return jsonify({"error": "Unable to create RSVP"}), 400

    result = event_with_counts(conn, event_id)
    conn.close()
    return jsonify({"message": "RSVP confirmed", "event": result}), 201

@rsvp_bp.delete("/<int:event_id>/rsvp")
def cancel_rsvp(event_id):
    data = request.get_json(silent=True) or {}
    email = (data.get("student_email") or "").strip().lower()
    if not email:
        return jsonify({"error": "student_email is required"}), 400
    conn = get_db()
    cur = conn.execute("DELETE FROM rsvps WHERE event_id=? AND student_email=?",
                       (event_id, email))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "RSVP not found"}), 404
    return jsonify({"message": "RSVP cancelled"})
