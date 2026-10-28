def row_to_dict(row):
    return dict(row) if row else None

def event_with_counts(conn, event_id):
    row = conn.execute("""
        SELECT e.*,
               (SELECT COUNT(*) FROM rsvps r WHERE r.event_id=e.id AND r.status='confirmed') AS rsvp_count,
               (SELECT COUNT(*) FROM attendance a WHERE a.event_id=e.id AND a.attended=1) AS attended_count
        FROM events e WHERE e.id=?
    """, (event_id,)).fetchone()
    return row_to_dict(row)

def all_events(conn):
    rows = conn.execute("""
        SELECT e.*,
               (SELECT COUNT(*) FROM rsvps r WHERE r.event_id=e.id AND r.status='confirmed') AS rsvp_count,
               (SELECT COUNT(*) FROM attendance a WHERE a.event_id=e.id AND a.attended=1) AS attended_count
        FROM events e ORDER BY e.start_time
    """).fetchall()
    return [dict(r) for r in rows]
