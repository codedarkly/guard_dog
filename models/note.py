from mongoframes import *
from datetime import datetime

class Note(SubFrame):
    _fields = {
        'id',
        'title',
        'category',
        'note',
        'priority',
        'date_added'
    }

    def add_note(user, note):
        user.notes.append(note)
        user.update()
        return 'Note added', 200

    def remove_note(user, note_id):
        try:
           result = [(key,note) for key, note in enumerate(user['notes']) if note_id in note['id']]
           id = int([item[0] for item in result][0])
           del user.notes[id]
           user.update()
           return 'Note removed', 200
        except (IndexError, TypeError):
            return 'Note does not exist', 404

    def retrieve_note(user, note_id):
        try:
            return [note for note in user['notes'] if note_id in note['id']][0]
        except (IndexError, TypeError):
            return 'Note does not exist', 404

    def retrieve_notes(user):
        try:
            return user.notes
        except AttributeError:
            return 'User has no notes', 404

    def edit_note():
        pass
