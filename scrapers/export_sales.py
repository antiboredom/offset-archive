import pandas as pd


def main():
    xl = pd.ExcelFile("./Voluntary-Registry-Offsets-Database--v9-December-2023.xlsx")
    acr = pd.read_excel(xl, "ACR Retirements")
    car = pd.read_excel(xl, "CAR Retirements")
    gold = pd.read_excel(xl, "Gold Retirements")
    ver = pd.read_excel(xl, "VCS Issuances & Retirements")
    print(acr, car, gold, ver)


if __name__ == "__main__":
    main()
