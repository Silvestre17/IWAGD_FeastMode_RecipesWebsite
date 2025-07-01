from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.core.paginator import Paginator, UnorderedObjectListWarning
import warnings

from .models import Receita, Ingrediente, User, Perfil, Comentario, Classificacao

warnings.filterwarnings("ignore", category=UnorderedObjectListWarning)  # Desativar os 'warnings' do Paginator


# --------------- Documentação das Mensagens ---------------
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/

# Página Inicial do Website
def home(request):
    # Obter as 6 receitas com melhor classificação
    # QUERY | Obter as Receitas -> Calcular a média do campo 'rating' do objeto Classificação e
    #         Ordenar por ordem descendente
    top6_receitas = Receita.objects.annotate(avg_rating=Avg('classificacao__rating')) \
                        .order_by('-avg_rating')[:6]
    return render(request, 'recipe/home.html', {"top6_receitas": top6_receitas})


# Página 404 customizada
# Fonte: https://stackoverflow.com/questions/35156134/how-to-properly-setup-custom-handler404-in-django#answer-58411485
def handler404(request, exception):
    return render(request, 'recipe/404.html')


# Página dos Contactos
def contactos(request):
    return render(request, 'recipe/contactos.html')


# Página com a Lista de Receitas Todas
def receitas(request):
    # Obter todas as Receitas da Base de Dados
    receitas_todas = Receita.objects.all()

    # Paginação - https://docs.djangoproject.com/en/4.2/topics/pagination/
    pagina = Paginator(object_list=receitas_todas, per_page=6)
    # Nota: Caso se pretenda apresentar mais receitas por página basta apenas alterar o valor do parâmetro 'per_page'

    pagina_n = request.GET.get('pagina')
    pagina = pagina.get_page(pagina_n)

    # Não temos de passar as receitas, dado que o Paginator do django guarda os objetos 'Receitas'
    return render(request, 'recipe/receitas.html', {'pagina': pagina, 'categoria': 'tudo'})


# Função para filtar as Receitas por Categorias
def mudar_categoria(request, categoria):
    # Obter todas as Receitas de uma certa categoria da Base de Dados
    receitas_categoria = Receita.objects.filter(categoria__contains=categoria)

    # Paginação - https://docs.djangoproject.com/en/4.2/topics/pagination/
    pagina = Paginator(object_list=receitas_categoria, per_page=6)
    pagina_n = request.GET.get('pagina')
    pagina = pagina.get_page(pagina_n)
    return render(request, 'recipe/receitas.html', {"pagina": pagina, 'categoria': categoria})


# Função para filtar segundo a Tag - 'Grau de Dificuldade'
def mudar_grau_dificuldade(request, grau_dificuldade):
    # Obter todas as Receitas de um certo grau de dificuldade da Base de Dados
    receitas_grau_dificuldade = Receita.objects.filter(grau_dificuldade=grau_dificuldade)

    # Paginação - https://docs.djangoproject.com/en/4.2/topics/pagination/
    pagina = Paginator(object_list=receitas_grau_dificuldade, per_page=6)
    pagina_n = request.GET.get('pagina')
    pagina = pagina.get_page(pagina_n)
    return render(request, 'recipe/receitas.html', {"pagina": pagina,
                                                    'categoria': 'tudo',
                                                    'grau_dificuldade': grau_dificuldade})


# Função para Filtrar as Receitas
def receitas_filtros(request, categoria):
    # Caso o User tenha selecionado alguma Categoria
    if categoria != 'tudo':
        # Filtrar as Receitas pela Categoria (se fornecida no URL)
        receitas_filtradas = Receita.objects.filter(categoria__contains=categoria)
    else:
        # Obter todas as Receitas da Base de Dados
        receitas_filtradas = Receita.objects.all()

    # Obter os filtros aplicados
    pesquisa = request.GET.get('pesquisa', '')
    grau_dificuldade = request.GET.get('grau_dificuldade', 'None')
    filtrar = request.GET.get('filtrar', 'None')

    # Filtrar por Todas
    if filtrar == 'Todas':
        receitas_filtradas = Receita.objects.all()

    # Aplicar filtros
    if pesquisa:
        # Filtrar por Título
        receitas_filtradas = receitas_filtradas.filter(titulo__icontains=pesquisa)

    if grau_dificuldade != 'None':
        # Filtrar por Grau de Dificuldade
        receitas_filtradas = receitas_filtradas.filter(grau_dificuldade=grau_dificuldade)

    if filtrar != '-':

        # Filtrar por Data de Publicação Mais Recente
        if filtrar == 'Recentes':
            receitas_filtradas = receitas_filtradas.order_by('-pub_data')

        # Filtrar por Melhor Classificadas
        # QUERY | Clacular a Classificação Média de todas as Receitas e Ordenar da melhor para a pior
        elif filtrar == 'Classificadas':
            receitas_filtradas = receitas_filtradas.annotate(avg_rating=Avg('classificacao__rating')) \
                .order_by('-avg_rating')

        # Filtrar por Mais Comentadas
        # QUERY | Contar o Nº de Comentários de todas as Receitas e Ordenar da mais para a menos comentada
        elif filtrar == 'Comentadas':
            receitas_filtradas = receitas_filtradas.annotate(num_comentarios=Count('comentario')) \
                .order_by('-num_comentarios')

    # Paginação - https://docs.djangoproject.com/en/4.2/topics/pagination/
    pagina = Paginator(object_list=receitas_filtradas, per_page=6)
    pagina_n = request.GET.get('pagina')
    pagina = pagina.get_page(pagina_n)
    return render(request, 'recipe/receitas.html', {"pagina": pagina, 'categoria': categoria})


