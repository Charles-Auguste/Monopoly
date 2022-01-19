# test multiples de 33,22,11

def return_multiples():
    for i in range(1000):
        if (i%11 == 0 and i%22 == 0 and i%33 == 0):
            print(i)

return_multiples()