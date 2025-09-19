from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pandas as pd
import plotly.express as pe
from plotly.offline import plot
from unicodedata import normalize, combining
import warnings
from django.conf import settings
import os
import psycopg2
import unicodedata

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto) 
        if unicodedata.category(c) != 'Mn'
    )
# Create your views here.


def retornarMensagem(request):
    conn = psycopg2.connect(
    dbname="planilha_ic",
    user="alexandre",
    password="123",
    host="localhost",
    port="5432"
    )

    filtros = request.GET.get('filtros').split("MMM")
    variavel_interesse = request.GET.get('campo')
    stringQuery = 'SELECT mensagem FROM frontend_filtros'
    camposEmOrdemParaConsulta = ["curso","periodo","ingresso","sexo","cor","nacionalidade","cidade_nascimento","cidade_moradia"]
    if filtros:
        stringQuery += " WHERE "
        stringQuery += f"variavel_interesse = '{variavel_interesse}' AND "
        for numfiltro in range(len(filtros)):
            try:
                campo,valor = filtros[numfiltro].split(":")
                if len(str(campo).split()) > 1:
                    if 'moradia' in str(campo).lower():
                        campo = 'cidade_moradia'
                    elif 'nascimento' in str(campo).lower():
                        campo = 'cidade_nascimento'
                    else:
                        campo = remover_acentos(str(campo).split()[0])
                if numfiltro == len(filtros) - 1:
                    stringQuery += f"{campo} = \'{valor}\';"
                else:
                    stringQuery += f"{campo} = \'{valor}\' AND "
            except:
                if numfiltro == len(filtros) -1 :
                    stringQuery += f"{camposEmOrdemParaConsulta[numfiltro]} = '';"
                else:
                    stringQuery += f"{camposEmOrdemParaConsulta[numfiltro]} = '' AND "
        
        cursor = conn.cursor()
        cursor.execute(stringQuery)
        dados = cursor.fetchall()
        cursor.close()
        
        return JsonResponse({"mensagem":dados})

    
    

