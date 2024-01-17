# -*- coding: utf-8 -*-
"""
Created on Sun May 09 10:42:56 2023

@author: balka
"""
def string_with_arrows(text, pos_start, pos_end): # bir metin içindeki belirli bir konum aralığını işaretleyen oklarla görsel bir şekilde vurgulamak için kullanılır.
    result = ''

    #pos_start ve pos_end parametrelerini kullanarak ilgili metin satırının ve sütununun bulunduğu konumları belirler. Daha sonra, işaretlenen satırın başından itibaren (col_start) ve satırın sonuna kadar (col_end) ok işaretlerini ekler. Bu işlem, işaretlenen aralığı görsel olarak vurgular.
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
   
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
       
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

       
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

    
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')
#Sonuç olarak, işaretlenmiş metin ve oklar içeren bir dize döndürülür. Bu dize, metindeki satır sonu karakterleri ve sekme karakterlerini temizler.