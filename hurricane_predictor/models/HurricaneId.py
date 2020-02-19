from hurricane_predictor import db

class HurricaneId(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hurricane_id = db.Column(db.String(128))
    hurricane_name = db.Column(db.String(128))
