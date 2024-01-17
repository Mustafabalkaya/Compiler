# -*- coding: utf-8 -*-
"""
Created on Sun May 09 14:42:14 2023

@author: balka
"""
# temel bir yorumlayıcıyı temsil eder ve kullanıcının ifadelerini çalıştırıp sonuçlarını döndürür.

import basic

while True:
    text = input('Lütfen İfadeyi Giriniz > ')

    result, error = basic.run('<stdin>', text)
    
    print(result)

    if error: print(error.as_string())

    elif result: print(result)