# Página de Detalhes das Receitas
def detalhe(request, receita_titulo):
    # Obter a Receita e Comentários correpondentes
    receita = get_object_or_404(Receita, titulo__iexact=receita_titulo)
    comentarios = Comentario.objects.filter(receita=receita)

    # Obter a Classificação do User, se este tiver logado
    if request.user.is_authenticated:
        classificacao_user = Classificacao.objects.filter(receita=receita, user=request.user)
    else:
        # Caso não esteja logado, fica 'None'
        classificacao_user = None

    # Processar os filtros dos Comentários do Forms
    filtro = request.GET.get('filtrar')
    if filtro:
        if filtro == 'MaisRecentes':
            comentarios = comentarios.order_by('-com_data')
        elif filtro == 'MenosRecentes':
            comentarios = comentarios.order_by('com_data')
        elif filtro == 'MelhorClassificados':
            comentarios = comentarios.order_by('-classificacao__rating')
        elif filtro == 'PiorClassificados':
            comentarios = comentarios.order_by('classificacao__rating')

    # Paginação - https://docs.djangoproject.com/en/4.2/topics/pagination/
    pagina = Paginator(object_list=comentarios, per_page=6)
    pagina_n = request.GET.get('pagina')
    pagina = pagina.get_page(pagina_n)

    return render(request, 'recipe/detalhe.html', {'receita': receita,
                                                   'pagina': pagina,
                                                   'classificacao_user': classificacao_user})


# Função para adicionar a Review (Apenas Classificação / Comentário e Classificação)
def review(request, receita_titulo):
    receita = get_object_or_404(Receita, titulo__iexact=receita_titulo)

    # Verificar se está preenchido:
    try:
        if request.method == "POST":
            comentario_texto = request.POST["comentario"]
            classificacao = int(request.POST["classificacao"])

            # Caso 1 | Utilizador apenas classifica a receita (pela 1º vez)
            if (1 <= classificacao <= 5 and not comentario_texto and
                    Classificacao.objects.filter(user=request.user, receita=receita).exists() is False):
                add_classificacao = Classificacao.objects.create(user=request.user,
                                                                 receita=receita,
                                                                 rating=classificacao)
                add_classificacao.save()

                # Incrementar as avaliações do User
                request.user.perfil.aumentar_total_avaliacoes()

                messages.success(request, 'Avaliação dada com sucesso!')
                return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))

            # Caso 2 | Utilizador classifica a receita e comenta (pela 1º vez)
            elif (1 <= classificacao <= 5 and comentario_texto and
                  Classificacao.objects.filter(user=request.user, receita=receita).exists() is False):
                add_classificacao = Classificacao.objects.create(user=request.user,
                                                                 receita=receita,
                                                                 rating=classificacao)
                add_classificacao.save()
                add_comentario = Comentario.objects.create(user=request.user,
                                                           receita=receita,
                                                           comentario=comentario_texto,
                                                           classificacao=add_classificacao)
                add_comentario.save()

                # Incrementar as avaliações e comentários do User
                request.user.perfil.aumentar_total_avaliacoes()
                request.user.perfil.aumentar_total_cometarios()

                messages.success(request, 'Comentário adicionado com sucesso!')
                return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))

            # Caso 3 | Utilizador já classificou a receita (e comentou) - Atualiza o comentário
            elif Classificacao.objects.filter(user=request.user, receita=receita).exists() is True:
                classificacao = Classificacao.objects.filter(user=request.user, receita=receita)[0]

                if comentario_texto:
                    try:
                        # Verifica se o User já comentou a receita
                        comentario_user = Comentario.objects.filter(user=request.user,
                                                                    receita=receita,
                                                                    classificacao=classificacao)[0]

                        # Caso seja True altera para o novo
                        comentario_user.comentario = comentario_texto
                        comentario_user.save()

                        messages.success(request, 'Comentário atualizado com sucesso!')
                        return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))

                    except IndexError:
                        # Caso em que o comentário ainda não foi realizado
                        add_comentario = Comentario.objects.create(user=request.user,
                                                                   receita=receita,
                                                                   comentario=comentario_texto,
                                                                   classificacao=classificacao)
                        add_comentario.save()

                        # Incrementar os comentários do User
                        request.user.perfil.aumentar_total_cometarios()

                        messages.success(request, 'Comentário adicionado com sucesso!')
                        return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))
                else:
                    messages.error(request, "Já classificou a receita. Apenas pode alterar o comentário!")
                    return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))

        else:
            messages.error(request, "Não selecionou nenhuma classificação. Volte a tentar!")
            return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))
    except ValueError:
        pass

    # Caso o User não tenha dado Classificação e apenas Comentado, ou não tenha inserido nada
    messages.error(request, "Não classificou a receita. Volte a tentar!")
    return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita_titulo]))


