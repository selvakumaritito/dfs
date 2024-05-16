import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, EmailField, BooleanField, MultipleFileField, \
    DateField, SelectField, DateTimeField, FormField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    email = StringField("Email-ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    email = StringField("Email-ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Your Name", validators=[DataRequired()])
    submit = SubmitField("Let Me In")








class NameEntry(FlaskForm):
    name = StringField("Name: ")
    time_in = DateTimeField("Time In:")
    time_out = DateTimeField("Time Out: ")
    hours = IntegerField("No. of Hours: ")


class TimeSheet(FlaskForm):
    date = DateField("Date: ")
    sheet_no = IntegerField("Sheet No:", default=0)
    hotel = StringField("Hotel: ", default='')
    name1 = StringField("Name: ", default='')
    time_in1 = IntegerField("Time In1:", default=0)
    time_out1 = IntegerField("Time Out1: ", default=0)
    time_in1a = IntegerField("Time In2:", default=0)
    time_out1a = IntegerField("Time Out2: ", default=0)
    hours1 = IntegerField("No. of Hours: ", default=0)
    name2 = StringField("Name: ", default='')
    time_in2 = IntegerField("Time In1:", default=0)
    time_out2 = IntegerField("Time Out1: ", default=0)
    time_in2a = IntegerField("Time In2:", default=0)
    time_out2a = IntegerField("Time Out2: ", default=0)
    hours2 = IntegerField("No. of Hours: ", default=0)
    name3 = StringField("Name: ", default='')
    time_in3 = IntegerField("Time In1:", default=0)
    time_out3 = IntegerField("Time Out1: ", default=0)
    time_in3a = IntegerField("Time In2:", default=0)
    time_out3a = IntegerField("Time Out2: ", default=0)
    hours3 = IntegerField("No. of Hours: ", default=0)
    name4 = StringField("Name: ", default='')
    time_in4 = IntegerField("Time In1:", default=0)
    time_out4 = IntegerField("Time Out1: ", default=0)
    time_in4a = IntegerField("Time In2:", default=0)
    time_out4a = IntegerField("Time Out2: ", default=0)
    hours4 = IntegerField("No. of Hours: ", default=0)
    name5 = StringField("Name: ", default='')
    time_in5 = IntegerField("Time In1:", default=0)
    time_out5 = IntegerField("Time Out1: ", default=0)
    time_in5a = IntegerField("Time In2:", default=0)
    time_out5a = IntegerField("Time Out2: ", default=0)
    hours5 = IntegerField("No. of Hours: ", default=0)

    # date = DateField("Date: ")
    # sheet_no = IntegerField("Sheet No:", default=None)
    # hotel = StringField("Hotel: ", default="")
    # name1 = StringField("Name: ", default="")
    # time_in1 = IntegerField("Time In:", default=9)
    # time_out1 = IntegerField("Time Out: ", default=18)
    # hours1 = IntegerField("No. of Hours: ", default=9)
    # name2 = StringField("Name: ", default="")
    # time_in2 = DateTimeField("Time In:", default=9)
    # time_out2 = DateTimeField("Time Out: ", default=18)
    # hours2 = IntegerField("No. of Hours: ", default=18)
    # name3 = StringField("Name: ", default="")
    # time_in3 = DateTimeField("Time In:", default=9)
    # time_out3 = DateTimeField("Time Out: ", default=18)
    # hours3 = IntegerField("No. of Hours: ", default=18)
    # name4 = StringField("Name: ", default="")
    # time_in4 = DateTimeField("Time In:", default=9)
    # time_out4 = DateTimeField("Time Out: ", default=18)
    # hours4 = IntegerField("No. of Hours: ", default=18)
    # name5 = StringField("Name: ", default="")
    # time_in5 = DateTimeField("Time In:", default=9)
    # time_out5 = DateTimeField("Time Out: ", default=18)
    # hours5 = IntegerField("No. of Hours: ", default=17)

    submit = SubmitField("Submit Timesheet")


class RosterStaff(FlaskForm):
    name = StringField("Name: ", default="")
    time_a = IntegerField("Time In 1: ", default=0)
    time_b = IntegerField("Time Out 1: ", default=0)
    time_c = IntegerField("Time In 2: ", default=0)
    time_d = IntegerField("Time Out 2: ", default=0)
    pick_up = IntegerField("Pick Up: ", default=0)
    remarks = StringField("Remarks: ", default="")


class RosterHotel(FlaskForm):
    hotel_name = StringField("Hotel Name: ", default="")
    staff1 = FormField(RosterStaff)
    staff2 = FormField(RosterStaff)
    staff3 = FormField(RosterStaff)
    staff4 = FormField(RosterStaff)
    staff5 = FormField(RosterStaff)
    staff6 = FormField(RosterStaff)


class Roster(FlaskForm):
    hotel1 = FormField(RosterHotel)
    hotel2 = FormField(RosterHotel)
    hotel3 = FormField(RosterHotel)
    hotel4 = FormField(RosterHotel)
    hotel5 = FormField(RosterHotel)
    hotel6 = FormField(RosterHotel)
    hotel7 = FormField(RosterHotel)

    submit = SubmitField("Submit Roster: ")


class RosterExtend(FlaskForm):
    # Hotel 1
    hotel1 = StringField("Hotel Name: ", default="")
    # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # 7 hotels and 6 staffs - so - from 11 to 76

    # Staff 1
    name11 = StringField("Name: ", default="")
    time_a_11 = IntegerField("Time In 1: ", default=0)
    time_b_11 = IntegerField("Time Out 1: ", default=0)
    time_c_11 = IntegerField("Time In 2: ", default=0)
    time_d_11 = IntegerField("Time Out 2: ", default=0)
    pick_up_11 = IntegerField("Pick Up: ", default=0)
    remarks_11 = StringField("Remarks: ", default="")

    # Staff 2
    name12 = StringField("Name: ", default="")
    time_a_12 = IntegerField("Time In 1: ", default=0)
    time_b_12 = IntegerField("Time Out 1: ", default=0)
    time_c_12 = IntegerField("Time In 2: ", default=0)
    time_d_12 = IntegerField("Time Out 2: ", default=0)
    pick_up_12 = IntegerField("Pick Up: ", default=0)
    remarks_12 = StringField("Remarks: ", default="")

    # Staff 3
    name13 = StringField("Name: ", default="")
    time_a_13 = IntegerField("Time In 1: ", default=0)
    time_b_13 = IntegerField("Time Out 1: ", default=0)
    time_c_13 = IntegerField("Time In 2: ", default=0)
    time_d_13 = IntegerField("Time Out 2: ", default=0)
    pick_up_13 = IntegerField("Pick Up: ", default=0)
    remarks_13 = StringField("Remarks: ", default="")

    # Staff 4
    name14 = StringField("Name: ", default="")
    time_a_14 = IntegerField("Time In 1: ", default=0)
    time_b_14 = IntegerField("Time Out 1: ", default=0)
    time_c_14 = IntegerField("Time In 2: ", default=0)
    time_d_14 = IntegerField("Time Out 2: ", default=0)
    pick_up_14 = IntegerField("Pick Up: ", default=0)
    remarks_14 = StringField("Remarks: ", default="")

    # Staff 5
    name15 = StringField("Name: ", default="")
    time_a_15 = IntegerField("Time In 1: ", default=0)
    time_b_15 = IntegerField("Time Out 1: ", default=0)
    time_c_15 = IntegerField("Time In 2: ", default=0)
    time_d_15 = IntegerField("Time Out 2: ", default=0)
    pick_up_15 = IntegerField("Pick Up: ", default=0)
    remarks_15 = StringField("Remarks: ", default="")

    # Staff 6
    name16 = StringField("Name: ", default="")
    time_a_16 = IntegerField("Time In 1: ", default=0)
    time_b_16 = IntegerField("Time Out 1: ", default=0)
    time_c_16 = IntegerField("Time In 2: ", default=0)
    time_d_16 = IntegerField("Time Out 2: ", default=0)
    pick_up_16 = IntegerField("Pick Up: ", default=0)
    remarks_16 = StringField("Remarks: ", default="")

    # Hotel 2
    hotel2 = StringField("Hotel Name: ", default="")
    # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # 7 hotels and 6 staffs - so - from 11 to 76

    # Staff 1
    name21 = StringField("Name: ", default="")
    time_a_21 = IntegerField("Time In 1: ", default=0)
    time_b_21 = IntegerField("Time Out 1: ", default=0)
    time_c_21 = IntegerField("Time In 2: ", default=0)
    time_d_21 = IntegerField("Time Out 2: ", default=0)
    pick_up_21 = IntegerField("Pick Up: ", default=0)
    remarks_21 = StringField("Remarks: ", default="")

    # Staff 2
    name22 = StringField("Name: ", default="")
    time_a_22 = IntegerField("Time In 1: ", default=0)
    time_b_22 = IntegerField("Time Out 1: ", default=0)
    time_c_22 = IntegerField("Time In 2: ", default=0)
    time_d_22 = IntegerField("Time Out 2: ", default=0)
    pick_up_22 = IntegerField("Pick Up: ", default=0)
    remarks_22 = StringField("Remarks: ", default="")

    # Staff 3
    name23 = StringField("Name: ", default="")
    time_a_23 = IntegerField("Time In 1: ", default=0)
    time_b_23 = IntegerField("Time Out 1: ", default=0)
    time_c_23 = IntegerField("Time In 2: ", default=0)
    time_d_23 = IntegerField("Time Out 2: ", default=0)
    pick_up_23 = IntegerField("Pick Up: ", default=0)
    remarks_23 = StringField("Remarks: ", default="")

    # Staff 4
    name24 = StringField("Name: ", default="")
    time_a_24 = IntegerField("Time In 1: ", default=0)
    time_b_24 = IntegerField("Time Out 1: ", default=0)
    time_c_24 = IntegerField("Time In 2: ", default=0)
    time_d_24 = IntegerField("Time Out 2: ", default=0)
    pick_up_24 = IntegerField("Pick Up: ", default=0)
    remarks_24 = StringField("Remarks: ", default="")

    # Staff 5
    name25 = StringField("Name: ", default="")
    time_a_25 = IntegerField("Time In 1: ", default=0)
    time_b_25 = IntegerField("Time Out 1: ", default=0)
    time_c_25 = IntegerField("Time In 2: ", default=0)
    time_d_25 = IntegerField("Time Out 2: ", default=0)
    pick_up_25 = IntegerField("Pick Up: ", default=0)
    remarks_25 = StringField("Remarks: ", default="")

    # Staff 6
    name26 = StringField("Name: ", default="")
    time_a_26 = IntegerField("Time In 1: ", default=0)
    time_b_26 = IntegerField("Time Out 1: ", default=0)
    time_c_26 = IntegerField("Time In 2: ", default=0)
    time_d_26 = IntegerField("Time Out 2: ", default=0)
    pick_up_26 = IntegerField("Pick Up: ", default=0)
    remarks_26 = StringField("Remarks: ", default="")

    # Hotel 3
    hotel3 = StringField("Hotel Name: ", default="")
    # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # 7 hotels and 6 staffs - so - from 11 to 76

    # Staff 1
    name31 = StringField("Name: ", default="")
    time_a_31 = IntegerField("Time In 1: ", default=0)
    time_b_31 = IntegerField("Time Out 1: ", default=0)
    time_c_31 = IntegerField("Time In 2: ", default=0)
    time_d_31 = IntegerField("Time Out 2: ", default=0)
    pick_up_31 = IntegerField("Pick Up: ", default=0)
    remarks_31 = StringField("Remarks: ", default="")

    # Staff 2
    name32 = StringField("Name: ", default="")
    time_a_32 = IntegerField("Time In 1: ", default=0)
    time_b_32 = IntegerField("Time Out 1: ", default=0)
    time_c_32 = IntegerField("Time In 2: ", default=0)
    time_d_32 = IntegerField("Time Out 2: ", default=0)
    pick_up_32 = IntegerField("Pick Up: ", default=0)
    remarks_32 = StringField("Remarks: ", default="")

    # Staff 3
    name33 = StringField("Name: ", default="")
    time_a_33 = IntegerField("Time In 1: ", default=0)
    time_b_33 = IntegerField("Time Out 1: ", default=0)
    time_c_33 = IntegerField("Time In 2: ", default=0)
    time_d_33 = IntegerField("Time Out 2: ", default=0)
    pick_up_33 = IntegerField("Pick Up: ", default=0)
    remarks_33 = StringField("Remarks: ", default="")

    # Staff 4
    name34 = StringField("Name: ", default="")
    time_a_34 = IntegerField("Time In 1: ", default=0)
    time_b_34 = IntegerField("Time Out 1: ", default=0)
    time_c_34 = IntegerField("Time In 2: ", default=0)
    time_d_34 = IntegerField("Time Out 2: ", default=0)
    pick_up_34 = IntegerField("Pick Up: ", default=0)
    remarks_34 = StringField("Remarks: ", default="")

    # Staff 5
    name35 = StringField("Name: ", default="")
    time_a_35 = IntegerField("Time In 1: ", default=0)
    time_b_35 = IntegerField("Time Out 1: ", default=0)
    time_c_35 = IntegerField("Time In 2: ", default=0)
    time_d_35 = IntegerField("Time Out 2: ", default=0)
    pick_up_35 = IntegerField("Pick Up: ", default=0)
    remarks_35 = StringField("Remarks: ", default="")

    # Staff 6
    name36 = StringField("Name: ", default="")
    time_a_36 = IntegerField("Time In 1: ", default=0)
    time_b_36 = IntegerField("Time Out 1: ", default=0)
    time_c_36 = IntegerField("Time In 2: ", default=0)
    time_d_36 = IntegerField("Time Out 2: ", default=0)
    pick_up_36 = IntegerField("Pick Up: ", default=0)
    remarks_36 = StringField("Remarks: ", default="")

    submit = SubmitField("Submit Roster")

    # # Hotel 4
    # hotel4 = StringField("Hotel Name: ", default="")
    # # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # # 7 hotels and 6 staffs - so - from 11 to 76
    #
    # # Staff 1
    # name11 = StringField("Name: ", default="")
    # time_a_11 = IntegerField("Time In 1: ", default=0)
    # time_b_11 = IntegerField("Time Out 1: ", default=0)
    # time_c_11 = IntegerField("Time In 2: ", default=0)
    # time_d_11 = IntegerField("Time Out 2: ", default=0)
    # pick_up_11 = IntegerField("Pick Up: ", default=0)
    # remarks_11 = StringField("Remarks: ", default="")
    #
    # # Staff 2
    # name12 = StringField("Name: ", default="")
    # time_a_12 = IntegerField("Time In 1: ", default=0)
    # time_b_12 = IntegerField("Time Out 1: ", default=0)
    # time_c_12 = IntegerField("Time In 2: ", default=0)
    # time_d_12 = IntegerField("Time Out 2: ", default=0)
    # pick_up_12 = IntegerField("Pick Up: ", default=0)
    # remarks_12 = StringField("Remarks: ", default="")
    #
    # # Staff 3
    # name13 = StringField("Name: ", default="")
    # time_a_13 = IntegerField("Time In 1: ", default=0)
    # time_b_13 = IntegerField("Time Out 1: ", default=0)
    # time_c_13 = IntegerField("Time In 2: ", default=0)
    # time_d_13 = IntegerField("Time Out 2: ", default=0)
    # pick_up_13 = IntegerField("Pick Up: ", default=0)
    # remarks_13 = StringField("Remarks: ", default="")
    #
    # # Staff 4
    # name14 = StringField("Name: ", default="")
    # time_a_14 = IntegerField("Time In 1: ", default=0)
    # time_b_14 = IntegerField("Time Out 1: ", default=0)
    # time_c_14 = IntegerField("Time In 2: ", default=0)
    # time_d_14 = IntegerField("Time Out 2: ", default=0)
    # pick_up_14 = IntegerField("Pick Up: ", default=0)
    # remarks_14 = StringField("Remarks: ", default="")
    #
    # # Staff 5
    # name15 = StringField("Name: ", default="")
    # time_a_15 = IntegerField("Time In 1: ", default=0)
    # time_b_15 = IntegerField("Time Out 1: ", default=0)
    # time_c_15 = IntegerField("Time In 2: ", default=0)
    # time_d_15 = IntegerField("Time Out 2: ", default=0)
    # pick_up_15 = IntegerField("Pick Up: ", default=0)
    # remarks_15 = StringField("Remarks: ", default="")
    #
    # # Staff 6
    # name16 = StringField("Name: ", default="")
    # time_a_16 = IntegerField("Time In 1: ", default=0)
    # time_b_16 = IntegerField("Time Out 1: ", default=0)
    # time_c_16 = IntegerField("Time In 2: ", default=0)
    # time_d_16 = IntegerField("Time Out 2: ", default=0)
    # pick_up_16 = IntegerField("Pick Up: ", default=0)
    # remarks_16 = StringField("Remarks: ", default="")
    #
    # # Hotel 5
    # hotel5 = StringField("Hotel Name: ", default="")
    # # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # # 7 hotels and 6 staffs - so - from 11 to 76
    #
    # # Staff 1
    # name11 = StringField("Name: ", default="")
    # time_a_11 = IntegerField("Time In 1: ", default=0)
    # time_b_11 = IntegerField("Time Out 1: ", default=0)
    # time_c_11 = IntegerField("Time In 2: ", default=0)
    # time_d_11 = IntegerField("Time Out 2: ", default=0)
    # pick_up_11 = IntegerField("Pick Up: ", default=0)
    # remarks_11 = StringField("Remarks: ", default="")
    #
    # # Staff 2
    # name12 = StringField("Name: ", default="")
    # time_a_12 = IntegerField("Time In 1: ", default=0)
    # time_b_12 = IntegerField("Time Out 1: ", default=0)
    # time_c_12 = IntegerField("Time In 2: ", default=0)
    # time_d_12 = IntegerField("Time Out 2: ", default=0)
    # pick_up_12 = IntegerField("Pick Up: ", default=0)
    # remarks_12 = StringField("Remarks: ", default="")
    #
    # # Staff 3
    # name13 = StringField("Name: ", default="")
    # time_a_13 = IntegerField("Time In 1: ", default=0)
    # time_b_13 = IntegerField("Time Out 1: ", default=0)
    # time_c_13 = IntegerField("Time In 2: ", default=0)
    # time_d_13 = IntegerField("Time Out 2: ", default=0)
    # pick_up_13 = IntegerField("Pick Up: ", default=0)
    # remarks_13 = StringField("Remarks: ", default="")
    #
    # # Staff 4
    # name14 = StringField("Name: ", default="")
    # time_a_14 = IntegerField("Time In 1: ", default=0)
    # time_b_14 = IntegerField("Time Out 1: ", default=0)
    # time_c_14 = IntegerField("Time In 2: ", default=0)
    # time_d_14 = IntegerField("Time Out 2: ", default=0)
    # pick_up_14 = IntegerField("Pick Up: ", default=0)
    # remarks_14 = StringField("Remarks: ", default="")
    #
    # # Staff 5
    # name15 = StringField("Name: ", default="")
    # time_a_15 = IntegerField("Time In 1: ", default=0)
    # time_b_15 = IntegerField("Time Out 1: ", default=0)
    # time_c_15 = IntegerField("Time In 2: ", default=0)
    # time_d_15 = IntegerField("Time Out 2: ", default=0)
    # pick_up_15 = IntegerField("Pick Up: ", default=0)
    # remarks_15 = StringField("Remarks: ", default="")
    #
    # # Staff 6
    # name16 = StringField("Name: ", default="")
    # time_a_16 = IntegerField("Time In 1: ", default=0)
    # time_b_16 = IntegerField("Time Out 1: ", default=0)
    # time_c_16 = IntegerField("Time In 2: ", default=0)
    # time_d_16 = IntegerField("Time Out 2: ", default=0)
    # pick_up_16 = IntegerField("Pick Up: ", default=0)
    # remarks_16 = StringField("Remarks: ", default="")
    #
    # # Hotel 6
    # hotel6 = StringField("Hotel Name: ", default="")
    # # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # # 7 hotels and 6 staffs - so - from 11 to 76
    #
    # # Staff 1
    # name11 = StringField("Name: ", default="")
    # time_a_11 = IntegerField("Time In 1: ", default=0)
    # time_b_11 = IntegerField("Time Out 1: ", default=0)
    # time_c_11 = IntegerField("Time In 2: ", default=0)
    # time_d_11 = IntegerField("Time Out 2: ", default=0)
    # pick_up_11 = IntegerField("Pick Up: ", default=0)
    # remarks_11 = StringField("Remarks: ", default="")
    #
    # # Staff 2
    # name12 = StringField("Name: ", default="")
    # time_a_12 = IntegerField("Time In 1: ", default=0)
    # time_b_12 = IntegerField("Time Out 1: ", default=0)
    # time_c_12 = IntegerField("Time In 2: ", default=0)
    # time_d_12 = IntegerField("Time Out 2: ", default=0)
    # pick_up_12 = IntegerField("Pick Up: ", default=0)
    # remarks_12 = StringField("Remarks: ", default="")
    #
    # # Staff 3
    # name13 = StringField("Name: ", default="")
    # time_a_13 = IntegerField("Time In 1: ", default=0)
    # time_b_13 = IntegerField("Time Out 1: ", default=0)
    # time_c_13 = IntegerField("Time In 2: ", default=0)
    # time_d_13 = IntegerField("Time Out 2: ", default=0)
    # pick_up_13 = IntegerField("Pick Up: ", default=0)
    # remarks_13 = StringField("Remarks: ", default="")
    #
    # # Staff 4
    # name14 = StringField("Name: ", default="")
    # time_a_14 = IntegerField("Time In 1: ", default=0)
    # time_b_14 = IntegerField("Time Out 1: ", default=0)
    # time_c_14 = IntegerField("Time In 2: ", default=0)
    # time_d_14 = IntegerField("Time Out 2: ", default=0)
    # pick_up_14 = IntegerField("Pick Up: ", default=0)
    # remarks_14 = StringField("Remarks: ", default="")
    #
    # # Staff 5
    # name15 = StringField("Name: ", default="")
    # time_a_15 = IntegerField("Time In 1: ", default=0)
    # time_b_15 = IntegerField("Time Out 1: ", default=0)
    # time_c_15 = IntegerField("Time In 2: ", default=0)
    # time_d_15 = IntegerField("Time Out 2: ", default=0)
    # pick_up_15 = IntegerField("Pick Up: ", default=0)
    # remarks_15 = StringField("Remarks: ", default="")
    #
    # # Staff 6
    # name16 = StringField("Name: ", default="")
    # time_a_16 = IntegerField("Time In 1: ", default=0)
    # time_b_16 = IntegerField("Time Out 1: ", default=0)
    # time_c_16 = IntegerField("Time In 2: ", default=0)
    # time_d_16 = IntegerField("Time Out 2: ", default=0)
    # pick_up_16 = IntegerField("Pick Up: ", default=0)
    # remarks_16 = StringField("Remarks: ", default="")
    #
    # # Hotel 7
    # hotel7 = StringField("Hotel Name: ", default="")
    # # in name11 - the first '1' represents the hotel no., whereas the second '1' represents the staff number
    # # 7 hotels and 6 staffs - so - from 11 to 76
    #
    # # Staff 1
    # name11 = StringField("Name: ", default="")
    # time_a_11 = IntegerField("Time In 1: ", default=0)
    # time_b_11 = IntegerField("Time Out 1: ", default=0)
    # time_c_11 = IntegerField("Time In 2: ", default=0)
    # time_d_11 = IntegerField("Time Out 2: ", default=0)
    # pick_up_11 = IntegerField("Pick Up: ", default=0)
    # remarks_11 = StringField("Remarks: ", default="")
    #
    # # Staff 2
    # name12 = StringField("Name: ", default="")
    # time_a_12 = IntegerField("Time In 1: ", default=0)
    # time_b_12 = IntegerField("Time Out 1: ", default=0)
    # time_c_12 = IntegerField("Time In 2: ", default=0)
    # time_d_12 = IntegerField("Time Out 2: ", default=0)
    # pick_up_12 = IntegerField("Pick Up: ", default=0)
    # remarks_12 = StringField("Remarks: ", default="")
    #
    # # Staff 3
    # name13 = StringField("Name: ", default="")
    # time_a_13 = IntegerField("Time In 1: ", default=0)
    # time_b_13 = IntegerField("Time Out 1: ", default=0)
    # time_c_13 = IntegerField("Time In 2: ", default=0)
    # time_d_13 = IntegerField("Time Out 2: ", default=0)
    # pick_up_13 = IntegerField("Pick Up: ", default=0)
    # remarks_13 = StringField("Remarks: ", default="")
    #
    # # Staff 4
    # name14 = StringField("Name: ", default="")
    # time_a_14 = IntegerField("Time In 1: ", default=0)
    # time_b_14 = IntegerField("Time Out 1: ", default=0)
    # time_c_14 = IntegerField("Time In 2: ", default=0)
    # time_d_14 = IntegerField("Time Out 2: ", default=0)
    # pick_up_14 = IntegerField("Pick Up: ", default=0)
    # remarks_14 = StringField("Remarks: ", default="")
    #
    # # Staff 5
    # name15 = StringField("Name: ", default="")
    # time_a_15 = IntegerField("Time In 1: ", default=0)
    # time_b_15 = IntegerField("Time Out 1: ", default=0)
    # time_c_15 = IntegerField("Time In 2: ", default=0)
    # time_d_15 = IntegerField("Time Out 2: ", default=0)
    # pick_up_15 = IntegerField("Pick Up: ", default=0)
    # remarks_15 = StringField("Remarks: ", default="")
    #
    # # Staff 6
    # name16 = StringField("Name: ", default="")
    # time_a_16 = IntegerField("Time In 1: ", default=0)
    # time_b_16 = IntegerField("Time Out 1: ", default=0)
    # time_c_16 = IntegerField("Time In 2: ", default=0)
    # time_d_16 = IntegerField("Time Out 2: ", default=0)
    # pick_up_16 = IntegerField("Pick Up: ", default=0)
    # remarks_16 = StringField("Remarks: ", default="")
    #


class Archives(FlaskForm):
    date1 = DateField("From Date: ")
    date2 = DateField("To Date: ")
    submit = SubmitField("Go!")


class ActionItem(FlaskForm):
    content = StringField("", default="")
    submit = SubmitField("Add Item")
