def tinh_laiKep(p, r, n, t):
   return p * (1 + r/n) ** (n * t)

p = int(input('Số tiền gốc: '))
r = float(input('Lãi suất hằng năm: '))
n = int(input('Số kì tính lãi suất 1 năm: '))
t = int(input('Số năm: '))

result = tinh_laiKep(p, r, n, t)
print(f'Kết quả: {result}')