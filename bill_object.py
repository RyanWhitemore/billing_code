from fpdf import FPDF

class Bill:
    def __init__(self):
        self.windows = 0
        self.windows_total = 0.00
        self.entry_doors = 0
        self.entry_doors_total = 0.00
        self.french_doors = 0
        self.french_doors_total = 0.00
        self.sgd = 0
        self.sgd_total = 0.00
        self.sgd_extra = 0
        self.sgd_extra_total = 0.00
        self.extra_labor = 0
        self.extra_labor_total = 0.00
        self.receipts = 0
        self.measure = 0
        self.total = 0
        self.customer_name = ''
        self.file_name = ''

    def update_attribute(self, attribute, input):
        setattr(self, attribute, input)
    
    def make_totals(self):
        self.windows_total = self.windows * 125
        self.entry_doors_total = self.entry_doors * 300
        self.french_doors_total = self.french_doors * 400
        self.sgd_total = self.sgd * 300
        self.sgd_extra_total = self.sgd_extra * 50
        self.extra_labor_total = self.extra_labor * 80 
    
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
        self.total = self.windows_total + \
            self.entry_doors_total + \
            self.french_doors_total + \
            self.sgd_total + \
            self.sgd_extra_total + \
            self.extra_labor_total + \
            self.receipts + \
            self.measure
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
        self.create_row('windows', self.windows, self.windows_total, pdf, top, offset, 20)
        # create third row
        self.create_row('Entry doors', self.entry_doors, self.entry_doors_total, pdf, top, offset, 30)
        # create fourth row
        self.create_row('French doors', self.french_doors, self.french_doors_total, pdf, top, offset, 40)
        # create fith row
        self.create_row('Sliding doors', self.sgd, self.sgd_total, pdf, top, offset, 50)
        # create sixth row
        self.create_row('Extra panels', self.sgd_extra, self.sgd_extra_total, pdf, top, offset, 60)
        # create seventh row
        self.create_row('Hours labor', self.extra_labor, self.extra_labor_total, pdf, top, offset, 70)
        # create eighth row
        self.create_row('Receipts', ' ', self.receipts, pdf, top, offset, 80)
        # create ninth row
        self.create_row('Measure', ' ', self.measure, pdf, top, offset, 90)
        # create total row
        pdf.x = offset + 40
        pdf.multi_cell(40, 10, str(self.total), 1, 0)

        pdf.output(self.file_name)

bill = Bill()


bill.update_attribute('windows', 12)
bill.update_attribute('entry_doors', 2)
bill.update_attribute('french_doors', 1)
bill.update_attribute('sgd', 1)
bill.update_attribute('sgd_extra', 0)
bill.update_attribute('extra_labor', 2)
bill.add_receipts(58.93)
bill.is_measure('yes')
bill.add_name('customer')
bill.update_attribute('windows', 10)
bill.get_bill_total()

print()

bill.generate_bill()
