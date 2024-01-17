# -*- coding: utf-8 -*-
"""
Created on Sun May 08 12:28:15 2023

@author: balka
"""
import string

from string_with_arrows import *

DIGITS = '0123456789' #DIGITS sabiti '0123456789' değerine atanıyor.

LETTERS = string.ascii_letters #LETTERS sabiti, string.ascii_letters ifadesi kullanılarak tüm harfleri içeren bir dizeye atanıyor. Bu, hem büyük harfleri ('ABCDEFGHIJKLMNOPQRSTUVWXYZ') hem de küçük harfleri ('abcdefghijklmnopqrstuvwxyz') içerir.

LETTERS_DIGITS = LETTERS + DIGITS #LETTERS_DIGITS sabiti, LETTERS ve DIGITS dize sabitlerinin birleştirilmesiyle oluşturuluyor. Bu, hem harfleri hem de rakamları içeren bir dizeyi temsil eder.

class Error: #Burda karşılaşılacak olan hataları ve bu hataların ne olduğunu gösteren bir sınıf oluşturduk ve gerekli işlemleri gerçekleştirdik
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details


    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result
class IllegalCharError(Error): #IllegalCharError sınıfı geçersiz karakter hatası için özel işlemler veya ayrıntılar ekleyebilir. Bu, kodun hatayı daha iyi işlemesini ve hata türlerini daha iyi ayırt etmesini sağlar.
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Character', details)


class ExpectedCharError(Error): #ExpectedCharError sınıfı beklenen karakter hatası için özel işlemler veya ayrıntılar ekleyebilir
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error): #InvalidSyntaxError sınıfı geçersiz sözdizimi hatası için özel işlemler veya ayrıntılar ekleyebilir
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Geçersiz Syntax', details)


class RTError(Error): #RTError sınıfı çalışma zamanı hatası için özel işlemler veya ayrıntılar ekleyebilir. Ayrıca, context parametresi aracılığıyla hatanın bağlamını da ekleyebilir, yani hatanın hangi durumda ve hangi bağlamda ortaya çıktığını temsil edebilir
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context
    
    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result
               


class Position: #Bu kod, bir derleyici yazılımların temel bileşenlerini temsil etmek için kullanılabilir. 
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)



TT_INT = 'TT_INT' 
TT_FLOAT = 'FLOAT'  
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'    
TT_MINUS = 'MINUS'  
TT_DIV = 'DIV'    
TT_MUL = 'MUL'      
TT_EQ = 'EQ'        
TT_POW = 'POW'
TT_LPAREN = 'LPAREN'  
TT_RPAREN = 'RPAREN'
TT_EOF = "EOF"
TT_EE = 'EE'  
TT_NE = 'NE'  
TT_LT = 'LT'  
TT_GT = 'GT'  
TT_LTE = 'LTE' 
TT_GTE = 'GTE' 
KEYWORDS = [
    'BALKAYA',   
    'AND',   
    'OR',    
    'NOT',   
    'IF',    
    'THEN',  
    'ELIF',  
    'ELSE',     
    'TO',    
    'STEP',  
    'WHILE'  
]
class Token:#Token sınıfı, bir derleyicide kullanılan bir tokeni temsil eder. 
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):#bir tokenin türünü (type_), değerini (value), başlangıç (pos_start) ve bitiş (pos_end) pozisyonlarını alır. Başlangıç pozisyonu belirtilmişse, pos_start'ın bir kopyasını alarak pos_start ve pos_end'i ayarlar. pos_end'i bir karakter ilerleterek günceller.
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    
    def matches(self, type_, value):#matches yöntemi, bir tokenın belirli bir tür ve değere sahip olup olmadığını kontrol eder. Eşleşme durumunda True, aksi takdirde False döndürür.
        return self.type == type_ and self.value == value

    
    def __repr__(self):#_repr__ yöntemi, bir tokenin dize temsilini döndürür. Eğer tokenin değeri varsa, type:value formatında bir dize döndürülür. Değer yoksa, sadece type döndürülür.
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer: #Lexer sınıfı, bir metin içindeki karakterleri tokenlere dönüştürmek için kullanılır.
    
    def __init__(self, fn, text): #bu yöntem, fn (dosya adı) ve text (metin) parametrelerini alır. pos (konum) ve current_char (geçerli karakter) özelliklerini ayarlar ve advance yöntemini çağırarak başlangıç pozisyonunu günceller.
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):#advance yöntemi, konumu ve geçerli karakteri günceller.

       
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

   
    def make_tokens(self):#make_tokens yöntemi, metinden token listesi oluşturur. Geçerli karakter None olana kadar döngü devam eder.

        tokens = [] #Döngü içinde farklı durumları kontrol ederek ilgili tokenleri oluşturur ve tokens listesine ekler.        
        while self.current_char != None:
            
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            
            elif self.current_char == '+':
               
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()  
               
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
               
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
             
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                self.advance()
            
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    
    def make_number(self): #make_number yöntemi, sayı tokenlerini oluşturur. Sayıyı oluştururken nokta kullanımını kontrol eder.       
        num_str = ''
       
        dot_count = 0 
        pos_start = self.pos.copy()
    
        while self.current_char != None and self.current_char in DIGITS + '.':
          
            if self.current_char == '.':
                if dot_count == 1:  
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
               
            self.advance()

          
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
       
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    
    def make_identifier(self): #make_identifier yöntemi, tanımlayıcı tokenlerini oluşturur. Harf, rakam veya alt çizgi karakterlerini içerir.
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
         
        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (sonra '!')")    
    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)  
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)    
    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
