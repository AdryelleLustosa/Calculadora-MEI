# Essa é um código para analisar de forma simples se o empreendedor precisa ou não fazer sua declaração de imposto de renda. 

from fpdf import FPDF


####### Funções ######

class MEI_Calculadora:
    
    def __init__(self, faturamento: float, despesas: float, tipo_atividade = int):
        self.faturamento = faturamento
        self.despesas = despesas
        self.tipo_atividade = tipo_atividade
        self.valorIsento = 0
        self.valorIsentoValidado = 0
        self.valorTributavel = 0
        self.lucrobruto = 0


    def obter_faturamento(self): # Método para coletar as informações dos usuarios

        # Solicitação do Faturamento, fazendo a validação se é um número valido e se está dentro do limite do MEI.

        # Valida se o valor digitado é um valor valido.
        try: 
            self.faturamento = float(self.faturamento)
        except ValueError:
            return(False, "Erro: Faturamento deve ser um número válido.")
            
        # Valida se o valor está dendo do limite do MEI, e se não é negativo.
        if self.faturamento > 81000:
            return(False,"""Atenção: Seu faturamento ultrapassou o limite anual de 81.000,00 deifinido para o MEI.
                            Para orientações, fale com um contador: ALCONTÁBIL@gmail.com""")
        elif self.faturamento <= 0:
            return(False, "Faturamento deve ser um número válido.")
        else: 
            return(True, "Informação coletada com Sucesso")

       
    def obter_despesas(self): # Método solicitação valor das despesas

         # Valida se o valor digitado é um valor valido.
        try: 
            self.despesas = float(self.despesas)
        except ValueError:
            return("Erro: O valor das despesas deve ser um número válido.")
            
                
        # Valida de o valor das despesas não ultrapassa o faturamento e não é negativo
        if self.despesas >= (self.faturamento - (self.faturamento * 0.20)):
            return(False, """Atenção: suas despesas não devem exceder 80% do faturamento anual do MEI.
                            Para orientações, fale com um contador: ALCONTÁBIL@gmail.com""")
        elif self.despesas < 0:
            return(False, "Erro: O valor das despesas deve ser um número válido.")
        else: return(True, "Informação coletada com Sucesso")

    def obter_atividade(self): # Método Solicitação do tipo de atividade.

        # Valida se o valor digitado é um valor valido.
        try: 
            self.tipo_atividade = float(self.tipo_atividade)
        except ValueError:
            return(False,"Erro: Escolha uma opção valida.")
            

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


         # Aqui é uma validação porque o valor isento não pode ultrapassar o valor do lucro real da empresa.  

        self.lucrobruto = self.faturamento  - self.despesas
        if self.valorIsento > self.lucrobruto:
            self.valorIsentoValidado = self.lucrobruto
        else:
            self.valorIsentoValidado = self.valorIsento

        return self.valorIsentoValidado

      


    def parcela_tributavel (self): # Método para calcular parcela Tributavel
        self.valorTributavel = (self.faturamento - self.despesas - self.valorIsento)
        if self.valorTributavel < 0:
            self.valorTributavel = 0


        return self.valorTributavel


    def validacao_final (self): # Validação final, saber se o usuario precisa ou não declara o imposto de renda.
        if self.valorTributavel <= 33888:
            return (False, "Seu rendimento tributável ficou abaixo do limite de R$ 33.888,00; "
            "Portanto VOCÊ NÃO ESTÀ OBRIGADO(A) a declarar o IRPF."
        )
        else:
            return (True,"Seu rendimento tributável excedeu o limite de R$ 33.888,00; "
            "Portanto VOCÊ ESTÀ OBRIGADO(A) a declarar o IRPF. Baixe as instruções para sua declaração"
        )

    def gerar_pdf_com_dados_e_imagens(self):
     
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

    # Título
        pdf.set_text_color(30, 41, 59) 
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Resumo da Declaração do MEI", ln=True, align="C")
        pdf.ln(5)

    # Dados principais
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, f"Segue abaixo as instruções para você declarar os seus rendimentos.", ln=True)
        pdf.ln(0)

        # Formatação de moeda 
        isento_str = f"R$ {self.valorIsentoValidado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        trib_str = f"R$ {self.valorTributavel:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Dados principais
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(
            0, 5,
            f"Sua Parcela Isenta: {isento_str}  |  Parcela Tributável: {trib_str}",
            ln=True
        )
        pdf.ln(10)

    # Instruções para preenchimento
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, "Caminho para preencher na declaração:", ln=True)
        pdf.ln(5)

    # Imagem 1: Rendimento Tributável
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 5, "O CNPJ da sua fonte pagadora é o CNPJ do seu MEI", ln=True)
        pdf.cell(0, 10, "1. Rendimento Tributável Rec. Pessoa Jurídica - Aqui você preenche o valor do seu rendimento tributavel.", ln=True)
        pdf.image("Rendimento Tributavel.png", x=10, y=pdf.get_y(), w=130)
        pdf.ln(80)  # espaço após a imagem

    # Imagem 2: Rendimento Isento
        pdf.ln(15)
        pdf.cell(0, 10, "2. Rendimento Isentos - Lucros e Dividendos - Aqui você preenche o valor do seu rendimento isento.", ln=True)
        pdf.ln(5)
        pdf.image("Rendimento Isento.png", x=10, y=pdf.get_y(), w=140)
        pdf.ln(5)

    # Contato
        pdf.ln(80)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 8, f"Para maiores dúvidas, ou precisar de ajuda, entre em contato com: ALCONTÁBIL@gmail.com", ln=True)
        


    # Retorna os bytes
        return pdf.output(dest="S").encode("latin-1", "replace") 
        
       






        
        

        
     

