from bill_object import Bill

def main():
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
    bill.get_bill_total()


    bill.generate_bill()


if __name__ == '__main__':
    main()