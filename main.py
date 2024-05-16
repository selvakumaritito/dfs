from flask import Flask, render_template, redirect, url_for, send_file, flash, request, jsonify, Response
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from forms import *
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Text, Float, LargeBinary
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from flask import abort
from werkzeug.utils import secure_filename
import os
from roster_sheet import create_roster
import base64
from io import BytesIO
from dateutil.parser import parse

home_directory = os.path.expanduser('~')

# gunicorn error check deploy

# app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = "kkkkk"
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@localhost/test"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dfx_db_seis.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# creating login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        admin = User.query.all()
        admin_id = []
        for i in admin:
            id_ = i.id
            admin_id.append(id_)
        print(admin_id)
        if current_user not in admin:
            return abort(403)
        # Otherwise, continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# to create dates list for master_ts
def date_range_list(start_date, end_date):
    # Return list of datetime.date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(str(curr_date))
        curr_date += timedelta(days=1)
    return date_list


# Create database classes

# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))

    # relationships
    # TODO 1 - Employee Master
    employee = relationship("employeeMaster", back_populates="user")
    # TODO 2 - roster Master
    roster = relationship("rosterMaster", back_populates="user")
    # TODO 3 - Time sheet master
    timesheet = relationship("timesheetMaster", back_populates="user")
    # TODO 4 - Leave Appln Master
    leave = relationship("leaveApplicationMaster", back_populates="user")
    # TODO 5 - Passport Appln Master
    passport = relationship("passportApplicationMaster", back_populates="user")


class employeeMaster(db.Model):
    __tablename__ = "employeeMaster"
    id = Column(Integer, primary_key=True)
    employeeID = Column(String(300))
    joining_date = Column(DateTime)
    name = Column(String(300))
    addressUae = Column(String(300))
    poBox = Column(String(300))
    mobilePersonal = Column(Integer)
    mobileHome = Column(Integer)
    personalMail = Column(String(300))
    addressHome = Column(String(300))
    passportNumber = Column(Integer)
    nationality = Column(String(300))
    ownCar = Column(Boolean)
    carRent = Column(Boolean)
    company_laptop = Column(String(300))
    company_mobile = Column(String(300))
    emUaeName = Column(String(300))
    emUaeRel = Column(String(300))
    emUaeAddr = Column(String(300))
    emUaeMobileNumber = Column(Integer)
    emUaeHomeNumber = Column(Integer)
    originCountry = Column(String(300))
    emCoName = Column(String(300))
    emCoRel = Column(String(300))
    emCoAddr = Column(String(300))
    emCoMobileNumber = Column(Integer)
    emCoHomeNumber = Column(Integer)

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="employee")

    departmentId = Column(Integer, ForeignKey("departmentMaster.id"))
    department = relationship("departmentMaster", back_populates="employee")

    # relationships as parent
    # TODO 1 - document Master
    document = relationship("documentMaster", back_populates="employee")
    # TODO 2 - actionItem Master
    actionItem = relationship("actionItemMaster", back_populates="employee")
    # TODO 3 - Leave Appln Master
    leave = relationship("leaveApplicationMaster", back_populates="employee")
    # TODO 4 - Passport Appln Master
    passport = relationship("passportApplicationMaster", back_populates="employee")
    # TODO 5 - Time sheet Entry master
    timesheet = relationship("timesheetEntryMaster", back_populates="employee")
    # TODO 6 - Roster Entry master
    roster = relationship("rosterEntryMaster", back_populates="employee")
    # TODO 7 - Employee details
    details = relationship("employeeDetails", back_populates="employee")
    # TODO 8 - Image
    img__ = relationship('Img', back_populates='employee')


class rosterMaster(db.Model):
    __tablename__ = "rosterMaster"
    id = Column(Integer, primary_key=True)
    date = Column(String(300))

    # relationship as parent
    entry = relationship("rosterEntryMaster", back_populates="roster")

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="roster")


class timesheetMaster(db.Model):
    __tablename__ = "timesheetMaster"
    id = Column(Integer, primary_key=True)
    date = Column(String(300))
    sheet_no = Column(Integer)

    # relationship as parent
    entry = relationship("timesheetEntryMaster", back_populates="timesheet")

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="timesheet")

    hotelID = Column(Integer, ForeignKey("hotelMaster.id"))
    hotel = relationship("hotelMaster", back_populates="timesheet")


class hotelMaster(db.Model):
    __tablename__ = "hotelMaster"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    address = Column(String(300))
    # TODO - add interval and rate to the table
    interval = Column(String(300))
    rate = Column(Float)

    # relationship as parent
    rosterEntry = relationship("rosterEntryMaster", back_populates="hotel")
    timesheet = relationship("timesheetMaster", back_populates="hotel")


class departmentMaster(db.Model):
    __tablename__ = "departmentMaster"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))

    # relationship as parent
    employee = relationship("employeeMaster", back_populates="department")


class documentMaster(db.Model):
    __tablename__ = "documentMaster"
    id = Column(Integer, primary_key=True)
    documentName = Column(String(300))
    documentDirectory = Column(LargeBinary)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="document")


class employeeDetails(db.Model):
    __tablename__ = "employeeDetails"
    id = Column(Integer, primary_key=True)
    payments_done = Column(String(300))
    payments_pending = Column(String(300))
    total_leaves = Column(String(300))
    visa_expiry = Column(String(300))
    dummy1 = Column(String(300))
    dummy2 = Column(String(300))
    dummy3 = Column(String(300))
    dummy4 = Column(String(300))

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="details")


class Img(db.Model):
    __tablename__ = "Img"
    id = Column(Integer, primary_key=True)
    img = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    mimetype = Column(Text, nullable=False)
    # employeeID = Column(Integer)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="img__")


class actionItemMaster(db.Model):
    __tablename__ = "actionItemMaster"
    id = Column(Integer, primary_key=True)
    actionText = Column(String(300))

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="actionItem")


class leaveApplicationMaster(db.Model):
    __tablename__ = "leaveApplicationMaster"
    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    company = Column(String(300))
    dept = Column(String(300))
    designation = Column(String(300))
    nationality = Column(String(300))
    pass_no = Column(String(300))  # TODO change to string
    emp = Column(String(300))

    # type of leave
    leave_type = Column(String(300))

    # Personal Details
    addr_wol = Column(String(300))
    con_per = Column(String(300))
    rel = Column(String(300))
    pol = Column(String(300))
    # sign = StringField("Signature and Date")
    dot = Column(DateTime)
    con_wol = Column(String(300))
    sub_emp = Column(String(300))
    leave_f = Column(DateTime)
    leave_t = Column(DateTime)
    no_days = Column(Integer)
    air_tic = Column(String(300))

    # Guarantors
    g1_name = Column(String(300))
    g1_dept = Column(String(300))
    g1_id_no = Column(Integer)
    # g1_sign = IntegerField("Sign and Date")
    g2_name = Column(String(300))
    g2_dept = Column(String(300))
    g2_id_no = Column(Integer)
    # g2_sign = IntegerField("Sign and Date")

    # HR Dept
    doj = Column(DateTime)
    tla = Column(Integer)
    less_this = Column(Integer)
    nod_app = Column(Integer)
    dor = Column(DateTime)
    eligibility = Column(String(300))
    last_leave = Column(String(300))
    balance_leave = Column(Integer)
    release_date = Column(DateTime)
    # sign_hr = StringField("Sign & Date HR Assistant: ")

    # If Annual Leave not Approved
    amt_appr = Column(Integer)
    cheq_no = Column(Integer)
    # empl_sign = StringField("Employee Signature: ")
    pbc = Column(String(300))
    bank_tr = Column(String(300))
    date_tr = Column(DateTime)

    # Approval
    approved_by = Column(String(300))
    approved_by_2 = Column(String(300))

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="leave")

    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="leave")


class passportApplicationMaster(db.Model):
    __tablename__ = "passportApplicationMaster"
    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    emp_no = Column(Integer)
    pow = Column(String(300))
    days_req = Column(String(300))
    remarks = Column(String(300))

    # guarantors
    g1_name = Column(String(300))
    g1_dept = Column(String(300))
    g1_id_no = Column(Integer)
    g2_name = Column(String(300))
    g2_dept = Column(String(300))
    g2_id_no = Column(Integer)

    # approval
    checked_by = Column(String(300))
    appr_by_lm = Column(String(300))
    appr_by_hr = Column(String(300))
    dir_op = Column(String(300))

    # issue
    pass_rec = Column(String(300))
    date_pass_rec = Column(DateTime)
    lc_rec = Column(String(300))
    date_lc_rec = Column(DateTime)

    # return
    pass_rec_e = Column(String(300))
    date_pass_rec_e = Column(DateTime)
    lc_rec_e = Column(String(300))
    date_lc_rec_e = Column(DateTime)

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="passport")

    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="passport")


class timesheetEntryMaster(db.Model):
    __tablename__ = "timesheetEntryMaster"
    id = Column(Integer, primary_key=True)
    timeIn1 = Column(Integer)
    timeOut1 = Column(Integer)
    timeIn2 = Column(Integer)
    timeOut2 = Column(Integer)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="timesheet")

    timesheetID = Column(Integer, ForeignKey("timesheetMaster.id"))
    timesheet = relationship("timesheetMaster", back_populates="entry")


