from mib import db


class Lottery(db.Model):
    # The name of the table that we explicitly set
    __tablename__ = 'Lottery'

    contestant_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, *args, **kw):
        super(Lottery, self).__init__(*args, **kw)

    def set_contestant(self, contestant_id):
        self.contestant_id = contestant_id
