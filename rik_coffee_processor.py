import json
from datetime import datetime

class TransactionProcessor:
    def __init__(self):
        self.branches_data = {}
        self.products_data = {}

    def parse_raw_transaction(self, raw_str):
        try:
            # Vi du chuoi raw: '30, 50, Ca phe sua, 100, TP.HCM, 15/08/2025'
            # Quy uoc thu tu: [So_Luong, Don_Gia, Ten_Mon, Ma_Ban, Chi_Nhanh, Ngay_Giao_Dich]
            parts = [p.strip() for p in raw_str.split(',')]
            if len(parts) < 6:
                raise ValueError('Du lieu khong du cac truong thong tin can thiet')

            quantity = int(parts[0])
            unit_price = float(parts[1])
            product_name = parts[2]
            table_no = parts[3]
            branch_name = parts[4]
            date_str = parts[5]

            # Kiem tra tinh hop le cua du lieu
            if quantity <= 0 or unit_price < 0:
                raise ValueError('So luong hoac don gia khong hop le')

            total_amount = quantity * unit_price

            return {
                'quantity': quantity,
                'unit_price': unit_price,
                'product_name': product_name,
                'table_no': table_no,
                'branch_name': branch_name,
                'date': date_str,
                'total_amount': total_amount
            }
        except Exception as e:
            print(f'Loi khi phan tich cu phap dong du lieu: {raw_str}. Chi tiet: {str(e)}')
            return None

    def aggregate_transaction(self, transaction):
        if not transaction:
            return

        branch = transaction['branch_name']
        product = transaction['product_name']
        amount = transaction['total_amount']

        # Cong don doanh thu theo chi nhanh
        if branch not in self.branches_data:
            self.branches_data[branch] = 0.0
        self.branches_data[branch] += amount

        # Cong don doanh thu theo san pham
        if product not in self.products_data:
            self.products_data[product] = 0
        self.products_data[product] += transaction['quantity']

    def generate_dashboard_report(self):
        print('=== DASHBOARD QUAN LY RIK-COFFEE ===')
        print(f'Thoi gian xuat bao cao: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        print('------------------------------------')
        
        print('1. DOANH THU THEO CHI NHANH:')
        for branch, revenue in self.branches_data.items():
            print(f' - Chi nhanh {branch}: {revenue:,.0f} VND')
        
        print('\n2. SAN PHAM BAN CHAY (SO LUONG):')
        sorted_products = sorted(self.products_data.items(), key=lambda x: x[1], reverse=True)
        for product, qty in sorted_products:
            print(f' - {product}: {qty} ly')
        print('====================================')

if __name__ == '__main__':
    # Gia lap danh sach cac hoa don thong tin tho nhan duoc tu cac chi nhanh
    raw_invoices = [
        '30, 50000, Ca phe sua, 100, TP.HCM, 15/08/2025',
        '15, 45000, Bac xiu, 102, TP.HCM, 15/08/2025',
        '40, 50000, Ca phe sua, 201, Ha Noi, 15/08/2025',
        '25, 60000, Tra dao, 105, Da Nang, 15/08/2025',
        '10, 50000, Ca phe sua, 104, TP.HCM, 15/08/2025',
        'loi_du_lieu_khong_hop_le_123', 
        '-5, 50000, Ca phe den, 101, TP.HCM, 15/08/2025'
    ]

    processor = TransactionProcessor()
    
    print('Bat dau qua trinh doc va chuan hoa du lieu dau vao...')
    for invoice in raw_invoices:
        parsed_data = processor.parse_raw_transaction(invoice)
        if parsed_data:
            processor.aggregate_transaction(parsed_data)
            
    print('\nDu lieu da duoc xu ly thanh cong. Dang tai tao Dashboard...\n')
    processor.generate_dashboard_report()