import re
import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk



currenciesList = ["PLN", "EUR", "USD", "GBP", "CZK",    # Lista do sprawdzania czy wprowadzona przez uzytkownika waluta istnieje
                  "DKK", "HUF", "JPY", "RON", "SEK",
                  "CHF", "ISK", "NOK", "TRY", "AUD",
                  "BRL", "CAD", "CNY", "HKD", "IDR",
                  "ILS", "INR", "KRW", "MXN", "MYR",
                  "NZD", "PHP", "SGD", "THB", "ZAR",
                  "BGN",]
currentRate = {}                                        # Słownik waluty i jej wartości
URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"   # adres do aktualnych kursów walut z europejskiego banku centralnego w formacie XML


class bank():
    def __init__(self):
        self.update()
    def update(self):
        '''Metoda pobiera aktualne kursy walut z banku z adresu url,
        który jest plikiem formatu xml. Plik ten zostaje otwarty
        jako "file" a następnie za pomocą biblioteki ET
        przekształcony na strukturę danych typu drzewo
        '''
        response = requests.get(URL)                            # wykorzystanie funkcji get() z biblioteki request do pobierania zawartości URL
        with open("eurofxref-daily.xml", "wb") as file:
            file.write(response.content)
        tree = ET.parse("eurofxref-daily.xml")                  # Przeanalizowanie pliku XML przez funkcję parse() z biblioteki ET
        root = tree.getroot()                                   # i przekształcenie na strukturę drzewa przez funkcję getroot()
        '''Pętla wczytująca dane z drzewa pliku XML, przechodząca przez
        każdy element o budowie <Cube currency='BGN' rate='1.9558'/>
        i zapisujący go do słownika currentRate
        '''
        for i in range(0, 30):
            temp = root[2][0][i].attrib
            currentRate[temp['currency']] = 1/float(temp['rate'])
            pass
        self.set("PLN") # Zamieniamy od razu na pln bo z europejskiego banku pobiera z wartosciami dla eur


    def exist(self, currencyName):
        '''Metoda sprawdza czy waluta istnieje bez zmian w kwotach i kursach
        '''
        if currencyName in currenciesList:
            return True
        else:
            return False
        

    def set(self, newCurrency):
        '''Metoda sprawdza czy wprowadzona waluta istnieje sprawdzając listę currenciesList
        Jeśli tak metoda set zmienia walutę użytkownika, pozostawiając kwotę użytkownika bez zmian

        '''
        newCurrency = newCurrency
        if newCurrency != user1.currency and newCurrency in currenciesList:
            tempBalance = user1.balance
            self.changeRate(newCurrency)
            user1.balance = tempBalance

            return True
        else:
            return True


    def changeRate(self, newCurrency):
        '''Funkcja do przekształcenia słownika z kursami walut z kwotami
        dopasowanymi do wybranej aktualnie waluty
        '''
        user1.balance = user1.balance / currentRate[newCurrency]
        setValue = currentRate.get(newCurrency)
        for i in currentRate:
            if i != newCurrency:
                tempRate = currentRate.get(i)/setValue
                currentRate.update({i : tempRate})
            else:
                currentRate.update({i: 1/setValue})
        currentRate[user1.currency] = currentRate.pop(newCurrency)
        user1.currency = newCurrency
        return


class user():
    def __init__(self, balance, currency, currencyBuy):
        self.balance = balance              # Wybrana przez uzytkownika waluta (domyślnie EUR - aktualne kursy walut są pobrane
        self.currency = currency
        self.currencyBuy = currencyBuy         # z europejskiego banku z wartościami dla EUR. Później jest możliwość przekształcenia waluty i cen)


def btnSell(name):
    menuButtonSell.configure(text = name)
    cantor.set(name)
    updateCantorDisplay()
    if name == user1.currencyBuy:
        exchangeValue = entry_var.get()
        buyValue.configure(text = exchangeValue)
        return
    exchangeValue = float(entry_var.get()) / currentRate[user1.currencyBuy]
    buyValue.configure(text = exchangeValue)


def btnBuy(name):
    menuButtonBuy.configure(text = name)
    user1.currencyBuy = name
    if name == user1.currency:
        exchangeValue = entry_var.get()
        buyValue.configure(text = exchangeValue)
        return
    exchangeValue = float(entry_var.get()) / currentRate[user1.currencyBuy]
    buyValue.configure(text = exchangeValue)


def on_entry_change(var, index, mode):
    exchangeValue = float(entry_var.get()) / currentRate[user1.currencyBuy]
    buyValue.configure(text = exchangeValue)
user1 = user(0, "EUR", "EUR")
cantor = bank()



window = tk.Tk()
window.title("Kantor")
window.geometry("450x300")
window.columnconfigure(0, weight = 66)
window.columnconfigure(1, weight = 34)

exchangeDisplay = tk.Frame(master = window)
exchangeDisplay.grid(row = 0, column = 0)

userMenu = tk.Frame(master = window)
userMenu.grid(row = 0, column = 1)

menuButtonSell = ttk.Menubutton(master = userMenu, text = "PLN", direction='left')
menuButtonSell.grid(row = 0, column = 0, sticky = 'E')

menuButtonSell_sub_menu = tk.Menu(menuButtonSell, tearoff = False)

for currency in currenciesList:
    menuButtonSell_sub_menu.add_command(label = currency, command = lambda currency = currency: btnSell(currency))
menuButtonSell.configure(menu = menuButtonSell_sub_menu)

menuButtonBuy = ttk.Menubutton(master = userMenu, text = "EUR", direction='left')
menuButtonBuy.grid(row = 1, column = 0, sticky = 'E')

menuButtonBuy_sub_menu = tk.Menu(menuButtonBuy, tearoff = False)

for currency in currenciesList:
    menuButtonBuy_sub_menu.add_command(label = currency, command = lambda currency = currency: btnBuy(currency))
menuButtonBuy.configure(menu = menuButtonBuy_sub_menu)

buyValue = tk.Label(master = userMenu, text = "0")
buyValue.grid(row = 1, column = 1, sticky = 'W')

entry_var = tk.StringVar()
entry_var.trace_add("write", on_entry_change)

entryValue = tk.Entry(master = userMenu, textvariable = entry_var)
entryValue.grid(row = 0, column = 1, sticky = 'W')



    
def updateCantorDisplay():
    i = 0
    j = 0
    for name in currenciesList:
        if i == int(len(currenciesList)/2):
            j = 4
            i = 0
        if user1.currency == name:
            continue
        currency = name
        currencySellValue = currency + "SellValue"
        value = str("     " + "%.4f" % currentRate[currency])

        currency = ttk.Label(master = exchangeDisplay, text = currency)
        currency.grid(row = i, column = 1 + j, sticky = 'w')

        currencySellValue = ttk.Label(master= exchangeDisplay, text = value)
        currencySellValue.grid(row = i, column = 2 + j, sticky = 'e')

        empty2 = ttk.Label(master = exchangeDisplay, text = "       ")
        empty2.grid(row = i, column = 3 + j)

        i += 1
        

updateCantorDisplay()
window.mainloop() 