class rosterEntryMaster(db.Model):
    __tablename__ = "rosterEntryMaster"
    id = Column(Integer, primary_key=True)
    timeIn1 = Column(Integer)
    timeOut1 = Column(Integer)
    timeIn2 = Column(Integer)
    timeOut2 = Column(Integer)
    pickUp = Column(Integer)
    remark = Column(String(300))
    absent = Column(String(300))
    pickUp2 = Column(Integer)  # TODO add pickup2

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="roster")

    rosterID = Column(Integer, ForeignKey("rosterMaster.id"))
    roster = relationship("rosterMaster", back_populates="entry")

    hotelID = Column(Integer, ForeignKey("hotelMaster.id"))
    hotel = relationship("hotelMaster", back_populates="rosterEntry")

with app.app_context():
    db.create_all()
## postgres


##


# Forms
class LeaveForm(FlaskForm):
    # employees = employeeMaster.query.all()
    # employee_name = [i.name for i in employees]
    # details
    date = DateField("Date: ")
    name = SelectField(u'Name of the Employee', coerce=str)
    company = StringField("Company: ")
    dept = StringField("Department: ")
    designation = StringField("Designation: ")
    nationality = StringField("Nationality: ")
    pass_no = StringField("Passport No.: ")
    emp = StringField("EMP No.: ")

    # type of leave
    leave_type = SelectField(u'Leave Type',
                             choices=['Vacation', 'Emergency Leave', "Annual Leave", "Cash-in Lieu", "Leave w/o Pay",
                                      "Sick Leave", "Public Holiday"])

    # Personal Details
    addr_wol = StringField("Address While on Leave")
    con_per = StringField("Contact person")
    rel = StringField("Relation")
    pol = StringField("Purpose of Leave")
    # sign = StringField("Signature and Date")
    dot = DateField("Date of Travel")
    con_wol = StringField("Contact Number(s) While on Leave")
    sub_emp = StringField("Substitute Employee")
    leave_f = DateField("Leave From")
    leave_t = DateField("Leave To")
    no_days = IntegerField("Number of Days:")
    air_tic = StringField("Air Ticket Details")

    # Guarantors
    g1_name = StringField(u'Guarantor 1')
    g1_dept = StringField("Department: ")
    g1_id_no = IntegerField("ID No.: ")
    # g1_sign = IntegerField("Sign and Date")
    g2_name = StringField(u'Guarantor 2')
    g2_dept = StringField("Department: ")
    g2_id_no = IntegerField("ID No.: ")
    # g2_sign = IntegerField("Sign and Date")

    # HR Dept
    doj = DateField("Date of Joining: ")
    tla = IntegerField("Total Leave Available")
    less_this = IntegerField("Less this leave: ")
    nod_app = IntegerField("No. of Days Approved")
    dor = DateField("Date of Return")
    eligibility = StringField("Eligibility")
    last_leave = StringField("Period/Date of Last Leave: ")
    balance_leave = IntegerField("Balance: ")
    release_date = DateField("Release Date: ")
    # sign_hr = StringField("Sign & Date HR Assistant: ")

    # If Annual Leave not Approved
    amt_appr = IntegerField("Amount Approved: ")
    cheq_no = IntegerField("Cheque No.: ")
    # empl_sign = StringField("Employee Signature: ")
    pbc = StringField("Paid by Cash:")
    bank_tr = StringField("Bank Transfer")
    date_tr = DateField("Date: ")

    # Approval
    approved_by = StringField(u'Approved By')
    # lm_sign = StringField("Sign & Date Line Manager")
    approved_by_2 = StringField(u'Approved By')
    # md_sign = StringField("Sing & Date Managing Director ")

    # submit
    submit = SubmitField("Submit Leave Form")


class PassportForm(FlaskForm):
    # employees = employeeMaster.query.all()
    # employee_name = [i.name for i in employees]
    date = DateField("Date: ")
    emp_no = IntegerField("Emp No.: ")
    name = SelectField(u'Name of the Employee:', coerce=str)
    pow = StringField("Purpose of Withdrawal")
    # sign = StringField("Signature")
    days_req = StringField("Days Required")
    remarks = StringField("Remarks")

    # guarantors
    g1_name = StringField(u'Name: ')
    g1_dept = StringField("Department: ")
    g1_id_no = IntegerField("ID No.: ")
    # g1_sign = IntegerField("Sign and Date")
    g2_name = StringField(u'Name: ')
    g2_dept = StringField("Department: ")
    g2_id_no = IntegerField("ID No.: ")
    # g2_sign = IntegerField("Sign and Date")

    # approval
    checked_by = StringField(u"Checked By | Name: ")
    # checked_by_sign = StringField("Sign: ")
    appr_by_lm = StringField(u"Approved By | Line Manager: ")
    # appr_by_lm_sign = StringField("Sign: ")
    appr_by_hr = StringField(u"Approved By | HR Manager: ")
    # appr_by_hr_sign = StringField("Sign: ")
    dir_op = StringField(u"CEO: ")
    # dir_op_sign = StringField("Sign")

    # issue
    pass_rec = StringField(u"Passport Received | Name: ")
    date_pass_rec = DateField('Date: ')
    lc_rec = StringField(u"Labor Card Received by HRD: ")
    date_lc_rec = DateField("Date: ")

    # sign_pass = StringField("Signature: ")
    # sign_lc = StringField("Signature: ")

    # return
    pass_rec_e = StringField(u"Passport Received | Name: ")
    date_pass_rec_e = DateField('Date: ')
    lc_rec_e = StringField(u"Labor Card Received by Employee: ")
    date_lc_rec_e = DateField("Date: ")

    # sign_pass_e = StringField("Signature: ")
    # sign_lc_e = StringField("Signature: ")

    # submit
    submit = SubmitField("Submit Passport Request Form")


class RegistrationForm(FlaskForm):
    with app.app_context():
        department_ = departmentMaster.query.all()
        department_name = [i.name for i in department_]
    # print(department_name)
    name = StringField("Name:       ", validators=[DataRequired()])
    joining_date = DateField("Joining Date:")
    department_e = StringField(u"Department: ")
    employee_id = StringField("Employee ID: ")
    address_uae = StringField("Address UAE:     ", validators=[DataRequired()])
    po_box = StringField("P. O. Box:    ", validators=[DataRequired()])
    mobile_p = IntegerField("Personal Mobile No.:   ", validators=[DataRequired()])
    mobile_h = IntegerField("Home Mobile No.:", validators=[DataRequired()])
    personal_mail = EmailField("Personal Mail ID: ")
    address_home = StringField("Home Address (Country of Origin):")
    passport_no = StringField("Passport No.: ")
    nationality = StringField("Nationality: ")
    own_car = BooleanField("Driving Own Car?: ")
    car_rent = BooleanField("Company Car:")
    company_laptop = StringField("Company Laptop Details: ")
    company_mobile = StringField("Company Mobile Details: ")
    e_uae_name = StringField("Name: ")
    e_uae_rel = StringField("Relationship: ")
    e_uae_addr = StringField("Address: ")
    e_uae_mob = IntegerField("Mobile No.:")
    e_uae_hom = IntegerField("Home No.:")
    origin_country = StringField("Country of Origin:")
    e_co_name = StringField("Name: ")
    e_co_rel = StringField("Relationship: ")
    e_co_addr = StringField("Address: ")
    e_co_mob = IntegerField("Mobile No.:")
    e_co_hom = IntegerField("Home No.:")
    upload = MultipleFileField("Upload Multiple Documents")
    submit = SubmitField("Complete Registration")

    """
    use this code to determine which submit field is selected in main1.py
     if form.validate_on_submit():
        if form.user_stats.data:
            return redirect(url_for('user_stats'))
        elif form.room_stats.data:
            return redirect(url_for('room_stats'))

    return render_template('stats.html', form=form)

    Or rather can have another page for uploading documents - that's better
    """


# to convert time to int
def getTimeInt(time):
    b = time.split(':')
    if int(b[0]) < 10:
        b[0] = '0' + b[0]
    else:
        b[0] = b[0]
    c = b[0] + b[1]
    d = int(c)
    # print(d)
    return d


def getTimeStr(time):
    time = int(time)
    hour = time // 100
    minutes = time - (hour * 100)
    if hour < 10:
        hour_str = '0' + str(hour)
    else:
        hour_str = str(hour)
    if minutes < 10:
        min_str = '0' + str(minutes)
    else:
        min_str = str(minutes)
    time_str = hour_str + ':' + min_str
    # print(time_str)
    return time_str


def total_time_hrs(time):
    c__ = time // 100
    # print(f"c__: {c__}")
    d__ = time - c__ * 100
    # print(f"d__: {d__}")
    e___ = d__ / 60
    # print(f"e___: {e___}")
    total_hrs = c__ + e___
    return round(total_hrs, 2)


# Website routes
@app.route('/', methods=["GET", "POST"])
def cover():
    return render_template("index.html")


@app.route('/admin-register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            # user already exists
            flash("You've already signed up with that email, login instead")
            return redirect(url_for('login'))

        new_user = User(email=form.email.data,
                        password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8),
                        name=form.name.data,
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Logged in successfully.')
        return redirect(url_for('home'))

    return render_template("admin_register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        # email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))

        # Password incorrect
        elif not check_password_hash(user.password, form.password.data):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))

        # email exists and password correct
        else:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html", user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def home():
    return render_template("home.html", user=current_user)


