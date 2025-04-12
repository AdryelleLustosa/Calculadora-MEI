# Essa é um código para analisar de forma simples se o empreendedor precisa ou não fazer sua declaração de imposto de renda. 

####### Funções ######

class MEI_Calculadora:
    
    def __init__(self, faturamento: float, despesas: float, tipo_atividade = int):
        self.faturamento = faturamento
        self.despesas = despesas
        self.tipo_atividade = tipo_atividade
        self.valorIsento = 0
        self.valorTributavel = 0


    def coleta_de_informações(self):

        # Solicitação do Faturamento, fazendo a validação se é um número valido e se está dentro do limite do MEI.
        try: 
            self.faturamento = float(self.faturamento)
        except ValueError:
            print("Erro: Faturamento deve ser um número válido.")
            return None

        if self.faturamento > 81000:
            print('fatuamento maior que o permitido')
            return
        elif self.faturamento < 0:
            print("Erro: Faturamento deve ser um número válido.")
            return
        else:print("Informação coletada com Sucesso")

        
        # Solicitação valor das despesas
        try: 
            self.despesas = float(self.despesas)
        except ValueError:
            print("Erro: O valor das despesas deve ser um número válido.")
            return None
                
        if self.despesas >= self.faturamento:
            print("O valor das despesas não deve ultrapassar o valor da faturamento")
            return
        elif self.despesas < 0:
            print("Erro: O valor das despesas deve ser um número válido.")
            return
        else: print("Informação coletada com Sucesso")

        # Solicitação do tipo de atividade.
        try: 
            self.tipo_atividade = float(self.tipo_atividade)
        except ValueError:
            print("Erro: Escolha uma opção valida.")
            return None

        if self.tipo_atividade > 3 or self.tipo_atividade <= 0:
            print("Escolha um opção valida")
            return
        else: print("Informação coletada com Sucesso")
        

    
    def parcela_isenta (self):
        if self.tipo_atividade == 1: # Comércio, indústria e transporte de cargas 
            self.valorIsento = (self.faturamento * 0.08)
        elif self.tipo_atividade == 2: # Transporte de passageiros 
            self.valorIsento = (self.faturamento * 0.16)
        elif self.tipo_atividade == 3: # Serviços
            self.valorIsento = (self.faturamento * 0.32)

        print(self.valorIsento)

    def parcela_tributavel (self):
        self.valorTributavel = (self.faturamento - self.despesas - self.valorIsento)
        print(f"O valor tributavel é:R$ {self.valorTributavel:.2f}")

    def validação(self):
        if self.valorTributavel <= 33888:
            print(f"O seu valor tributavel foi abaixo do esperado, não é necessario declarar imposto de renda")
        
        else:
            print("Você precisa declarar o imposto de renda")

        

teste = MEI_Calculadora(20000, 22000, 1)
teste.coleta_de_informações()
teste.parcela_isenta()
teste.parcela_isenta()
teste.validação()









        
        

        
     

