from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from forms import *
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from flask import abort
import os

# app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = "kkkkk"
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///dfx_db_uno.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# creating login manager
login_manager = LoginManager()
login_manager.init_app(app)


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

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("Users", back_populates="employee")

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


class rosterMaster(db.Model):
    __tablename__ = "rosterMaster"
    id = Column(Integer, primary_key=True)

    # relationship as parent
    entry = relationship("rosterEntryMaster", back_populates="roster")

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("Users", back_populates="roster")


class timesheetMaster(db.Model):
    __tablename__ = "timesheetMaster"
    id = Column(Integer, primary_key=True)

    # relationship as parent
    entry = relationship("timesheetEntryMaster", back_populates="timesheet")

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("Users", back_populates="timesheet")

    hotelID = Column(Integer, ForeignKey("hotelMaster.id"))
    hotel = relationship("hotelMaster", back_populates="timesheet")


class hotelMaster(db.Model):
    __tablename__ = "hotelMaster"
    id = Column(Integer, primary_key=True)

    # relationship as parent
    rosterEntry = relationship("rosterEntryMaster", back_populates="hotel")
    timesheet = relationship("timesheetMaster", back_populates="hotel")


class departmentMaster(db.Model):
    __tablename__ = "departmentMaster"
    id = Column(Integer, primary_key=True)

    # relationship as parent
    employee = relationship("employeeMaster", back_populates="department")


class documentMaster(db.Model):
    __tablename__ = "documentMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="document")


class actionItemMaster(db.Model):
    __tablename__ = "actionItemMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="actionItem")


class leaveApplicationMaster(db.Model):
    __tablename__ = "leaveApplicationMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("Users", back_populates="leave")

    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="leave")


class passportApplicationMaster(db.Model):
    __tablename__ = "passportApplicationMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    createdBy = Column(Integer, ForeignKey("Users.id"))
    user = relationship("Users", back_populates="passport")

    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="passport")


class timesheetEntryMaster(db.Model):
    __tablename__ = "timesheetEntryMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="timesheet")

    timesheetID = Column(Integer, ForeignKey("timesheetMaster.id"))
    timesheet = relationship("timesheetMaster", back_populates="entry")


class rosterEntryMaster(db.Model):
    __tablename__ = "rosterEntryMaster"
    id = Column(Integer, primary_key=True)

    # relationships as child
    employeeID = Column(Integer, ForeignKey("employeeMaster.id"))
    employee = relationship("employeeMaster", back_populates="roster")

    rosterID = Column(Integer, ForeignKey("rosterMaster.id"))
    roster = relationship("rosterMaster", back_populates="entry")

    hotelID = Column(Integer, ForeignKey("hotelMaster.id"))
    hotel = relationship("hotelMaster", back_populates="rosterEntry")
