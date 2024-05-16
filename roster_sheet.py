import xlsxwriter
from datetime import datetime


def create_roster(employee, hotel, time_data, entries, date_data):
    workbook = xlsxwriter.Workbook('specsheet.xlsx')
    current_datetime = datetime.today().date().timetuple()
    str_current_datetime = str(current_datetime)
    a__ = datetime.now()
    a_ = a__.strftime("%a, %d %b %Y %H-%M-%S")

    worksheet = workbook.add_worksheet()

    header = workbook.add_format(
        {'align': 'center', 'font_size': 13, 'font': 'Arial', 'bold': True, 'bottom': 1, 'top': 1, 'right': 1,
         'left': 1, 'border_color': '#2C3333',
         'bg_color': '#47A992', 'font_color': '#F9FBE7'})

    header2 = workbook.add_format(
        {'align': 'center', 'font_size': 13, 'font': 'Arial', 'bold': True, 'bottom': 1, 'top': 1, 'right': 1,
         'left': 1, 'border_color': '#2C3333',
         'bg_color': '#1B9C85', 'font_color': '#F9FBE7'})

    subH = workbook.add_format(
        {'align': 'center', 'font_size': 9, 'font': 'Arial', 'bold': True, 'bottom': 1, 'top': 1, 'right': 1, 'left': 1,
         'border_color': '#2C3333',
         'bg_color': '#99A98F'})

    roster_color = {'Off': '#16FF00', 'Absent': '#FF0303', 'Sick': '#FFED00', 'Vacation': '#82CD47',
                    'Public Holiday': '#146C94', 'Office': '#83764F'}

    font_color__ = {'Off': '#F9FBE7', 'Absent': '#F9FBE7', 'Sick': '#000000', 'Vacation': '#000000',
                    'Public Holiday': '#F9FBE7', 'Office': '#F9FBE7'}

    def absents_color(absent):
        color__ = roster_color[str(absent)]
        f_color = font_color__[str(absent)]
        subH_color = workbook.add_format(
            {'align': 'center', 'font_size': 9, 'font': 'Arial', 'bold': True, 'bottom': 1, 'top': 1, 'right': 1,
             'left': 1,
             'border_color': '#2C3333',
             'bg_color': color__, 'font_color': f_color})

        return subH_color

    subH_blank = workbook.add_format(
        {'align': 'center', 'font_size': 9, 'font': 'Arial', 'bold': True, 'bottom': 1, 'top': 1, 'right': 1, 'left': 1,
         'border_color': '#2C3333',
         'bg_color': '#F0EDD4'})

    column_width = [{'name': 'A:A', 'size': 5}, {'name': 'B:B', 'size': 9}, {'name': 'C:C', 'size': 20},
                    {'name': 'D:D', 'size': 22},
                    {'name': 'E:E', 'size': 25}, {'name': 'F:F', 'size': 12}, {'name': 'G:G', 'size': 10},
                    ]

    for i in column_width:
        worksheet.set_column(i['name'], i['size'])

    # worksheet.write('A1', 'Flow Control Commune Pvt Ltd', )
    worksheet.merge_range('A1:G1', "DUTY ROSTER", header)
    worksheet.merge_range('A2:C2', f"DATE: {date_data[0]}", header2)
    worksheet.merge_range('D2:G2', f"{date_data[2]}, {date_data[1]}", header2)
    worksheet.write('A3', 'S.NO', subH)
    worksheet.write('B3', 'No of Staff', subH)
    worksheet.write('C3', 'STAFF', subH)
    worksheet.write('D3', 'HOTEL', subH)
    worksheet.write('E3', 'DUTY TIME', subH)
    worksheet.write('F3', 'PICK UP TIME', subH)
    worksheet.write('G3', 'REMARK', subH)

    for i in range(len(employee)):
        if entries[i].absent == 'none':
            worksheet.write(f'A{4 + i}', i + 1, subH_blank)
            worksheet.write(f'B{4 + i}', i + 1, subH_blank)
            worksheet.write(f'C{4 + i}', employee[i], subH_blank)
            worksheet.write(f'D{4 + i}', hotel[i], subH_blank)
            if time_data[i]['timeIn2'] == '00:00':
                worksheet.write(f'E{4 + i}', f"{time_data[i]['timeIn1']} - {time_data[i]['timeOut1']}", subH_blank)
            else:
                worksheet.write(f'E{4 + i}',
                                f"{time_data[i]['timeIn1']} - {time_data[i]['timeOut1']}/{time_data[i]['timeIn2']} - {time_data[i]['timeOut2']}",
                                subH_blank)
            worksheet.write(f'F{4 + i}', f"{time_data[i]['pickUp']}/{time_data[i]['pickUp2']}", subH_blank)
            worksheet.write(f'G{4 + i}', entries[i].remark, subH_blank)
        else:
            worksheet.write(f'A{4 + i}', i + 1, subH_blank)
            worksheet.write(f'B{4 + i}', i + 1, subH_blank)
            worksheet.write(f'C{4 + i}', employee[i], subH_blank)
            worksheet.merge_range(f'D{4 + i}:G{4 + i}', entries[i].absent, absents_color(entries[i].absent))

    workbook.close()
