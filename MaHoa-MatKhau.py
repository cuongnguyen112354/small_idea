def CaNhan(firstCharTen, sumLenTen):
   ketQua = '{}#{}{}{}{}{}{}'
   print('Kết quả: ' + ketQua.format(firstCharTen, sumLenTen, sumLenTen+3, sumLenTen-3, sumLenTen*3, sumLenTen, sumLenTen//3))

def CongViec(firstCharTen, sumLenTen):
   ketQua = '{}${}{}{}{}{}{}'
   print('Kết quả: ' + ketQua.format(firstCharTen, sumLenTen, sumLenTen*4, sumLenTen//4, sumLenTen+4, sumLenTen, sumLenTen-4))

def MaHoa(ten, loai):
   splitTen = ten.split(' ')
   lenTen = []
   firstCharTen = ''
   sumLenTen = 0
   for i in splitTen:
      lenTen.append(len(i))
      firstCharTen += i[0]
   for i in lenTen:
      sumLenTen += i

   if loai == 3:
      CaNhan(firstCharTen, sumLenTen//len(lenTen))
   elif loai == 4:
      CongViec(firstCharTen, sumLenTen//len(lenTen))
   else:
      print('Tham số loại phải là 3 hoặc 4')

ten = str(input('Nhập tên ứng dụng: '))
loai = int(input('Nhập loại Cá nhân là "3" và Công việc là "4": '))
MaHoa(ten,loai)