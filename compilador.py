import re
input_file_list = []
number =[]
string = []

class PrePro:
    @staticmethod
    def espaco(input):
        for line in input:
            for char in line:
                if(char != "\n"):
                    input_file_list.append(char)
        input_file_string = ''.join(map(str, input_file_list))

        espaco_entre_numeros = re.search('[0-9] +[0-9]', input_file_string)
        espaco_entre_numeros_e_letras = re.search('[a-z] +[0-9]', input_file_string)

        if espaco_entre_numeros or espaco_entre_numeros_e_letras:
            raise Exception("Erro nos espaços")
        else:
            input_sem_espaco = input_file_string.replace(" ","")
            return input_sem_espaco

    @staticmethod
    def comentarios(input):
        input_sem_comentarios = re.sub('/\*(.*?)\*/', '', input)
        input_com_comentario_errado = re.search('/\*', input_sem_comentarios)
        if input_com_comentario_errado:
            raise Exception("Erro no comentario")
        return input_sem_comentarios

class Node:
    def __init__ (self,value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, table):
        pass

class ProgOp(Node):
    def evaluate(self,table):
        self.children.evaluate(table)

class FuncDec(Node):
    def evaluate(self,table):
        table.set("") #TODO

class FuncCall(Node):
    def evaluate(self,table):
        table.set("") #TODO chamar funcoes 

class CmdsOp(Node):    
    def evaluate(self, table):
        for child in self.children:
            child.evaluate(table)

class VarDec(Node):    
    def evaluate(self, table):
        for child in self.children:
            table.set(child.value, None, self.value)

class TriOp(Node):
    def evaluate(self, table):
        if(self.value == 'IF'):
            val_exp = self.children[0].evaluate(table)
            if(self.children[2] != None):
                if(val_exp):
                    self.children[1].evaluate(table)
                else:
                    self.children[2].evaluate(table)
            else:
                if(val_exp):
                    self.children[1].evaluate(table)
        else:
            raise Exception("Erro no Triop")
    
class BinOp(Node):
    def evaluate(self, table):
        if self.value ==  'ATRI':
            if table.check(self.children[0].value):
                tipo_val_esq = table.get(self.children[0].value)[1]
                tipo_val_dir = self.children[1].evaluate(table)[1]
                if(tipo_val_esq == tipo_val_dir):
                    table.set(self.children[0].value, self.children[1].evaluate(table),  tipo_val_esq)
                else:
                    raise Exception("Erro: Tipos diferentes")
        else:
            val_esq = self.children[0].evaluate(table)
            if self.value == 'WHILE':
                while(val_esq):
                    self.children[1].evaluate(table)
                    val_esq = self.children[0].evaluate(table)
            else:
                val_dir = self.children[1].evaluate(table)
                if (val_esq[1] == val_dir[1]):
                    val_esq = val_esq[0]
                    val_dir = val_dir[0]
                    if self.value == 'PLUS':
                        return [val_esq + val_dir,  'INT']
                    elif self.value == 'MINUS':
                        return [val_esq - val_dir, 'INT']
                    elif self.value == 'MULT':
                        return [val_esq * val_dir, 'INT']
                    elif self.value == 'DIV':
                        return [val_esq // val_dir, 'INT']
                    elif self.value == 'AND':
                        return [val_esq and val_dir, 'CHAR']
                    elif self.value == 'OR':
                        return [val_esq or val_dir, 'CHAR']
                    elif self.value == 'GREATER':
                        return [val_esq > val_dir, 'CHAR']
                    elif self.value == 'LESS':
                        return [val_esq < val_dir, 'CHAR']
                    elif self.value == 'EQUAL':
                        return [val_esq == val_dir, 'CHAR']
                    else:
                        raise Exception("Erro no Binop")
                else:
                    raise Exception("Erro: Tipos diferentes")

class UnOp(Node):
    def evaluate(self,table):
        child = self.children[0].evaluate(table)
        if self.value == 'PLUS':
            return child
        elif self.value == 'MINUS':
            return -child
        elif self.value == 'PRINTF':
            print(child)
        elif self.value == 'NOT':
            return not child
        else:
            raise Exception("Erro no UnOp")

class IntVal(Node):
    def evaluate(self,table):
        return [int(self.value), 'INT']

class VarVal(Node):
    def evaluate(self, table):
        v = table.get(self.value)
        return v[0]

class Scanf(Node):
    def evaluate(self, table):
        return [int(input()), 'INT'] 

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, table):
        pass