# Página de Adicinar Receita
@login_required(login_url="recipe:login_page")
def adicionar_receita(request):
    return render(request, 'recipe/adicionar_receita.html')


# Função para Criar a Receita na base de dados
@login_required(login_url="recipe:login_page")
def criar_receita(request):

    # Adicionar a nova Receita
    if request.method == "POST":

        titulo = request.POST.get('titulo-receita')
        # Confirmar que não existe Receitas com o mesmo título (É o nosso 'ID' da receita)
        if Receita.objects.filter(titulo=titulo).exists():
            messages.warning(request, 'Já existe uma Receita com esse Título! Por favor, coloque outro!')
            return HttpResponseRedirect(reverse('recipe:adicionar_receita'))

        categoria = request.POST.get('categoria-receita')
        modo_preparacao = request.POST.get('modo-preparação')
        calorias = request.POST.get('calorias')
        tempo_preparacao = request.POST.get('tempo-preparacao')
        grau_dificuldade = request.POST.get('grau_dificuldade')
        doses = request.POST.get('doses')

        foto = request.FILES['foto-receita']
        fs = FileSystemStorage(location='media/recipe_image')
        filename = fs.save(request.user.username + "-" + foto.name, foto)

        # Crie a nova Receita
        nova_receita = Receita(
            autor=request.user,
            titulo=titulo,
            categoria=categoria,
            modo_prep=modo_preparacao,
            calorias=calorias,
            tempo_prep=tempo_preparacao,
            grau_dificuldade=grau_dificuldade,
            doses=doses,
            imagem='recipe_image/'+filename
        )

        nova_receita.save()

        # Adicionar Ingredientes à nova Receita
        for key, value in request.POST.items():
            if key.startswith('ingrediente'):
                ingrediente = value
                unidade = request.POST.get(f'unidade{key.replace("ingrediente", "")}')
                quantidade = request.POST.get(f'quantidade{key.replace("ingrediente", "")}')
                extra = request.POST.get(f'extra-ingrediente{key.replace("ingrediente", "")}')
                novo_ingrediente = Ingrediente(
                    receita=nova_receita,
                    ingrediente=ingrediente,
                    unidade=unidade,
                    quantidade=quantidade,
                    extra_opcional=extra
                )
                novo_ingrediente.save()

        # Redirecionar para a página de detalhes da nova Receita
        messages.success(request, 'Receita Adicionada com Sucesso!')
        return redirect('recipe:detalhe', receita_titulo=nova_receita.titulo)

    messages.error(request, 'Não foi possível Adicionar a Receita! Tente de Novo!')
    return HttpResponseRedirect(reverse('recipe:adicionar_receita'))


# View para Remover Receita
@login_required(login_url="recipe:login_page")
def remover_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)

    # Verifica se o User é o autor da receita ou um administrador
    if request.user == receita.autor or request.user.is_staff:
        receita.delete()
        messages.success(request, 'Receita eliminada com sucesso!')
        return HttpResponseRedirect(reverse('recipe:home'))

    else:
        # O User não tem permissão para remover esta receita
        messages.error(request, 'Não podes remover esta receita! Apenas o seu autor e os administradores a podem remover! 💥')
        return HttpResponseRedirect(reverse('recipe:home'))