df_processado = pd.read_excel(os.path.join(
    settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx'))


def home(request):

    return render(request, 'grafico.html')


def retornarColunas(request):
    caminho_arquivo = os.path.join(
        settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx')
    df = pd.read_excel(caminho_arquivo)
    retornar = [ coluna.strip() for coluna in df.columns if coluna not in ['Curso','Período de estudo','Ano de ingresso na universidade', 'Idade de ingresso na universidade','Sexo','Gênero','Cor ou raça','Nacionalidade','Cidade e estado/província de nascimento','Cidade e estado/província onde mora']]
    return JsonResponse({"colunas": retornar})


def retornarNaoColunas(request):
    caminho_arquivo_bruto = os.path.join(
        settings.BASE_DIR, 'static', 'arquivos', 'a_processar', 'dados_brutos.xlsx')
    caminho_arquivo_processado = os.path.join(
        settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx')
    df = pd.read_excel(caminho_arquivo_bruto)
    df_processado = pd.read_excel(caminho_arquivo_processado)
    naoColunasBruto = set(df.columns)
    colunasProcessado = set(df_processado.columns)
    naoColunas = naoColunasBruto.difference(colunasProcessado)

    return JsonResponse({"colunas": list(naoColunas)})

def gerarGraficoApexCharts(request):
    variavel_interesse = request.GET.get("campo")
    filtro = request.GET.get('filtros')
    caminho_arquivo = os.path.join(
        settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx')
    df = pd.read_excel(caminho_arquivo)
    if variavel_interesse and filtro:
        filtros = filtro.split('MMM')
        while '' in filtros:
            filtros.remove('')
        filtrosDic = dict()
        for filtro in filtros:
            filtrosDic[filtro.split(':')[0]] = filtro.split(':')[1]
        for chaveDic in filtrosDic.keys():
            if str(filtrosDic[chaveDic]).isnumeric():
                df = df[df[chaveDic] == int(filtrosDic[chaveDic])] 
            else:  
                df = df[df[chaveDic] == filtrosDic[chaveDic]]
        
        df = df[variavel_interesse]
        retornar = dict()
        for campo in df.tolist():

            if pd.isna(campo):
                continue
            if retornar.get(campo) == None:
                retornar[campo] =  1
            else:
                retornar[campo] += 1 
        print(retornar)
        retornar = dict(sorted(retornar.items(),key= lambda x : x[0].split('-')[0]))
        return JsonResponse({'x':list(retornar.keys()),'y':list(retornar.values())})

        
        
    elif variavel_interesse:
        df = df[variavel_interesse].unique().tolist()
        
    return JsonResponse({'10':10})
    
    
def salvarMensagemNoBanco(request):
    conn = psycopg2.connect(
    dbname="planilha_ic",
    user="alexandre",
    password="123",
    host="localhost",
    port="5432"
    )
    camposEmOrdemParaConsulta = ["curso","periodo","ingresso","sexo","cor","nacionalidade","cidade_nascimento","cidade_moradia"]
    campo = request.GET.get("campo")
    filtros = request.GET.get("filtros")
    mensagem = request.GET.get("mensagem")
    queryUpdate = f"UPDATE frontend_filtros SET mensagem = '{mensagem}' WHERE variavel_interesse = '{campo}' AND "
    queryInsert = f"INSERT INTO public.frontend_filtros (curso, periodo, ingresso, sexo, cor, nacionalidade, cidade_nascimento, cidade_moradia, mensagem, variavel_interesse) VALUES("
    
    filtros = filtros.split("MMM")
    for filtro in range(len(filtros)):
        atualFiltro = filtros[filtro].split(':')
        if len(atualFiltro) > 1:
            if filtro == len(filtros) - 1:
           
                if 'moradia' in atualFiltro[0]:
                    queryUpdate += f"cidade_moradia = '{atualFiltro[1]}';"
                elif 'nascimento' in atualFiltro[0]:
                    queryUpdate += f"cidade_nascimento = '{atualFiltro[1]}';"
                else:  
                    queryUpdate += f"{atualFiltro[0]} = '{atualFiltro[1]}';"
                queryInsert += f"'{atualFiltro[1]}'); "
            else:
                if 'moradia' in atualFiltro[0]:
                    queryUpdate += f"cidade_moradia = '{atualFiltro[1]}' AND "
                elif 'nascimento' in atualFiltro[0]:
                    queryUpdate += f"cidade_nascimento = '{atualFiltro[1]}' AND "
                elif 'Período' in atualFiltro[0]:
                    queryUpdate += f"periodo = '{atualFiltro[1]}' AND "
                else:  
                    queryUpdate += f"{atualFiltro[0]} = '{atualFiltro[1]}' AND "
                queryInsert += f"'{atualFiltro[1]}', "

        else:
            if filtro == len(filtros) - 1:
                queryUpdate += f"{camposEmOrdemParaConsulta[filtro]} = '';"
            else:
                queryUpdate += f"{camposEmOrdemParaConsulta[filtro]} = '' AND "
                
            queryInsert += f"'',  "
                
    queryInsert += f"'{mensagem}','{campo}');"
    cursor = conn.cursor()

    cursor.execute(queryUpdate)
    if cursor.rowcount == 1:
        mensagemRetornar = "Salvo com sucesso"
    else:
    
        mensagemRetornar = "Erro ao salvar, não se encontra esse registro no banco de dados!\nTentando criar novo dado de mensagem para esses filtros"
        cursor.execute(queryInsert)
    cursor.close()
    conn.commit()
            
    return JsonResponse({"mensagem":mensagemRetornar})     
    
    


# def exibirDadosGrafico(request):
#     # ordem> curso > periodo > ingresso >  sexo > cor > nacionalidade > cidade nascimento > cidade moradia
#     caminho_arquivo = os.path.join(
#         settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx')
#     df = pd.read_excel(caminho_arquivo)
#     campo = request.GET.get("campo")
#     filtro = request.GET.get('filtros')
#     if campo:
#         if filtro and filtro != "":
#             filtro = str(filtro).split("M")
#             while '' in filtro:
#                 filtro.remove('')
#             if filtro == [] and campo:
#                 dicGraph = dict()
#                 for valor in df[campo].tolist():

#                     if dicGraph.get(valor) != None:
#                         dicGraph[valor] += 1
#                     else:
#                         dicGraph.update({valor: 1})
#                 dicGraph = dict(sorted(dicGraph.items()))

#                 filteredDf = pd.DataFrame(list(dicGraph.items()), columns=[
#                                         "Categoria", "Contagem"])

#                 grafico = pe.bar(filteredDf, x="Categoria", y="Contagem",
#                                 title="Gráfico de Barras Dinâmico")

#                 grafico_html = plot(grafico, output_type='div')
#                 return render(request, 'grafico.html', {'grafico': grafico_html})
#             elif filtro == []:
#                 return render(request, 'index.html')
#             novoFiltro = []
#             for item in filtro:
#                 novoFiltro.append(tuple(item.split(':')))

#             dicGraph = dict()
#             # df_filtered1 = df[(df['horario'] == filtro_hora) & (df['data'] == filtro_data)]
#             filtro_acumulativo = True
#             for campoPlanilha, valor in novoFiltro:
#                 filtro_acumulativo &= (df[campoPlanilha] == valor)

#             # Aplicando o filtro ao DataFrame
#             campoJaFiltrado = df.loc[filtro_acumulativo, campo].tolist()
#             for valor in campoJaFiltrado:

#                 if dicGraph.get(valor) != None:
#                     dicGraph[valor] += 1
#                 else:
#                     dicGraph.update({valor: 1})
#             dicGraph = dict(sorted(dicGraph.items()))

#             filteredDf = pd.DataFrame(list(dicGraph.items()), columns=[
#                                     "Categoria", "Contagem"])

#             grafico = pe.bar(filteredDf, x="Categoria", y="Contagem",
#                             title="Gráfico de Barras Dinâmico")

#             grafico_html = plot(grafico, output_type='div')
#             return render(request, 'grafico.html', {'grafico': grafico_html})
            
#         else:
#             dicGraph = dict()
#             for valor in df[str(campo)].tolist():

#                 if dicGraph.get(valor) != None:
#                     dicGraph[valor] += 1
#                 else:
#                     dicGraph.update({valor: 1})
#             dicGraph = dict(sorted(dicGraph.items()))

#             filteredDf = pd.DataFrame(list(dicGraph.items()), columns=[
#                                     "Categoria", "Contagem"])

#             grafico = pe.bar(filteredDf, x="Categoria", y="Contagem",
#                             title="Gráfico de Barras Dinâmico")

#             grafico_html = plot(grafico, output_type='div')
#             return render(request, 'grafico.html', {'grafico': grafico_html})
#     else:
#         return render(request, 'index.html')

def remover_acentos_e_pontuacao(texto: str):
    texto = texto.lower().replace('-', ',').replace('/', ',').replace('(',
                        ',').replace(")", '').replace(',', " ") + " ".strip()
    estados = [' sp ', ' pi ', ' ce ', ' mg ', ' rj ', ' es ', ' ba ', ' pe ', ' ma ', ' sc ', ' rs ', ' pr ', ' am ',
        ' pa ', ' ap ', ' to ', ' rn ', ' al ', ' se ', ' pb ', ' ro ', ' rr ', ' ac ', ' mt ', ' ms ', ' go ', ' df ']
    
    status = 0
    for estado in estados:
        if estado in texto:
            texto = texto.replace(f"{estado}", "").strip()
            status = 1
    if status == 1:
        if texto.split(" ")[0] == 'são' or texto.split(" ")[0] == 'rio' or texto.split(" ")[0] == 'boa' or texto.split(" ")[0] == 'sao':
            try:
                texto = texto.split()[0] + texto.split()[1]
            except:
                texto = texto.split()[0]
        else:
            texto = texto.split()[0]
    return ''.join(
     [c for c in normalize('NFD', texto) if not combining(c)]
    )


def verificarPorcentagemNumerosInteiros(lista: list[int]) -> float | int:
    valoresInteiros = 0
    for item in lista:
        try:
            item = int(item)
            valoresInteiros += 1
        except:
            pass
    valorTotal = len(lista)
    parteEquacaoRegraDe3_1 = valoresInteiros * 100
    parteEquacaoRegraDe3_2 = valorTotal
    porcentagem = parteEquacaoRegraDe3_1 / parteEquacaoRegraDe3_2
    return round(porcentagem, 2)


def criarMediaParaValoresInteiros(numero: int) -> str:
    return f"{int((numero//5))*5}-{(int((numero//5))*5)+4}"


def removerLetrasDeCamposNumericos(palavra: str) -> int:
    palavra = str(palavra)
    retornar = ''
    for caractere in palavra:
        if caractere.isdigit():
            retornar += caractere
    if retornar == "":
        
        return 0
 
    return int(retornar)


def api_curso(request):
    global df_processado
    return JsonResponse({"colunas": list(sorted(df_processado['Curso'].unique().tolist()))})


def api_periodo(request):
    global df_processado
    return JsonResponse({"colunas": list(sorted(df_processado['Período de estudo'].unique().tolist()))})


def api_ingresso(request):
    global df_processado
    return JsonResponse({"colunas": list(sorted(df_processado['Ano de ingresso na universidade'].unique().tolist()))})


def api_sexo(request):
    global df_processado
    return JsonResponse({"colunas": list(sorted(df_processado['Sexo'].unique().tolist()))})


def api_cor(request):
    global df_processado
    return JsonResponse({"colunas": list(sorted(df_processado['Cor ou raça'].unique().tolist()))})


def api_nacionalidade(request):
    global df_processado
    return JsonResponse({"colunas":list(sorted(df_processado['Nacionalidade'].unique().tolist()))})

def api_cidade_nascimento(request):
    global df_processado
    return JsonResponse({"colunas":list(sorted(df_processado['Cidade e estado/província de nascimento'].unique().tolist()))})

def api_cidade_moradia(request):
    global df_processado
    return JsonResponse({"colunas":list(sorted(df_processado['Cidade e estado/província onde mora'].unique().tolist()))})

def colunaTotalmenteNumerica(lista) -> bool:
    for elemento in lista:
        if isinstance(elemento,str):
            return False
    return True    

def retornarValoresDeCampo(request):
    df = os.path.join(settings.BASE_DIR, 'static','arquivos','b_processado','dados.xlsx')
    variavel_interesse = request.GET.get('campo')
    return df[variavel_interesse]
             
            
def processamentoInicial(request):
    warnings.filterwarnings("ignore")

    lista_arquivos_processados = []

    for nomeArquivo in os.listdir(os.path.join(settings.BASE_DIR, 'static', 'arquivos', 'a_processar')):
        caminho_arquivo = os.path.join(settings.BASE_DIR, 'static', 'arquivos', 'a_processar', nomeArquivo)
        df = pd.read_excel(caminho_arquivo)
        referencia = len(df['Carimbo de data/hora'])
        
        df_temporario = pd.DataFrame()
        for coluna in [x.strip() for x in df.columns]:
            try:
                if len(df[coluna].unique()) == 1 and coluna != "Ano de ingresso na universidade":
                    df.drop(labels=coluna, axis=1, inplace=True)

                elif len(df[coluna]) == len(set(df[coluna])) and len(df[coluna].unique()) == referencia:
                    df.drop(labels=coluna, axis=1, inplace=True)

                elif verificarPorcentagemNumerosInteiros(df[coluna].tolist()) > 80:
                    
                    df[coluna] = df[coluna].apply(lambda x: removerLetrasDeCamposNumericos(x))
                    df_temporario[coluna] = df[coluna]  

                    if colunaTotalmenteNumerica(df[coluna].tolist()) and coluna != "Ano de ingresso na universidade" and len(df[coluna].unique()) > 5:
                        df[coluna] = df[coluna].apply(lambda x: criarMediaParaValoresInteiros(x))
                        df_temporario[coluna] = df[coluna]  

                else:
                    # df[coluna] = df[coluna].apply(lambda x: remover_acentos_e_pontuacao(str(x)))
                    df_temporario[coluna] = df[coluna]
            except Exception as ex:
                print("key nao encontrada : " , ex)  
                
        lista_arquivos_processados.append(df_temporario)

    arquivo_saida = pd.concat(lista_arquivos_processados, ignore_index=True)
    caminho_saida = os.path.join(settings.BASE_DIR, 'static', 'arquivos', 'b_processado', 'dados.xlsx')
    arquivo_saida.to_excel(caminho_saida, index=False)
    global df_processado
    df_processado = arquivo_saida

    return render(request,"index.html")
        
