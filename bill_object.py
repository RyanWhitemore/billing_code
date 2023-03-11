from fpdf import FPDF

class Bill:
    def __init__(self):
        self.num_windows = 0
        self.windows_total = 0.00
        self.num_entry_doors = 0
        self.entry_doors_total = 0.00
        self.num_french_doors = 0
        self.french_doors_total = 0.00
        self.num_sgd = 0
        self.sgd_total = 0.00
        self.num_sgd_extra_panels = 0
        self.sgd_extra_total = 0.00
        self.hours_extra_labor = 0
        self.extra_labor_total = 0.00
        self.receipt_total = 0
        self.measure = 0
        self.total = 0
        self.customer_name = ''
        self.file_name = ''

    def update_attribute(self, attribute, input):
        if attribute == 'measure':
            if input == 1:
                self.measure = 125
            else:
                pass
        elif attribute == 'receipts':
            self.receipts = input
        else:
            setattr(self, attribute, input)
    
    def make_totals(self):
        self.windows_total = int(self.num_windows) * 125
        self.entry_doors_total = int(self.num_entry_doors) * 300
        self.french_doors_total = int(self.num_french_doors) * 400
        self.sgd_total = int(self.num_sgd) * 300
        self.sgd_extra_total = int(self.num_sgd_extra_panels) * 50
        self.extra_labor_total = int(self.hours_extra_labor) * 80 
    
    def add_receipts(self, input):
        self.receipts = float(input)
    
    def is_measure(self, input):
        if input.upper() == 'YES':
            self.measure = 125.00
        else:
            self.measure = 0.00

    def add_name(self, name):
        self.customer_name = name
        self.file_name = name + '_bill.pdf'

    def get_bill_total(self):
        self.make_totals()
        self.total = float(self.receipt_total) + \
            int(self.windows_total) + \
            int(self.entry_doors_total) + \
            int(self.french_doors_total) + \
            int(self.sgd_total) + \
            int(self.sgd_extra_total) + \
            int(self.extra_labor_total) + \
            int(self.measure)
        return self.total
    
    def create_row(self, col_1, col_2, col_3, pdf, top, offset, y):
        pdf.multi_cell(40, 10, col_1, 1, 0)
        pdf.x = offset
        pdf.y = top + y
        pdf.multi_cell(40, 10, str(col_2), 1, 0)
        pdf.x = offset + 40
        pdf.y = top + y
        pdf.multi_cell(40, 10, str(col_3), 1, 0)


    
    def generate_bill(self):
        self.get_bill_total()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        top = pdf.y
        offset = pdf.x + 40
        # create header
        pdf.multi_cell(120, 10, str(self.customer_name), 1, 0)
        # create first row
        self.create_row('Type', 'Number', 'Total', pdf, top, offset, 10)
        # create second row
        self.create_row('windows', self.num_windows, self.windows_total, pdf, top, offset, 20)
        # create third row
        self.create_row('Entry doors', self.num_entry_doors, self.entry_doors_total, pdf, top, offset, 30)
        # create fourth row
        self.create_row('French doors', self.num_french_doors, self.french_doors_total, pdf, top, offset, 40)
        # create fith row
        self.create_row('Sliding doors', self.num_sgd, self.sgd_total, pdf, top, offset, 50)
        # create sixth row
        self.create_row('Extra panels', self.num_sgd_extra_panels, self.sgd_extra_total, pdf, top, offset, 60)
        # create seventh row
        self.create_row('Hours labor', self.hours_extra_labor, self.extra_labor_total, pdf, top, offset, 70)
        # create eighth row
        self.create_row('Receipts', ' ', self.receipt_total, pdf, top, offset, 80)
        # create ninth row
        self.create_row('Measure', ' ', self.measure, pdf, top, offset, 90)
        # create total row
        pdf.x = offset + 40
        pdf.multi_cell(40, 10, str(self.total), 1, 0)

        return pdf

class User:
    def __init__(self, user, password):
        self.user = user
        self.password = password
    
    def update_user(self, username):
        self.user = username
    
    def update_password(self, password):
        self.password = password