class NumberNode:#Bu sınıfımız bir sayı düğümünü temsil eder. Sayı düğümü, bir sayıyı içeren bir tokenle ilişkilendirilir ve bu düğümün pozisyon bilgileri tutulur. Bu düğüm, bir dil ağacı (AST) yapısında kullanılabilir ve sayısal ifadeleri temsil eden bir bileşen olarak işlev görür.
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    
    def __repr__(self):
        return f'{self.tok}'


class VarAccessNode: #Bu sınıfımız bir değişken erişimi düğümünü temsil eder. Değişken erişimi düğümü, bir değişken adı tokeni ile ilişkilendirilir ve bu düğümün pozisyon bilgileri tutulur. Bu düğüm, bir dil ağacı (AST) yapısında kullanılabilir ve değişken erişimini temsil eden bir bileşen olarak işlev görür.
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode: #Bu sınıfımız bir değişken atama düğümünü temsil eder. Değişken atama düğümü, bir değişken adı tokeni ve bir değer düğümü ile ilişkilendirilir. Bu düğüm, bir dil ağacı (AST) yapısında kullanılabilir ve değişken atamasını temsil eden bir bileşen olarak işlev görür.
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode: #Bu sınıfımız bir ikili işlem düğümünü temsil eder. İkili işlem düğümü, bir işlemi (ör. toplama, çıkarma, çarpma) temsil eden bir operatör tokeni ve sol ile sağ operandları temsil eden alt düğümlerle ilişkilendirilir. Bu düğüm, bir dil ağacı (AST) yapısında kullanılabilir ve ikili işlemleri temsil eden bir bileşen olarak işlev görür.
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode: #Bu sınıfımız bir tekli işlem düğümünü temsil eder. Tekli işlem düğümü, bir işlemi (ör. artı, eksi) temsil eden bir operatör tokeni ve işlemi uygulanacak düğümü (node) içerir. Bu düğüm, bir dil ağacı (AST) yapısında kullanılabilir ve tekli işlemleri temsil eden bir bileşen olarak işlev görür.
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class IfNode: #Bu sınıfımız birden çok koşulun olduğu bir "if-else" ifadesini temsil eden bir düğüm oluşturur. Her bir koşul ifadesi ve ilgili kod bloğu cases listesinde bulunur ve else_case özelliği ile opsiyonel olarak belirtilen "else" durumu kontrol edilir. Bu düğüm, programın akışını kontrol etmek için kullanılan bir yapıdır ve belirli koşullara bağlı olarak farklı kod bloklarını çalıştırır.
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (
            self.else_case or self.cases[len(self.cases) - 1][0]).pos_end



class WhileNode: #Bu sınıfımız bir koşulun doğru olduğu sürece tekrarlanan bir döngüyü temsil eden bir düğüm oluşturur. Koşul, condition_node özelliği ile ifade edilir ve döngü gövdesi, body_node özelliği ile belirtilen kod bloğunu içerir. Bu düğüm, bir koşulu kontrol eder ve koşul doğru olduğu sürece döngü gövdesini tekrar tekrar çalıştırır.
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


