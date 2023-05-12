import socket
import threading

class Processo:
    def __init__(self, id, endereco):
        self.id = id
        self.endereco = endereco
        self.esta_ativo = True
        self.lider = None

    def enviar_mensagem(self, endereco_destino):
        if not self.esta_ativo:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(endereco_destino)
            mensagem = f"{self.id}:ELEICAO"
            sock.sendall(mensagem.encode())
            sock.close()
            print(f"Processo {self.id} enviou mensagem para {endereco_destino}")
        except:
            print(f"Processo {self.id} não pode enviar mensagem para {endereco_destino}")

    def receber_mensagem(self, mensagem):
        if not self.esta_ativo:
            return
        remetente, conteudo = mensagem.split(":")
        print(f"Processo {self.id} recebeu mensagem de {remetente}: {conteudo}")
        if conteudo == "ELEICAO":
            self.lider = None
            for processo in processos:
                if processo.id > self.id:
                    processo.enviar_mensagem(processo.endereco)
                elif processo.id < self.id:
                    self.enviar_mensagem(processo.endereco)
            self.verificar_lider()

    def iniciar_eleicao(self):
        if not self.esta_ativo:
            return
        print(f"Processo {self.id} inicia eleição")
        self.lider = self
        for processo in processos:
            if processo.id > self.id:
                self.enviar_mensagem(processo.endereco)
                break
        self.verificar_lider()

    def verificar_lider(self):
        if not self.esta_ativo:
            return
        for processo in processos:
            if processo.lider is None:
                return
            elif processo.lider.id > self.lider.id:
                self.lider = processo.lider
        if self.lider == self:
            print(f"Processo {self.id} é o líder")
            for processo in processos:
                if processo.id != self.id:
                    processo.enviar_mensagem(processo.endereco)

    def falhar(self):
        self.esta_ativo = False
        if self.lider == self:
            for processo in processos:
                if processo.id > self.id:
                    processo.iniciar_eleicao()
                    break
        else:
            self.lider = None

class Servidor:
    def __init__(self, endereco):
        self.endereco = endereco
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.endereco)
        self.sock.listen(1)
        self.thread = threading.Thread(target=self.ouvir)
        self.thread.start()

    def ouvir(self):
        while True:
            conexao, endereco = self.sock.accept()
            mensagem = conexao.recv(1024)
            for processo in processos:
                if processo.endereco == endereco:
                    processo.receber_mensagem(mensagem.decode())
                    break
            conexao.close()


if __name__ == "__main__":
    processos = [
        Processo(1, ("localhost", 5001)),
        Processo(2, ("localhost", 5002)),
        Processo(3, ("localhost", 5003)),
        Processo(4, ("localhost", 5004)),
        Processo(5, ("localhost", 5005)),
    ]

    servidores = [
        Servidor(("localhost", 5001)),
        Servidor(("localhost", 5002)),
        Servidor(("localhost", 5003)),
        Servidor(("localhost", 5004)),
        Servidor(("localhost", 5005)),
    ]
    n=0
    for processo in processos:
        processos[n].iniciar_eleicao()
        n+=1
