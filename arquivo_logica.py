# Essa é um código para analisar de forma simples se o empreendedor precisa ou não fazer sua declaração de imposto de renda. 

####### Funções ######

class MEI_Calculadora:
    
    def __init__(self, faturamento: float, despesas: float, tipo_atividade = int):
        self.faturamento = faturamento
        self.despesas = despesas
        self.tipo_atividade = tipo_atividade
        self.valorIsento = 0
        self.valorTributavel = 0


    def obter_faturamento(self): # Método para coletar as informações dos usuarios

        # Solicitação do Faturamento, fazendo a validação se é um número valido e se está dentro do limite do MEI.

        # Valida se o valor digitado é um valor valido.
        try: 
            self.faturamento = float(self.faturamento)
        except ValueError:
            print("Erro: Faturamento deve ser um número válido.")
            return None

        # Valida se o valor está dendo do limite do MEI, e se não é negativo.
        if self.faturamento > 81000:
            return(False,'faturamento maior que o permitido')
        elif self.faturamento < 0:
            return(False, "Erro: Faturamento deve ser um número válido.")
        else: 
            return(True, "Informação coletada com Sucesso")

       
    def obter_despesas(self): # Método solicitação valor das despesas

         # Valida se o valor digitado é um valor valido.
        try: 
            self.despesas = float(self.despesas)
        except ValueError:
            print("Erro: O valor das despesas deve ser um número válido.")
            return None
                
        # Valida de o valor das despesas não ultrapassa o faturamento e não é negativo
        if self.despesas >= self.faturamento:
            return(False, "O valor das despesas não deve ultrapassar o valor da faturamento")
        elif self.despesas < 0:
            return(False, "Erro: O valor das despesas deve ser um número válido.")
        else: return(True, "Informação coletada com Sucesso")

    def obter_atividade(self): # Método Solicitação do tipo de atividade.

        # Valida se o valor digitado é um valor valido.
        try: 
            self.tipo_atividade = float(self.tipo_atividade)
        except ValueError:
            print("Erro: Escolha uma opção valida.")
            return None

        # Valida se está escolhendo uma das opções possiveis. Não podendo ser maior que 3 e menor que 0.
        if self.tipo_atividade > 3 or self.tipo_atividade <= 0:
            return(False,"Escolha um opção valida")
        else: return(True, "Informação coletada com Sucesso")
        

    
    def parcela_isenta (self): # Método para calcular a parcela isenta

        if self.tipo_atividade == 1: # Comércio, indústria e transporte de cargas 
            self.valorIsento = (self.faturamento * 0.08)
        elif self.tipo_atividade == 2: # Transporte de passageiros 
            self.valorIsento = (self.faturamento * 0.16)
        elif self.tipo_atividade == 3: # Serviços
            self.valorIsento = (self.faturamento * 0.32)

        return self.valorIsento


    def parcela_tributavel (self): # Método para calcular parcela Tributavel
        self.valorTributavel = (self.faturamento - self.despesas - self.valorIsento)
        return self.valorTributavel


    def validação_final (self): # Validação final, saber se o usuario precisa ou não declara o imposto de renda.
        if self.valorTributavel <= 33888:
            return(False, f"O seu valor tributavel foi abaixo do esperado, não é necessario declarar imposto de renda")
        
        else:
            return(True, "Você precisa declarar o imposto de renda")

        









        
        

        
     

