from hurricane_predictor import db


class HurricaneRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    hurricane_id = db.Column(db.Integer, db.ForeignKey('hurricane_id.id'), nullable=False)
