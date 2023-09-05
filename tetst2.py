from random import uniform

LOWEST_TEMP = 9.8
MAXIMUM_TEMP = 45.5

temps = []
for i in range(500):
    temps.append(uniform(LOWEST_TEMP, MAXIMUM_TEMP))

print(f"Max temprature in list: {max(temps)}")
print(f"Average temprature in list: {sum(temps) / len(temps)}")

print("Tempratures above 35 celcius in Jeddah:- ")
for temp in temps:
    if temp > 35:
        print(temp)