# Página de Editar Receita
@login_required(login_url="recipe:login_page")
def editar_receita(request, receita_titulo):
    # Obter o objeto da Receita
    receita = get_object_or_404(Receita, titulo=receita_titulo)

    # Verifique se o User é o Autor da Receita ou um Administrador
    if request.user != receita.autor and not request.user.is_staff:
        messages.error(request, "Não tem permissão para editar a Receita!")
        return HttpResponseRedirect(reverse('recipe:home'))

    # Obter os Ingredientes associados à Receita
    ingredientes = Ingrediente.objects.filter(receita=receita)

    return render(request, 'recipe/editar_receita.html', {'receita': receita,
                                                          'ingredientes': ingredientes})


# View de Editar Receita
@login_required(login_url="recipe:login_page")
def editar_receita_view(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)

    # Verifique se o User é o Autor da Receita ou Administrador
    if request.user != receita.autor and not request.user.is_staff:
        messages.error(request, "Não tem permissão para editar a Receita!")
        return HttpResponseRedirect(reverse('recipe:home'))

    # Atualizar as Informações da Receita
    if request.method == "POST":
        categoria = request.POST.get('categoria-receita')
        modo_preparacao = request.POST.get('modo-preparação')
        calorias = request.POST.get('calorias')
        tempo_preparacao = request.POST.get('tempo-preparacao')
        grau_dificuldade = request.POST.get('grau_dificuldade')
        doses = request.POST.get('doses')

        receita.categoria = categoria
        receita.modo_prep = modo_preparacao
        receita.calorias = calorias
        receita.tempo_prep = tempo_preparacao
        receita.grau_dificuldade = grau_dificuldade
        receita.doses = doses

        # Atualizar a imagem da Receita, caso exista:
        nova_foto_receita = request.FILES.get('foto-receita')
        if nova_foto_receita:
            fs = FileSystemStorage(location='media/recipe_image')
            filename = fs.save(receita.titulo + "-" + nova_foto_receita.name, nova_foto_receita)
            # Se uma nova foto de perfil for dada, atualizar a foto
            receita.imagem = 'recipe_image/' + filename

        receita.save()

        # Atualizar os Ingredientes [Apagar os que tinha e colocar de novo]
        Ingrediente.objects.filter(receita=receita).delete()
        for key, value in request.POST.items():
            if key.startswith('ingrediente'):
                ingrediente = value
                unidade = request.POST.get(f'unidade{key.replace("ingrediente", "")}')
                quantidade = request.POST.get(f'quantidade{key.replace("ingrediente", "")}')
                extra = request.POST.get(f'extra-ingrediente{key.replace("ingrediente", "")}')
                novo_ingrediente = Ingrediente(
                    receita=receita,
                    ingrediente=ingrediente,
                    unidade=unidade,
                    quantidade=quantidade,
                    extra_opcional=extra
                )
                novo_ingrediente.save()

        # Redirecionar para a página de detalhes da Receita atualizada
        messages.success(request, 'Receita Atualizada com Sucesso!')
        return redirect('recipe:detalhe', receita_titulo=receita.titulo)
    else:
        messages.error(request, 'Não foi possível Atualizar a Receita! Tente de Novo!')
        return HttpResponseRedirect(reverse('recipe:detalhe', args=[receita.titulo]))


# Página de Registo
def registar_page(request):
    return render(request, 'recipe/registo.html')


# Função para adicionar o Registo na Base de Dados e criar o seu Perfil Pessoal
def adicionar_registo(request):
    # Garantir que o User coloca apenas o Primeiro e Último nome
    if len(request.POST["name"].split()) > 2:
        # Mensagem de Aviso
        messages.warning(request, "Insere apenas o Primeiro e Último Nome!")
        return render(request, 'recipe/registo.html')

    first_name = request.POST["name"].split()[0]
    last_name = request.POST["name"].split()[-1]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    # Verificar se o Username já foi utilizado
    if User.objects.filter(username=username).exists():
        # Mensagem de Aviso
        messages.warning(request, "O nome de utilizador já foi escolhido!")
        return render(request, 'recipe/registo.html')

    user = User.objects.create_user(first_name=first_name,
                                    last_name=last_name,
                                    username=username,
                                    email=email,
                                    password=password)

    # Adicionar a imagem de Perfil ao User se existir
    try:
        if 'profile-photo' in request.FILES:
            profile_photo = request.FILES['profile-photo']
            fs = FileSystemStorage(location='media/foto_perfil')
            filename = fs.save(username + "-" + profile_photo.name, profile_photo)

            # Criar o Perfil com a foto selecionada
            profile = Perfil(user=user, foto='foto_perfil/' + filename, descricao_pessoal="")
            profile.save()
            return HttpResponseRedirect(reverse('recipe:login_page'))
        else:
            # Se nenhuma foto foi fornecida, ou não tenha sido guardada corretamente, use uma foto padrão
            default_photo_path = static('user_default.png')
            profile = Perfil(user=user, foto=default_photo_path, descricao_pessoal="")
            profile.save()
            return HttpResponseRedirect(reverse('recipe:login_page'))
    except KeyError:
        messages.warning(request, "Ocorreu um Erro! Verifique se preencheu corretamente os espaços e tente de novo!")
        return render(request, 'recipe/registo.html')


