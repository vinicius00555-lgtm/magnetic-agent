# Magnetic Field Memory & Frequency-Based Autonomous Agent
import os, sys, time, subprocess, json, random, requests, threading, math

ARQUIVO_MEMORIA = "agente_memoria_frequencia.json"
ARQUIVO_LOG = "agente_autonomo_log.txt"
PASTA_SKILLS = "skills"

class MemoriaCampoMagnetico:
    def __init__(self):
        self.campo = []

    def vetorizar(self, texto, dim=16):
        vec = [0.0] * dim
        for i, char in enumerate(texto):
            vec[i % dim] += ord(char) / 255.0
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def similaridade(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a * a for a in v1))
        n2 = math.sqrt(sum(b * b for b in v2))
        if n1 == 0 or n2 == 0: return 0.0
        return dot / (n1 * n2)

    def processar_estmulo(self, item_texto, limiar_anulacao=0.88):
        nova_freq = self.vetorizar(item_texto)
        if not self.campo or len(self.campo) > 30:
            self.campo = [{"texto": item_texto, "vetor": nova_freq}]
            return "reset_campo"
        max_ressonancia = 0.0
        for elemento in self.campo:
            res = self.similaridade(elemento["vetor"], nova_freq)
            if res > max_ressonancia:
                max_ressonancia = res
        if max_ressonancia >= limiar_anulacao:
            return "anulado"
        self.campo.append({"texto": item_texto, "vetor": nova_freq})
        return "atraido"

class NucleoHardFrequencia:
    def __init__(self):
        self.assuntos_hard = [
            "Autonomous Agents Architecture", "Advanced Prompt Engineering",
            "Local LLMs Ollama", "Vector Databases FAISS",
            "Human Computer Communication", "Dynamic Code Execution Sandbox",
            "Reddit HackerNews Tech Scraping", "Self Reflection Error Recovery",
            "Multi Agent Collaboration", "Windows PowerShell Automation",
            "Asynchronous Python Requests", "Cybersecurity Defensive Tools",
            "Git Automation Python", "JSON Schema Validation", "Continuous Learning Weights"
        ]
        self.memoria_campo = MemoriaCampoMagnetico()
        self.rodando = True
        self.contador_estagnacao = 0

    def registrar_log(self, texto):
        horario = time.strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{horario}] {texto}\n"
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(linha)
        print(linha.strip())

    def criar_skill(self, tema):
        nome_limpo = tema.strip().lower().replace(" ", "_").replace("-", "_")
        caminho = os.path.join(PASTA_SKILLS, f"{nome_limpo}_skill.py")
        if not os.path.exists(caminho):
            codigo = f"# Resonance Skill: {nome_limpo}\ndef execute():\n    print('[Active Skill] Running routine for: {nome_limpo}')\n"
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(codigo)
            self.registrar_log(f"[Auto-Evolution] New skill generated: {nome_limpo}")

    def loop_cognitivo(self):
        while self.rodando:
            escolha = random.choice(self.assuntos_hard)
            if self.contador_estagnacao > 3:
                escolha = f"{escolha} breakthrough core engine 2026"
                self.contador_estagnacao = 0
            self.registrar_log(f"[Field Cycle] Tuning frequency to: '{escolha}'")
            url = f"https://api.github.com/search/repositories?q={escolha.replace(' ', '+')}+stars:>30&sort=updated&order=desc&per_page=2"
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if r.status_code == 200:
                    itens = r.json().get("items", [])
                    if not itens:
                        self.contador_estagnacao += 1
                    for i in itens:
                        item_str = f"{i['full_name']} (★ {i['stargazers_count']}) - {i['description'] or 'No desc'}"
                        status = self.memoria_campo.processar_estmulo(item_str)
                        if status in ["atraido", "reset_campo"]:
                            self.contador_estagnacao = 0
                            self.registrar_log(f"[Magnetic Attraction] New pattern integrated into the field.")
                            self.criar_skill(escolha.split(" breakthrough")[0])
                        elif status == "anulado":
                            self.contador_estagnacao += 1
                            self.registrar_log(f"[Magnetic Nullification] Identical noise repelled.")
            except:
                pass
            for _ in range(8):
                if not self.rodando: break
                time.sleep(1)

    def iniciar(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("="*75)
        print(" ☤ AUTONOMOUS CORE — MAGNETIC FIELD MEMORY & FREQUENCY")
        print(" Commands: 'listar skills', 'memoria', /cmd <command>, or 'sair'")
        print("="*75)
        t = threading.Thread(target=self.loop_cognitivo, daemon=True)
        t.start()
        while True:
            try:
                msg = input("\nYou (or Command): ").strip()
                if not msg: continue
                if msg.lower() in ["sair", "exit"]:
                    self.rodando = False
                    break
                if msg.lower() in ["listar skills", "skills"]:
                    print(os.listdir(PASTA_SKILLS))
                elif msg.lower() in ["memoria", "estado"]:
                    print(f"Total nodes in magnetic field: {len(self.memoria_campo.campo)}")
                elif msg.startswith("/cmd "):
                    print(subprocess.getoutput(msg[5:].strip()))
                else:
                    status = self.memoria_campo.processar_estmulo(msg)
                    print(f"Agent: External stimulus processed -> [{status.upper()}]")
            except (KeyboardInterrupt, EOFError):
                self.rodando = False
                break

if __name__ == "__main__":
    NucleoHardFrequencia().iniciar()
