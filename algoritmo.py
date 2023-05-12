class Processo:
    def __init__(self, id):
        self.id = id
        self.esta_ativo = True
        self.lider = None

    def enviar_mensagem(self, processo):
        if processo.esta_ativo:
            print(f"Processo {self.id} envia mensagem para processo {processo.id}")
        else:
            print(f"Processo {self.id} não pode enviar mensagem para processo {processo.id} porque está inativo")

    def receber_mensagem(self, processo):
        if processo.esta_ativo:
            print(f"Processo {self.id} recebe mensagem de processo {processo.id}")
            if processo.lider is not None:
                print(f"Processo {self.id} detecta que processo {processo.lider.id} é o líder")
                self.lider = processo.lider
        else:
            print(f"Processo {self.id} não pode receber mensagem de processo {processo.id} porque está inativo")

    def iniciar_eleicao(self, processos):
        if not self.esta_ativo:
            return
        print(f"Processo {self.id} inicia eleição")
        self.lider = self
        for processo in processos:
            if processo.id > self.id:
                self.enviar_mensagem(processo)
                self.receber_mensagem(processo)
                if self.lider != self:
                    break
        if self.lider == self:
            print(f"Processo {self.id} é o líder")
            for processo in processos:
                if processo.id < self.id:
                    processo.enviar_mensagem(self)
                    processo.receber_mensagem(self)

    def falhar(self):
        self.esta_ativo = False
        if self.lider == self:
            for processo in processos:
                if processo.id > self.id:
                    processo.iniciar_eleicao(processos)
                    break
        else:
            self.lider = None


if __name__ == "__main__":
    p1 = Processo(1)
    p2 = Processo(2)
    p3 = Processo(3)
    p4 = Processo(4)
    processos = [p1, p2, p3, p4]

    p2.falhar()

    p1.iniciar_eleicao(processos)
