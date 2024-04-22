from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome= nome
        self.data_nascimento = data_nascimento
        self.cpf= cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("excedeu saldo")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque com sucesso")
            return True
        else:
            print("operação falhou")

        return False


    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("deposito com sucesso")
        else:
            print("valor infomado invalido.")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente,limite = 500,limite_saques =3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self,valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]

        )

        excedeu_limite = valor > self.limite

        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("operação falhou! limite excedido")

        elif excedeu_saques:
            print("operação falhou! Numero maixmo de saques excedidos")

        else:
            return super().sacar(valor)

        return False


    def __str__(self) -> str:
        return f"""\
            Agencia:\t {self.agencia}
            C/C:\t\t{self.numero}
            Titulo:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def acicionar_transacao(self, transacao):
        self._transacoes.append(
            {

            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime
            ("%d-%m%y %H:%M:%s")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    def registar(self, conta):
        sucesso_transacao= conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicioar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor= valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuario
        [q]\tSair

    """
    return input(textwrap.dedent(menu))

def filtar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf ==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_contas_clientes(cliente):
    if not cliente.contas:
        print("cliente não possui conta")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não encontrado")
        return
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_contas_clientes(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf= input("informe o cpf do cliente: ")
    cliente = filtar_cliente(cpf,clientes)

    if not cliente:
        print("\nCliente não encontrado")
        return
    valor =  float(input("informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_contas_clientes(clientes)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado")
        return
    
    conta = recuperar_contas_clientes(cliente)
    if not conta:
        return
    
    print("\n ===============extrato==============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimetações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("======================================")

def criar_cliente(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado")
        return
    
    nome = input("Iforme o nome completo: ")
    data_nasciemento = input("informe a data de nascimento (dd-mm-aaa): ")
    endereco = input("informe o endereço: ")

    cliente = PessoaFisica(nome= nome, data_nascimento=data_nasciemento, cpf= cpf, endereco=endereco)
    
    clientes.append(cliente)
    print("\n cliente criado com sucesso")

def criar_conta(clientes, contas):
    numero_conta = input("Informe o número da conta: ")
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\nConta criada com sucesso")

def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("operação invalida")    



main()
