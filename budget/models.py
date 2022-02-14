from budget import db

class project_details(db.Model):
    project_details_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name=db.Column(db.String(100), nullable=False)
    client_name=db.Column(db.String(100), nullable=False)
    status_flag=db.Column(db.Integer, db.ForeignKey('status_type.status_type_id'),
        nullable=False)
    commence_date=db.Column(db.DateTime,nullable=False)
    duration_inweeks=db.Column(db.Integer)
    def __repr__(self):
        return f'{self.project_details_id}'


class workstream(db.Model):
    workstream_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.workstream_id,self.name}'
    def __init__(self,name):
        self.name=name


class labor_category(db.Model):
    labor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    labor_type=db.Column(db.String(100))
    country=db.Column(db.String(100))
    cost_per_hour=db.Column(db.Float)

    def __repr__(self):
        return f'{self.labor_id, self.labor_type, self.country,self.cost_per_hour}'
    def __init__(self,type,country,cost):
        self.labor_type=type
        self.country=country
        self.cost_per_hour=cost

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role_id=db.Column(db.Integer, db.ForeignKey('role.role_id'),
        nullable=False)
    status_type=db.Column(db.Integer, db.ForeignKey('status_type.status_type_id'),
        nullable=False)
    def __init(self,email_id,first_name,last_name,role_id,status_type):
        self.email_id=email_id
        self.first_name=first_name
        self.last_name=last_name
        self.role_id=role_id
        self.status_type=status_type

    def __repr__(self):
        return f'{self.user_id, self.email_id, self.first_name, self.last_name}'


class role(db.Model):
    role_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name=db.Column(db.String(100))

class project_budget(db.Model):
    project_budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id=db.Column(db.Integer, db.ForeignKey('project_details.project_details_id'),
        nullable=False)
    prepared_by=db.Column(db.Integer, db.ForeignKey('user.user_id'),
        nullable=False)
    created_date=db.Column(db.DateTime)
    last_modified_date=db.Column(db.DateTime)
    total_budget=db.Column(db.Float)
    def __init__(self, project_id,   prepared_by):
        self.project_id=project_id
        self.prepared_by=prepared_by
class budget_breakdown(db.Model):
    budget_breakdown_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_budget_id=db.Column(db.Integer, db.ForeignKey('project_budget.project_budget_id'),
        nullable=False)
    labor_category_id=db.Column(db.Integer, db.ForeignKey('labor_category.labor_id'),
        nullable=False)
    labor_hours=db.Column(db.Integer)
    workstream_id=db.Column(db.Integer, db.ForeignKey('workstream.workstream_id'),
        nullable=False)
    pay_per_hour=db.Column(db.Float)
    def __init__(self,project_budget_id,labor_category_id,labor_hours,workstream_id,pay_per_hour):
        self.project_budget_id=project_budget_id
        self.labor_category_id=labor_category_id
        self.labor_hours=labor_hours
        self.workstream_id=workstream_id
        self.pay_per_hour=pay_per_hour

    def __repr__(self):
        return f'{self.project_budget_id}'

class status_type(db.Model):
    status_type_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    type=db.Column(db.String(100))

    def __repr__(self):
        return f'{self.status_type_id, self.type}'