class ParseResult: #Bu sınıfımız ayrıştırma işleminin sonucunu takip etmek için kullanılan ParseResult sınıfını temsil eder. Bu sınıf, ilerleme sayısını, olası bir hata durumunu ve elde edilen düğümü (node) tutar. Ayrıca, ayrıştırma işleminde ilerlemeyi ve hata durumunu kaydetmek için çeşitli yöntemler sağlar.
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

class Parser: #Parser sınıfı, belirli bir dilin ifadelerini ayrıştırmak için kullanılır.
    def __init__(self, tokens): #tokens listesini alır ve tok_idx ve current_tok özelliklerini başlatır. tok_idx başlangıçta -1 olarak ayarlanır ve advance yöntemi çağrılarak bir ilerleme sağlanır.
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ): #tok_idx değerini bir birim artırır ve eğer geçerli bir belirteç (token) varsa, current_tok özelliğine bu belirteci atar. Son olarak, current_tok değerini döndürür.

        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):#ifadeyi ayrıştırır ve ParseResult nesnesi döndürür. Eğer bir hata yoksa ve belirteçlerin sonuna gelinmemişse, geçersiz sözdizimi hatası oluşturulur.
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
               
            ))
        return res

    def if_expr(self): #IF ifadesini ayrıştırır. İfade başladığında IF belirteci kontrol edilir ve uygun hatalar oluşturulur. Ardından, expr yöntemi kullanılarak koşul ve ifade ayrıştırılır. Koşul-ifade çifti, cases listesine eklenir. Daha sonra, ELIF ifadesi varsa, aynı işlem tekrarlanır. Son olarak, ELSE ifadesi varsa, else_case değişkenine ifade ayrıştırılır. IfNode düğümü oluşturulur ve başarıyla sonuçlandırılır.
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"IF' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'THEN' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"'THEN' Bekleniyor"
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))


    def while_expr(self): #WHILE döngüsünü ayrıştırır. İfade başladığında WHILE belirteci kontrol edilir ve uygun hatalar oluşturulur. Ardından, expr yöntemi kullanılarak koşul ve döngü gövdesi ayrıştırılır. WhileNode düğümü oluşturulur ve başarıyla sonuçlandırılır.
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'WHILE' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'THEN' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def atom(self): #temel ifadeleri ayrıştırır. Bu ifadeler arasında sayılar, tanımlayıcılar, parantez içindeki ifadeler, IF ifadesi ve WHILE döngüsü yer alır. Uygun düğüm oluşturulur ve başarıyla sonuçlandırılır.
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "')' Bekleniyor"
                ))

        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

       

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Beklenenler int, float, identifier, '+', '-', '('"
        ))
    
#matematiksel operatörleri ve karşılaştırma operatörlerini içeren ifadeleri

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    #Matematiksel işlemler için  kullanacağımız ifade
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    #Eşitlkik Kontrol İfadeleri ( ==, <=, vb.)
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(
            self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Beklenen int, float, tipidedir, '+', '-', '(' veya 'NOT'"
            ))

        return res.success(node)  #Sonucu Dön

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'BALKAYA'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Tanımlayıcı Bekleniyor"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Bekleniyor'='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(
            self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Beklenen 'BALKAYA', int, float, identifier, '+', '-' veya '('"
            ))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)


class RTResult: #çalışma zamanı sonuçlarını temsil eder 
    def __init__(self): #value ve error özelliklerini başlatır. Başlangıçta, value ve error değerleri None olarak ayarlanır.
        self.value = None
        self.error = None

    def register(self, res): #başka bir RTResult nesnesini alır. Eğer bu nesne bir hata içeriyorsa, error özelliğini bu hatayla günceller. Aksi takdirde, value özelliğini döndürür.
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value): # bir değeri başarıyla temsil eden bir RTResult nesnesini oluşturur. Bu değer value özelliğine atanır ve nesne döndürülür.
        self.value = value
        return self

    def failure(self, error): # bir hatayı temsil eden bir RTResult nesnesini oluşturur. Bu hata error özelliğine atanır ve nesne döndürülür.
        self.error = error
        return self


