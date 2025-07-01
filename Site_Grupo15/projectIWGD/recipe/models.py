from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    foto = models.ImageField(upload_to='foto_perfil', null=True, blank=True)
    descricao_pessoal = models.TextField(max_length=5000, null=True, blank=True)
    total_comentarios = models.IntegerField(default=0)
    total_avaliacoes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    # Método que incrementa o nº total de receitas comentadas
    def aumentar_total_cometarios(self):
        self.total_comentarios += 1
        self.save()

    # Método que incrementa o nº total de receitas classificadas
    def aumentar_total_avaliacoes(self):
        self.total_avaliacoes += 1
        self.save()


class Receita(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, null=False, blank=False)
    doses = models.IntegerField(null=False, default=1)
    pub_data = models.DateTimeField(verbose_name='Data de Publicacao', default=timezone.now)
    tempo_prep = models.PositiveSmallIntegerField(null=False, default=1)

    # NOTA: models.CharField(choices=OPCOES) | OPCOES são uma lista de tuplos (valor a guardar na bd,
    #                                                                          valor a apresentar)
    # Documentação: https://docs.djangoproject.com/en/4.2/ref/models/fields/
    grau_dificuldade = models.CharField(max_length=100,
                                        choices=[('Fácil', 'Fácil'),
                                                 ('Médio', 'Médio'),
                                                 ('Dificil', 'Dificil'), ], null=False)

    categoria = models.CharField(max_length=100,
                                 choices=[('Carne', 'Carne'), ('Peixe', 'Peixe'),
                                          ('Vegetariano/Vegan', 'Vegetariano/Vegan'), ('Salada', 'Salada'),
                                          ('Sobremesa', 'Sobremesa'), ('Entrada', 'Entrada'), ], null=False)

    calorias = models.PositiveIntegerField(null=False, default=1)
    modo_prep = models.TextField(null=False, blank=False, default='')
    imagem = models.ImageField(upload_to='recipe_image', null=True, blank=True)

    # Função para contar o nº de comentários associado à receita
    def numero_de_comentarios(self):
        return self.comentario_set.count()

    # Função para contar o nº de classificações associado à receita
    def numero_de_classificacoes(self):
        return self.classificacao_set.count()

    # Função para calcular a média de avaliações da receita
    def media_avaliacoes(self):
        classificacoes = self.classificacao_set.all()
        if classificacoes.exists():
            return round(sum([c.rating for c in classificacoes]) / classificacoes.count(), 2)
        return 0

    # Função para calcular a % do rating (Função útil para o template)
    def calcular_percentagem_media_estrelas(self):
        # Caso particular para as estrelas serem pintadas de forma perfeita
        if self.media_avaliacoes() % 1 == 0.5:
            return self.media_avaliacoes() / 5 * 100 + 1.75
        return self.media_avaliacoes() / 5 * 100

    def __str__(self):
        return f'{self.autor.username} | {self.titulo}'


class Ingrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.CharField(max_length=200, null=False)
    quantidade = models.CharField(max_length=100,
                                  choices=[('Unidades', 'Unidades'), ('g', 'g'), ('Kg', 'Kg'),
                                           ('mL', 'mL'), ('L', 'L'), ('q.b.', 'q.b.'), ], null=False)
    unidade = models.PositiveIntegerField(default=0, null=False)
    extra_opcional = models.CharField(max_length=400, default='', blank=True, null=True)

    def __str__(self):
        return f'{self.receita.titulo} | {self.ingrediente}'


class Classificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, default='', choices=((1, '1'),
                                                                  (2, '2'),
                                                                  (3, '3'),
                                                                  (4, '4'),
                                                                  (5, '5'),))
    ava_data = models.DateTimeField(verbose_name='Data da Avaliacao', default=timezone.now)

    # Função para calcular a % do rating (Função útil para o template)
    def calcular_percentagem_estrelas(self):
        return self.rating / 5 * 100

    # https://docs.djangoproject.com/en/4.2/ref/models/options/ - Documentação do 'unique_together'
    class Meta:
        # Criar uma restrição de unicidade que garantirá que cada combinação de 'user' e 'receita' seja única
        # - Assim cada 'User' só pode avaliar uma receita uma vez.
        unique_together = (('user', 'receita'),)

    def __str__(self):
        return f'{self.user.username} | {self.receita.titulo} | {self.rating}'


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    comentario = models.TextField(null=False, blank=False, default='')
    com_data = models.DateTimeField(verbose_name='Data do Comentario', default=timezone.now)
    classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.receita.titulo} | {self.classificacao.rating} | {self.comentario}'
