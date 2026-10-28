from flask import Blueprint, jsonify, request
from ..database import get_db
from ..models import all_events, event_with_counts

events_bp = Blueprint("events", __name__, url_prefix="/api/events")

@events_bp.get("")
def list_events():
    conn = get_db()
    data = all_events(conn)
    conn.close()
    return jsonify(data)

@events_bp.get("/<int:event_id>")
def get_event(event_id):
    conn = get_db()
    data = event_with_counts(conn, event_id)
    conn.close()
    if not data:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(data)

@events_bp.post("")
def create_event():
    data = request.get_json(silent=True) or {}
    required = ["title", "start_time", "end_time"]
    missing = [x for x in required if not data.get(x)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    try:
        capacity = int(data.get("capacity", 100))
        if capacity < 1:
            raise ValueError
    except ValueError:
        return jsonify({"error": "capacity must be a positive integer"}), 400

    conn = get_db()
    cur = conn.execute("""INSERT INTO events
        (title, description, category, venue, start_time, end_time, capacity)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data["title"], data.get("description",""), data.get("category","Other"),
         data.get("venue","Campus"), data["start_time"], data["end_time"], capacity))
    conn.commit()
    result = event_with_counts(conn, cur.lastrowid)
    conn.close()
    return jsonify(result), 201

@events_bp.put("/<int:event_id>")
def update_event(event_id):
    data = request.get_json(silent=True) or {}
    conn = get_db()
    if not event_with_counts(conn, event_id):
        conn.close()
        return jsonify({"error": "Event not found"}), 404
    fields = ["title","description","category","venue","start_time","end_time","capacity"]
    updates, values = [], []
    for field in fields:
        if field in data:
            updates.append(f"{field}=?")
            values.append(data[field])
    if not updates:
        conn.close()
        return jsonify({"error": "No fields to update"}), 400
    values.append(event_id)
    conn.execute(f"UPDATE events SET {', '.join(updates)} WHERE id=?", values)
    conn.commit()
    result = event_with_counts(conn, event_id)
    conn.close()
    return jsonify(result)

@events_bp.delete("/<int:event_id>")
def delete_event(event_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Event deleted"})