class Number: #Number sınıfı, bir sayı değerini temsil eder. Bu sayı değeri, value özelliğiyle tutulur. Ayrıca, konum bilgisini (pos_start ve pos_end) ve bağlam bilgisini (context) içeren özelliklere de sahiptir.
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Sıfır(0) a bölme hatası',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

    #Üs(Kuvvet Alma)
    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
    #Eşitlik Durumu
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
    #Eşit Değil Durumu (Değil Eşit)
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
    #Küçüktür Durumu
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
    #Büyüktür Durumu
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
    #Küçük Eşittir Durumu
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
    #Büyük Eşittir Durumu
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
    #VE Durumu
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
    #VEYA Durumu
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
    #Değil Durumu (not)
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    def is_true(self):
        return self.value != 0

    def copy(self): #bir Number nesnesinin değerini ve diğer özelliklerini koruyarak bir kopya oluşturmak için kullanılabilir. Bu kopya, bağımsız olarak kullanılabilir veya başka işlemlerde kullanılabilir.
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


class Context: #Bu sınıfımız, dilbilgisel yapıları yönetmek ve yürütme sırasında bağlamları takip etmek için kullanılır.
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


class SymbolTable: #Bu Sınıfımız dilbilgisel yapıları yönetmek ve sembol tablosu üzerinde sembol değerlerini saklamak ve erişmek için kullanılır.
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
class Interpreter: # Interpreter sınıfı, AST (Abstract Syntax Tree) düğümlerini ziyaret ederek ifadelerin yorumlanmasını gerçekleştirir. Her düğüm türü için bir visit metoduna sahiptir.run fonksiyonu, kaynak kodu alır ve onu parçalayarak tokenlara ayırır (lexer), ardından bu tokenları kullanarak bir soyut sentaks ağacı oluşturur (parser). Son olarak, oluşturulan AST'yi yorumlayıcıya geçirir ve sonucu döndürür. 
    def visit(self, node, context): #visit metodu, AST düğümlerini ziyaret eder ve ilgili visit metodu bulunamazsa no_visit_method metoduyla birlikte hata oluşturur.       
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')    
    def visit_NumberNode(self, node, context): #sayı düğümünü ziyaret eder, sayıyı oluşturur ve sonucunu döndürür
        return RTResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )
    def visit_VarAccessNode(self, node, context): #değişken erişim düğümünü ziyaret eder, sembol tablosunda ilgili değişkeni arar ve değerini döndürür.
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' tanımlanmadı.",
                context
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    def visit_VarAssignNode(self, node, context): # değişken atama düğümünü ziyaret eder, sağ tarafındaki değeri ziyaret eder ve sembol tablosuna değişkeni ve değerini ekler.
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context): #ikili operatör düğümünü ziyaret eder, sol ve sağ taraftaki ifadeleri ziyaret eder ve ilgili operatöre göre işlem yapar.
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context): #tekli operatör düğümünü ziyaret eder, içindeki ifadeyi ziyaret eder ve ilgili operatöre göre işlem yapar.
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context): # koşul düğümünü ziyaret eder, koşulu değerlendirir ve uygun duruma göre ilgili ifadeyi ziyaret eder
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context): # döngü düğümünü ziyaret eder, başlangıç, bitiş ve adım ifadelerini ziyaret eder ve belirtilen koşullara göre döngüyü çalıştırır.
        res = RTResult()
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res
        if node.step_value_node:
            step_value = res.register(
                self.visit(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)
        i = start_value.value
        if step_value.value >= 0:
            def condition(): return i < end_value.value
        else:
            def condition(): return i > end_value.value
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)
    
    def visit_WhileNode(self, node, context): #while döngüsü düğümünü ziyaret eder, koşulu değerlendirir ve koşul doğru olduğu sürece döngüyü çalıştırır.
        res = RTResult()
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res
            if not condition.is_true():
                break
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)
    


global_symbol_table = SymbolTable() # sembol tablosunu temsil eder. Değişken adları ve değerleri arasındaki ilişkiyi yönetir.   
global_symbol_table.set("NULL", Number(0))

global_symbol_table.set("FALSE", Number(0))

global_symbol_table.set("TRUE", Number(1))



def run(fn, text): 
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