class SymbleTable(object):
    def __init__(self):
        self.table = {}
    
    def get(self, var):
        return self.table[var]
    
    def set(self, var, value, tipo):
        self.table[var] = [value, tipo]
    
    def check(self, var):
        return var in self.table

class Token(object):

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador(object):

    def __init__(self, origem, posicao, atual):
        self.origem = origem
        self.posicao = posicao
        self.atual = atual
    
    def selecionarProximo(self):

        if(self.posicao == len(self.origem)):
            t = Token('FIM', 'null')
            self.atual = t
       
        else:
            character = self.origem[self.posicao]
            if(character == ' '):
                while((self.posicao != len(self.origem)) and character== ' '):
                    self.posicao = self.posicao+1
                    character = self.origem[self.posicao]
                if(self.posicao == len(self.origem)):
                    t = Token('FIM', 'null')
                    self.atual = t

            character = self.origem[self.posicao]

            if(character.isdigit()):
                while(character.isdigit()):
                    number.append(character)
                    self.posicao = self.posicao+1
                    if(self.posicao != len(self.origem)):
                        character = self.origem[self.posicao]
                    else:
                        break

                number_token = ''.join(map(str, number))
                t = Token('INT', number_token)
                self.atual = t
                del number[:]
            
            elif(character.isalpha()):
                while(character.isalpha() or character.isdigit() or character == "_"):
                    string.append(character)
                    self.posicao = self.posicao+1
                    if(self.posicao != len(self.origem)):
                        character = self.origem[self.posicao]
                    else:
                        break

                string_token = ''.join(map(str, string))
                if(string_token == "printf"):    
                    t = Token('PRINTF', string_token)
                elif(string_token == "scanf"):    
                    t = Token('SCANF', string_token)
                elif(string_token == "if"):    
                    t = Token('IF', string_token)
                elif(string_token == "else"):    
                    t = Token('ELSE', string_token)
                elif(string_token == "while"):    
                    t = Token('WHILE', string_token)
                elif(string_token == "void"):    
                    t = Token('VOID', string_token)
                elif(string_token == "int"):    
                    t = Token('INT', string_token)
                elif(string_token == "char"):    
                    t = Token('CHAR', string_token)
                elif(string_token == "return"):    
                    t = Token('RETURN', string_token)
                else:
                    t = Token('VAR', string_token)
                self.atual = t
                del string[:]
            
            elif character == "+":
                t = Token('PLUS', 'null')
                self.atual = t
                self.posicao = self.posicao+1 

            elif character is '-':
                t=Token('MINUS', 'null') 
                self.atual = t
                self.posicao = self.posicao+1 

            elif character == '/':
                t = Token('DIV', 'null')
                self.atual = t
                self.posicao = self.posicao+1

            elif character == '*':
                t = Token('MULT', 'null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '(':
                t = Token('OPEN_P','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == ')':
                t = Token('CLOSE_P','null')
                self.atual = t
                self.posicao = self.posicao+1

            elif character == '{':
                t = Token('OPEN_C','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '}':
                t = Token('CLOSE_C','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '=':
                if(self.origem[self.posicao+1] != '='):
                    t = Token('ATRI','null')
                    self.atual = t
                    self.posicao = self.posicao+1
                else:
                    self.posicao = self.posicao+1
                    t = Token('EQUAL','null')
                    self.atual = t
                    self.posicao = self.posicao+1
            
            elif character == ';':
                t = Token('SEMICOLON','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == ',':
                t = Token('COLON','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '&':
                if(self.origem[self.posicao+1] == '&'):
                    self.posicao = self.posicao+1
                    t = Token('AND','null')
                    self.atual = t
                    self.posicao = self.posicao+1

            elif character == '|':
                if(self.origem[self.posicao+1] == '|'):
                    self.posicao = self.posicao+1
                    t = Token('OR','null')
                    self.atual = t
                    self.posicao = self.posicao+1
            
            elif character == '!':
                t = Token('NOT','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '>':
                t = Token('GREATER','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '<':
                t = Token('LESS','null')
                self.atual = t
                self.posicao = self.posicao+1
   
    def peek(self, num):
        pos = self.posicao
        for x in range (0, num):
            if(pos == len(self.origem)):
                t = Token('FIM', 'null')
            else:
                character = self.origem[pos]
                if(character == ' '):
                    while((pos != len(self.origem)) and character== ' '):
                        pos = pos+1
                        character = self.origem[pos]
                    if(pos == len(self.origem)):
                        t = Token('FIM', 'null')
                        
                character = self.origem[pos]

                if(character.isdigit()):
                    while(character.isdigit()):
                        number.append(character)
                        pos = pos+1
                        if(pos != len(self.origem)):
                            character = self.origem[pos]
                        else:
                            break

                    number_token = ''.join(map(str, number))
                    t = Token('INT', number_token)
                    del number[:]
                
                elif(character.isalpha()):
                    while(character.isalpha() or character.isdigit() or character == "_"):
                        string.append(character)
                        pos = pos+1
                        if(pos != len(self.origem)):
                            character = self.origem[pos]
                        else:
                            break

                    string_token = ''.join(map(str, string))
                    if(string_token == "printf"):    
                        t = Token('PRINTF', string_token)
                    elif(string_token == "scanf"):    
                        t = Token('SCANF', string_token)
                    elif(string_token == "if"):    
                        t = Token('IF', string_token)
                    elif(string_token == "else"):    
                        t = Token('ELSE', string_token)
                    elif(string_token == "while"):    
                        t = Token('WHILE', string_token)
                    elif(string_token == "void"):    
                        t = Token('VOID', string_token)
                    elif(string_token == "int"):    
                        t = Token('INT', string_token)
                    elif(string_token == "char"):    
                        t = Token('CHAR', string_token)
                    elif(string_token == "return"):    
                        t = Token('RETURN', string_token)
                    else:
                        t = Token('VAR', string_token)
                    
                    del string[:]
                
                elif character == "+":
                    t = Token('PLUS', 'null')

                elif character is '-':
                    t=Token('MINUS', 'null') 

                elif character == '/':
                    t = Token('DIV', 'null')

                elif character == '*':
                    t = Token('MULT', 'null')

                elif character == '(':
                    t = Token('OPEN_P','null')

                elif character == ')':
                    t = Token('CLOSE_P','null')

                elif character == '{':
                    t = Token('OPEN_C','null')

                elif character == '}':
                    t = Token('CLOSE_C','null')

                elif character == '=':
                    if(self.origem[pos+1] != '='):
                        t = Token('ATRI','null')

                    else: 
                        t = Token('EQUAL','null')

                elif character == ';':
                    t = Token('SEMICOLON','null')

                elif character == ',':
                    t = Token('COLON','null')

                elif character == '&':
                    if(self.origem[pos+1] == '&'):
                        
                        t = Token('AND','null')

                elif character == '|':
                    if(self.origem[pos+1] == '|'):
                        
                        t = Token('OR','null')

                elif character == '!':
                    t = Token('NOT','null')

                elif character == '>':
                    t = Token('GREATER','null')

                elif character == '<':
                    t = Token('LESS','null')
        return t
            

class Analisador(object):

    def __init__(self,tokens,table):
        self.tokens = tokens
        self.table = table
        self.numFunc = 0
    
    def programa(self):
        raiz_children = [] 
        while(self.tokens.atual.tipo != 'FIM'):
            self.numFunc+=1
            func_dec_children =[]
            func_dec_children.append(self.tipo())
            if(self.tokens.atual.tipo == 'VAR'):
                name_func = self.tokens.atual.valor
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'OPEN_P'):
                    self.tokens.selecionarProximo()
                    while(self.tokens.atual.tipo != 'CLOSE_P'):
                        tipo_arg = self.tipo()
                        arg = VarVal(self.tokens.atual.valor,[])
                        vd = VarDec (tipo_arg, [arg])
                        func_dec_children.append(vd)
                        self.tokens.selecionarProximo()
                        while(self.tokens.atual.tipo == 'COLON'):
                            self.tokens.selecionarProximo()
                            tipo_arg = self.tipo()
                            arg = VarVal(self.tokens.atual.valor,[])
                            vd = VarDec (tipo_arg, [arg])
                            func_dec_children.append(vd)
                            self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'CLOSE_P'):
                        self.tokens.selecionarProximo()
                        func_dec_children.append(self.comandos())
                        fd = FuncDec(name_func, func_dec_children)
                        raiz_children.append(fd)
                        self.tokens.selecionarProximo()
                    else:
                        raise Exception ("Erro: Fechar Parenteses")
                else:
                    raise Exception ("Erro: Abrir Parenteses")
            else:
                raise Exception ("Erro: Func")
        self.numFunc-=1
        if(self.numFunc==0):
            fc = FuncCall('main', [])
            raiz_children.append(fc)
            return CmdsOp(None, raiz_children) 

    def comandos(self):
        if(self.tokens.atual.tipo == 'OPEN_C'):
            self.tokens.selecionarProximo()
            comandos_children = []
            while(self.tokens.atual.tipo != 'CLOSE_C' and self.tokens.atual.tipo != 'FIM'):
                cmd = self.comando()
                comandos_children.append(cmd)
            if(self.tokens.atual.tipo == 'CLOSE_C'):
                return CmdsOp(None, comandos_children)
            elif(self.tokens.atual.tipo == 'FIM'):
                return
            else:
                raise Exception("Erro: Fechar Chaves")
        else:
            raise Exception ("Erro: Abrir Chaves")

    def tipo(self):
        if(self.tokens.atual.tipo == 'VOID'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        elif(self.tokens.atual.tipo == 'INT'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        elif(self.tokens.atual.tipo == 'CHAR'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        else:
            raise Exception("Erro: Tipo")

    def comando(self):
        if(self.tokens.atual.tipo == 'VAR'):
            return self.atribuicao()
        elif(self.tokens.atual.tipo == 'PRINTF'):
            self.tokens.selecionarProximo()
            return self.print()
        elif(self.tokens.atual.tipo == 'OPEN_C'):
            resultado = self.comandos()
            self.tokens.selecionarProximo()
            return resultado
        elif(self.tokens.atual.tipo == 'IF'):
            return self.ifExp()
        elif(self.tokens.atual.tipo == 'WHILE'):
            resultado = self.whileExp()
            return resultado
        elif(self.tokens.atual.tipo == 'VOID' or self.tokens.atual.tipo == 'INT' or self.tokens.atual.tipo == 'CHAR'):
            p2 = self.tokens.peek(2)
            if (p2.tipo == 'OPEN_P'):
                resultado = self.programa()
                return resultado
            else:
                return self.declaracao()
        elif(self.tokens.atual.tipo == 'RETURN'):
            resultado = self.returnExp()
            self.tokens.selecionarProximo()
            return resultado
        else:
            raise Exception("Erro no comando")
    
    def returnExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado = UnOp('RETURN', [self.expressao()])
            if(self.tokens.atual.tipo=='CLOSE_P'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'SEMICOLON'):
                        self.tokens.selecionarProximo() 
                        return resultado
                    else:
                        raise Exception("Erro: Ponto e virgula")
            else:
                raise Exception("Erro: Fechar parenteses")
        else:
            raise Exception("Erro: Abrir parenteses")
    
    def declaracao(self):
        tipo = self.tokens.atual.tipo
        self.tokens.selecionarProximo()
        declaracao_children = []
        if(self.tokens.atual.tipo == 'VAR'):
            var = VarVal(self.tokens.atual.valor,[])
            declaracao_children.append(var)
            self.tokens.selecionarProximo()
            while(self.tokens.atual.tipo=='COLON'):
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'VAR'):
                    var = VarVal(self.tokens.atual.valor,[])
                    declaracao_children.append(var)
                    self.tokens.selecionarProximo()
                else:
                    raise Exception("Erro declaração com virgula")
            if(self.tokens.atual.tipo == 'SEMICOLON'):
                self.tokens.selecionarProximo()
                return VarDec (tipo, declaracao_children)
            else:
                raise Exception("Erro: Ponto e virgula")
        else:
            raise Exception("Erro declaração")

    def whileExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado1 = self.booleanExp()
            if(self.tokens.atual.tipo == "CLOSE_P"):
                self.tokens.selecionarProximo()
                resultado2 = self.comando()
                return BinOp('WHILE', [resultado1, resultado2])
            else:
                raise Exception("Erro: fechar parentases no while")
        else:
            raise Exception("Erro: abir parentases no while")

    def ifExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado1 = self.booleanExp()
            if(self.tokens.atual.tipo == "CLOSE_P"):
                self.tokens.selecionarProximo()
                resultado2 = self.comando()
                if(self.tokens.atual.tipo == "ELSE"):
                    self.tokens.selecionarProximo()
                    resultado3 = self.comando()
                else:
                    resultado3 = None
                return TriOp('IF', [resultado1, resultado2, resultado3])
            else:
                raise Exception("Erro: fechar parentases no if")
        else:
            raise Exception("Erro: abrir parentases no if")

    def print(self):
        if(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            resultado = UnOp('PRINTF', [self.expressao()])
            if(self.tokens.atual.tipo=='CLOSE_P'):
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'SEMICOLON'):
                    self.tokens.selecionarProximo() 
                    return resultado
                else:
                    raise Exception("Erro: Ponto e virgula")
            else:
                raise Exception("Erro: Fechar parenteses")
        else:
            raise Exception("Erro: Abrir parenteses")

    def atribuicao(self):
        name = VarVal(self.tokens.atual.valor,[])
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == 'ATRI'):
            self.tokens.selecionarProximo()
            if(self.tokens.atual.tipo == 'SCANF'):
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'OPEN_P'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'CLOSE_P'):
                        self.tokens.selecionarProximo()
                        resultado = Scanf('SCANF',[])
            elif(self.tokens.atual.tipo == 'VAR'):
                peek_token = self.tokens.peek(1)
                if(peek_token.tipo == 'OPEN_P'):
                    resultado = self.funcCall()
                    self.tokens.selecionarProximo()
                else:
                    resultado = self.expressao()
            else:
                resultado = self.expressao()
            if(self.tokens.atual.tipo == 'SEMICOLON'):
                self.tokens.selecionarProximo() 
            else:
                raise Exception("Erro: Ponto e virgula")
            return BinOp('ATRI',[name, resultado])
        else:
            raise Exception("Erro: Inserir '=' ")

    def funcCall(self):
        func_call_arg =[]
        if(self.tokens.atual.tipo == 'VAR'):
            name_func = self.tokens.atual.valor
            self.tokens.selecionarProximo() 
        if(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo() 
            while(self.tokens.atual.tipo != 'CLOSE_P'):
                exp = self.expressao()
                func_call_arg.append(exp)
                while(self.tokens.atual.tipo == 'COLON'):
                    self.tokens.selecionarProximo() 
                    exp = self.expressao()
                    func_call_arg.append(exp)
                if(self.tokens.atual.tipo == 'CLOSE_P'):
                    return FuncCall(name_func, func_call_arg)
                else:
                    raise Exception("Erro: Funcao sem fechar parenteses")
        else:
            raise Exception ("Erro: Funcao sem abrir parenteses")
    
    def expressao(self):
        resultado = self.termo()
        while(self.tokens.atual.tipo == 'PLUS' or self.tokens.atual.tipo == 'MINUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.termo()])
        return resultado
    
    def termo(self):
        resultado = self.fator()
        while(self.tokens.atual.tipo == 'MULT' or self.tokens.atual.tipo == 'DIV'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.fator()])
        return resultado 
       
    def fator(self):
        if(self.tokens.atual.tipo == 'PLUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = UnOp(op, [self.fator()])
            return resultado
        elif(self.tokens.atual.tipo == 'MINUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = UnOp(op, [self.fator()])
            return resultado
        elif(self.tokens.atual.tipo == 'INT'):
            resultado = IntVal(self.tokens.atual.valor,[])
            self.tokens.selecionarProximo()
            return resultado
        elif(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            resultado = self.expressao()
            if(self.tokens.atual.tipo == 'CLOSE_P'):
                self.tokens.selecionarProximo()
                return resultado
            else:
                raise Exception("Erro: Fechar parenteses")
        elif(self.tokens.atual.tipo == 'VAR'):
            peek_token = self.tokens.peek(1)
            if(peek_token.tipo == 'OPEN_P'):
                resultado = self.funcCall()
                self.tokens.selecionarProximo()
                return resultado
            else:
                resultado = VarVal(self.tokens.atual.valor,[])
                self.tokens.selecionarProximo()
                return resultado
        else:
            raise Exception("Erro no fator")
    
    def booleanExp(self):
        resultado = self.booleanTerm()
        while(self.tokens.atual.tipo == 'OR'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, self.booleanTerm()])
        return resultado
    
    def booleanTerm(self):
        resultado = self.booleanFactor()
        while(self.tokens.atual.tipo == 'AND'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, self.booleanFactor()])
        return resultado

    def booleanFactor(self):
        if(self.tokens.atual.tipo == 'NOT'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return UnOp(op,[self.booleanFactor()])
        else:
            return self.relExp()
    
    def relExp(self):
        resultado = self.expressao()
        if(self.tokens.atual.tipo == 'GREATER' or self.tokens.atual.tipo == 'LESS' or self.tokens.atual.tipo == 'EQUAL'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return BinOp(op, [resultado, self.expressao()])
        else:
            raise Exception("Erro: relOp errado")

if __name__ == "__main__":

    with open('input.c', 'r') as myfile:
        input_file=myfile.read().replace('\n', '')
    input_file = PrePro.comentarios(input_file)

    table = SymbleTable()
    tokenizador = Tokenizador(input_file,0,'null')
    tokenizador.selecionarProximo()
    analisador = Analisador(tokenizador, table)
    r = analisador.programa()
    tokenizador.selecionarProximo()

    if(tokenizador.atual.tipo == 'FIM'):
        print("semantico")
        r.evaluate(table)
    else:
        raise Exception("Erro: Análise terminou antes do fim do arquivo de entrada")

