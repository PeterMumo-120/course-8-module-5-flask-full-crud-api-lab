
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# POST /events - Create a new event from JSON input
@app.route('/events', methods=['POST'])
def create_event():
    """Create a new event.

    Expects JSON like: { "title": "Hackathon" }
    Returns the created event and a 201 status code.
    """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID (simple in-memory strategy)
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, data['title'])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    """Update an existing event's title.

    Expects JSON like: { "title": "New Title" }
    Returns the updated event or 404 if not found.
    """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required for update"}), 400

    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    event.title = data['title']
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event by id.

    Returns a 200 with a confirmation message, or 404 if the event does not exist.
    """
    global events
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != event_id]
    return jsonify({"message": "Event deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)