@app.route('/registration', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def registration():
    form = RegistrationForm()
    department_ = departmentMaster.query.all()
    department_name = [i.name for i in department_]
    if request.method == "POST":
        department_ = request.form.get("department_e")
        if department_:
            department = db.session.query(departmentMaster).filter_by(name=department_).first()
        else:
            department = db.session.query(departmentMaster).filter_by(id=1).first()
        a_date = datetime.datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d').date()
        nationality_passportNo = f"{request.form.get('nationality')}+{request.form.get('passport_no')}"
        mobile_string = f"{request.form.get('e_uae_addr')}+{request.form.get('mobile_p')}+{request.form.get('mobile_h')}+{request.form.get('e_uae_mob')}+{request.form.get('e_co_mob')}"
        if request.form.get('own_car') == 'y':
            own_car = True
        else:
            own_car = False

        if request.form.get('car_rent') == 'y':
            car_rent = True
        else:
            car_rent = False
        new_employee = employeeMaster(
            name=request.form.get("name"),
            addressUae=request.form.get('address_uae'),
            poBox=request.form.get('po_box'),
            mobilePersonal=1,
            mobileHome=1,
            personalMail=request.form.get('personal_mail'),
            addressHome=request.form.get('address_home'),
            passportNumber=0,
            nationality=nationality_passportNo,
            ownCar=own_car,
            carRent=car_rent,
            emUaeName=request.form.get('e_uae_name'),
            emUaeRel=request.form.get('e_uae_rel'),
            emUaeAddr=mobile_string,
            emUaeMobileNumber=1,
            emUaeHomeNumber=request.form.get('e_uae_hom'),
            originCountry=request.form.get('origin_country'),
            emCoName=request.form.get('e_co_name'),
            emCoRel=request.form.get('e_co_rel'),
            emCoAddr=request.form.get('e_co_addr'),
            emCoMobileNumber=1,
            emCoHomeNumber=request.form.get('e_co_hom'),
            employeeID=request.form.get('employee_id'),
            joining_date=a_date,
            company_laptop=request.form.get('company_laptop'),
            company_mobile=request.form.get('company_mobile'),
            user=current_user,
            department=department
        )

        db.session.add(new_employee)

        db.session.commit()
        new_detail = employeeDetails(payments_done='', employee=new_employee)
        db.session.add(new_detail)
        db.session.commit()
        return render_template("upload_doc.html", name=form.name.data, user=current_user, emp_id=new_employee.id)

    return render_template("reg2.html", form=form, user=current_user, depts=department_name)


@app.route("/doc", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def doc():
    if request.method == 'POST':
        directory = request.form.get('name')
        employee_element = db.session.query(employeeMaster).filter_by(id=directory).first()
        #
        # # Parent Directory path
        # parent_dir = home_directory
        #
        # # Path
        # path = os.path.join(parent_dir, directory)

        # Create the directory
        # 'GeeksForGeeks' in
        # '/home / User / Documents'
        # os.mkdir(path)

        # UPLOAD_FOLDER = f"{home_directory}/{directory}"
        # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        files = request.files.getlist("file")  # other multiple files
        pic = request.files.get('photo')  # photo file
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        # str__ = base64.b64encode(pic.read())
        # print(str__)
        pic_byte = pic.read()
        # b = bytearray(pic_byte)
        # session_data = str(base64.b64encode(pic_byte).decode())
        # print(session_data)

        session_data = base64.b64encode(pic_byte).decode()

        img__ = Img(img=session_data, name=filename, mimetype=mimetype, employee=employee_element)
        db.session.add(img__)
        db.session.commit()
        # photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        for file in files:
            upload__ = documentMaster(documentName=file.filename, documentDirectory=file.read(),
                                      employee=employee_element)
            db.session.add(upload__)
            db.session.commit()
            print(file.filename)
        # Save pic in folder

        # new_doc = documentMaster(documentName=photo, documentDirectory=UPLOAD_FOLDER, employee=employee_element)
        # db.session.add(new_doc)

        return render_template("reg_suc.html", name=request.form.get('name_'), user=current_user,
                               employee=employee_element)


@app.route('/download/<upload_id>', methods=["GET", "POST"])
def download(upload_id):
    upload__ = documentMaster.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload__.documentDirectory), as_attachment=True, download_name=upload__.documentName)


@app.route('/delete_upload/<upload_id>', methods=["GET", "POST"])
def delete_upload(upload_id):
    entry_to_delete = documentMaster.query.filter_by(id=upload_id).first()
    employee_id = entry_to_delete.employeeID
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for('employee_view', employee_id=employee_id))


@app.route('/image/<int:id>')
def get_img(id):
    with app.app_context():
        img = Img.query.filter_by(id=id).first()
        if not img:
            return 'Img Not Found!', 404

        # print(img.img)
        # print(repr(img.img))
        img_ = base64.b64decode(img.img)

        return Response(img_, mimetype=img.mimetype)


