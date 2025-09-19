"""
URL configuration for projetoPlanilha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from frontend.views import retornarMensagem,retornarColunas, home, retornarNaoColunas, processamentoInicial, api_cidade_moradia, api_cor, api_cidade_nascimento, api_curso, api_ingresso, api_nacionalidade, api_periodo, api_sexo, gerarGraficoApexCharts,salvarMensagemNoBanco
urlpatterns = [
    path('admin/', admin.site.urls),
    path('exibir/', retornarColunas),
    path('exibirnaocolunas/', retornarNaoColunas),
    path('page/', home),
    path('gerar-grafico/', home),
    path("gerar-grafico/exibirCurso", api_curso),
    path("gerar-grafico/exibirSexo", api_sexo),
    path("gerar-grafico/exibirCor", api_cor),
    path("gerar-grafico/exibirMoradia", api_cidade_moradia),
    path("gerar-grafico/exibirNascimento", api_cidade_nascimento),
    path("gerar-grafico/exibirPeriodo", api_periodo),
    path("gerar-grafico/exibirIngresso", api_ingresso),
    path("gerar-grafico/exibirNacionalidade", api_nacionalidade),
    path("", processamentoInicial),
    path("t/", gerarGraficoApexCharts),
    path("m/",retornarMensagem),
    path("sm/",salvarMensagemNoBanco),

]