# Página de Login
def login_page(request):
    return render(request, 'recipe/login.html')


# Função para realizar o Login do User
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)

        # Verifica se este Login foi feito na página dos detalhes da Receita para comentar
        if 'comment' in request.POST:
            messages.success(request, 'Login com sucesso! Já pode classificar a receita!')
            return HttpResponseRedirect(reverse('recipe:detalhe', args=[request.POST['comment']]), {'user': user})

        # Caso tenha feito Login pela página
        else:
            messages.success(request, 'Login com sucesso!')
            return HttpResponseRedirect(reverse('recipe:home'), {'user': user})

    else:
        messages.error(request, 'Utilizador não existe! Tente novamente com outro username/password.')
        return HttpResponseRedirect(reverse('recipe:login_page'))


# Função para realizar o Logout do User
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout com Sucesso!')
    return HttpResponseRedirect(reverse("recipe:home"))


# Página de Perfil do User
@login_required(login_url="recipe:login_page")
def perfil(request, username):
    user = get_object_or_404(User, username=username)

    # Obter as 5 receitas com melhor classificação para o User
    # QUERY | Filtrar as Receitas cujo o User é autor -> Calcular a média do campo 'rating' do objeto Classificação e
    #         Ordenar por ordem descendente
    top_receitas_user = Receita.objects.filter(autor=user) \
                               .annotate(avg_rating=Avg('classificacao__rating')) \
                               .order_by('-avg_rating')[:5]
    return render(request, 'recipe/perfil.html', {'user': user, 'top_receitas_user': top_receitas_user})


# Página para Editar o Perfil
@login_required(login_url="recipe:login_page")
def editar_perfil(request, username):
    # Obter o objeto Perfil do User
    perfil = get_object_or_404(Perfil, user=request.user)

    # Confirmar se o User está logado na conta a editar
    if request.user.username == username:
        return render(request, 'recipe/editar_perfil.html', {'perfil': perfil})
    else:
        messages.error(request, "Apenas o Utilizador pode editar o Perfil!")
        return render(request, 'recipe/perfil.html', {'perfil', perfil})


# Função para Editar o Perfil
@login_required(login_url="recipe:login_page")
def editar_perfil_view(request, username):
    # Obter o objeto Perfil do User
    perfil = get_object_or_404(Perfil, user=request.user)

    # Verifica se o Username é o mesmo do User da 'request'
    if request.user.username == username:
        if request.method == 'POST':

            # Alterar as Informações Pessoais
            primeiro_nome = request.POST.get('first-name')
            request.user.first_name = primeiro_nome

            ultimo_nome = request.POST.get('last-name')
            request.user.last_name = ultimo_nome

            email = request.POST.get('email')
            request.user.email = email

            # Alterar Foto de perfil
            nova_foto_perfil = request.FILES.get('editar-foto-perfil')
            apagar_foto = request.POST.get('apagar-foto-perfil')

            if nova_foto_perfil:
                # Se uma nova foto de perfil for dada, atualizar a foto
                fs = FileSystemStorage(location='media/foto_perfil')
                filename = fs.save(request.user.username + "-" + nova_foto_perfil.name, nova_foto_perfil)
                perfil.foto = 'foto_perfil/' + filename

            if apagar_foto:
                # Se a opção para apagar a foto for selecionada, defina a foto como a default
                perfil.foto = static('user_default.png')

            # Alterar a Descrição Pessoal
            descricao_pessoal = request.POST.get('sobre-mim')
            perfil.descricao_pessoal = descricao_pessoal

            perfil.save()
            request.user.save()

            messages.success(request, 'Perfil atualizado com sucesso!')
            return HttpResponseRedirect(reverse('recipe:perfil', args=[username]))

    messages.error(request, "Apenas o Utilizador pode editar o Perfil!")
    return render(request, 'recipe/perfil.html', {'perfil', perfil})
