import time

a = int(input("Masukkan angka: "))
print("Hitung mundur dimulai!")

for i in range(a, 0, -1):
    print(i)
    time.sleep(1)
print("Waktu habis!")