@app.route('/leave', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def leave():
    form = LeaveForm()
    employees = employeeMaster.query.all()
    entries = [i.name for i in employees]

    form.name.choices = entries

    if form.validate_on_submit():
        employee = db.session.query(employeeMaster).filter_by(name=form.name.data).first()

        new_leave = leaveApplicationMaster(
            date=form.date.data,
            company=form.company.data,
            dept=form.dept.data,
            designation=form.designation.data,
            nationality=form.nationality.data,
            pass_no=form.pass_no.data,
            emp=form.emp.data,
            leave_type=form.leave_type.data,
            addr_wol=form.addr_wol.data,
            con_per=form.con_per.data,
            rel=form.rel.data,
            pol=form.pol.data,
            dot=form.dot.data,
            con_wol=form.con_wol.data,
            sub_emp=form.sub_emp.data,
            leave_f=form.leave_f.data,
            leave_t=form.leave_t.data,
            no_days=form.no_days.data,
            air_tic=form.air_tic.data,
            g1_name=form.g1_name.data,
            g1_dept=form.g1_dept.data,
            g1_id_no=form.g1_id_no.data,
            g2_name=form.g2_name.data,
            g2_dept=form.g2_dept.data,
            g2_id_no=form.g2_id_no.data,
            doj=form.doj.data,
            tla=form.tla.data,
            less_this=form.less_this.data,
            nod_app=form.nod_app.data,
            dor=form.dor.data,
            eligibility=form.eligibility.data,
            last_leave=form.last_leave.data,
            balance_leave=form.balance_leave.data,
            release_date=form.release_date.data,
            amt_appr=form.amt_appr.data,
            cheq_no=form.cheq_no.data,
            pbc=form.pbc.data,
            bank_tr=form.bank_tr.data,
            date_tr=form.date_tr.data,
            approved_by=form.approved_by.data,
            approved_by_2=form.approved_by_2.data,
            employee=employee,
            user=current_user
        )
        db.session.add(new_leave)
        db.session.commit()
        return redirect(url_for('leaveList'))
    return render_template("leave.html", form=form, employee=employees, user=current_user, entries=entries)


@app.route('/leave-list', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def leaveList():
    leave_list = leaveApplicationMaster.query.all()
    date_list = [parse(str(leave_.date)[:10]).strftime("%d/%m/%Y") for leave_ in leave_list]

    # # a = str(employee_element.joining_date)
    # # formatted_date = parse(a[:10])
    # date_str = formatted_date.strftime("%d/%m/%Y")
    return render_template('leave_list.html', data=leave_list, len=range(len(leave_list)), user=current_user,
                           date_list=date_list)


@app.route('/leave-edit/<leave_id>', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def leaveEdit(leave_id):
    form = LeaveForm()

    employees = employeeMaster.query.all()
    entries = [i.name for i in employees]

    form.name.choices = entries

    leave_element = leaveApplicationMaster.query.get(leave_id)
    leave_date = leave_element.date
    leave_f_date = leave_element.leave_f
    leave_t_date = leave_element.leave_t
    leave_dot_date = leave_element.dot
    leave_dor_date = leave_element.dor
    leave_rd_date = leave_element.release_date
    leave_tr_date = leave_element.date_tr
    leave_date_str = str(leave_date)[:10]
    leave_f_str = str(leave_f_date)[:10]
    leave_t_str = str(leave_t_date)[:10]
    leave_dot_str = str(leave_dot_date)[:10]
    leave_dor_str = str(leave_dor_date)[:10]
    leave_rd_str = str(leave_rd_date)[:10]
    leave_tr_str = str(leave_tr_date)[:10]
    date_data = [leave_date_str, leave_f_str, leave_t_str, leave_dot_str, leave_dor_str, leave_rd_str, leave_tr_str]

    if request.method == 'POST':
        employee = db.session.query(employeeMaster).filter_by(name=form.name.data).first()
        leave_element.date = form.date.data
        leave_element.company = form.company.data
        leave_element.dept = form.dept.data
        leave_element.designation = form.designation.data
        leave_element.nationality = form.nationality.data
        leave_element.pass_no = form.pass_no.data
        leave_element.emp = form.emp.data
        leave_element.leave_type = form.leave_type.data
        leave_element.addr_wol = form.addr_wol.data
        leave_element.con_per = form.con_per.data
        leave_element.rel = form.rel.data
        leave_element.pol = form.pol.data
        leave_element.dot = form.dot.data
        leave_element.con_wol = form.con_wol.data
        leave_element.sub_emp = form.sub_emp.data
        leave_element.leave_f = form.leave_f.data
        leave_element.leave_t = form.leave_t.data
        leave_element.no_days = form.no_days.data
        leave_element.air_tic = form.air_tic.data
        leave_element.g1_name = form.g1_name.data
        leave_element.g1_dept = form.g1_dept.data
        leave_element.g1_id_no = form.g1_id_no.data
        leave_element.g2_name = form.g2_name.data
        leave_element.g2_dept = form.g2_dept.data
        leave_element.g2_id_no = form.g2_id_no.data
        leave_element.doj = form.doj.data
        leave_element.tla = form.tla.data
        leave_element.less_this = form.less_this.data
        leave_element.nod_app = form.nod_app.data
        leave_element.dor = form.dor.data
        leave_element.eligibility = form.eligibility.data
        leave_element.last_leave = form.last_leave.data
        leave_element.balance_leave = form.balance_leave.data
        leave_element.release_date = form.release_date.data
        leave_element.amt_appr = form.amt_appr.data
        leave_element.cheq_no = form.cheq_no.data
        leave_element.pbc = form.pbc.data
        leave_element.bank_tr = form.bank_tr.data
        leave_element.date_tr = form.date_tr.data
        leave_element.approved_by = form.approved_by.data
        leave_element.approved_by_2 = form.approved_by_2.data
        leave_element.employee = employee
        leave_element.user = current_user
        db.session.commit()
        return redirect(url_for("leaveList"))
    return render_template('leave_edit.html', data=leave_element, form=form, date_str=date_data, user=current_user)


@app.route('/passport', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def passport():
    form = PassportForm()
    employees = employeeMaster.query.all()
    entries = [i.name for i in employees]

    form.name.choices = entries

    if form.validate_on_submit():
        employee = db.session.query(employeeMaster).filter_by(name=form.name.data).first()

        new_pp = passportApplicationMaster(
            date=form.date.data,
            emp_no=form.emp_no.data,
            pow=form.pow.data,
            days_req=form.days_req.data,
            remarks=form.remarks.data,
            g1_name=form.g1_name.data,
            g1_dept=form.g1_dept.data,
            g1_id_no=form.g1_id_no.data,
            g2_name=form.g2_name.data,
            g2_dept=form.g2_dept.data,
            g2_id_no=form.g2_id_no.data,
            checked_by=form.checked_by.data,
            appr_by_lm=form.appr_by_lm.data,
            appr_by_hr=form.appr_by_hr.data,
            dir_op=form.dir_op.data,
            pass_rec=form.pass_rec.data,
            date_pass_rec=form.date_pass_rec_e.data,
            lc_rec=form.lc_rec.data,
            date_lc_rec=form.date_lc_rec_e.data,
            pass_rec_e=form.pass_rec_e.data,
            date_pass_rec_e=form.date_pass_rec_e.data,
            lc_rec_e=form.lc_rec_e.data,
            date_lc_rec_e=form.date_lc_rec_e.data,
            employee=employee,
            user=current_user
        )
        db.session.add(new_pp)
        db.session.commit()
        return redirect(url_for('passportList'))
    return render_template("passport.html", form=form, user=current_user, entries=entries)


@app.route('/pp-list', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def passportList():
    # leave_list = passportApplicationMaster.query.all()
    leave_list = passportApplicationMaster.query.order_by(passportApplicationMaster.date.asc()).all()
    date_list = [parse(str(leave_.date)[:10]).strftime("%d/%m/%Y") for leave_ in leave_list]
    return render_template('pp_list.html', data=leave_list, len=range(len(leave_list)), user=current_user,
                           date_list=date_list)


@app.route('/pp-edit/<pp_id>', methods=["GET", "POST"])
# Mark with decorator
@admin_only
def ppEdit(pp_id):
    form = PassportForm()

    employees = employeeMaster.query.all()
    entries = [i.name for i in employees]

    form.name.choices = entries

    passport_element = passportApplicationMaster.query.get(pp_id)
    pp_date = passport_element.date
    pp_pass_date = passport_element.date_pass_rec
    pp_lc_date = passport_element.date_lc_rec
    pp_pass_e_dot_date = passport_element.date_pass_rec_e
    pp_lc_e_date = passport_element.date_lc_rec_e
    pp_date_str = str(pp_date)[:10]
    pp_pass_str = str(pp_pass_date)[:10]
    pp_lc_str = str(pp_lc_date)[:10]
    pp_pass_e_str = str(pp_pass_e_dot_date)[:10]
    pp_lc_e_str = str(pp_lc_e_date)[:10]
    date_data = [pp_date_str, pp_pass_str, pp_lc_str, pp_pass_e_str, pp_lc_e_str]
    if request.method == 'POST':
        employee = db.session.query(employeeMaster).filter_by(name=form.name.data).first()
        passport_element.date = form.date.data
        passport_element.emp_no = form.emp_no.data
        passport_element.pow = form.pow.data
        passport_element.days_req = form.days_req.data
        passport_element.remarks = form.remarks.data
        passport_element.g1_name = form.g1_name.data
        passport_element.g1_dept = form.g1_dept.data
        passport_element.g1_id_no = form.g1_id_no.data
        passport_element.g2_name = form.g2_name.data
        passport_element.g2_dept = form.g2_dept.data
        passport_element.g2_id_no = form.g2_id_no.data
        passport_element.checked_by = form.checked_by.data
        passport_element.appr_by_lm = form.appr_by_lm.data
        passport_element.appr_by_hr = form.appr_by_hr.data
        passport_element.dir_op = form.dir_op.data
        passport_element.pass_rec = form.pass_rec.data
        passport_element.date_pass_rec = form.date_pass_rec_e.data
        passport_element.lc_rec = form.lc_rec.data
        passport_element.date_lc_rec = form.date_lc_rec_e.data
        passport_element.pass_rec_e = form.pass_rec_e.data
        passport_element.date_pass_rec_e = form.date_pass_rec_e.data
        passport_element.lc_rec_e = form.lc_rec_e.data
        passport_element.date_lc_rec_e = form.date_lc_rec_e.data
        passport_element.employee = employee
        passport_element.user = current_user
        db.session.commit()
        return redirect(url_for("passportList"))
    return render_template('pp_edit.html', data=passport_element, form=form, date_str=date_data, user=current_user)


@app.route("/ts", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def timesheet():
    employee_list = employeeMaster.query.all()
    employee_name = [i.name for i in employee_list]
    employees = employeeMaster.query.all()
    hotels = hotelMaster.query.all()
    data_ = [employees, hotels]
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        a = jsonify(data).json

        hotel_element = db.session.query(hotelMaster).filter_by(name=a['hotel'][0]).first()
        new_timesheet = timesheetMaster(date=a['date'][0], sheet_no=a['sheetNo'][0], user=current_user,
                                        hotel=hotel_element)

        # Create logic to check whether ts is added properly - Create a page for success and not success
        # Create logic for checking duplicates
        # print(type(a['date'][0]))
        db.session.add(new_timesheet)
        db.session.commit()

        for i in range(len(a['name'])):
            if a['name'][i] != '':
                employee_element = db.session.query(employeeMaster).filter_by(name=a['name'][i]).first()
                ts_element = new_timesheet
                new_entry = timesheetEntryMaster(timeIn1=getTimeInt(a['timeIn1'][i]),
                                                 timeIn2=getTimeInt(a['timeIn2'][i]),
                                                 timeOut1=getTimeInt(a['timeOut1'][i]),
                                                 timeOut2=getTimeInt(a['timeOut2'][i]),
                                                 employee=employee_element, timesheet=ts_element)
                db.session.add(new_entry)
                db.session.commit()

        return render_template("ts_success_db.html", data=a, len=range(len(a['name'])), user=current_user)

    today = date.today()
    return render_template("timesheet.html", array=employee_name, data=data_, user=current_user, date_=today)


@app.route("/roster", methods=["GET", "POST"])
# # Mark with decorator
@admin_only
def roster():
    all_roster = rosterMaster.query.order_by(rosterMaster.date.asc()).all()
    dates_list = []
    for i in all_roster:
        date_el = i.date
        dates_list.append(date_el)

    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        a = jsonify(data).json

        got_date = a['date'][0]
        got_date_year = got_date[6:10]
        got_date_day = got_date[0:2]
        got_date_month = got_date[3:5]
        format_date = f"{got_date_year}-{got_date_month}-{got_date_day}"
        new_roster = rosterMaster(date=format_date, user=current_user)
        db.session.add(new_roster)
        db.session.commit()

        # Create logic for checking duplicates
        # create a mechanism to tell the user

        roster_element = new_roster

        for i in range(len(a['hotel'])):
            if a['hotel'][i] != '':  # check if there's no entry
                hotel_element = db.session.query(hotelMaster).filter_by(name=a['hotel'][i]).first()
                nameStr = "name" + str(i + 1)
                timeInStr1 = "timeInA" + str(i + 1)
                timeOutStr1 = "timeOutA" + str(i + 1)
                timeInStr2 = "timeInB" + str(i + 1)
                timeOutStr2 = "timeOutB" + str(i + 1)
                pickupA = "pickUpA" + str(i + 1)
                pickupB = "pickUpB" + str(i + 1)
                remarks = "remarks" + str(i + 1)
                absent = "absent" + str(i + 1)

                for j in range(len(a[nameStr])):
                    if a[nameStr][j] != '':
                        employee_element = db.session.query(employeeMaster).filter_by(name=a[nameStr][j]).first()
                        new_entry = rosterEntryMaster(timeIn1=getTimeInt(a[timeInStr1][j]),
                                                      timeOut1=getTimeInt(a[timeOutStr1][j]),
                                                      timeIn2=getTimeInt(a[timeInStr2][j]),
                                                      timeOut2=getTimeInt(a[timeOutStr2][j]),
                                                      pickUp=getTimeInt(a[pickupA][j]),
                                                      pickUp2=getTimeInt(a[pickupB][j]),
                                                      remark=a[remarks][j], absent=a[absent][j],
                                                      employee=employee_element, roster=roster_element,
                                                      hotel=hotel_element)
                        # Add pickup 2 TODO
                        db.session.add(new_entry)
                        db.session.commit()

        # return render_template("roster_complete.html", date=today, data=value)
        # print(a)
        return redirect(url_for("roster_single", roster_id=new_roster.id))
    # form = RosterExtend()
    # if form.validate_on_submit():
    #     data_form = form.data
    #     value = sortRosterData(data_form)
    #
    #     # create logic to add values in db - rosterMaster, rosterEntryMaster
    #     # Get hotel id


@app.route("/roster_date", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def roster_date():
    all_roster = rosterMaster.query.all()
    dates_list = []
    employees = employeeMaster.query.all()
    # for i in employees:
    #         # print(i.name)
    #     # print('no employee')
    hotels = hotelMaster.query.all()
    # for i in hotels:
    #         # print(i.name)
    data_ = [employees, hotels]
    for i in all_roster:
        date_el = i.date
        dates_list.append(date_el)

    if request.method == "POST":
        date_roster = request.form.get('date')
        rosters = rosterMaster.query.all()
        dates = []
        for roster in rosters:
            i = roster.date
            dates.append(i)
        if date_roster in dates:
            return render_template("roster_date.html", array=dates_list,
                                   msg="Roster with the same date exists. Choose new one.", user=current_user)
        elif date_roster:
            return render_template('roster_new_picklist.html', date_roster=date_roster, data=data_, user=current_user)
        else:
            return render_template("roster_date.html", array=dates_list, msg="Choose a date to continue")

    return render_template("roster_date.html", array=dates_list, msg="")


@app.route("/download_roster/<roster_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def download_roster(roster_id):
    roster_entries = db.session.query(rosterEntryMaster).filter_by(rosterID=roster_id).all()
    roster_element = rosterMaster.query.get(roster_id)
    roster_date_ = roster_element.date
    roster_day = datetime.datetime.strptime(roster_date_, "%Y-%m-%d").strftime('%A')
    roster_full_date = datetime.datetime.strptime(roster_date_, '%Y-%m-%d').strftime('%B %d, %Y')
    employee_list = []
    hotel_list = []
    time_lists = []
    roster_color = {'Off': '#16FF00', 'Absent': '#FF0303', 'Sick': '#FFED00', 'Vacation': '#82CD47',
                    'Public Holiday': '#146C94', 'Office': '#83764F'}
    for i in roster_entries:
        employee = i.employee
        hotel = i.hotel
        hotel_list.append(hotel.name)
        employee_list.append(employee.name)
        ti1 = getTimeStr(i.timeIn1)
        ti2 = getTimeStr(i.timeIn2)
        to1 = getTimeStr(i.timeOut1)
        to2 = getTimeStr(i.timeOut2)
        pu = getTimeStr(i.pickUp)
        pu2 = getTimeStr(i.pickUp2)
        # TODO Add pickup 2
        time_dict = {'timeIn1': ti1, 'timeIn2': ti2, 'timeOut1': to1, 'timeOut2': to2, 'pickUp': pu, 'pickUp2': pu2}
        time_lists.append(time_dict)

    date_data = [roster_date_, roster_day, roster_full_date]
    create_roster(employee_list, hotel_list, time_lists, roster_entries, date_data)
    path = "specsheet.xlsx"
    current_datetime = datetime.datetime.today().date().timetuple()

    str_current_datetime = str(current_datetime)
    a__ = datetime.datetime.now()
    a_ = a__.strftime("%a, %d %b %Y %H-%M-%S")
    spec_sheet_name = f'Roster_{roster_date_}_.xlsx'

    return send_file(path, as_attachment=True, download_name=spec_sheet_name)


# download_roster(3)


# Hotel report
@app.route("/add_hotel", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def add_hotel():
    if request.method == "POST":
        new_hotel = hotelMaster(name=request.form.get('name'), address=request.form.get('address'),
                                interval=request.form.get('interval'), rate=request.form.get('rate'))
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for("hotel_report"))
    return render_template("add_hotel.html", user=current_user)


@app.route("/del_hotel/<hotel_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_hotel(hotel_id):
    entry_to_delete = hotelMaster.query.get(hotel_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("hotel_report"))


@app.route("/edit_hotel/<hotel_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def edit_hotel(hotel_id):
    hotel_element = hotelMaster.query.get(hotel_id)
    if request.method == 'POST':
        hotel_element.name = request.form.get('name')
        hotel_element.address = request.form.get('address')
        hotel_element.interval = request.form.get('interval')
        hotel_element.rate = request.form.get('rate')
        db.session.commit()
        return redirect(url_for('hotel_report'))
    return render_template('hotel_edit.html', hotel=hotel_element, user=current_user)


@app.route("/hotel_report", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def hotel_report():
    hotel_list = hotelMaster.query.all()
    return render_template("hotel_report.html", ts=hotel_list, len=range(len(hotel_list)), user=current_user)


# Department Report
@app.route("/add_department", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def add_department():
    if request.method == "POST":
        new_d = request.form.get('name')
        all_depts = departmentMaster.query.all()
        dept_names = [dep.name for dep in all_depts]
        print(new_d, dept_names)
        if request.form.get('name') in dept_names:
            return render_template("add_dept.html", user=current_user,
                                   msg=f'Department: "{new_d}"" already exists, try adding a new one.')
        else:
            new_department = departmentMaster(name=request.form.get('name'))
            db.session.add(new_department)
            db.session.commit()
        return redirect(url_for("department_report"))
    return render_template("add_dept.html", user=current_user, msg='')


@app.route("/del_dept/<dept_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_dept(dept_id):
    entry_to_delete = departmentMaster.query.get(dept_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("department_report"))


@app.route("/edit_dept/<dept_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def edit_dept(dept_id):
    dept_element = departmentMaster.query.get(dept_id)
    if request.method == 'POST':
        dept_element.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for("department_report"))
    return render_template('dept_edit.html', dept=dept_element, user=current_user)


@app.route("/empl_dept/<dept_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def empl_dept(dept_id):
    dept_element = departmentMaster.query.get(dept_id)
    employee_list = db.session.query(employeeMaster).filter_by(department=dept_element).all()
    date_test = '2022-09-01'
    roster_element = db.session.query(rosterMaster).filter_by(date=date_test).first()
    if roster_element:
        roster_entries = db.session.query(rosterEntryMaster).filter_by(rosterID=roster_element.id).all()
        off_days = 0
        for i in roster_entries:
            if i.absent != 'none':
                off_days += 1
    else:
        off_days = 0
        roster_entries = []

    data = {'Task': 'Hours per Day', 'Absent': off_days, 'Present': len(roster_entries)}
    department = []
    for ts in employee_list:
        department_element = departmentMaster.query.get(ts.departmentId)
        if department_element:
            department_name = department_element.name
        else:
            department_name = "None"
        department.append(department_name)
    return render_template("employee_report.html", ts=employee_list, len=range(len(department)), departments=department,
                           data=data, user=current_user)


@app.route("/department_report", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def department_report():
    hotel_list = departmentMaster.query.all()
    return render_template("department_report.html", ts=hotel_list, len=range(len(hotel_list)), user=current_user)


@app.route("/reports", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def reports():
    return render_template("reports.html", user=current_user)


@app.route("/archives", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def archives():
    hotels = hotelMaster.query.all()
    form = Archives()
    employee_list = employeeMaster.query.all()
    if form.validate_on_submit():
        data1 = form.date1.data
        data2 = form.date2.data
        date_list = date_range_list(data1, data2)
        ts_list = []
        for i in date_list:
            ts_element = db.session.query(timesheetMaster).filter_by(date=i).first()
            if not ts_element:
                return render_template("archives.html", form=form, msg="Choose correct dates", user=current_user)
            else:
                ts_list.append(ts_element)
        print(len(ts_list))
        master_ts_list = []
        for i in range(len(employee_list)):
            ms_dict = {"name": employee_list[i].name, "hours": [], 'hotel': []}
            for j in range(len(ts_list)):
                ts_entry_element = db.session.query(timesheetEntryMaster).filter_by(employeeID=employee_list[i].id,
                                                                                    timesheetID=ts_list[j].id).first()
                if not ts_entry_element:
                    roster_element = db.session.query(rosterMaster).filter_by(date=ts_list[j].date).first()
                    if not roster_element:
                        hours = "N/A"

                        hotel = hotels[0]
                    else:
                        rs_entry_element = db.session.query(rosterEntryMaster).filter_by(employeeID=employee_list[i].id,
                                                                                         rosterID=roster_element.id).first()
                        if (not rs_entry_element) or (rs_entry_element.absent == "none"):
                            hours = "N/A"
                            hotel = hotels[0]
                        else:
                            hours = rs_entry_element.absent
                        try:
                            hotel = rs_entry_element.hotel
                        except:
                            hotel = hotels[0]
                        # hotel = "abc"


                else:
                    hours_ = ts_entry_element.timeOut1 - ts_entry_element.timeIn1 + ts_entry_element.timeOut2 - ts_entry_element.timeIn2
                    hours = total_time_hrs(hours_)
                    hotel = ts_element.hotel

                    # print(ts_entry_element.timeOut1)

                ms_dict['hours'].append(hours)
                ms_dict['hotel'].append(hotel)
            master_ts_list.append(ms_dict)
            # print(master_ts_list)

        hours_sum = []
        for i in master_ts_list:
            sum_hours = 0
            for j in i['hours']:
                # print(type(j))
                if type(j) != str:
                    sum_hours = sum_hours + j

            hours_sum.append(sum_hours)
        # print(hours_sum)

        analytic_data = []
        for i in range(len(hours_sum)):
            total_hours = hours_sum[i]
            extra_hours = hours_sum[i] - 260
            total_extra = 5 * extra_hours
            if master_ts_list[i]['hotel'][0].interval == 'monthly':
                productivity = master_ts_list[i]['hotel'][0].rate
            else:
                productivity = hours_sum[i] * master_ts_list[i]['hotel'][0].rate

            analytic_data_dict = {'productivity': productivity, 'total_hours': total_hours, 'extra_hours': extra_hours,
                                  'total_extra': total_extra}
            analytic_data.append(analytic_data_dict)

        return render_template("masterTs.html", data=master_ts_list, dates=date_list, len=range(len(date_list)),
                               user=current_user, new_data=analytic_data)
    return render_template("archives.html", form=form, msg="", user=current_user)


@app.route("/roster_archive", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def roster_archive():
    rosters_list = rosterMaster.query.order_by(rosterMaster.date.asc()).all()
    # date_list = [datetime.datetime.strptime(entry.date, '%d%m%Y')'%Y-%m-%d' for entry in rosters_list]
    date_list = [parse(entry.date).strftime("%d/%m/%Y") for entry in rosters_list]
    return render_template("roster_archive_list.html", rosters=rosters_list, len=range(len(rosters_list)),
                           user=current_user, date_list=date_list)


@app.route("/del_roster/<roster_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_roster(roster_id):
    entry_to_delete = rosterMaster.query.get(roster_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("roster_archive"))


@app.route("/roster_single/<roster_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def roster_single(roster_id):
    roster_entries = db.session.query(rosterEntryMaster).filter_by(rosterID=roster_id).all()
    roster_element = rosterMaster.query.get(roster_id)
    roster_date = roster_element.date
    try:
        roster_day = datetime.datetime.strptime(roster_date, "%Y-%m-%d").strftime('%A')
        roster_full_date = datetime.datetime.strptime(roster_date, '%Y-%m-%d').strftime('%B %d, %Y')
    except ValueError:
        roster_day = datetime.datetime.strptime(roster_date, "%Y-%d-%m").strftime('%A')
        roster_full_date = datetime.datetime.strptime(roster_date, '%Y-%d-%m').strftime('%B %d, %Y')

    employee_list = []
    hotel_list = []
    time_lists = []
    roster_color = {'Off': '#16FF00', 'Absent': '#FF0303', 'Sick': '#FFED00', 'Vacation': '#82CD47',
                    'Public Holiday': '#146C94', 'Office': '#83764F'}
    for i in roster_entries:
        employee = i.employee
        hotel = i.hotel
        hotel_list.append(hotel.name)
        try:
            employee_list.append(employee.name)
        except AttributeError:
            employee_list.append('Undefined')
        ti1 = getTimeStr(i.timeIn1)
        ti2 = getTimeStr(i.timeIn2)
        to1 = getTimeStr(i.timeOut1)
        to2 = getTimeStr(i.timeOut2)
        pu = getTimeStr(i.pickUp)
        pu2 = getTimeStr(i.pickUp2)
        # TODO Add pickup 2
        time_dict = {'timeIn1': ti1, 'timeIn2': ti2, 'timeOut1': to1, 'timeOut2': to2, 'pickUp': pu, 'pickUp2': pu2}
        time_lists.append(time_dict)
    return render_template("roster_entries.html", entries=roster_entries, employees=employee_list, hotels=hotel_list,
                           len=range(len(roster_entries)), date=roster_full_date, day=roster_day, time_data=time_lists,
                           user=current_user, color=roster_color, roster_id=roster_id)


@app.route("/roster_single_edit/<roster_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def roster_single_edit(roster_id):
    absence_reasons = ['none', 'Off', 'Absent', 'Sick', 'Vacation', 'Office']
    roster_entries = db.session.query(rosterEntryMaster).filter_by(rosterID=roster_id).all()
    employee_list = []
    hotel_list = []
    employees = employeeMaster.query.all()
    hotels = hotelMaster.query.all()
    data_ = [employees, hotels]
    roster_element = rosterMaster.query.get(roster_id)
    roster_date = roster_element.date
    try:
        roster_day = datetime.datetime.strptime(roster_date, "%Y-%d-%m").strftime('%A')
        roster_full_date = datetime.datetime.strptime(roster_date, '%Y-%d-%m').strftime('%B %d, %Y')
    except ValueError:
        roster_day = datetime.datetime.strptime(roster_date, "%Y-%m-%d").strftime('%A')
        roster_full_date = datetime.datetime.strptime(roster_date, '%Y-%m-%d').strftime('%B %d, %Y')
    roster_color = {'Off': '#16FF00', 'Absent': '#FF0303', 'Sick': '#FFED00', 'Vacation': '#82CD47',
                    'Public Holiday': '#146C94', 'Office': '#83764F'}
    time_lists = []
    for i in roster_entries:
        roster_dict = {''}
        employee = i.employee
        hotel = i.hotel
        hotel_list.append(hotel.name)
        try:
            employee_list.append(employee.name)
        except AttributeError:
            employee_list.append('Undefined')
        ti1 = getTimeStr(i.timeIn1)
        ti2 = getTimeStr(i.timeIn2)
        to1 = getTimeStr(i.timeOut1)
        to2 = getTimeStr(i.timeOut2)
        pu = getTimeStr(i.pickUp)
        pu2 = getTimeStr(i.pickUp2)
        # TODO Add pickup 2
        time_dict = {'timeIn1': ti1, 'timeIn2': ti2, 'timeOut1': to1, 'timeOut2': to2, 'pickUp': pu, 'pickUp2': pu2}
        time_lists.append(time_dict)
    return render_template("roster_entries_edit.html", entries=roster_entries, employees=employee_list,
                           hotels=hotel_list,
                           len=range(len(roster_entries)), date=roster_full_date, day=roster_day, data=data_,
                           time_data=time_lists, user=current_user, color=roster_color, ab=absence_reasons)


@app.route("/add_roster_element/<roster_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def add_roster_element(roster_id):
    if request.method == 'POST':
        hotel_element = db.session.query(hotelMaster).filter_by(name=request.form.get('hotel')).first()
        employee_element = db.session.query(employeeMaster).filter_by(name=request.form.get('name')).first()
        roster_element = db.session.query(rosterMaster).filter_by(id=roster_id).first()
        roster_entries = db.session.query(rosterEntryMaster).filter_by(roster=roster_element).all()
        # Do not add to db if entry with user exists
        if employee_element not in [roster_.employee for roster_ in roster_entries]:  # list comprehension
            new_entry = rosterEntryMaster(timeIn1=getTimeInt(request.form.get('timeIn1')),
                                          timeOut1=getTimeInt(request.form.get('timeOut1')),
                                          timeIn2=getTimeInt(request.form.get('timeIn2')),
                                          timeOut2=getTimeInt(request.form.get('timeOut2')),
                                          pickUp=getTimeInt(request.form.get('pickUp')),
                                          pickUp2=getTimeInt(request.form.get('pickUp2')),
                                          remark=request.form.get('remarks'), absent=request.form.get('absent'),
                                          employee=employee_element, roster=roster_element,
                                          hotel=hotel_element)
            # TODO Add pick up 2
            db.session.add(new_entry)
            db.session.commit()

        return redirect(url_for("roster_single_edit", roster_id=roster_id))


@app.route("/update_roster_element/<roster_entry_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def update_roster_element(roster_entry_id):
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        a = jsonify(data).json
        roster_entry_element = rosterEntryMaster.query.get(int(roster_entry_id))
        roster_entry_element.timeIn1 = getTimeInt(a['timeIn1'][0])
        roster_entry_element.timeOut1 = getTimeInt(a['timeOut1'][0])
        roster_entry_element.timeIn2 = getTimeInt(a['timeIn2'][0])
        roster_entry_element.timeOut2 = getTimeInt(a['timeOut2'][0])
        roster_entry_element.pickUp = getTimeInt(a['pickUp'][0])
        roster_entry_element.pickUp2 = getTimeInt(a['pickUp2'][0])
        roster_entry_element.remark = a['remarks'][0]
        roster_entry_element.absent = a['absent'][0]
        db.session.commit()

        return redirect(url_for("roster_single_edit", roster_id=roster_entry_element.rosterID))


@app.route("/del_roster_element/<entry_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_roster_element(entry_id):
    entry_to_delete = rosterEntryMaster.query.get(entry_id)
    roster_id = entry_to_delete.rosterID
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("roster_single_edit", roster_id=roster_id))


# timesheet edit/view

@app.route("/timesheet_archive", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def timesheet_archive():
    # timesheet_list = timesheetMaster.query.all()
    timesheet_list = timesheetMaster.query.order_by(timesheetMaster.date.asc()).all()
    hotels = []
    date_list = [parse(entry.date).strftime("%d/%m/%Y") for entry in timesheet_list]

    for ts in timesheet_list:
        hotel_element = hotelMaster.query.get(ts.hotelID)

        hotel_name = hotel_element.name
        hotels.append(hotel_name)

    return render_template("timesheet_archive_list.html", user=current_user, ts=timesheet_list, len=range(len(hotels)),
                           hotels=hotels, date_list=date_list)


@app.route("/del_timesheet/<ts_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_timesheet(ts_id):
    entry_to_delete = timesheetMaster.query.get(ts_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("timesheet_archive"))


@app.route("/timesheet_single/<timesheet_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def timesheet_single(timesheet_id):
    timesheet_entries = db.session.query(timesheetEntryMaster).filter_by(timesheetID=timesheet_id).all()
    ts_element = timesheetMaster.query.get(timesheet_id)
    sheet_no = ts_element.sheet_no
    date__ = parse(ts_element.date).strftime("%d/%m/%Y")
    hotel_element = hotelMaster.query.get(ts_element.hotelID)
    hotel_name = hotel_element.name
    employee_list = []
    time_lists = []
    for i in timesheet_entries:
        employee = db.session.query(employeeMaster).filter_by(id=i.employeeID).first()
        employee_list.append(employee.name)
        ti1 = getTimeStr(i.timeIn1)
        ti2 = getTimeStr(i.timeIn2)
        to1 = getTimeStr(i.timeOut1)
        to2 = getTimeStr(i.timeOut2)
        time_dict = {'timeIn1': ti1, 'timeIn2': ti2, 'timeOut1': to1, 'timeOut2': to2}
        time_lists.append(time_dict)
    return render_template("timesheet_entries.html", user=current_user, entries=timesheet_entries,
                           employees=employee_list,
                           hotel_name=hotel_name,
                           len=range(len(timesheet_entries)), date__=date__, sheet=sheet_no, time_data=time_lists,
                           ts_id=timesheet_id)


@app.route("/timesheet_single_edit/<timesheet_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def timesheet_single_edit(timesheet_id):
    timesheet_entries = db.session.query(timesheetEntryMaster).filter_by(timesheetID=timesheet_id).all()
    ts_element = timesheetMaster.query.get(timesheet_id)
    sheet_no = ts_element.sheet_no
    date__ = parse(ts_element.date).strftime("%d/%m/%Y")
    hotel_element = hotelMaster.query.get(ts_element.hotelID)
    hotel_name = hotel_element.name
    employee_list = []
    employees = employeeMaster.query.all()
    hotels = hotelMaster.query.all()
    data_ = [employees, hotels]
    time_lists = []
    for i in timesheet_entries:
        employee = db.session.query(employeeMaster).filter_by(id=i.employeeID).first()
        employee_list.append(employee.name)
        employee = db.session.query(employeeMaster).filter_by(id=i.employeeID).first()
        employee_list.append(employee.name)
        ti1 = getTimeStr(i.timeIn1)
        ti2 = getTimeStr(i.timeIn2)
        to1 = getTimeStr(i.timeOut1)
        to2 = getTimeStr(i.timeOut2)
        time_dict = {'timeIn1': ti1, 'timeIn2': ti2, 'timeOut1': to1, 'timeOut2': to2}
        time_lists.append(time_dict)
    return render_template("timesheet_entries_edit.html", entries=timesheet_entries, employees=employee_list,
                           hotel_name=hotel_name,
                           len=range(len(timesheet_entries)), date__=date__, sheet=sheet_no, data=data_,
                           time_data=time_lists, user=current_user)


@app.route("/add_ts_element/<ts_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def add_ts_element(ts_id):
    if request.method == 'POST':
        ts_element = timesheetMaster.query.get(ts_id)
        hotel_element = hotelMaster.query.get(ts_element.hotelID)
        employee_element = db.session.query(employeeMaster).filter_by(name=request.form.get('name')).first()
        new_entry = timesheetEntryMaster(timeIn1=getTimeInt(request.form.get('timeIn1')),
                                         timeOut1=getTimeInt(request.form.get('timeOut1')),
                                         timeIn2=getTimeInt(request.form.get('timeIn2')),
                                         timeOut2=getTimeInt(request.form.get('timeOut2')),
                                         employee=employee_element, timesheet=ts_element)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("timesheet_single_edit", timesheet_id=ts_id))


@app.route("/del_ts_element/<entry_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def del_ts_element(entry_id):
    entry_to_delete = timesheetEntryMaster.query.get(entry_id)
    ts_id = entry_to_delete.timesheetID
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("timesheet_single_edit", timesheet_id=ts_id))


# Delete

# reports

@app.route("/employee_report", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def employee_report():
    employee_list = employeeMaster.query.all()
    date_test = '2022-09-01'
    roster_element = db.session.query(rosterMaster).filter_by(date=date_test).first()
    if roster_element:
        roster_entries = db.session.query(rosterEntryMaster).filter_by(rosterID=roster_element.id).all()
        off_days = 0
        for i in roster_entries:
            if i.absent != 'none':
                off_days += 1
    else:
        off_days = 0
        roster_entries = []

    data = {'Task': 'Hours per Day', 'Absent': off_days, 'Present': len(roster_entries)}
    department = []
    for ts in employee_list:
        department_element = departmentMaster.query.get(ts.departmentId)
        if department_element:
            department_name = department_element.name
        else:
            department_name = "None"
        department.append(department_name)
    return render_template("employee_report.html", ts=employee_list, len=range(len(department)), departments=department,
                           data=data, user=current_user)


@app.route("/employee_edit/<employee_id>", methods=["GET", "POST"])
# Mark with decoratorr
@admin_only
def employee_edit(employee_id):
    form = RegistrationForm()
    department_ = departmentMaster.query.all()
    department_name = [i.name for i in department_]
    employee_element = employeeMaster.query.get(employee_id)
    # print(employee_element.joining_date)
    a = str(employee_element.joining_date)
    date_str = a[:10]
    # print(date_str)
    nationality_string = employee_element.nationality
    nationality_ = nationality_string.split('+')[0]
    passport_ = nationality_string.split('+')[1]

    mobile_details_string = employee_element.emUaeAddr
    em_uae_addr, mobile_p, mobile_h, e_uae_mob, e_co_mob = mobile_details_string.split('+')[0], \
                                                           mobile_details_string.split('+')[1], \
                                                           mobile_details_string.split('+')[2], \
                                                           mobile_details_string.split('+')[3], \
                                                           mobile_details_string.split('+')[4]
    mob_det = [em_uae_addr, mobile_p, mobile_h, e_uae_mob, e_co_mob]
    if request.method == "POST":
        nationality_passportNo = f"{request.form.get('nationality')}+{request.form.get('passport_no')}"
        mobile_string = f"{request.form.get('e_uae_addr')}+{request.form.get('mobile_p')}+{request.form.get('mobile_h')}+{request.form.get('e_uae_mob')}+{request.form.get('e_co_mob')}"
        if request.form.get('own_car') == 'y':
            own_car = True
        else:
            own_car = False

        if request.form.get('car_rent') == 'y':
            car_rent = True
        else:
            car_rent = False
        a_date = datetime.datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d').date()
        department_ = request.form.get("department_e")
        department = db.session.query(departmentMaster).filter_by(name=department_).first()
        employee_element.name = request.form.get("name")
        employee_element.addressUae = request.form.get('address_uae')
        employee_element.poBox = request.form.get('po_box')
        employee_element.mobilePersonal = 1
        employee_element.mobileHome = 1
        employee_element.personalMail = request.form.get('personal_mail')
        employee_element.addressHome = request.form.get('address_home')
        employee_element.passportNumber = 0
        employee_element.nationality = nationality_passportNo
        employee_element.ownCar = own_car
        employee_element.carRent = car_rent
        employee_element.emUaeName = request.form.get('e_uae_name')
        employee_element.emUaeRel = request.form.get('e_uae_rel')
        employee_element.emUaeAddr = mobile_string
        employee_element.emUaeMobileNumber = 1
        employee_element.emUaeHomeNumber = request.form.get('e_uae_hom')
        employee_element.originCountry = request.form.get('origin_country')
        employee_element.emCoName = request.form.get('e_co_name')
        employee_element.emCoRel = request.form.get('e_co_rel')
        employee_element.emCoAddr = request.form.get('e_co_addr')
        employee_element.emCoMobileNumber = 1
        employee_element.emCoHomeNumber = request.form.get('e_co_hom')
        employee_element.employeeID = request.form.get('employee_id')
        employee_element.joining_date = a_date
        employee_element.company_laptop = request.form.get('company_laptop')
        employee_element.company_mobile = request.form.get('company_mobile')
        employee_element.user = current_user
        employee_element.department = department
        db.session.commit()
        return redirect(url_for("upload_edit", employee_id=employee_element.id))
    return render_template("employee_edit.html", data=employee_element, form=form, date_str=date_str,
                           nationality=nationality_, passport=passport_, mob_det=mob_det, user=current_user,
                           depts=department_name)


@app.route("/upload_edit/<employee_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def upload_edit(employee_id):
    emp_element = employeeMaster.query.get(employee_id)
    doc_s = documentMaster.query.filter_by(employee=emp_element).all()
    img_s = Img.query.filter_by(employee=emp_element).all()
    if request.method == 'POST':
        directory = request.form.get('name')
        employee_element = db.session.query(employeeMaster).filter_by(id=directory).first()

        files = request.files.getlist("file")  # other multiple files
        pic = request.files.get('photo')  # photo file
        if pic:
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            pic_byte = pic.read()

            session_data = base64.b64encode(pic_byte).decode()

            img__ = Img(img=session_data, name=filename, mimetype=mimetype, employee=employee_element)
            db.session.add(img__)
            db.session.commit()
        for file in files:
            upload__ = documentMaster(documentName=file.filename, documentDirectory=file.read(),
                                      employee=employee_element)
            db.session.add(upload__)
            db.session.commit()
            print(file.filename)
        return redirect(url_for('employee_view', employee_id=employee_element.id))
    return render_template("upload_edit.html", name=emp_element.name, user=current_user, emp_id=emp_element.id,
                           docs=doc_s, img_=img_s)


@app.route("/employee_view/<employee_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def employee_view(employee_id):
    form = ActionItem()
    employee_element = employeeMaster.query.get(employee_id)
    detail_element = db.session.query(employeeDetails).filter_by(employee=employee_element).first()
    a = str(employee_element.joining_date)
    formatted_date = parse(a[:10])
    date_str = formatted_date.strftime("%d/%m/%Y")
    actionItems = db.session.query(actionItemMaster).filter_by(employeeID=employee_id).all()
    doc_element = db.session.query(documentMaster).filter_by(employeeID=employee_id).first()
    img_element__ = db.session.query(Img).filter_by(employee=employee_element).all()
    doc_s = documentMaster.query.filter_by(employee=employee_element).all()

    if len(img_element__) > 0:
        img_element = img_element__[-1]
        print("img len is greateer than 0")
        if img_element:
            print('image elemement is there')
            img_id = int(img_element.id)
            # img_url = doc_element.documentName
            img_url = f"https://dfxhr.herokuapp.com/image/{img_id}"
            # http://127.0.0.1:5000
            # https://dfshr.herokuapp.com
        else:
            print(f"img element is not there")
            img_url = 'https://www.kindpng.com/picc/m/252-2524695_dummy-profile-image-jpg-hd-png-download.png'
    # get total hours worked
    else:
        print('len of image element is 0')
        img_url = 'https://www.kindpng.com/picc/m/252-2524695_dummy-profile-image-jpg-hd-png-download.png'
    # get total hours worked
    print(img_url)
    ts_employee = db.session.query(timesheetEntryMaster).filter_by(employeeID=employee_id).all()
    totalHours = 0
    for i in ts_employee:
        b = (i.timeOut1 - i.timeIn1) + (i.timeOut2 - i.timeIn2)
        totalHours += b

    # get profile completion %
    list_empl = [employee_element.name,
                 employee_element.addressUae,
                 employee_element.poBox,
                 employee_element.mobilePersonal,
                 employee_element.mobileHome,
                 employee_element.personalMail,
                 employee_element.addressHome,
                 employee_element.passportNumber,
                 employee_element.nationality,
                 employee_element.emUaeName,
                 employee_element.emUaeRel,
                 employee_element.emUaeAddr,
                 employee_element.emUaeMobileNumber,
                 employee_element.emUaeHomeNumber,
                 employee_element.originCountry,
                 employee_element.emCoName,
                 employee_element.emCoRel,
                 employee_element.emCoAddr,
                 employee_element.emCoMobileNumber,
                 employee_element.emCoHomeNumber,
                 employee_element.employeeID,
                 employee_element.joining_date,
                 employee_element.company_laptop,
                 employee_element.company_mobile]
    profileCompletion = 0
    for i in list_empl:
        if not i:
            profileCompletion += 1

    profilePercent = ((len(list_empl) - profileCompletion) / len(list_empl)) * 100

    # Get total leaves
    leave_element = db.session.query(leaveApplicationMaster).filter_by(employee=employee_element).all()
    t_leaves = 0
    for le in leave_element:
        if le:
            leaves = le.leave_t - le.leave_f
            leaves_taken = int(leaves.days)
            # print(f"total leaves: {leaves}, {leaves_taken}")
        else:
            leaves_taken = 0

        t_leaves += leaves_taken
    if detail_element.total_leaves and detail_element.total_leaves != 'None':
        try:
            total_leaves_pending = int(detail_element.total_leaves) - t_leaves
        except ValueError:
            total_leaves_pending = 0
    else:
        total_leaves_pending = 0
    if form.validate_on_submit():
        newActionItem = actionItemMaster(actionText=form.content.data, employee=employee_element)
        db.session.add(newActionItem)
        db.session.commit()
        return redirect(url_for("employee_view", employee_id=employee_id))

    return render_template("employee_view.html", employee=employee_element, form=form, date_str=date_str,
                           workedHours=totalHours, profile=round(profilePercent, 0), items=actionItems, img_url=img_url,
                           len=range(len(actionItems)), user=current_user, details=detail_element,
                           p_l=total_leaves_pending, docs=doc_s)


@app.route("/employee_details/<employee_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def employee_details(employee_id):
    employee_element = employeeMaster.query.get(employee_id)
    detail_element = db.session.query(employeeDetails).filter_by(employee=employee_element).first()
    a = str(employee_element.joining_date)
    date_str = a[:10]
    actionItems = db.session.query(actionItemMaster).filter_by(employeeID=employee_id).all()
    doc_element = db.session.query(documentMaster).filter_by(employeeID=employee_id).first()
    img_element__ = db.session.query(Img).filter_by(employeeID=employee_id).all()
    if len(img_element__) > 0:
        img_element = img_element__[-1]
        if img_element:
            img_id = int(img_element.id)
            # img_url = doc_element.documentName
            img_url = f"https://dfxhr.herokuapp.com/image/{img_id}"
        else:
            img_url = 'https://www.kindpng.com/picc/m/252-2524695_dummy-profile-image-jpg-hd-png-download.png'
    # get total hours worked
    else:
        img_url = 'https://www.kindpng.com/picc/m/252-2524695_dummy-profile-image-jpg-hd-png-download.png'
    # get total hours worked
    print(img_url)
    ts_employee = db.session.query(timesheetEntryMaster).filter_by(employeeID=employee_id).all()
    totalHours = 0
    for i in ts_employee:
        b = (i.timeOut1 - i.timeIn1) + (i.timeOut2 - i.timeIn2)
        totalHours += b

    # get profile completion %
    list_empl = [employee_element.name,
                 employee_element.addressUae,
                 employee_element.poBox,
                 employee_element.mobilePersonal,
                 employee_element.mobileHome,
                 employee_element.personalMail,
                 employee_element.addressHome,
                 employee_element.passportNumber,
                 employee_element.nationality,
                 employee_element.emUaeName,
                 employee_element.emUaeRel,
                 employee_element.emUaeAddr,
                 employee_element.emUaeMobileNumber,
                 employee_element.emUaeHomeNumber,
                 employee_element.originCountry,
                 employee_element.emCoName,
                 employee_element.emCoRel,
                 employee_element.emCoAddr,
                 employee_element.emCoMobileNumber,
                 employee_element.emCoHomeNumber,
                 employee_element.employeeID,
                 employee_element.joining_date,
                 employee_element.company_laptop,
                 employee_element.company_mobile]
    profileCompletion = 0
    for i in list_empl:
        if not i:
            profileCompletion += 1

    profilePercent = ((len(list_empl) - profileCompletion) / len(list_empl)) * 100

    if request.method == "POST":
        detail_element.payments_done = request.form.get('done')
        detail_element.payments_pending = request.form.get('pending_p')
        detail_element.total_leaves = request.form.get('pending_l')
        detail_element.visa_expiry = request.form.get('visa')
        db.session.commit()
        return redirect(url_for('employee_view', employee_id=employee_id))

    return render_template("employee_view_edit.html", employee=employee_element, date_str=date_str,
                           workedHours=totalHours, profile=round(profilePercent, 0), items=actionItems, img_url=img_url,
                           len=range(len(actionItems)), user=current_user, details=detail_element)


@app.route("/employee_delete/<employee_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def employee_delete(employee_id):
    entry_to_delete = employeeMaster.query.get(employee_id)
    img__ = db.session.query(Img).filter_by(employeeID=employee_id).first()
    # db.session.delete(img__)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("employee_report"))


@app.route("/action_item_del/<entry_id>", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def action_item_del(entry_id):
    entry_to_delete = actionItemMaster.query.get(entry_id)
    employee_id = entry_to_delete.employeeID
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for("employee_view", employee_id=employee_id))


@app.route("/image_view", methods=["GET", "POST"])
# Mark with decorator
@admin_only
def image_view():
    img_data = Img.query.all()
    return render_template('image.html', data=img_data, user=current_user)


def delete_roster_timesheet():
    timesheet_entries = timesheetEntryMaster.query.all()
    roster_entries = rosterEntryMaster.query.all()
    timesheets = timesheetMaster.query.all()
    rosters = rosterMaster.query.all()
    for i in timesheet_entries:
        db.session.delete(i)
        db.session.commit()
    for i in roster_entries:
        db.session.delete(i)
        db.session.commit()
    for i in timesheets:
        db.session.delete(i)
        db.session.commit()
    for i in rosters:
        db.session.delete(i)
        db.session.commit()


# images = Img.query.all()
# for i in images:
#     db.session.delete(i)
#     db.session.commit()

# delete_roster_timesheet()


if __name__ == "__main__":
    app.run(debug=True)

# Jan 2023
